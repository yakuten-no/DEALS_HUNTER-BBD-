"""
The Offer model: a normalized representation of one discount/cashback/
condition attached to a RetailerListing. `is_guaranteed` is the field that
implements D-006 (project-memory/DECISIONS.md): guaranteed discounts apply
without extra conditions; conditional ones (bank card, exchange, coupon,
EMI, membership, limited eligibility) do not. Cashback is its own
`offer_type` and is never netted into an "effective price" regardless of
`is_guaranteed` -- see app/deal_engine/assessment.py for exactly how these
are combined.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.enums import OfferType
from app.utils import UTCDatetime, utcnow


class OfferBase(SQLModel):
    retailer_listing_id: int = Field(foreign_key="retailer_listings.id", index=True)
    # Plain str, validated as the OfferType Literal only at the API layer
    # -- see app/models/enums.py for why.
    offer_type: str = Field(max_length=30)
    title: str = Field(min_length=1, max_length=300, description="Short label, e.g. '10% off with HDFC cards'.")
    description: str | None = Field(default=None, max_length=1000)
    discount_amount: int | None = Field(default=None, ge=0, description="Flat INR discount, if stated.")
    discount_percentage: float | None = Field(default=None, ge=0, le=100, description="Percentage discount, if stated.")
    is_guaranteed: bool = Field(
        default=False,
        description="True only if this applies with no extra requirements. False = conditional (D-006).",
    )
    conditions: str | None = Field(default=None, max_length=1000, description="Free-text eligibility/conditions.")
    valid_from: UTCDatetime | None = None
    valid_until: UTCDatetime | None = None


class Offer(OfferBase, table=True):
    __tablename__ = "offers"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class OfferCreate(OfferBase):
    # Overrides the table's plain-str field with the validated Literal --
    # see app/models/enums.py for why the table column itself stays plain str.
    offer_type: OfferType


class OfferUpdate(SQLModel):
    offer_type: OfferType | None = None
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=1000)
    discount_amount: int | None = Field(default=None, ge=0)
    discount_percentage: float | None = Field(default=None, ge=0, le=100)
    is_guaranteed: bool | None = None
    conditions: str | None = Field(default=None, max_length=1000)
    valid_from: UTCDatetime | None = None
    valid_until: UTCDatetime | None = None


class OfferRead(OfferBase):
    id: int
    created_at: datetime
    updated_at: datetime
