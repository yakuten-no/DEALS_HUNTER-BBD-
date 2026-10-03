"""Service layer for Retailer records. No delete endpoint by design --
retailers are reference data; deactivate with is_active=False instead of
deleting, which sidesteps having to decide what happens to its listings."""

from sqlmodel import Session, select

from app.models.retailer import Retailer, RetailerCreate, RetailerUpdate
from app.services.db_helpers import commit_unique
from app.utils import utcnow


def create_retailer(session: Session, data: RetailerCreate) -> Retailer:
    retailer = Retailer.model_validate(data)
    session.add(retailer)
    commit_unique(session, "A retailer with this slug already exists.")
    session.refresh(retailer)
    return retailer


def list_retailers(session: Session, is_active: bool | None = None) -> list[Retailer]:
    statement = select(Retailer).order_by(Retailer.name)
    if is_active is not None:
        statement = statement.where(Retailer.is_active == is_active)
    return list(session.exec(statement).all())


def get_retailer(session: Session, retailer_id: int) -> Retailer | None:
    return session.get(Retailer, retailer_id)


def get_retailer_by_slug(session: Session, slug: str) -> Retailer | None:
    return session.exec(select(Retailer).where(Retailer.slug == slug)).first()


def update_retailer(session: Session, retailer: Retailer, data: RetailerUpdate) -> Retailer:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(retailer, field, value)
    retailer.updated_at = utcnow()
    session.add(retailer)
    commit_unique(session, "A retailer with this slug already exists.")
    session.refresh(retailer)
    return retailer
