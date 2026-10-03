"""Tests for /api/retailer-listings."""


def _make_variant(client, storage_gb=128):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    return client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": storage_gb}).json()


def _make_retailer(client, name="Flipkart", slug="flipkart"):
    return client.post("/api/retailers", json={"name": name, "slug": slug}).json()


def test_create_listing(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    response = client.post(
        "/api/retailer-listings",
        json={
            "retailer_id": retailer["id"],
            "product_variant_id": variant["id"],
            "product_url": "https://www.flipkart.com/nothing-phone-3a",
            "listing_title": "Nothing Phone (3a), 128GB",
            "availability": "in_stock",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["availability"] == "in_stock"
    assert body["is_demo"] is False


def test_create_listing_rejects_invalid_availability_value(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    response = client.post(
        "/api/retailer-listings",
        json={
            "retailer_id": retailer["id"],
            "product_variant_id": variant["id"],
            "product_url": "https://www.flipkart.com/x",
            "availability": "definitely_not_a_real_status",
        },
    )
    assert response.status_code == 422


def test_create_listing_rejects_nonexistent_retailer_or_variant(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)

    bad_retailer = client.post(
        "/api/retailer-listings",
        json={"retailer_id": 999999, "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    )
    assert bad_retailer.status_code == 422

    bad_variant = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": 999999, "product_url": "https://x.com/b"},
    )
    assert bad_variant.status_code == 422


def test_create_listing_rejects_duplicate_url(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    payload = {"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/same"}
    assert client.post("/api/retailer-listings", json=payload).status_code == 201
    duplicate = client.post("/api/retailer-listings", json=payload)
    assert duplicate.status_code >= 400  # unique constraint -- see test_retailers.py's note on this


def test_same_variant_can_have_listings_across_multiple_retailers(client):
    variant = _make_variant(client)
    flipkart = _make_retailer(client, "Flipkart", "flipkart")
    amazon = _make_retailer(client, "Amazon India", "amazon-in")

    client.post(
        "/api/retailer-listings",
        json={"retailer_id": flipkart["id"], "product_variant_id": variant["id"], "product_url": "https://flipkart.com/x"},
    )
    client.post(
        "/api/retailer-listings",
        json={"retailer_id": amazon["id"], "product_variant_id": variant["id"], "product_url": "https://amazon.in/x"},
    )

    listings = client.get("/api/retailer-listings", params={"product_variant_id": variant["id"]}).json()
    assert len(listings) == 2
    assert {listing["retailer_id"] for listing in listings} == {flipkart["id"], amazon["id"]}


def test_list_listings_includes_latest_price(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    listing = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()

    # Explicit, clearly-ordered timestamps -- not relying on two calls to
    # "now" a few milliseconds apart to land in a guaranteed order.
    client.post(
        "/api/price-observations",
        json={"retailer_listing_id": listing["id"], "observed_price": 24999, "observed_at": "2026-01-01T00:00:00"},
    )
    client.post(
        "/api/price-observations",
        json={"retailer_listing_id": listing["id"], "observed_price": 22999, "observed_at": "2026-01-08T00:00:00"},
    )

    listings = client.get("/api/retailer-listings").json()
    assert len(listings) == 1
    assert listings[0]["latest_price"] == 22999  # the later-dated observation, not the later-created one


def test_list_listings_latest_price_is_none_without_observations(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    )
    listings = client.get("/api/retailer-listings").json()
    assert listings[0]["latest_price"] is None


def test_get_missing_listing_returns_404(client):
    assert client.get("/api/retailer-listings/999999").status_code == 404


def test_update_listing_availability(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    listing = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()

    response = client.put(f"/api/retailer-listings/{listing['id']}", json={"availability": "out_of_stock"})
    assert response.status_code == 200
    assert response.json()["availability"] == "out_of_stock"


def test_delete_listing_with_history_is_blocked(client):
    variant = _make_variant(client)
    retailer = _make_retailer(client)
    listing = client.post(
        "/api/retailer-listings",
        json={"retailer_id": retailer["id"], "product_variant_id": variant["id"], "product_url": "https://x.com/a"},
    ).json()
    client.post("/api/price-observations", json={"retailer_listing_id": listing["id"], "observed_price": 24999})

    response = client.delete(f"/api/retailer-listings/{listing['id']}")
    assert response.status_code == 409
