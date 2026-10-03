"""Tests for /api/offers."""


import itertools

# Product names, retailer slugs and listing URLs are all unique in the
# database, so a helper that may be called more than once per test (e.g. to
# build two separate listings) must generate distinct values on each call.
_counter = itertools.count(1)


def _make_listing(client):
    n = next(_counter)
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": f"Phone {n}a"}).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": f"Retailer {n}", "slug": f"retailer-{n}"}).json()
    return client.post(
        "/api/retailer-listings",
        json={
            "retailer_id": retailer["id"],
            "product_variant_id": variant["id"],
            "product_url": f"https://x.com/listing-{n}",
        },
    ).json()


def test_create_guaranteed_offer(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/offers",
        json={
            "retailer_listing_id": listing["id"],
            "offer_type": "instant_discount",
            "title": "Instant discount",
            "discount_amount": 1000,
            "is_guaranteed": True,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["is_guaranteed"] is True
    assert body["discount_amount"] == 1000


def test_create_conditional_offer_with_percentage(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/offers",
        json={
            "retailer_listing_id": listing["id"],
            "offer_type": "bank_discount",
            "title": "5% off with HDFC cards",
            "discount_percentage": 5,
            "is_guaranteed": False,
            "conditions": "Valid only with HDFC Bank credit cards.",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["is_guaranteed"] is False
    assert body["discount_percentage"] == 5
    assert body["conditions"]


def test_create_offer_rejects_invalid_offer_type(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/offers",
        json={"retailer_listing_id": listing["id"], "offer_type": "not_a_real_type", "title": "x"},
    )
    assert response.status_code == 422


def test_create_offer_rejects_nonexistent_listing(client):
    response = client.post(
        "/api/offers", json={"retailer_listing_id": 999999, "offer_type": "coupon", "title": "x"}
    )
    assert response.status_code == 422


def test_create_offer_rejects_percentage_over_100(client):
    listing = _make_listing(client)
    response = client.post(
        "/api/offers",
        json={"retailer_listing_id": listing["id"], "offer_type": "coupon", "title": "x", "discount_percentage": 150},
    )
    assert response.status_code == 422


def test_list_offers_scoped_to_listing(client):
    listing_a = _make_listing(client)
    listing_b = _make_listing(client)
    client.post("/api/offers", json={"retailer_listing_id": listing_a["id"], "offer_type": "coupon", "title": "A"})
    client.post("/api/offers", json={"retailer_listing_id": listing_b["id"], "offer_type": "coupon", "title": "B"})

    only_a = client.get("/api/offers", params={"retailer_listing_id": listing_a["id"]}).json()
    assert len(only_a) == 1
    assert only_a[0]["title"] == "A"


def test_get_missing_offer_returns_404(client):
    assert client.get("/api/offers/999999").status_code == 404


def test_update_offer(client):
    listing = _make_listing(client)
    offer = client.post(
        "/api/offers", json={"retailer_listing_id": listing["id"], "offer_type": "coupon", "title": "SAVE10"}
    ).json()
    response = client.put(f"/api/offers/{offer['id']}", json={"is_guaranteed": True})
    assert response.status_code == 200
    assert response.json()["is_guaranteed"] is True
    assert response.json()["title"] == "SAVE10"  # untouched


def test_delete_offer(client):
    listing = _make_listing(client)
    offer = client.post(
        "/api/offers", json={"retailer_listing_id": listing["id"], "offer_type": "coupon", "title": "SAVE10"}
    ).json()
    response = client.delete(f"/api/offers/{offer['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/offers/{offer['id']}").status_code == 404
