"""
Seed a small set of CLEARLY LABELLED demo/fixture data for manually
exercising the Data Explorer during development.

============================== DEMO DATA ONLY ===============================
Everything this script creates is fictional. Retailer names are real (they
are just reference facts about which retailers exist -- see Retailer's
module docstring), but the product ("Democorp Demo Phone Alpha/Beta"),
every listing, every price, and every offer is made up for demonstration
purposes. Every Product and RetailerListing this script creates has
is_demo=True, and every PriceObservation/Offer's source_note/description
says so explicitly. None of it is a real observed price. Never remove the
is_demo flag or the DEMO SEED DATA labels to make this look more real.
===============================================================================

This is entirely optional and NOT run automatically anywhere (not on
backend startup, not in tests -- pytest uses its own small, isolated
fixtures instead, never this script). Run it yourself if you want
something to look at in the Data Explorer:

    cd backend
    python -m scripts.seed_demo_data

Safe to run more than once: if the demo data already exists, it says so
and exits without creating duplicates or raising an ugly error.
"""

import sys
from datetime import datetime, timedelta

from sqlmodel import Session

from app.database import engine, init_db
from app.models.offer import OfferCreate
from app.models.price_observation import PriceObservationCreate
from app.models.product import ProductCreate
from app.models.product_variant import ProductVariantCreate
from app.models.retailer import RetailerCreate
from app.models.retailer_listing import RetailerListingCreate
from app.services import (
    offer_service,
    price_observation_service,
    product_service,
    product_variant_service,
    retailer_listing_service,
    retailer_service,
)
from app.utils import utcnow

DEMO_NOTE = "DEMO SEED DATA -- not a real observed price, fixture only"

# Real retailer names (see the note at the top of this file for why that's fine) --
# these rows may already exist from earlier real usage, so we look them up
# by slug and only create what's missing.
RETAILERS = [
    RetailerCreate(name="Flipkart", slug="flipkart", website="https://www.flipkart.com"),
    RetailerCreate(name="Amazon India", slug="amazon-in", website="https://www.amazon.in"),
    RetailerCreate(name="Croma", slug="croma", website="https://www.croma.com"),
]


def days_ago(n: int) -> datetime:
    return utcnow() - timedelta(days=n)


def get_or_create_retailer(session: Session, data: RetailerCreate):
    existing = retailer_service.get_retailer_by_slug(session, data.slug)
    if existing is not None:
        return existing, False
    return retailer_service.create_retailer(session, data), True


def seed() -> None:
    print("=" * 70)
    print("BBD HUNTER -- DEMO DATA SEED SCRIPT")
    print("Everything this creates is fictional fixture data. See the")
    print("module docstring in this file for exactly what that means.")
    print("=" * 70)

    init_db()

    with Session(engine) as session:
        # --- Guard: if our demo product already exists, stop here rather
        # than raising a confusing UniqueConstraint error partway through. ---
        existing_products = product_service.list_products(session, is_demo=True, limit=1)
        if existing_products:
            print("\nDemo data already present (found an existing is_demo=True product).")
            print("Nothing to do -- delete it via the API first if you want to reseed.")
            return

        print("\nCreating retailers (real names, reference data only -- see docstring)...")
        retailers = {}
        for data in RETAILERS:
            retailer, created = get_or_create_retailer(session, data)
            retailers[data.slug] = retailer
            print(f"  {'created' if created else 'found existing'}: {retailer.name}")

        print("\nCreating DEMO products...")
        alpha = product_service.create_product(
            session,
            ProductCreate(
                brand="Democorp",
                model_name="Demo Phone Alpha",
                category="smartphone",
                description="Fictional phone used only to populate the Data Explorer for development. Not a real product.",
                is_demo=True,
            ),
        )
        beta = product_service.create_product(
            session,
            ProductCreate(
                brand="Democorp",
                model_name="Demo Phone Beta",
                category="smartphone",
                description="Fictional phone used only to populate the Data Explorer for development. Not a real product.",
                is_demo=True,
            ),
        )
        print(f"  created: {alpha.brand} {alpha.model_name} (id={alpha.id})")
        print(f"  created: {beta.brand} {beta.model_name} (id={beta.id})")

        print("\nCreating variants...")
        alpha_black = product_variant_service.create_variant(
            session,
            ProductVariantCreate(product_id=alpha.id, storage_gb=128, ram_gb=8, color="Black", variant_name="8GB / 128GB / Black"),
        )
        alpha_white = product_variant_service.create_variant(
            session,
            ProductVariantCreate(product_id=alpha.id, storage_gb=256, ram_gb=12, color="White", variant_name="12GB / 256GB / White"),
        )
        beta_blue = product_variant_service.create_variant(
            session,
            ProductVariantCreate(product_id=beta.id, storage_gb=128, ram_gb=8, color="Blue", variant_name="8GB / 128GB / Blue"),
        )
        print(f"  created {alpha_black.variant_name}, {alpha_white.variant_name}, {beta_blue.variant_name}")

        print("\nCreating listings...")
        # Downward price trend + guaranteed and conditional offers.
        flipkart_alpha_black = retailer_listing_service.create_listing(
            session,
            RetailerListingCreate(
                retailer_id=retailers["flipkart"].id,
                product_variant_id=alpha_black.id,
                product_url="https://www.flipkart.com/demo/demo-phone-alpha-8-128-black",
                listing_title="Democorp Demo Phone Alpha (8GB/128GB, Black) [DEMO]",
                availability="in_stock",
                is_demo=True,
            ),
        )
        # Out of stock, single observation -- demonstrates "insufficient history".
        amazon_alpha_black = retailer_listing_service.create_listing(
            session,
            RetailerListingCreate(
                retailer_id=retailers["amazon-in"].id,
                product_variant_id=alpha_black.id,
                product_url="https://www.amazon.in/dp/DEMOALPHA8128BLK",
                listing_title="Democorp Demo Phone Alpha (8GB/128GB, Black) [DEMO]",
                availability="out_of_stock",
                is_demo=True,
            ),
        )
        # No price observations at all -- demonstrates the "no history yet" empty state.
        croma_alpha_white = retailer_listing_service.create_listing(
            session,
            RetailerListingCreate(
                retailer_id=retailers["croma"].id,
                product_variant_id=alpha_white.id,
                product_url="https://www.croma.com/demo/demo-phone-alpha-12-256-white",
                listing_title="Democorp Demo Phone Alpha (12GB/256GB, White) [DEMO]",
                availability="in_stock",
                is_demo=True,
            ),
        )
        # Cashback example.
        flipkart_beta_blue = retailer_listing_service.create_listing(
            session,
            RetailerListingCreate(
                retailer_id=retailers["flipkart"].id,
                product_variant_id=beta_blue.id,
                product_url="https://www.flipkart.com/demo/demo-phone-beta-8-128-blue",
                listing_title="Democorp Demo Phone Beta (8GB/128GB, Blue) [DEMO]",
                availability="in_stock",
                is_demo=True,
            ),
        )
        print("  created 4 demo listings across Flipkart, Amazon India, and Croma")

        print("\nCreating price observations (clearly-labelled fixture data)...")
        downward_trend = [(28, 24999, 27999), (21, 23999, 27999), (14, 22999, 26999), (7, 21999, 26999), (0, 20999, 26999)]
        for days, price, mrp in downward_trend:
            price_observation_service.create_observation(
                session,
                PriceObservationCreate(
                    retailer_listing_id=flipkart_alpha_black.id,
                    observed_price=price,
                    mrp=mrp,
                    observed_at=days_ago(days),
                    source_note=DEMO_NOTE,
                ),
            )
        price_observation_service.create_observation(
            session,
            PriceObservationCreate(
                retailer_listing_id=amazon_alpha_black.id,
                observed_price=21499,
                mrp=27999,
                observed_at=days_ago(2),
                source_note=DEMO_NOTE,
            ),
        )
        for days, price in [(10, 19999), (0, 19499)]:
            price_observation_service.create_observation(
                session,
                PriceObservationCreate(
                    retailer_listing_id=flipkart_beta_blue.id,
                    observed_price=price,
                    mrp=22999,
                    observed_at=days_ago(days),
                    source_note=DEMO_NOTE,
                ),
            )
        print("  created 8 price observations (croma_alpha_white deliberately has none)")

        print("\nCreating offers...")
        offer_service.create_offer(
            session,
            OfferCreate(
                retailer_listing_id=flipkart_alpha_black.id,
                offer_type="instant_discount",
                title="[DEMO] Instant discount",
                description=DEMO_NOTE,
                discount_amount=1000,
                is_guaranteed=True,
            ),
        )
        offer_service.create_offer(
            session,
            OfferCreate(
                retailer_listing_id=flipkart_alpha_black.id,
                offer_type="bank_discount",
                title="[DEMO] 5% off with Demo Bank cards",
                description=DEMO_NOTE,
                discount_percentage=5,
                is_guaranteed=False,
                conditions="Valid only with Demo Bank credit/debit cards -- fictional, for demonstration.",
            ),
        )
        offer_service.create_offer(
            session,
            OfferCreate(
                retailer_listing_id=flipkart_beta_blue.id,
                offer_type="cashback",
                title="[DEMO] \u20b9500 cashback via Demo Wallet",
                description=DEMO_NOTE,
                discount_amount=500,
                is_guaranteed=True,
            ),
        )
        print("  created 3 offers (1 guaranteed, 1 conditional, 1 cashback)")

    print("\nDone. All rows created have is_demo=True and are clearly labelled [DEMO] / 'DEMO SEED DATA'.")
    print("Start the backend and frontend, then open the Data Explorer to see them.")


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:  # noqa: BLE001 -- top-level script entry point
        print(f"\nSeed script failed: {exc}", file=sys.stderr)
        raise
