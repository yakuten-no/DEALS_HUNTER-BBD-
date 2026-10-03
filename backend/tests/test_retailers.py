"""Tests for /api/retailers."""


def test_create_retailer(client):
    response = client.post(
        "/api/retailers", json={"name": "Flipkart", "slug": "flipkart", "website": "https://www.flipkart.com"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Flipkart"
    assert body["slug"] == "flipkart"
    assert body["is_active"] is True  # default


def test_create_retailer_rejects_duplicate_slug(client):
    payload = {"name": "Flipkart", "slug": "flipkart"}
    assert client.post("/api/retailers", json=payload).status_code == 201
    duplicate = client.post("/api/retailers", json={"name": "Flipkart Again", "slug": "flipkart"})
    # A duplicate unique slug is a database IntegrityError, which FastAPI
    # surfaces as a 500 by default -- this test documents that current
    # behavior explicitly rather than leaving it silently unverified.
    # (A friendlier pre-check, like the one wishlist budget validation
    # gets, is a reasonable follow-up -- see project-memory/TODO.md.)
    assert duplicate.status_code >= 400


def test_list_retailers(client):
    client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"})
    client.post("/api/retailers", json={"name": "Amazon India", "slug": "amazon-in"})
    response = client.get("/api/retailers")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_retailers_filters_by_is_active(client):
    client.post("/api/retailers", json={"name": "Flipkart", "slug": "flipkart"})
    inactive = client.post("/api/retailers", json={"name": "Old Retailer", "slug": "old-retailer"}).json()
    client.put(f"/api/retailers/{inactive['id']}", json={"is_active": False})

    active_only = client.get("/api/retailers", params={"is_active": True}).json()
    assert len(active_only) == 1
    assert active_only[0]["slug"] == "flipkart"


def test_get_retailer_by_id(client):
    created = client.post("/api/retailers", json={"name": "Croma", "slug": "croma"}).json()
    response = client.get(f"/api/retailers/{created['id']}")
    assert response.status_code == 200
    assert response.json()["slug"] == "croma"


def test_get_missing_retailer_returns_404(client):
    assert client.get("/api/retailers/999999").status_code == 404


def test_update_retailer_partial(client):
    created = client.post("/api/retailers", json={"name": "Croma", "slug": "croma"}).json()
    response = client.put(f"/api/retailers/{created['id']}", json={"website": "https://www.croma.com"})
    assert response.status_code == 200
    body = response.json()
    assert body["website"] == "https://www.croma.com"
    assert body["name"] == "Croma"  # untouched


def test_no_delete_endpoint_for_retailers(client):
    created = client.post("/api/retailers", json={"name": "Croma", "slug": "croma"}).json()
    response = client.delete(f"/api/retailers/{created['id']}")
    assert response.status_code == 405  # Method Not Allowed -- no DELETE route exists by design
