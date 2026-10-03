"""CRUD endpoints for Offer records."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models.offer import OfferCreate, OfferRead, OfferUpdate
from app.services import offer_service as service

router = APIRouter(prefix="/api/offers", tags=["offers"])


def _get_or_404(session: Session, offer_id: int):
    offer = service.get_offer(session, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return offer


@router.post("", response_model=OfferRead, status_code=status.HTTP_201_CREATED)
def create_offer(data: OfferCreate, session: Session = Depends(get_session)):
    """422 if retailer_listing_id doesn't refer to a real listing."""
    return service.create_offer(session, data)


@router.get("", response_model=list[OfferRead])
def list_offers(
    retailer_listing_id: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return service.list_offers(session, retailer_listing_id=retailer_listing_id, limit=limit, offset=offset)


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, session: Session = Depends(get_session)):
    return _get_or_404(session, offer_id)


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(offer_id: int, data: OfferUpdate, session: Session = Depends(get_session)):
    offer = _get_or_404(session, offer_id)
    return service.update_offer(session, offer, data)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, session: Session = Depends(get_session)):
    offer = _get_or_404(session, offer_id)
    service.delete_offer(session, offer)
