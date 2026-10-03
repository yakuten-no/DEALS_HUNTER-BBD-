"""Service layer for RetailerListing records."""

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.offer import Offer
from app.models.price_observation import PriceObservation
from app.models.product_variant import ProductVariant
from app.models.retailer import Retailer
from app.models.retailer_listing import (
    RetailerListing,
    RetailerListingCreate,
    RetailerListingListItem,
    RetailerListingUpdate,
)
from app.services.db_helpers import commit_unique
from app.services.errors import HasDependentsError, NotFoundReferenceError
from app.services.price_observation_service import get_latest_observations_by_listing
from app.utils import utcnow


def create_listing(session: Session, data: RetailerListingCreate) -> RetailerListing:
    if session.get(Retailer, data.retailer_id) is None:
        raise NotFoundReferenceError(f"No retailer with id {data.retailer_id}")
    if session.get(ProductVariant, data.product_variant_id) is None:
        raise NotFoundReferenceError(f"No product variant with id {data.product_variant_id}")
    listing = RetailerListing.model_validate(data)
    session.add(listing)
    commit_unique(session, "A listing with this product URL already exists.")
    session.refresh(listing)
    return listing


def list_listings(
    session: Session,
    product_variant_id: int | None = None,
    retailer_id: int | None = None,
    is_demo: bool | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[RetailerListingListItem]:
    statement = select(RetailerListing).order_by(RetailerListing.id).limit(limit).offset(offset)
    if product_variant_id is not None:
        statement = statement.where(RetailerListing.product_variant_id == product_variant_id)
    if retailer_id is not None:
        statement = statement.where(RetailerListing.retailer_id == retailer_id)
    if is_demo is not None:
        statement = statement.where(RetailerListing.is_demo == is_demo)
    listings = list(session.exec(statement).all())

    listing_ids = [listing.id for listing in listings]
    latest_by_listing = get_latest_observations_by_listing(session, listing_ids)

    result: list[RetailerListingListItem] = []
    for listing in listings:
        latest = latest_by_listing.get(listing.id)
        result.append(
            RetailerListingListItem(
                **listing.model_dump(),
                latest_price=latest.observed_price if latest else None,
                latest_observed_at=latest.observed_at if latest else None,
            )
        )
    return result


def get_listing(session: Session, listing_id: int) -> RetailerListing | None:
    return session.get(RetailerListing, listing_id)


def update_listing(session: Session, listing: RetailerListing, data: RetailerListingUpdate) -> RetailerListing:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(listing, field, value)
    listing.updated_at = utcnow()
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


def delete_listing(session: Session, listing: RetailerListing) -> None:
    observation_count = session.execute(
        select(func.count(PriceObservation.id)).where(PriceObservation.retailer_listing_id == listing.id)
    ).scalar_one()
    offer_count = session.execute(
        select(func.count(Offer.id)).where(Offer.retailer_listing_id == listing.id)
    ).scalar_one()
    if observation_count > 0 or offer_count > 0:
        raise HasDependentsError(
            f"Cannot delete listing {listing.id}: it has {observation_count} price observation(s) and "
            f"{offer_count} offer(s). Deleting it would lose that history -- delete those first if you're "
            "sure, or keep the listing."
        )
    session.delete(listing)
    session.commit()
