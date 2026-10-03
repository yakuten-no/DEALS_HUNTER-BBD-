"""
The PriceObservation model: one timestamped price sighting for one
RetailerListing. This is append-only by design -- there is deliberately
no update or delete endpoint (see app/routers/price_observations.py).
"Do not overwrite historical prices" is enforced by simply never exposing
a way to.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel

from app.utils import UTCDatetime, utcnow


class PriceObservationBase(SQLModel):
    retailer_listing_id: int = Field(foreign_key="retailer_listings.id", index=True)
    observed_price: int = Field(ge=0, description="Whole INR, matching the Wishlist model's convention.")
    mrp: int | None = Field(default=None, ge=0, description="Original/MRP price as shown on the listing, if available.")
    currency: str = Field(default="INR", max_length=10)
    source_note: str | None = Field(
        default=None,
        max_length=300,
        description="Free-text context, e.g. how this was collected. Demo/fixture rows must say so here.",
    )


class PriceObservation(PriceObservationBase, table=True):
    __tablename__ = "price_observations"

    id: int | None = Field(default=None, primary_key=True)
    # The timestamp the price was actually true in the world. Indexed:
    # this is the field every history query orders and filters by.
    observed_at: datetime = Field(default_factory=utcnow, index=True)
    # When we recorded it -- usually the same instant as observed_at in
    # V0.2 (no live collectors yet), but conceptually distinct, and worth
    # keeping separate now rather than needing a migration to add it later
    # once collection delay is a real thing (a backfilled or delayed
    # observation would have created_at meaningfully later than observed_at).
    created_at: datetime = Field(default_factory=utcnow)


class PriceObservationCreate(PriceObservationBase):
    # Allows a caller (e.g. the seed script) to backdate observed_at to
    # build a realistic-looking history; defaults to "now" if omitted.
    observed_at: UTCDatetime | None = None


class PriceObservationRead(PriceObservationBase):
    id: int
    observed_at: datetime
    created_at: datetime
