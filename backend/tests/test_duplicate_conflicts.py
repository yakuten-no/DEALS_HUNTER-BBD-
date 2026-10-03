"""Duplicate values for unique fields must be a clean HTTP 409, never an
unhandled database error (which surfaced as a 500 before this fix)."""


def _retailer(client, name="Flipkart", slug="flipkart"):
    return client.post("/api/retailers", json={"name": name, "slug": slug})


def _product(client, brand="Nothing", model="Phone 3a"):
    return client.post("/api/products", json={"brand": brand, "model_name": model})


def test_duplicate_retailer_slug_returns_409(client):
    assert _retailer(client).status_code == 201
    response = _retailer(client, name="Flipkart Again")
    assert response.status_code == 409
    assert "slug" in response.json()["detail"].lower()


def test_duplicate_product_returns_409_even_with_different_formatting(client):
    assert _product(client).status_code == 201
    # Normalization makes these the same product (case/whitespace differ only).
    assert _product(client, brand="Nothing", model="  phone   3A ").status_code == 409


def test_duplicate_variant_config_returns_409(client):
    product = _product(client).json()
    payload = {"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"}
    assert client.post("/api/product-variants", json=payload).status_code == 201
    assert client.post("/api/product-variants", json=payload).status_code == 409


def test_duplicate_listing_url_returns_409(client):
    product = _product(client).json()
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = _retailer(client).json()
    payload = {
        "retailer_id": retailer["id"],
        "product_variant_id": variant["id"],
        "product_url": "https://www.flipkart.com/p/1",
    }
    assert client.post("/api/retailer-listings", json=payload).status_code == 201
    assert client.post("/api/retailer-listings", json=payload).status_code == 409


def test_update_that_collides_returns_409(client):
    _retailer(client, name="Flipkart", slug="flipkart")
    other = _retailer(client, name="Croma", slug="croma").json()
    response = client.put(f"/api/retailers/{other['id']}", json={"slug": "flipkart"})
    assert response.status_code == 409


def test_database_remains_usable_after_a_409(client):
    """A failed commit must be rolled back so the next request succeeds."""
    assert _retailer(client).status_code == 201
    assert _retailer(client, name="Dup").status_code == 409
    assert _retailer(client, name="Croma", slug="croma").status_code == 201
    assert len(client.get("/api/retailers").json()) == 2
