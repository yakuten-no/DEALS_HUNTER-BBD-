"""Regression tests for the project-wide datetime convention:
timezone-aware UTC everywhere (see app/utils.py).

Root cause these guard against: the installed SQLModel stores `datetime`
columns as `UTCDateTime`, which rejects naive values. The app used to
generate naive timestamps, so every insert failed on a live run.
"""

from datetime import datetime, timedelta, timezone

import pytest
from sqlmodel import select

from app.models.offer import Offer
from app.models.price_observation import PriceObservation
from app.models.wishlist import Wishlist
from app.utils import ensure_utc, utcnow


def _utc_offset(dt: datetime):
    return dt.utcoffset()


def test_utcnow_is_timezone_aware_utc():
    now = utcnow()
    assert _utc_offset(now) == timedelta(0)


def test_ensure_utc_treats_naive_as_utc():
    naive = datetime(2026, 9, 30, 10, 0, 0)
    result = ensure_utc(naive)
    assert _utc_offset(result) == timedelta(0)
    assert result.replace(tzinfo=None) == naive  # same wall-clock value, now labelled UTC


def test_ensure_utc_converts_other_offsets_to_utc():
    ist = timezone(timedelta(hours=5, minutes=30))
    result = ensure_utc(datetime(2026, 9, 30, 15, 30, 0, tzinfo=ist))
    assert result == datetime(2026, 9, 30, 10, 0, 0, tzinfo=timezone.utc)
    assert _utc_offset(result) == timedelta(0)


def test_timestamps_round_trip_through_the_database_as_aware_utc(session):
    session.add(Wishlist(name="w", raw_query="q"))
    session.commit()
    stored = session.exec(select(Wishlist)).one()
    session.expire_all()
    stored = session.exec(select(Wishlist)).one()
    assert _utc_offset(stored.created_at) == timedelta(0)
    assert _utc_offset(stored.updated_at) == timedelta(0)


def _make_listing(client):
    product = client.post("/api/products", json={"brand": "Acme", "model_name": "Dt1"}).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": "R", "slug": "r"}).json()
    return client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/dt"},
    ).json()


@pytest.mark.parametrize(
    "sent, expected_utc",
    [
        ("2026-09-01T10:00:00", datetime(2026, 9, 1, 10, 0, tzinfo=timezone.utc)),  # naive -> UTC
        ("2026-09-01T10:00:00Z", datetime(2026, 9, 1, 10, 0, tzinfo=timezone.utc)),
        ("2026-09-01T15:30:00+05:30", datetime(2026, 9, 1, 10, 0, tzinfo=timezone.utc)),  # offset -> UTC
    ],
)
def test_observed_at_input_is_normalized_to_utc(client, session, sent, expected_utc):
    listing = _make_listing(client)
    response = client.post(
        "/api/price-observations",
        json={"retailer_listing_id": listing["id"], "observed_price": 50000, "observed_at": sent},
    )
    assert response.status_code == 201
    stored = session.exec(select(PriceObservation)).one()
    assert stored.observed_at == expected_utc
    assert _utc_offset(stored.observed_at) == timedelta(0)
    # And the API response itself carries an explicit UTC marker, so a
    # browser can't misread it as local time.
    assert datetime.fromisoformat(response.json()["observed_at"].replace("Z", "+00:00")) == expected_utc
    assert response.json()["observed_at"].endswith(("Z", "+00:00"))


def test_offer_validity_window_input_is_normalized_to_utc(client, session):
    listing = _make_listing(client)
    response = client.post(
        "/api/offers",
        json={
            "retailer_listing_id": listing["id"],
            "offer_type": "coupon",
            "title": "Window",
            "valid_from": "2026-09-01T00:00:00",
            "valid_until": "2026-09-30T23:59:59+05:30",
        },
    )
    assert response.status_code == 201
    stored = session.exec(select(Offer)).one()
    assert stored.valid_from == datetime(2026, 9, 1, tzinfo=timezone.utc)
    assert stored.valid_until == datetime(2026, 9, 30, 18, 29, 59, tzinfo=timezone.utc)


def test_observation_defaults_to_now_when_observed_at_omitted(client, session):
    listing = _make_listing(client)
    before = utcnow()
    assert (
        client.post(
            "/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 1}
        ).status_code
        == 201
    )
    after = utcnow()
    stored = session.exec(select(PriceObservation)).one()
    assert before <= stored.observed_at <= after


def test_history_orders_correctly_across_mixed_timezone_inputs(client):
    """Two observations sent with different offsets must order by the real
    instant they describe, not by their textual wall-clock time."""
    listing = _make_listing(client)
    # 10:00 UTC (sent as +05:30 wall-clock 15:30) is EARLIER than 12:00 UTC.
    for price, ts in [(200, "2026-09-01T12:00:00Z"), (100, "2026-09-01T15:30:00+05:30")]:
        client.post(
            "/api/price-observations",
            json={"retailer_listing_id": listing["id"], "observed_price": price, "observed_at": ts},
        )
    history = client.get("/api/price-observations", params={"retailer_listing_id": listing["id"]}).json()
    assert [o["observed_price"] for o in history] == [200, 100]  # newest first
