"""Tests for /api/product-variants."""


def _make_product(client, brand="Nothing", model_name="Phone 3a"):
    return client.post("/api/products", json={"brand": brand, "model_name": model_name}).json()


def test_create_variant(client):
    product = _make_product(client)
    response = client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] == product["id"]
    assert body["storage_gb"] == 128
    assert body["ram_gb"] == 8
    assert body["color"] == "Black"


def test_create_variant_rejects_nonexistent_product(client):
    response = client.post(
        "/api/product-variants", json={"product_id": 999999, "storage_gb": 128, "ram_gb": 8, "color": "Black"}
    )
    assert response.status_code == 422


def test_different_configs_do_not_collapse_into_one_variant(client):
    """8GB/128GB and 12GB/256GB must stay distinguishable -- D-007."""
    product = _make_product(client)
    a = client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"},
    ).json()
    b = client.post(
        "/api/product-variants",
        json={"product_id": product["id"], "storage_gb": 256, "ram_gb": 12, "color": "White"},
    ).json()
    assert a["id"] != b["id"]

    variants = client.get("/api/product-variants", params={"product_id": product["id"]}).json()
    assert len(variants) == 2
    configs = {(v["storage_gb"], v["ram_gb"], v["color"]) for v in variants}
    assert configs == {(128, 8, "Black"), (256, 12, "White")}


def test_create_variant_rejects_exact_duplicate_config(client):
    product = _make_product(client)
    payload = {"product_id": product["id"], "storage_gb": 128, "ram_gb": 8, "color": "Black"}
    assert client.post("/api/product-variants", json=payload).status_code == 201
    duplicate = client.post("/api/product-variants", json=payload)
    assert duplicate.status_code >= 400  # unique constraint -- see test_retailers.py's note on this


def test_list_variants_filters_by_product(client):
    product_a = _make_product(client, "Nothing", "Phone 3a")
    product_b = _make_product(client, "Samsung", "Galaxy S24")
    client.post("/api/product-variants", json={"product_id": product_a["id"], "storage_gb": 128})
    client.post("/api/product-variants", json={"product_id": product_b["id"], "storage_gb": 256})

    only_a = client.get("/api/product-variants", params={"product_id": product_a["id"]}).json()
    assert len(only_a) == 1
    assert only_a[0]["product_id"] == product_a["id"]


def test_get_missing_variant_returns_404(client):
    assert client.get("/api/product-variants/999999").status_code == 404


def test_update_variant(client):
    product = _make_product(client)
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    response = client.put(f"/api/product-variants/{variant['id']}", json={"color": "Blue"})
    assert response.status_code == 200
    assert response.json()["color"] == "Blue"
    assert response.json()["storage_gb"] == 128  # untouched


def test_delete_variant_without_listings_succeeds(client):
    product = _make_product(client)
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    response = client.delete(f"/api/product-variants/{variant['id']}")
    assert response.status_code == 204


def test_delete_variant_with_listings_is_blocked(client):
    product = _make_product(client)
    variant = client.post("/api/product-variants", json={"product_id": product["id"], "storage_gb": 128}).json()
    retailer = client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"}).json()
    client.post(
        "/api/retailer-listings",
        json={
            "retailer_id": retailer["id"],
            "product_variant_id": variant["id"],
            "product_url": "https://www.flipkart.com/x",
        },
    )

    response = client.delete(f"/api/product-variants/{variant['id']}")
    assert response.status_code == 409
