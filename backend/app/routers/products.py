"""CRUD endpoints for Product records."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models.product import ProductCreate, ProductDetail, ProductListItem, ProductRead, ProductUpdate
from app.services import product_service as service

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    return service.create_product(session, data)


@router.get("", response_model=list[ProductListItem])
def list_products(
    is_demo: bool | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return service.list_products(session, is_demo=is_demo, limit=limit, offset=offset)


@router.get("/{product_id}", response_model=ProductDetail)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """Detail view -- includes the product's variants (see ProductDetail)."""
    product = service.get_product_detail(session, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    """Partial update: only fields present in the request change."""
    product = service.get_product(session, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return service.update_product(session, product, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    """Blocked with 409 if the product still has variants -- see
    app/services/product_service.py for why this is RESTRICT, not CASCADE."""
    product = service.get_product(session, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    service.delete_product(session, product)
