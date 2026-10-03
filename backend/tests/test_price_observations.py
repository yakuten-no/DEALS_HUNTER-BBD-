"""Tests for /api/price-observations -- create + read only, by design."""


def _make_listing(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"}).json()
    return client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()


def test_create_observation(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/price-observations",
        json={"retailer_listing_id": listing["id"], "observed_price": 24999, "mrp": 27999},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["observed_price"] == 24999
    assert body["mrp"] == 27999
    assert body["currency"] == "INR"  # default
    assert body["observed_at"] is not None  # defaulted server-side


def test_create_observation_rejects_nonexistent_listing(client):
    response = client.post("/api/price-observations", json={"retailer_listing_id": 999999, "observed_price": 24999})
    assert response.status_code == 422


def test_create_observation_rejects_negative_price(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": -100}
    )
    assert response.status_code == 422


def test_multiple_observations_never_overwrite_each_other(client):
    """The core promise: a new observation is a new row, not an update to
    an existing one -- history is never lost."""
    listing = _make_listing(client)
    prices = [24999, 23999, 22999, 24999]  # deliberately includes a repeat and a rise, not just a clean decline
    for i, price in enumerate(prices):
        client.post(
            "/api/price-observations",
            json={
                "retailer_listing_id": listing["id"],
                "observed_price": price,
                "observed_at": f"2026-01-{i + 1:02d}T00:00:00",
            },
        )

    history = client.get("/api/price-observations", params={"retailer_listing_id": listing["id"]}).json()
    assert len(history) == 4
    assert [h["observed_price"] for h in history] == [24999, 22999, 23999, 24999]  # newest first


def test_list_observations_requires_retailer_listing_id(client):
    response = client.get("/api/price-observations")
    assert response.status_code == 422  # required query param missing


def test_get_single_observation(client):
    listing = _make_listing(client)
    created = client.post(
        "/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 24999}
    ).json()
    response = client.get(f"/api/price-observations/{created['id']}")
    assert response.status_code == 200
    assert response.json()["observed_price"] == 24999


def test_get_missing_observation_returns_404(client):
    assert client.get("/api/price-observations/999999").status_code == 404


def test_price_observations_have_no_update_endpoint(client):
    listing = _make_listing(client)
    created = client.post(
        "/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 24999}
    ).json()
    response = client.put(f"/api/price-observations/{created['id']}", json={"observed_price": 1})
    assert response.status_code == 405


def test_price_observations_have_no_delete_endpoint(client):
    listing = _make_listing(client)
    created = client.post(
        "/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 24999}
    ).json()
    response = client.delete(f"/api/price-observations/{created['id']}")
    assert response.status_code == 405
