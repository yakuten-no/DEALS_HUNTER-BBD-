"""Service layer for ProductVariant records."""

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.product import Product
from app.models.product_variant import ProductVariant, ProductVariantCreate, ProductVariantUpdate
from app.models.retailer_listing import RetailerListing
from app.services.db_helpers import commit_unique
from app.services.errors import HasDependentsError, NotFoundReferenceError
from app.utils import utcnow


def create_variant(session: Session, data: ProductVariantCreate) -> ProductVariant:
    if session.get(Product, data.product_id) is None:
        raise NotFoundReferenceError(f"No product with id {data.product_id}")
    variant = ProductVariant.model_validate(data)
    session.add(variant)
    commit_unique(session, "This product already has a variant with the same storage, RAM and colour.")
    session.refresh(variant)
    return variant


def list_variants(
    session: Session, product_id: int | None = None, limit: int = 100, offset: int = 0
) -> list[ProductVariant]:
    statement = select(ProductVariant).order_by(ProductVariant.id).limit(limit).offset(offset)
    if product_id is not None:
        statement = statement.where(ProductVariant.product_id == product_id)
    return list(session.exec(statement).all())


def get_variant(session: Session, variant_id: int) -> ProductVariant | None:
    return session.get(ProductVariant, variant_id)


def update_variant(session: Session, variant: ProductVariant, data: ProductVariantUpdate) -> ProductVariant:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(variant, field, value)
    variant.updated_at = utcnow()
    session.add(variant)
    commit_unique(session, "This product already has a variant with the same storage, RAM and colour.")
    session.refresh(variant)
    return variant


def delete_variant(session: Session, variant: ProductVariant) -> None:
    listing_count = session.execute(
        select(func.count(RetailerListing.id)).where(RetailerListing.product_variant_id == variant.id)
    ).scalar_one()
    if listing_count > 0:
        raise HasDependentsError(
            f"Cannot delete variant {variant.id}: it has {listing_count} retailer listing(s). "
            "Delete those first if you're sure, or keep the variant."
        )
    session.delete(variant)
    session.commit()
