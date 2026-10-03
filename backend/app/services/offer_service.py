"""Service layer for Offer records. Full CRUD -- unlike price observations,
offers can legitimately change (an offer expires, or was entered with a
typo) without violating the "never overwrite historical prices" rule,
which only applies to PriceObservation."""

from sqlmodel import Session, select

from app.models.offer import Offer, OfferCreate, OfferUpdate
from app.models.retailer_listing import RetailerListing
from app.services.errors import NotFoundReferenceError
from app.utils import utcnow


def create_offer(session: Session, data: OfferCreate) -> Offer:
    if session.get(RetailerListing, data.retailer_listing_id) is None:
        raise NotFoundReferenceError(f"No retailer listing with id {data.retailer_listing_id}")
    offer = Offer.model_validate(data)
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def list_offers(
    session: Session, retailer_listing_id: int | None = None, limit: int = 100, offset: int = 0
) -> list[Offer]:
    statement = select(Offer).order_by(Offer.id).limit(limit).offset(offset)
    if retailer_listing_id is not None:
        statement = statement.where(Offer.retailer_listing_id == retailer_listing_id)
    return list(session.exec(statement).all())


def get_offer(session: Session, offer_id: int) -> Offer | None:
    return session.get(Offer, offer_id)


def update_offer(session: Session, offer: Offer, data: OfferUpdate) -> Offer:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(offer, field, value)
    offer.updated_at = utcnow()
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def delete_offer(session: Session, offer: Offer) -> None:
    session.delete(offer)
    session.commit()
