"""
Tests for app.deal_engine.assess_deal -- the six scenarios named in the
V0.2 brief: under budget, over budget, price lower than the previous
observation, no historical data, a conditional offer, and an unavailable
listing.

These call assess_deal() directly against the `session` fixture rather
than going through the HTTP API, for precise control over the data each
scenario needs. test_deal_assessment_api_endpoint at the bottom exercises
the actual HTTP route once, to confirm the wiring works too.
"""

from datetime import timedelta

from app.deal_engine import assess_deal
from app.models.offer import Offer
from app.models.price_observation import PriceObservation
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.retailer import Retailer
from app.models.retailer_listing import RetailerListing
from app.models.wishlist import Wishlist
from app.utils import utcnow


def _make_listing(session, availability: str = "in_stock") -> RetailerListing:
    product = Product(brand="Nothing", model_name="Phone 3a", normalized_name="nothing phone 3a")
    session.add(product)
    session.commit()
    session.refresh(product)

    variant = ProductVariant(product_id=product.id, storage_gb=128, ram_gb=8, color="Black")
    session.add(variant)
    session.commit()
    session.refresh(variant)

    retailer = Retailer(name="Flipkart", slug="flipkart")
    session.add(retailer)
    session.commit()
    session.refresh(retailer)

    listing = RetailerListing(
        retailer_id=retailer.id,
        product_variant_id=variant.id,
        product_url="https://www.flipkart.com/nothing-phone-3a",
        availability=availability,
    )
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


def _add_observation(session, listing: RetailerListing, price: int, days_ago: int, mrp: int | None = None):
    observation = PriceObservation(
        retailer_listing_id=listing.id, observed_price=price, mrp=mrp, observed_at=utcnow() - timedelta(days=days_ago)
    )
    session.add(observation)
    session.commit()


def test_under_budget(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=55000, days_ago=0)
    wishlist = Wishlist(name="test", raw_query="test", budget_target=60000)

    assessment = assess_deal(session, listing, wishlist)

    assert assessment.signals.within_wishlist_target is True
    assert any("target budget" in reason for reason in assessment.reasons)


def test_over_budget(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=55000, days_ago=0)
    wishlist = Wishlist(name="test", raw_query="test", budget_max=50000)

    assessment = assess_deal(session, listing, wishlist)

    assert assessment.signals.within_wishlist_max is False
    assert any("maximum budget" in reason for reason in assessment.reasons)


def test_price_lower_than_previous_observation(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=7)
    _add_observation(session, listing, price=22999, days_ago=0)

    assessment = assess_deal(session, listing)

    assert assessment.signals.price_dropped_from_previous_observation is True
    assert assessment.signals.lowest_observed_in_history is True
    assert assessment.current_price == 22999


def test_price_not_lower_than_previous_observation(session):
    """The converse case: confirms the signal is a real comparison, not
    always True once there are 2+ observations."""
    listing = _make_listing(session)
    _add_observation(session, listing, price=22999, days_ago=7)
    _add_observation(session, listing, price=24999, days_ago=0)

    assessment = assess_deal(session, listing)

    assert assessment.signals.price_dropped_from_previous_observation is False
    assert assessment.signals.lowest_observed_in_history is False


def test_no_historical_data(session):
    listing = _make_listing(session)

    assessment = assess_deal(session, listing)

    assert assessment.signals.has_price_history is False
    assert assessment.signals.observation_count == 0
    assert assessment.current_price is None
    assert assessment.signals.price_dropped_from_previous_observation is None  # unknown, not False
    assert assessment.signals.lowest_observed_in_history is None  # unknown, not False
    assert any("no price history" in caveat.lower() for caveat in assessment.caveats)
    # The engine must never invent history to fill the gap.
    assert assessment.lowest_observed_price is None
    assert assessment.highest_observed_price is None


def test_insufficient_history_with_single_observation_is_unknown_not_false(session):
    """One observation exists, but that's not enough to claim a trend --
    the signal must be None (unknown), not False (checked, and no)."""
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=0)

    assessment = assess_deal(session, listing)

    assert assessment.signals.has_price_history is True
    assert assessment.signals.observation_count == 1
    assert assessment.signals.price_dropped_from_previous_observation is None
    assert assessment.signals.lowest_observed_in_history is None
    assert any("too little history" in caveat.lower() for caveat in assessment.caveats)


def test_conditional_offer(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=0)
    offer = Offer(
        retailer_listing_id=listing.id,
        offer_type="bank_discount",
        title="5% off with HDFC cards",
        discount_percentage=5,
        is_guaranteed=False,
    )
    session.add(offer)
    session.commit()

    assessment = assess_deal(session, listing)

    assert assessment.signals.has_conditional_offers is True
    assert assessment.signals.has_guaranteed_discount is False
    # 24999 * 5% = 1249.95, rounds to 1250 -- asserted as a literal so this
    # test can't silently pass by recomputing the same expression the
    # source code uses (and therefore drifting together if that expression
    # were ever wrong).
    assert assessment.conditional_discount_total == 1250
    assert assessment.potential_effective_price == 24999 - 1250
    assert any("conditional" in caveat.lower() for caveat in assessment.caveats)


def test_guaranteed_discount_reduces_effective_price_but_not_potential(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=0)
    offer = Offer(
        retailer_listing_id=listing.id, offer_type="instant_discount", title="Instant discount",
        discount_amount=1000, is_guaranteed=True,
    )
    session.add(offer)
    session.commit()

    assessment = assess_deal(session, listing)

    assert assessment.signals.has_guaranteed_discount is True
    assert assessment.guaranteed_discount_total == 1000
    assert assessment.effective_price_guaranteed == 23999
    # No conditional offers exist, so there's nothing "potential" beyond
    # the guaranteed price -- must not duplicate the same number under a
    # different label.
    assert assessment.potential_effective_price is None


def test_cashback_is_never_netted_into_effective_price(session):
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=0)
    offer = Offer(
        retailer_listing_id=listing.id, offer_type="cashback", title="\u20b9500 cashback",
        discount_amount=500, is_guaranteed=True,
    )
    session.add(offer)
    session.commit()

    assessment = assess_deal(session, listing)

    assert assessment.signals.has_cashback_offers is True
    assert assessment.cashback_total == 500
    # Cashback must never reduce the guaranteed or potential price, even
    # though this cashback offer is itself marked guaranteed -- D-006.
    assert assessment.guaranteed_discount_total == 0
    assert assessment.effective_price_guaranteed == 24999


def test_unavailable_listing(session):
    listing = _make_listing(session, availability="out_of_stock")
    _add_observation(session, listing, price=24999, days_ago=0)

    assessment = assess_deal(session, listing)

    assert assessment.signals.is_available is False
    assert assessment.listing_availability == "out_of_stock"
    assert any("out of stock" in caveat.lower() for caveat in assessment.caveats)


def test_mrp_discount_alone_is_labelled_a_caveat_not_a_reason(session):
    """D-005: an MRP discount must never be presented as proof of a good
    deal -- it should show up as informational, with an explicit caveat,
    never folded into `reasons`."""
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=0, mrp=49999)

    assessment = assess_deal(session, listing)

    assert assessment.mrp_discount_percentage is not None
    assert any("mrp discount is not" in caveat.lower() for caveat in assessment.caveats)
    assert not any("mrp" in reason.lower() for reason in assessment.reasons)


def test_never_claims_all_time_low_wording(session):
    """Only "lowest observed in our history" wording is allowed -- never
    "all-time low" (see project-memory/ARCHITECTURE.md section 6)."""
    listing = _make_listing(session)
    _add_observation(session, listing, price=24999, days_ago=7)
    _add_observation(session, listing, price=19999, days_ago=0)

    assessment = assess_deal(session, listing)

    assert assessment.signals.lowest_observed_in_history is True
    all_text = " ".join(assessment.reasons + assessment.caveats).lower()
    assert "all-time low" not in all_text
    assert "all time low" not in all_text


def test_deal_assessment_api_endpoint(client):
    """One end-to-end check that the router wiring actually works."""
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"}).json()
    listing = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()
    client.post("/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 24999})

    response = client.get(f"/api/retailer-listings/{listing['id']}/deal-assessment")
    assert response.status_code == 200
    body = response.json()
    assert body["current_price"] == 24999
    assert body["retailer_listing_id"] == listing["id"]


def test_deal_assessment_api_endpoint_with_unknown_wishlist_id_returns_404(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"}).json()
    listing = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()

    response = client.get(f"/api/retailer-listings/{listing['id']}/deal-assessment", params={"wishlist_id": 999999})
    assert response.status_code == 404
