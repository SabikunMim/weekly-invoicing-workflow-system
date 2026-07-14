from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_monthly_statement_successfully():
    client_response = client.post("/clients", json={
        "name": "Monthly Statement Client",
        "email": "monthly@example.com",
        "client_type": "group",
        "billing_frequency": "monthly",
        "notes": "Group client needing monthly statements",
    })

    client_id = client_response.json()["id"]

    response = client.post("/monthly-statements", json={
        "client_id": client_id,
        "statement_month": "2026-06",
        "due_date": "2026-07-10",
        "status": "pending",
        "total_amount": 1250.00,
        "sent_date": None,
        "notes": "Statement should be sent by the 10th.",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["client_id"] == client_id
    assert data["statement_month"] == "2026-06"
    assert data["due_date"] == "2026-07-10"
    assert data["status"] == "pending"
    assert data["total_amount"] == 1250.00


def test_create_monthly_statement_requires_existing_client():
    response = client.post("/monthly-statements", json={
        "client_id": 999,
        "statement_month": "2026-06",
        "due_date": "2026-07-10",
        "status": "pending",
        "total_amount": 500.00,
        "sent_date": None,
        "notes": None,
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_list_monthly_statements_returns_list():
    response = client.get("/monthly-statements")

    assert response.status_code == 200
    assert isinstance(response.json(), list)