from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint_returns_running_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_client_successfully():
    response = client.post("/clients", json={
        "name": "Sean Davoren",
        "email": "sean@example.com",
        "client_type": "business",
        "billing_frequency": "weekly",
        "notes": "Service business client"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sean Davoren"
    assert data["client_type"] == "business"
    assert data["billing_frequency"] == "weekly"
    assert "id" in data


def test_list_clients_returns_created_clients():
    response = client.get("/clients")

    assert response.status_code == 200
    assert isinstance(response.json(), list)