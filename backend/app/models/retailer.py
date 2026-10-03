"""
The Retailer model: reference data about a store BBD Hunter might track
listings from (Flipkart, Amazon India, Croma, ...). A Retailer row is just
a fact about which retailer exists -- it is never, on its own, a claim
about live pricing. See project-memory/DECISIONS.md for why retailers are
treated as safe-to-seed reference data while product/price/offer demo data
is kept clearly and structurally labelled as such.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel

from app.utils import utcnow


class RetailerBase(SQLModel):
    name: str = Field(min_length=1, max_length=200, description="Display name, e.g. 'Flipkart'.")
    slug: str = Field(
        min_length=1,
        max_length=100,
        index=True,
        unique=True,
        description="URL/code-safe identifier, e.g. 'flipkart'. Must be unique.",
    )
    website: str | None = Field(default=None, max_length=500, description="Base URL, e.g. https://www.flipkart.com")
    is_active: bool = Field(default=True, description="Whether this retailer is currently enabled for tracking.")


class Retailer(RetailerBase, table=True):
    __tablename__ = "retailers"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class RetailerCreate(RetailerBase):
    pass


class RetailerUpdate(SQLModel):
    """All fields optional -- only fields present in the request change."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    website: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class RetailerRead(RetailerBase):
    id: int
    created_at: datetime
    updated_at: datetime
