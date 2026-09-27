"""
Database engine and session management.

V0.1 uses SQLite and creates tables directly from the SQLModel class
definitions (`SQLModel.metadata.create_all`). There is no migration tool
yet -- that's a deliberate V0.1 scope cut, not an oversight (see
project-memory/DECISIONS.md). If a model's fields change during
development, the simplest fix is to delete the local database file at
database/bbd_hunter.db and let it regenerate; a real migration tool
(e.g. Alembic) should be introduced before this matters for real data.
"""

from collections.abc import Generator
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.config import settings


def _sqlite_file_path(database_url: str) -> Path | None:
    """Return the filesystem path a `sqlite:///...` URL points at.

    Returns None for in-memory databases (`sqlite://`, `sqlite:///:memory:`)
    or any non-SQLite URL, since there's no on-disk parent directory to
    create in those cases.
    """
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return None
    raw_path = database_url.removeprefix(prefix)
    if raw_path in ("", ":memory:"):
        return None
    return Path(raw_path)


# SQLite needs its containing directory to already exist -- it will
# happily create the .db file itself, but not any missing parent folders.
_db_path = _sqlite_file_path(settings.database_url)
if _db_path is not None:
    _db_path.parent.mkdir(parents=True, exist_ok=True)

# `check_same_thread=False` is required for SQLite specifically: FastAPI
# runs request handlers in a small thread pool, and SQLite's default
# driver otherwise refuses to reuse a connection across threads.
_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, echo=settings.debug, connect_args=_connect_args)


def init_db() -> None:
    """Create any tables that don't exist yet, based on registered models."""
    # Imported here (not at module load time) so that every model module
    # is registered on SQLModel.metadata before create_all runs, without
    # creating a circular import between database.py and the models.
    from app.models import wishlist  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that provides one database session per request."""
    with Session(engine) as session:
        yield session
