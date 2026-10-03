"""CRUD endpoints for Retailer records. No delete endpoint by design --
see app/services/retailer_service.py."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models.retailer import RetailerCreate, RetailerRead, RetailerUpdate
from app.services import retailer_service as service

router = APIRouter(prefix="/api/retailers", tags=["retailers"])


def _get_or_404(session: Session, retailer_id: int):
    retailer = service.get_retailer(session, retailer_id)
    if retailer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Retailer not found")
    return retailer


@router.post("", response_model=RetailerRead, status_code=status.HTTP_201_CREATED)
def create_retailer(data: RetailerCreate, session: Session = Depends(get_session)):
    return service.create_retailer(session, data)


@router.get("", response_model=list[RetailerRead])
def list_retailers(is_active: bool | None = Query(default=None), session: Session = Depends(get_session)):
    return service.list_retailers(session, is_active=is_active)


@router.get("/{retailer_id}", response_model=RetailerRead)
def get_retailer(retailer_id: int, session: Session = Depends(get_session)):
    return _get_or_404(session, retailer_id)


@router.put("/{retailer_id}", response_model=RetailerRead)
def update_retailer(retailer_id: int, data: RetailerUpdate, session: Session = Depends(get_session)):
    """Partial update: only fields present in the request change (same
    convention as PUT /api/wishlists/{id} in V0.1)."""
    retailer = _get_or_404(session, retailer_id)
    return service.update_retailer(session, retailer, data)
