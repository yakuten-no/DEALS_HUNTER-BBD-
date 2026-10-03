"""CRUD endpoints for ProductVariant records."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models.product_variant import ProductVariantCreate, ProductVariantRead, ProductVariantUpdate
from app.services import product_variant_service as service

router = APIRouter(prefix="/api/product-variants", tags=["product-variants"])


def _get_or_404(session: Session, variant_id: int):
    variant = service.get_variant(session, variant_id)
    if variant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")
    return variant


@router.post("", response_model=ProductVariantRead, status_code=status.HTTP_201_CREATED)
def create_variant(data: ProductVariantCreate, session: Session = Depends(get_session)):
    """422 if product_id doesn't refer to a real product (see
    app/main.py's NotFoundReferenceError handler)."""
    return service.create_variant(session, data)


@router.get("", response_model=list[ProductVariantRead])
def list_variants(
    product_id: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return service.list_variants(session, product_id=product_id, limit=limit, offset=offset)


@router.get("/{variant_id}", response_model=ProductVariantRead)
def get_variant(variant_id: int, session: Session = Depends(get_session)):
    return _get_or_404(session, variant_id)


@router.put("/{variant_id}", response_model=ProductVariantRead)
def update_variant(variant_id: int, data: ProductVariantUpdate, session: Session = Depends(get_session)):
    variant = _get_or_404(session, variant_id)
    return service.update_variant(session, variant, data)


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_variant(variant_id: int, session: Session = Depends(get_session)):
    """Blocked with 409 if the variant still has retailer listings."""
    variant = _get_or_404(session, variant_id)
    service.delete_variant(session, variant)
