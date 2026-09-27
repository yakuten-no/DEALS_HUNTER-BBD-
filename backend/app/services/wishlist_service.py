"""
Domain/service layer for wishlist entries.

Keeping this logic separate from the API routes (app/routers/wishlists.py)
means the same rules apply no matter how they're eventually invoked -- from
the REST API today, or from a future CLI, background job, or the
deterministic rule engine described in project-memory/ARCHITECTURE.md.
Routes should stay thin: parse the request, call a function here, translate
the result (or error) into an HTTP response.
"""

from sqlmodel import Session, select

from app.models.wishlist import Wishlist, WishlistCreate, WishlistUpdate
from app.utils import utcnow

_NAME_TRUNCATE_LENGTH = 60


class WishlistValidationError(ValueError):
    """Field values that are individually valid but inconsistent together.

    Example: budget_target higher than budget_max. Field-level checks
    (e.g. "must be >= 0") are handled by Pydantic on the model itself;
    this is for rules that span more than one field.
    """


def _default_name(raw_query: str) -> str:
    """Derive a short label from a query when the user doesn't give one.

    This is plain string truncation, not interpretation -- it does not
    attempt to understand the query. Real natural-language parsing is an
    AI feature planned for a later version (see project-memory/ROADMAP.md).
    """
    text = raw_query.strip()
    if len(text) <= _NAME_TRUNCATE_LENGTH:
        return text
    return text[: _NAME_TRUNCATE_LENGTH - 3].rstrip() + "..."


def _validate_budget_range(budget_target: int | None, budget_max: int | None) -> None:
    if budget_target is not None and budget_max is not None and budget_target > budget_max:
        raise WishlistValidationError("budget_target cannot be greater than budget_max")


def create_wishlist(session: Session, data: WishlistCreate) -> Wishlist:
    """Validate and persist a new wishlist entry."""
    _validate_budget_range(data.budget_target, data.budget_max)

    payload = data.model_dump()
    if not payload.get("name"):
        payload["name"] = _default_name(data.raw_query)

    wishlist = Wishlist.model_validate(payload)
    session.add(wishlist)
    session.commit()
    session.refresh(wishlist)
    return wishlist


def list_wishlists(session: Session) -> list[Wishlist]:
    """Return every wishlist entry, most recently created first."""
    statement = select(Wishlist).order_by(Wishlist.created_at.desc())
    return list(session.exec(statement).all())


def get_wishlist(session: Session, wishlist_id: int) -> Wishlist | None:
    """Look up one wishlist entry by id, or None if it doesn't exist."""
    return session.get(Wishlist, wishlist_id)


def update_wishlist(session: Session, wishlist: Wishlist, data: WishlistUpdate) -> Wishlist:
    """Apply only the fields present in `data` to an existing entry.

    Cross-field validation (budget_target vs budget_max) checks the
    *resulting* values -- combining whatever the request changes with
    whatever the record already has -- so a request that only touches
    budget_max still gets rejected if it would conflict with the
    existing budget_target, not just a newly-supplied one.
    """
    updates = data.model_dump(exclude_unset=True)

    resulting_target = updates.get("budget_target", wishlist.budget_target)
    resulting_max = updates.get("budget_max", wishlist.budget_max)
    _validate_budget_range(resulting_target, resulting_max)

    for field, value in updates.items():
        setattr(wishlist, field, value)
    wishlist.updated_at = utcnow()

    session.add(wishlist)
    session.commit()
    session.refresh(wishlist)
    return wishlist


def delete_wishlist(session: Session, wishlist: Wishlist) -> None:
    """Permanently remove a wishlist entry."""
    session.delete(wishlist)
    session.commit()
