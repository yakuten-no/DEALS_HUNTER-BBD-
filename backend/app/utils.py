"""Small helpers shared across the backend.

Datetime convention (project-wide): every timestamp is a timezone-aware
datetime in UTC. SQLModel's `datetime` column type (`UTCDateTime`) enforces
this at the database boundary -- it refuses naive values on write and
always returns aware UTC values on read, including on SQLite, which has no
native timezone support. Three pieces keep the rest of the code consistent
with that:

- `utcnow()`       the only way application code should ask for "now".
- `ensure_utc()`   normalizes a datetime from outside the app.
- `UTCDatetime`    a pydantic type that applies `ensure_utc` automatically
                   to API input fields, so a request can't reach the
                   database with a naive or non-UTC value.
"""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime) -> datetime:
    """Return `value` as a timezone-aware UTC datetime.

    - Aware values (e.g. "2026-09-30T10:00:00+05:30") are converted to UTC.
    - Naive values are interpreted as already being UTC. That is the
      convention V0.1 documented ("naive, but always UTC"), so callers that
      omit an offset keep the meaning they always had. A naive value is
      ambiguous by nature; this is a deliberate, documented default, not a
      guess about the caller's local time zone.
    """
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


# For annotating schema fields that accept a datetime from a caller.
UTCDatetime = Annotated[datetime, AfterValidator(ensure_utc)]
