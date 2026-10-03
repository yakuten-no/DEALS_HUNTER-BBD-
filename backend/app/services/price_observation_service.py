"""
Service layer for PriceObservation records.

Deliberately create + list + get only -- no update, no delete. Price
observations are historical fact once recorded; "do not overwrite
historical prices" is enforced by simply never exposing a way to (see the
model's module docstring and app/routers/price_observations.py).
"""

from sqlmodel import Session, select

from app.models.price_observation import PriceObservation, PriceObservationCreate
from app.models.retailer_listing import RetailerListing
from app.services.errors import NotFoundReferenceError
from app.utils import utcnow


def create_observation(session: Session, data: PriceObservationCreate) -> PriceObservation:
    if session.get(RetailerListing, data.retailer_listing_id) is None:
        raise NotFoundReferenceError(f"No retailer listing with id {data.retailer_listing_id}")
    payload = data.model_dump()
    if payload.get("observed_at") is None:
        payload["observed_at"] = utcnow()
    observation = PriceObservation.model_validate(payload)
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation


def list_observations(
    session: Session, retailer_listing_id: int, limit: int = 200, offset: int = 0
) -> list[PriceObservation]:
    """Full history for one listing, newest first."""
    statement = (
        select(PriceObservation)
        .where(PriceObservation.retailer_listing_id == retailer_listing_id)
        .order_by(PriceObservation.observed_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(session.exec(statement).all())


def get_observation(session: Session, observation_id: int) -> PriceObservation | None:
    return session.get(PriceObservation, observation_id)


def get_latest_observations_by_listing(session: Session, listing_ids: list[int]) -> dict[int, PriceObservation]:
    """Most recent observation per listing, across many listings, in ONE
    query -- not one query per listing (avoids N+1). Fetches all matching
    rows ordered newest-first and keeps the first one seen per listing_id,
    rather than a SQL window function: window-function support varies by
    the SQLite build actually installed, and this project favors code
    that's simply, verifiably correct over code that's clever but
    unverifiable in this environment (see project-memory/DECISIONS.md).
    Fine at V0.2's data scale; worth revisiting if observation volume
    grows a lot once real collectors exist.
    """
    if not listing_ids:
        return {}
    statement = (
        select(PriceObservation)
        .where(PriceObservation.retailer_listing_id.in_(listing_ids))
        .order_by(PriceObservation.observed_at.desc())
    )
    latest: dict[int, PriceObservation] = {}
    for observation in session.exec(statement).all():
        if observation.retailer_listing_id not in latest:
            latest[observation.retailer_listing_id] = observation
    return latest
