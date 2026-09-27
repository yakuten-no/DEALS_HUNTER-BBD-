"""Health/status endpoint used by the frontend's system-status panel."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session

from app.config import settings
from app.database import get_session

router = APIRouter(tags=["health"])


@router.get("/api/health")
def get_health(session: Session = Depends(get_session)) -> dict:
    """Report whether the API and database are actually reachable.

    This runs a trivial query against the database rather than assuming
    it's fine -- the `database` field below reflects what really
    happened, which is what lets the frontend show a genuine status
    instead of a hardcoded "connected".
    """
    try:
        session.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        database_status = "error"

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "database": database_status,
    }
