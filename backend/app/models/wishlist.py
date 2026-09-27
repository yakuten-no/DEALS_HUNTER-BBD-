"""
The wishlist domain model.

A wishlist entry is one thing the user wants to track. In V0.1 there is no
AI yet, so the only field we truly trust is `raw_query` -- exactly what the
user typed. Every "structured" field (budget, storage, priorities, ...) is
optional and defaults to "not specified." A later version will let AI
suggest values for these from `raw_query` (see project-memory/ROADMAP.md,
V0.5), but V0.1 never pretends that has already happened: nothing here is
inferred or guessed on the backend's own initiative.

Four classes share one set of fields, each for a different job:
- WishlistBase   shared field definitions (not a table on its own)
- Wishlist       the actual database table
- WishlistCreate what the API accepts when creating an entry
- WishlistUpdate what the API accepts when updating an entry (all optional)
- WishlistRead   what the API returns to clients
"""

from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.utils import utcnow


class WishlistBase(SQLModel):
    """Fields shared by every wishlist schema."""

    name: str = Field(min_length=1, max_length=200, description="Short label for this entry, e.g. 'Diwali upgrade'.")
    raw_query: str = Field(
        min_length=1,
        max_length=4000,
        description="The user's natural-language request, stored exactly as typed.",
    )

    # --- Structured preferences (all optional -- see module docstring) ---
    # Budget is stored in whole Indian Rupees (not paise), since retail
    # phone prices in India are effectively always whole rupees.
    budget_target: int | None = Field(default=None, ge=0, description="Comfortable target price in INR.")
    budget_max: int | None = Field(default=None, ge=0, description="Hard ceiling price in INR.")
    minimum_storage_gb: int | None = Field(default=None, ge=0)
    preferred_ram_gb: int | None = Field(default=None, ge=0)

    # Priority flags: True = the user cares about this, None = not stated.
    # There is deliberately no explicit "False" path exposed in the V0.1
    # UI (see frontend WishlistForm) -- an unchecked box just leaves the
    # preference unstated rather than asserting the user doesn't want it.
    camera_priority: bool | None = None
    gaming_priority: bool | None = None
    battery_priority: bool | None = None
    wireless_charging_preferred: bool | None = None

    preferred_brands: list[str] | None = None
    preferred_os: str | None = Field(default=None, max_length=100)


class Wishlist(WishlistBase, table=True):
    """The `wishlists` database table."""

    __tablename__ = "wishlists"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    # SQLite has no native array/list column type. SQLModel's plain type
    # annotation (inherited from WishlistBase) doesn't know how to store a
    # Python list, so only the table class overrides the field with an
    # explicit JSON column -- the request/response schemas below don't
    # need this, since they aren't mapped to a table.
    preferred_brands: list[str] | None = Field(default=None, sa_column=Column(JSON))


class WishlistCreate(WishlistBase):
    """Fields accepted by POST /api/wishlists.

    `name` is optional here even though it's required on the table: if
    omitted, the service layer derives a short name from `raw_query`
    (simple truncation -- not AI) before the row is created.
    """

    name: str | None = Field(default=None, max_length=200)


class WishlistUpdate(SQLModel):
    """Fields accepted by PUT /api/wishlists/{id}.

    Every field is optional. Only fields actually present in the request
    body are applied -- omitted fields leave the existing value untouched.
    (This makes PUT behave like a partial update rather than a full
    replace; see the docstring on the update endpoint for why.)
    """

    name: str | None = Field(default=None, min_length=1, max_length=200)
    raw_query: str | None = Field(default=None, min_length=1, max_length=4000)
    budget_target: int | None = Field(default=None, ge=0)
    budget_max: int | None = Field(default=None, ge=0)
    minimum_storage_gb: int | None = Field(default=None, ge=0)
    preferred_ram_gb: int | None = Field(default=None, ge=0)
    camera_priority: bool | None = None
    gaming_priority: bool | None = None
    battery_priority: bool | None = None
    wireless_charging_preferred: bool | None = None
    preferred_brands: list[str] | None = None
    preferred_os: str | None = Field(default=None, max_length=100)


class WishlistRead(WishlistBase):
    """Fields returned by the API.

    Inherits `name: str` (required) from WishlistBase unchanged -- only
    WishlistCreate relaxes it to optional. Every stored row always has a
    real name by the time it's read back (see WishlistCreate's docstring).
    """

    id: int
    created_at: datetime
    updated_at: datetime
