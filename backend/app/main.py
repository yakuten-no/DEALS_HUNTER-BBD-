"""
FastAPI application entry point.

Run with (from inside backend/, with the virtual environment active):
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routers import health, offers, price_observations, product_variants, products, retailer_listings, retailers, wishlists
from app.services.errors import DuplicateRecordError, HasDependentsError, NotFoundReferenceError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts, before it accepts requests.
    init_db()
    yield
    # (nothing to clean up on shutdown yet)


app = FastAPI(
    title="BBD Hunter API",
    description="Local-first AI shopping intelligence backend -- V0.2, product & deal data foundation.",
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


# Shared V0.2 error types (app/services/errors.py) are handled once, here,
# rather than with a try/except repeated in every new router function.
# V0.1's wishlist router predates this and keeps its own try/except
# pattern unchanged -- both are valid, and there's no working code to
# gain by refactoring it to match.
@app.exception_handler(NotFoundReferenceError)
async def handle_not_found_reference(request: Request, exc: NotFoundReferenceError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(DuplicateRecordError)
async def handle_duplicate_record(request: Request, exc: DuplicateRecordError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(HasDependentsError)
async def handle_has_dependents(request: Request, exc: HasDependentsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(health.router)
app.include_router(wishlists.router)
app.include_router(retailers.router)
app.include_router(products.router)
app.include_router(product_variants.router)
app.include_router(retailer_listings.router)
app.include_router(price_observations.router)
app.include_router(offers.router)
