"""Tests for /api/wishlists CRUD endpoints."""


def test_create_wishlist(client):
    payload = {
        "name": "Diwali upgrade",
        "raw_query": "Phone around 60k with a great camera and 256GB storage",
        "budget_target": 60000,
        "budget_max": 70000,
        "minimum_storage_gb": 256,
        "camera_priority": True,
        "preferred_brands": ["Nothing", "Samsung"],
    }
    response = client.post("/api/wishlists", json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["id"] is not None
    assert body["name"] == payload["name"]
    assert body["raw_query"] == payload["raw_query"]
    assert body["budget_target"] == 60000
    assert body["camera_priority"] is True
    assert body["preferred_brands"] == ["Nothing", "Samsung"]
    # Fields never mentioned in the payload stay genuinely unset, not guessed.
    assert body["gaming_priority"] is None
    assert body["preferred_os"] is None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_wishlist_derives_name_when_omitted(client):
    long_query = "A phone with an excellent camera, strong gaming performance, and long battery life for daily use"
    response = client.post("/api/wishlists", json={"raw_query": long_query})
    assert response.status_code == 201

    body = response.json()
    assert body["name"]  # a name was derived, not left blank
    assert body["name"] != long_query  # and it was actually shortened
    assert body["name"].endswith("...")


def test_create_wishlist_rejects_empty_raw_query(client):
    response = client.post("/api/wishlists", json={"name": "Something", "raw_query": ""})
    assert response.status_code == 422


def test_create_wishlist_requires_raw_query(client):
    response = client.post("/api/wishlists", json={"name": "No query given"})
    assert response.status_code == 422


def test_create_wishlist_treats_empty_name_as_omitted(client):
    """An empty-string name is treated the same as leaving it out entirely
    -- both fall back to a derived name -- rather than being rejected."""
    response = client.post("/api/wishlists", json={"name": "", "raw_query": "a query with no name given"})
    assert response.status_code == 201
    assert response.json()["name"] == "a query with no name given"


def test_create_wishlist_rejects_invalid_budget_range(client):
    payload = {"name": "Bad budget", "raw_query": "test", "budget_target": 80000, "budget_max": 50000}
    response = client.post("/api/wishlists", json=payload)
    assert response.status_code == 422


def test_create_wishlist_rejects_negative_budget(client):
    payload = {"name": "Negative budget", "raw_query": "test", "budget_target": -1000}
    response = client.post("/api/wishlists", json=payload)
    assert response.status_code == 422


def test_list_wishlists(client):
    client.post("/api/wishlists", json={"name": "A", "raw_query": "q1"})
    client.post("/api/wishlists", json={"name": "B", "raw_query": "q2"})

    response = client.get("/api/wishlists")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_wishlists_empty_when_none_created(client):
    response = client.get("/api/wishlists")
    assert response.status_code == 200
    assert response.json() == []


def test_get_wishlist_by_id(client):
    created = client.post("/api/wishlists", json={"name": "A", "raw_query": "q1"}).json()

    response = client.get(f"/api/wishlists/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_wishlist_returns_404(client):
    response = client.get("/api/wishlists/999999")
    assert response.status_code == 404


def test_update_wishlist_changes_only_given_fields(client):
    created = client.post("/api/wishlists", json={"name": "A", "raw_query": "q1"}).json()

    response = client.put(
        f"/api/wishlists/{created['id']}",
        json={"budget_target": 55000, "camera_priority": True},
    )
    assert response.status_code == 200

    body = response.json()
    assert body["budget_target"] == 55000
    assert body["camera_priority"] is True
    assert body["name"] == "A"  # untouched field is preserved
    assert body["raw_query"] == "q1"  # untouched field is preserved
    assert body["updated_at"] >= created["updated_at"]


def test_update_wishlist_rejects_invalid_budget_range_against_existing_value(client):
    created = client.post(
        "/api/wishlists",
        json={"name": "A", "raw_query": "q1", "budget_target": 60000, "budget_max": 70000},
    ).json()

    # Only budget_max is sent, but it now conflicts with the *stored* budget_target.
    response = client.put(f"/api/wishlists/{created['id']}", json={"budget_max": 50000})
    assert response.status_code == 422


def test_update_missing_wishlist_returns_404(client):
    response = client.put("/api/wishlists/999999", json={"name": "x"})
    assert response.status_code == 404


def test_delete_wishlist(client):
    created = client.post("/api/wishlists", json={"name": "A", "raw_query": "q1"}).json()

    response = client.delete(f"/api/wishlists/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/api/wishlists/{created['id']}")
    assert response.status_code == 404


def test_delete_missing_wishlist_returns_404(client):
    response = client.delete("/api/wishlists/999999")
    assert response.status_code == 404
