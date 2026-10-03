"""Small database helpers shared by the V0.2 services."""

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.services.errors import DuplicateRecordError


def commit_unique(session: Session, conflict_message: str) -> None:
    """Commit, translating a UNIQUE-constraint violation into a clean
    `DuplicateRecordError` (HTTP 409) instead of letting the raw database
    error escape as an unhandled 500.

    Only genuine unique violations are translated. Any other integrity
    error (a missing foreign key, a NOT NULL violation, ...) still
    propagates, because that would indicate a bug rather than a
    user-correctable conflict. The transaction is rolled back either way
    so the session stays usable afterwards.
    """
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        if "unique" in str(exc.orig).lower():
            raise DuplicateRecordError(conflict_message) from exc
        raise
