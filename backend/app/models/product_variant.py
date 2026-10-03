"""
The ProductVariant model: one specific buyable configuration of a Product
-- storage, RAM, and color, which must never be collapsed together (D-007
in project-memory/DECISIONS.md). "Nothing Phone (3a) Pro, 12GB/256GB,
White" is a ProductVariant; "Nothing Phone (3a) Pro" itself is the Product.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel, UniqueConstraint

from app.utils import utcnow


class ProductVariantBase(SQLModel):
    product_id: int = Field(foreign_key="products.id", index=True)
    storage_gb: int | None = Field(default=None, ge=0)
    ram_gb: int | None = Field(default=None, ge=0)
    color: str | None = Field(default=None, max_length=50)
    variant_name: str | None = Field(default=None, max_length=200, description="Human-readable label, e.g. '12GB / 256GB / White'.")
    sku: str | None = Field(default=None, max_length=100, description="Manufacturer SKU/model identifier, if known.")


class ProductVariant(ProductVariantBase, table=True):
    __tablename__ = "product_variants"
    # A best-effort uniqueness guard: SQL treats NULL as distinct from any
    # other NULL, so two variants that both leave (say) color unset will
    # NOT collide on this constraint even if everything else matches --
    # documented here rather than silently assumed airtight.
    __table_args__ = (
        UniqueConstraint("product_id", "storage_gb", "ram_gb", "color", name="uq_variant_product_config"),
    )

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(SQLModel):
    storage_gb: int | None = Field(default=None, ge=0)
    ram_gb: int | None = Field(default=None, ge=0)
    color: str | None = Field(default=None, max_length=50)
    variant_name: str | None = Field(default=None, max_length=200)
    sku: str | None = Field(default=None, max_length=100)
    # product_id is deliberately not updatable -- moving a variant to a
    # different product is a data-modeling decision, not a field edit;
    # delete and recreate instead if that's genuinely needed.


class ProductVariantRead(ProductVariantBase):
    id: int
    created_at: datetime
    updated_at: datetime
