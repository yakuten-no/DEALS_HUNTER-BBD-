"""
The RetailerListing model: one retailer's page for one specific
ProductVariant. The same ProductVariant can have many listings -- one per
retailer, or even several from different sellers on the same retailer
(hence `seller_name`).
"""

from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.enums import AvailabilityStatus
from app.utils import utcnow


class RetailerListingBase(SQLModel):
    retailer_id: int = Field(foreign_key="retailers.id", index=True)
    product_variant_id: int = Field(foreign_key="product_variants.id", index=True)
    seller_name: str | None = Field(default=None, max_length=200, description="Marketplace seller, if applicable.")
    external_listing_id: str | None = Field(default=None, max_length=200, description="The retailer's own ID for this listing.")
    product_url: str = Field(min_length=1, max_length=1000, index=True, unique=True)
    listing_title: str | None = Field(default=None, max_length=500, description="Title as shown on the retailer's page.")
    # Plain str, validated as Literal["in_stock","out_of_stock","unknown"]
    # only at the API layer -- see app/models/enums.py for why.
    availability: str = Field(default="unknown", max_length=20)
    is_demo: bool = Field(default=False, index=True, description="See Product.is_demo -- same purpose, listing level.")


class RetailerListing(RetailerListingBase, table=True):
    __tablename__ = "retailer_listings"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class RetailerListingCreate(RetailerListingBase):
    # Overrides the table's plain-str field with the validated Literal --
    # see app/models/enums.py for why the table column itself stays plain str.
    availability: AvailabilityStatus = "unknown"


class RetailerListingUpdate(SQLModel):
    seller_name: str | None = Field(default=None, max_length=200)
    external_listing_id: str | None = Field(default=None, max_length=200)
    listing_title: str | None = Field(default=None, max_length=500)
    availability: AvailabilityStatus | None = None
    # retailer_id, product_variant_id, and product_url are deliberately
    # not updatable for the same reason as ProductVariant.product_id above.


class RetailerListingRead(RetailerListingBase):
    id: int
    created_at: datetime
    updated_at: datetime


class RetailerListingListItem(RetailerListingRead):
    """List view: latest observed price, computed in one batched query
    across the whole page of results (see get_latest_observations_by_listing
    in app/services/price_observation_service.py) -- never one query per row."""

    latest_price: int | None = None
    latest_observed_at: datetime | None = None
