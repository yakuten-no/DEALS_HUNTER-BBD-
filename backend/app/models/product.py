"""
The Product model: a conceptual phone model, independent of any retailer
listing. "Nothing Phone (3a) Pro" is one Product; its different storage/
RAM/color configurations are ProductVariant rows (see product_variant.py).

`normalized_name` is never supplied by the API caller -- it's always
computed server-side from `brand` + `model_name` via
app.normalization.normalize_name(), the same way V0.1's wishlist service
derives a default `name` from `raw_query` rather than trusting client
input to already be consistent (see app/services/product_service.py).
"""

from datetime import datetime

from sqlmodel import Field, SQLModel, UniqueConstraint

from app.models.product_variant import ProductVariantRead
from app.utils import utcnow


class ProductBase(SQLModel):
    brand: str = Field(min_length=1, max_length=100, description="e.g. 'Nothing'.")
    model_name: str = Field(min_length=1, max_length=200, description="e.g. 'Phone (3a) Pro'.")
    category: str = Field(default="smartphone", max_length=50, description="Reserved for future non-phone categories.")
    description: str | None = Field(default=None, max_length=2000)


class Product(ProductBase, table=True):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("brand", "normalized_name", name="uq_product_brand_normalized_name"),)

    id: int | None = Field(default=None, primary_key=True)
    # Always server-computed -- see module docstring. Indexed since it's
    # the field future product-matching will search/compare on (OQ-3).
    normalized_name: str = Field(index=True)
    # Structurally marks fixture/demo rows so they can never be silently
    # mistaken for real tracked data -- see backend/scripts/seed_demo_data.py
    # and project-memory/DECISIONS.md.
    is_demo: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ProductCreate(ProductBase):
    is_demo: bool = False


class ProductUpdate(SQLModel):
    brand: str | None = Field(default=None, min_length=1, max_length=100)
    model_name: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    is_demo: bool | None = None


class ProductRead(ProductBase):
    id: int
    normalized_name: str
    is_demo: bool
    created_at: datetime
    updated_at: datetime


class ProductListItem(ProductRead):
    """List view: a cheap-to-compute variant count instead of the full
    nested list, so listing many products stays a small, fixed number of
    queries (see app/services/product_service.py)."""

    variant_count: int


class ProductDetail(ProductRead):
    """Detail view (GET /api/products/{id}): full nested variants."""

    variants: list[ProductVariantRead] = []
