"""Tests for GET /api/health."""


def test_health_reports_ok_status(client):
    response = client.get("/api/health")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "bbd-hunter"
    assert "version" in body


def test_health_reports_database_connected(client):
    """The database field is a real check, not a hardcoded value -- with
    the test database wired up, it should genuinely report 'connected'."""
    response = client.get("/api/health")
    assert response.json()["database"] == "connected"
