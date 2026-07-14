from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_invoice_record_successfully():
    client_response = client.post("/clients", json={
        "name": "Travel Group Client",
        "email": "group@example.com",
        "client_type": "group",
        "billing_frequency": "weekly",
        "notes": "Group booking client",
    })

    client_id = client_response.json()["id"]

    response = client.post("/invoice-records", json={
        "client_id": client_id,
        "week_start": "2026-06-13",
        "week_end": "2026-06-19",
        "service_description": "Weekly group activity billing",
        "amount": 450.00,
        "status": "pending",
        "notes": "Needs calendar verification",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["client_id"] == client_id
    assert data["amount"] == 450.00
    assert data["status"] == "pending"


def test_create_invoice_record_requires_existing_client():
    response = client.post("/invoice-records", json={
        "client_id": 999,
        "week_start": "2026-06-13",
        "week_end": "2026-06-19",
        "service_description": "Invalid client invoice",
        "amount": 100.00,
        "status": "pending",
        "notes": None,
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_list_invoice_records_returns_records():
    response = client.get("/invoice-records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)