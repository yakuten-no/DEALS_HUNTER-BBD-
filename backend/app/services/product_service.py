"""Service layer for Product records."""

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.product import Product, ProductCreate, ProductDetail, ProductListItem, ProductUpdate
from app.models.product_variant import ProductVariant, ProductVariantRead
from app.normalization import normalize_name
from app.services.db_helpers import commit_unique
from app.services.errors import HasDependentsError
from app.utils import utcnow


def create_product(session: Session, data: ProductCreate) -> Product:
    payload = data.model_dump()
    # normalized_name is always server-computed, never trusted from the
    # request -- see the Product model's module docstring.
    payload["normalized_name"] = normalize_name(f"{data.brand} {data.model_name}")
    product = Product.model_validate(payload)
    session.add(product)
    commit_unique(session, "A product with this brand and model name already exists.")
    session.refresh(product)
    return product


def list_products(
    session: Session, is_demo: bool | None = None, limit: int = 100, offset: int = 0
) -> list[ProductListItem]:
    statement = select(Product).order_by(Product.brand, Product.model_name).limit(limit).offset(offset)
    if is_demo is not None:
        statement = statement.where(Product.is_demo == is_demo)
    products = list(session.exec(statement).all())
    product_ids = [p.id for p in products]

    # One query for variant counts across every product on this page,
    # not one query per product (avoids N+1 -- see the V0.2 brief's
    # performance section). Uses session.execute() (not the SQLModel
    # convenience .exec()) since this is a multi-column aggregate select,
    # not a single-model select -- .execute() is the plain, well-documented
    # SQLAlchemy path for that shape of query.
    counts: dict[int, int] = {}
    if product_ids:
        count_statement = (
            select(ProductVariant.product_id, func.count(ProductVariant.id))
            .where(ProductVariant.product_id.in_(product_ids))
            .group_by(ProductVariant.product_id)
        )
        counts = dict(session.execute(count_statement).all())

    return [
        ProductListItem(**product.model_dump(), variant_count=counts.get(product.id, 0)) for product in products
    ]


def get_product(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def get_product_detail(session: Session, product_id: int) -> ProductDetail | None:
    product = session.get(Product, product_id)
    if product is None:
        return None
    variants = session.exec(
        select(ProductVariant).where(ProductVariant.product_id == product_id).order_by(ProductVariant.id)
    ).all()
    return ProductDetail(
        **product.model_dump(),
        variants=[ProductVariantRead.model_validate(v) for v in variants],
    )


def update_product(session: Session, product: Product, data: ProductUpdate) -> Product:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)
    # Keep normalized_name consistent if either input field changed.
    if "brand" in updates or "model_name" in updates:
        product.normalized_name = normalize_name(f"{product.brand} {product.model_name}")
    product.updated_at = utcnow()
    session.add(product)
    commit_unique(session, "A product with this brand and model name already exists.")
    session.refresh(product)
    return product


def delete_product(session: Session, product: Product) -> None:
    variant_count = session.execute(
        select(func.count(ProductVariant.id)).where(ProductVariant.product_id == product.id)
    ).scalar_one()
    if variant_count > 0:
        raise HasDependentsError(
            f"Cannot delete product {product.id}: it has {variant_count} variant(s). "
            "Delete those first if you're sure, or keep the product."
        )
    session.delete(product)
    session.commit()
