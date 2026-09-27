"""
FastAPI application entry point.

Run with (from inside backend/, with the virtual environment active):
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import health, wishlists


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts, before it accepts requests.
    init_db()
    yield
    # (nothing to clean up on shutdown yet)


app = FastAPI(
    title="BBD Hunter API",
    description="Local-first AI shopping intelligence backend -- V0.1 foundation.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(wishlists.router)
