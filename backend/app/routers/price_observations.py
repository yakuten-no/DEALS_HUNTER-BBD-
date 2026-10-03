"""Create and read endpoints for PriceObservation records. Deliberately no
PUT or DELETE -- see app/services/price_observation_service.py."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models.price_observation import PriceObservationCreate, PriceObservationRead
from app.services import price_observation_service as service

router = APIRouter(prefix="/api/price-observations", tags=["price-observations"])


@router.post("", response_model=PriceObservationRead, status_code=status.HTTP_201_CREATED)
def create_observation(data: PriceObservationCreate, session: Session = Depends(get_session)):
    """422 if retailer_listing_id doesn't refer to a real listing."""
    return service.create_observation(session, data)


@router.get("", response_model=list[PriceObservationRead])
def list_observations(
    retailer_listing_id: int = Query(..., description="Required -- history is always scoped to one listing."),
    limit: int = Query(default=200, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    """Full observation history for one listing, newest first."""
    return service.list_observations(session, retailer_listing_id=retailer_listing_id, limit=limit, offset=offset)


@router.get("/{observation_id}", response_model=PriceObservationRead)
def get_observation(observation_id: int, session: Session = Depends(get_session)):
    observation = service.get_observation(session, observation_id)
    if observation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price observation not found")
    return observation
