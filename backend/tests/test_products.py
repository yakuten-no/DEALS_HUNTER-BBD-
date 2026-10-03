"""Tests for /api/products."""


def test_create_product_computes_normalized_name(client):
    response = client.post(
        "/api/products",
        json={"brand": "Nothing", "model_name": "Phone (3a) Pro", "category": "smartphone"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["brand"] == "Nothing"
    assert body["model_name"] == "Phone (3a) Pro"
    # normalized_name is server-computed, never trusted from the request --
    # there was no normalized_name in the payload above at all.
    assert body["normalized_name"] == "nothing phone 3a pro"
    assert body["is_demo"] is False  # default


def test_create_product_ignores_client_supplied_normalized_name(client):
    """Even if a caller tries to set normalized_name directly, the
    server-computed value wins -- it's not part of ProductCreate's schema
    at all, so FastAPI/Pydantic silently drops the extra field."""
    response = client.post(
        "/api/products",
        json={"brand": "Nothing", "model_name": "Phone 3a", "normalized_name": "totally different value"},
    )
    assert response.status_code == 201
    assert response.json()["normalized_name"] == "nothing phone 3a"


def test_create_product_rejects_duplicate_brand_and_normalized_name(client):
    payload = {"brand": "Nothing", "model_name": "Phone 3a"}
    assert client.post("/api/products", json=payload).status_code == 201
    duplicate = client.post("/api/products", json=payload)
    assert duplicate.status_code >= 400  # unique constraint -- see test_retailers.py's note on this


def test_list_products_defaults_and_variant_count(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"},
    )
    client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 256, "ram_gb": 12, "color": "White"},
    )

    response = client.get("/api/products")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["variant_count"] == 2


def test_list_products_filters_by_is_demo(client):
    client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a", "is_demo": False})
    client.post("/api/products", json={"brand": "Democorp", "model_name": "Demo Alpha", "is_demo": True})

    real_only = client.get("/api/products", params={"is_demo": False}).json()
    demo_only = client.get("/api/products", params={"is_demo": True}).json()
    assert len(real_only) == 1 and real_only[0]["brand"] == "Nothing"
    assert len(demo_only) == 1 and demo_only[0]["brand"] == "Democorp"


def test_get_product_detail_includes_variants(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"},
    )

    response = client.get(f"/api/products/{product['id']}")
    assert response.status_code == 200
    body = response.json()
    assert len(body["variants"]) == 1
    assert body["variants"][0]["storage_gb"] == 128


def test_get_missing_product_returns_404(client):
    assert client.get("/api/products/999999").status_code == 404


def test_update_product_recomputes_normalized_name(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    response = client.put(f"/api/products/{product['id']}", json={"model_name": "Phone (3a) Pro"})
    assert response.status_code == 200
    assert response.json()["normalized_name"] == "nothing phone 3a pro"


def test_delete_product_without_variants_succeeds(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    response = client.delete(f"/api/products/{product['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/products/{product['id']}").status_code == 404


def test_delete_product_with_variants_is_blocked(client):
    product = client.post("/api/products", json={"brand": "Nothing", "model_name": "Phone 3a"}).json()
    client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"},
    )

    response = client.delete(f"/api/products/{product['id']}")
    assert response.status_code == 409
    # Nothing was lost -- the product and its variant are both still there.
    assert client.get(f"/api/products/{product['id']}").status_code == 200
