"""
Shared controlled-vocabulary types for the product/deal data model.

These are plain `typing.Literal` aliases, validated by Pydantic at the API
boundary -- not `enum.Enum` mapped to a SQLAlchemy `Enum` column. SQLAlchemy's
automatic Enum-to-column mapping has a real, version-dependent ambiguity
between storing a member's `.name` vs its `.value`, which can't be verified
without actually running the installed version (see project-memory/DECISIONS.md).
The table columns for these fields are plain `str`; only the Create/Update
API schemas use these Literal aliases for validation.
"""

from typing import Literal

AvailabilityStatus = Literal["in_stock", "out_of_stock", "unknown"]
AVAILABILITY_VALUES: tuple[str, ...] = ("in_stock", "out_of_stock", "unknown")

OfferType = Literal[
    "bank_discount",
    "coupon",
    "exchange_bonus",
    "cashback",
    "emi_offer",
    "card_discount",
    "instant_discount",
    "other",
]
OFFER_TYPE_VALUES: tuple[str, ...] = (
    "bank_discount",
    "coupon",
    "exchange_bonus",
    "cashback",
    "emi_offer",
    "card_discount",
    "instant_discount",
    "other",
)
