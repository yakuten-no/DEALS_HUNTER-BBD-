"""
Shared pytest fixtures for backend tests.

Tests run against an isolated in-memory SQLite database, so running the
suite never touches the real development database file at
database/bbd_hunter.db.

Run with `pytest` from inside the backend/ directory -- pytest.ini adds
this directory to the import path so `app` can be imported directly.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

# Point the app at an in-memory database *before* importing any app
# module, since app.config.Settings reads DATABASE_URL at import time.
# This means the app's own module-level engine never touches the real
# database file during tests, even before the fixtures below run.
os.environ["DATABASE_URL"] = "sqlite://"

from app.database import get_session  # noqa: E402  (must follow the os.environ line above)
from app.main import app  # noqa: E402


@pytest.fixture(name="session")
def session_fixture():
    """A fresh in-memory database, recreated for every test."""
    # StaticPool makes every connection from this engine share the same
    # in-memory database; without it, each connection would see a blank
    # database of its own, which breaks anything that opens more than
    # one connection (the app does, once per request).
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Match production (app/database.py): SQLite only enforces foreign keys
    # when this pragma is on for each connection, so without it the test
    # database would be more permissive than the real one.
    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """A FastAPI TestClient wired to the `session` fixture's database."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
