"""Small helpers shared across the backend."""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current time as a naive UTC datetime.

    SQLite has no native timezone-aware datetime type, so every timestamp
    in this project is stored naive but is always UTC by convention (never
    local time). Using one shared helper -- instead of `datetime.now()` or
    the deprecated `datetime.utcnow()` scattered around the codebase --
    keeps that convention consistent everywhere.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
