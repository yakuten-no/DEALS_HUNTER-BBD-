"""CRUD endpoints for RetailerListing records, plus the deal-assessment
computed view (GET /{id}/deal-assessment)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.deal_engine import DealAssessment, assess_deal
from app.models.retailer_listing import (
    RetailerListingCreate,
    RetailerListingListItem,
    RetailerListingRead,
    RetailerListingUpdate,
)
from app.services import retailer_listing_service as service
from app.services import wishlist_service

router = APIRouter(prefix="/api/retailer-listings", tags=["retailer-listings"])


def _get_or_404(session: Session, listing_id: int):
    listing = service.get_listing(session, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Retailer listing not found")
    return listing


@router.post("", response_model=RetailerListingRead, status_code=status.HTTP_201_CREATED)
def create_listing(data: RetailerListingCreate, session: Session = Depends(get_session)):
    """422 if retailer_id or product_variant_id don't refer to real rows."""
    return service.create_listing(session, data)


@router.get("", response_model=list[RetailerListingListItem])
def list_listings(
    product_variant_id: int | None = Query(default=None),
    retailer_id: int | None = Query(default=None),
    is_demo: bool | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return service.list_listings(
        session,
        product_variant_id=product_variant_id,
        retailer_id=retailer_id,
        is_demo=is_demo,
        limit=limit,
        offset=offset,
    )


@router.get("/{listing_id}", response_model=RetailerListingRead)
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    return _get_or_404(session, listing_id)


@router.put("/{listing_id}", response_model=RetailerListingRead)
def update_listing(listing_id: int, data: RetailerListingUpdate, session: Session = Depends(get_session)):
    listing = _get_or_404(session, listing_id)
    return service.update_listing(session, listing, data)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(listing_id: int, session: Session = Depends(get_session)):
    """Blocked with 409 if the listing still has price observations or
    offers -- deleting it would otherwise lose that history."""
    listing = _get_or_404(session, listing_id)
    service.delete_listing(session, listing)


@router.get("/{listing_id}/deal-assessment", response_model=DealAssessment)
def get_deal_assessment(
    listing_id: int,
    wishlist_id: int | None = Query(default=None, description="Compare against this wishlist's budget, if given."),
    session: Session = Depends(get_session),
):
    """A read-only, deterministic assessment -- see app/deal_engine/assessment.py.
    Nothing here is written to the database or AI-generated (D-003)."""
    listing = _get_or_404(session, listing_id)
    wishlist = None
    if wishlist_id is not None:
        wishlist = wishlist_service.get_wishlist(session, wishlist_id)
        if wishlist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist entry not found")
    return assess_deal(session, listing, wishlist)
