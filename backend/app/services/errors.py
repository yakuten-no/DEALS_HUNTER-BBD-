"""
Shared service-layer exceptions for the V0.2 product/deal data model.

Routers catch these and translate them into HTTP responses (422 for a
reference to something that doesn't exist, 409 for a delete blocked by
dependent rows) -- see app/routers/*.py. Kept separate from any one
service module so every V0.2 service can raise and catch the same types
consistently, the same way wishlist_service.WishlistValidationError works
in V0.1.
"""


class NotFoundReferenceError(ValueError):
    """A request referenced an id (e.g. product_id, retailer_id) that
    doesn't exist. Distinct from "the resource itself wasn't found" --
    this is about something the request *points at*."""


class HasDependentsError(ValueError):
    """A delete was blocked because dependent rows exist (e.g. deleting a
    Product that still has ProductVariants). Deliberately RESTRICT, not
    CASCADE: this app's core promise is never losing price history, so a
    delete never silently takes historical data down with it -- the
    caller must delete the dependents first, or keep the parent."""


class DuplicateRecordError(ValueError):
    """A create or update would duplicate a record that must be unique
    (e.g. a second retailer with the same slug, or a second listing for
    the same product URL). Mapped to HTTP 409 in app/main.py."""
