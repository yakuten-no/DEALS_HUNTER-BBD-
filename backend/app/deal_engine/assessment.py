"""
Deal assessment: given a listing's price history and offers (and,
optionally, a wishlist's budget), compute a transparent set of signals --
never a single opaque "deal score". Every number here is either a stored
value or simple arithmetic over stored values; nothing is estimated,
predicted, or AI-generated.

Ground rules this module exists to enforce (see project-memory/DECISIONS.md,
D-005 and D-006):
- Never call a price an "all-time low" -- only "lowest observed in our
  history", and only once there's enough history to make that meaningful.
- An MRP discount alone is never treated as evidence of a good deal.
- Guaranteed discounts, conditional discounts, and cashback are kept in
  three separate totals, never silently blended.
- When there isn't enough data to answer a question, the answer is `None`
  (unknown), not `False` (checked, and no).
"""

from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Session, select

from app.models.offer import Offer
from app.models.price_observation import PriceObservation
from app.models.retailer_listing import RetailerListing
from app.models.wishlist import Wishlist
from app.utils import utcnow

# Below this many observations, trend-dependent signals (did the price
# just drop? is this the lowest we've seen?) are reported as unknown
# rather than guessed from a single data point.
MIN_OBSERVATIONS_FOR_TREND = 2


class DealSignals(BaseModel):
    """Individual, inspectable signals. Deliberately not collapsed into a
    single score -- every claim here can be checked against the data that
    produced it (see the `reasons` list on DealAssessment)."""

    has_price_history: bool
    observation_count: int
    price_dropped_from_previous_observation: bool | None = None
    lowest_observed_in_history: bool | None = None
    within_wishlist_target: bool | None = None
    within_wishlist_max: bool | None = None
    has_guaranteed_discount: bool
    has_conditional_offers: bool
    has_cashback_offers: bool
    is_available: bool | None = None


class DealAssessment(BaseModel):
    retailer_listing_id: int
    assessed_at: datetime
    listing_availability: str

    current_price: int | None = None
    mrp: int | None = None
    mrp_discount_percentage: float | None = None

    lowest_observed_price: int | None = None
    highest_observed_price: int | None = None
    average_observed_price: float | None = None

    guaranteed_discount_total: int = 0
    conditional_discount_total: int = 0
    cashback_total: int = 0

    effective_price_guaranteed: int | None = None
    potential_effective_price: int | None = None

    signals: DealSignals
    reasons: list[str] = []
    caveats: list[str] = []


@dataclass
class _OfferTotals:
    guaranteed_discount: int = 0
    conditional_discount: int = 0
    cashback: int = 0
    has_conditional_offers: bool = False
    has_cashback_offers: bool = False
    reasons: list[str] = field(default_factory=list)


def _resolve_offer_amount(offer: Offer, current_price: int | None) -> int:
    """A flat `discount_amount` is used as-is; a `discount_percentage` is
    resolved against the current price if one is known. If an offer gives
    neither a usable amount nor a resolvable percentage, it contributes 0
    to totals but is still counted as present (its `title`/`conditions`
    still matter to a person reading the listing, even if we can't turn it
    into a number)."""
    if offer.discount_amount is not None:
        return offer.discount_amount
    if offer.discount_percentage is not None and current_price is not None:
        return round(current_price * offer.discount_percentage / 100)
    return 0


def _summarize_offers(offers: list[Offer], current_price: int | None) -> _OfferTotals:
    totals = _OfferTotals()
    for offer in offers:
        amount = _resolve_offer_amount(offer, current_price)
        if offer.offer_type == "cashback":
            # Cashback is never netted into an "effective price", whether
            # or not it's guaranteed -- it's tracked and shown separately
            # (D-006), so it doesn't even attempt an amount-based reason.
            totals.cashback += amount
            totals.has_cashback_offers = True
            continue
        if offer.is_guaranteed:
            totals.guaranteed_discount += amount
            if amount > 0:
                totals.reasons.append(f"Guaranteed offer applies: {offer.title}.")
        else:
            totals.conditional_discount += amount
            totals.has_conditional_offers = True
    return totals


def assess_deal(session: Session, listing: RetailerListing, wishlist: Wishlist | None = None) -> DealAssessment:
    """Compute a DealAssessment for one listing, optionally compared
    against one wishlist's budget. Read-only: this never writes to the
    database, and nothing it returns is persisted (see the module and
    package docstrings for why)."""
    observations = list(
        session.exec(
            select(PriceObservation)
            .where(PriceObservation.retailer_listing_id == listing.id)
            .order_by(PriceObservation.observed_at.desc())
        ).all()
    )
    offers = list(session.exec(select(Offer).where(Offer.retailer_listing_id == listing.id)).all())

    reasons: list[str] = []
    caveats: list[str] = []

    has_price_history = len(observations) > 0
    observation_count = len(observations)
    current_price = observations[0].observed_price if has_price_history else None
    mrp = observations[0].mrp if has_price_history else None

    lowest_observed_price = min(o.observed_price for o in observations) if has_price_history else None
    highest_observed_price = max(o.observed_price for o in observations) if has_price_history else None
    average_observed_price = (
        sum(o.observed_price for o in observations) / observation_count if has_price_history else None
    )

    mrp_discount_percentage: float | None = None
    if current_price is not None and mrp is not None and mrp > 0:
        mrp_discount_percentage = round((mrp - current_price) / mrp * 100, 1)
        caveats.append(
            "MRP discount is not, on its own, evidence of a genuine deal -- "
            "MRPs can be set arbitrarily high. Judged against price history instead."
        )

    price_dropped_from_previous: bool | None = None
    lowest_observed_in_history: bool | None = None
    if observation_count >= MIN_OBSERVATIONS_FOR_TREND:
        previous_price = observations[1].observed_price
        price_dropped_from_previous = current_price is not None and current_price < previous_price
        lowest_observed_in_history = current_price == lowest_observed_price
        if price_dropped_from_previous:
            reasons.append(f"Price dropped from the previous observation ({previous_price} -> {current_price}).")
        if lowest_observed_in_history:
            reasons.append(f"Lowest price observed in our history so far ({observation_count} observations).")
    elif has_price_history:
        caveats.append(
            f"Only {observation_count} price observation(s) so far -- too little history to tell "
            "whether this is a genuine drop or a record low yet."
        )
    else:
        caveats.append("No price history recorded for this listing yet.")

    offer_totals = _summarize_offers(offers, current_price)
    reasons.extend(offer_totals.reasons)
    if offer_totals.has_conditional_offers:
        caveats.append(
            "Conditional offers exist but require meeting extra conditions (bank card, exchange, coupon, "
            "EMI, membership, or limited eligibility) -- not guaranteed for every buyer."
        )
    if offer_totals.has_cashback_offers:
        caveats.append("Cashback is tracked separately and is never subtracted from the effective price shown.")

    effective_price_guaranteed = (
        current_price - offer_totals.guaranteed_discount if current_price is not None else None
    )
    potential_effective_price = (
        effective_price_guaranteed - offer_totals.conditional_discount
        if effective_price_guaranteed is not None and offer_totals.conditional_discount > 0
        else None
    )

    is_available: bool | None = None
    if listing.availability == "in_stock":
        is_available = True
    elif listing.availability == "out_of_stock":
        is_available = False
        caveats.append("This listing is currently out of stock.")
    else:
        caveats.append("Availability for this listing is unknown.")

    within_wishlist_target: bool | None = None
    within_wishlist_max: bool | None = None
    if wishlist is not None and current_price is not None:
        if wishlist.budget_target is not None:
            within_wishlist_target = current_price <= wishlist.budget_target
            if within_wishlist_target:
                reasons.append(f"Within your target budget of \u20b9{wishlist.budget_target:,}.")
        if wishlist.budget_max is not None:
            within_wishlist_max = current_price <= wishlist.budget_max
            if within_wishlist_max is False:
                reasons.append(f"Above your maximum budget of \u20b9{wishlist.budget_max:,}.")

    signals = DealSignals(
        has_price_history=has_price_history,
        observation_count=observation_count,
        price_dropped_from_previous_observation=price_dropped_from_previous,
        lowest_observed_in_history=lowest_observed_in_history,
        within_wishlist_target=within_wishlist_target,
        within_wishlist_max=within_wishlist_max,
        has_guaranteed_discount=offer_totals.guaranteed_discount > 0,
        has_conditional_offers=offer_totals.has_conditional_offers,
        has_cashback_offers=offer_totals.has_cashback_offers,
        is_available=is_available,
    )

    if not reasons:
        reasons.append("No meaningful discount signal found in the data currently available.")

    return DealAssessment(
        retailer_listing_id=listing.id,
        assessed_at=utcnow(),
        listing_availability=listing.availability,
        current_price=current_price,
        mrp=mrp,
        mrp_discount_percentage=mrp_discount_percentage,
        lowest_observed_price=lowest_observed_price,
        highest_observed_price=highest_observed_price,
        average_observed_price=average_observed_price,
        guaranteed_discount_total=offer_totals.guaranteed_discount,
        conditional_discount_total=offer_totals.conditional_discount,
        cashback_total=offer_totals.cashback,
        effective_price_guaranteed=effective_price_guaranteed,
        potential_effective_price=potential_effective_price,
        signals=signals,
        reasons=reasons,
        caveats=caveats,
    )
