"""CRUD endpoints for wishlist entries."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.models.wishlist import WishlistCreate, WishlistRead, WishlistUpdate
from app.services import wishlist_service as service

router = APIRouter(prefix="/api/wishlists", tags=["wishlists"])


def _get_or_404(session: Session, wishlist_id: int):
    wishlist = service.get_wishlist(session, wishlist_id)
    if wishlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist entry not found")
    return wishlist


@router.post("", response_model=WishlistRead, status_code=status.HTTP_201_CREATED)
def create_wishlist(data: WishlistCreate, session: Session = Depends(get_session)):
    """Create a new wishlist entry."""
    try:
        return service.create_wishlist(session, data)
    except service.WishlistValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get("", response_model=list[WishlistRead])
def list_wishlists(session: Session = Depends(get_session)):
    """List every wishlist entry, most recently created first."""
    return service.list_wishlists(session)


@router.get("/{wishlist_id}", response_model=WishlistRead)
def get_wishlist(wishlist_id: int, session: Session = Depends(get_session)):
    """Fetch one wishlist entry by id."""
    return _get_or_404(session, wishlist_id)


@router.put("/{wishlist_id}", response_model=WishlistRead)
def update_wishlist(wishlist_id: int, data: WishlistUpdate, session: Session = Depends(get_session)):
    """Update a wishlist entry.

    Only fields included in the request body are changed -- omitted
    fields keep their current value. (Strict REST convention would have
    PUT replace the whole resource and reserve partial updates for PATCH;
    this project uses PUT with partial-update behavior instead, since
    that's what a "click to change one field" wishlist UI actually needs.
    Documented here since it's a deliberate deviation, not an accident.)
    """
    wishlist = _get_or_404(session, wishlist_id)
    try:
        return service.update_wishlist(session, wishlist, data)
    except service.WishlistValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(wishlist_id: int, session: Session = Depends(get_session)):
    """Delete a wishlist entry."""
    wishlist = _get_or_404(session, wishlist_id)
    service.delete_wishlist(session, wishlist)
