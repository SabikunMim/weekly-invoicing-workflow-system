from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_verification_check_successfully():
    client_response = client.post("/clients", json={
        "name": "Verification Test Client",
        "email": "verify@example.com",
        "client_type": "group",
        "billing_frequency": "weekly",
        "notes": "Client used for verification testing",
    })

    client_id = client_response.json()["id"]

    invoice_response = client.post("/invoice-records", json={
        "client_id": client_id,
        "week_start": "2026-06-13",
        "week_end": "2026-06-19",
        "service_description": "Weekly verification billing",
        "amount": 300.00,
        "status": "pending",
        "notes": "Needs two-level verification",
    })

    invoice_record_id = invoice_response.json()["id"]

    response = client.post("/verification-checks", json={
        "invoice_record_id": invoice_record_id,
        "completeness_checked": True,
        "accuracy_checked": False,
        "checked_by": "Rashida",
        "status": "in_progress",
        "notes": "Completeness checked, accuracy pending.",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["invoice_record_id"] == invoice_record_id
    assert data["completeness_checked"] is True
    assert data["accuracy_checked"] is False
    assert data["status"] == "in_progress"


def test_create_verification_check_requires_existing_invoice_record():
    response = client.post("/verification-checks", json={
        "invoice_record_id": 999,
        "completeness_checked": True,
        "accuracy_checked": True,
        "checked_by": "Rashida",
        "status": "completed",
        "notes": None,
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice record not found"


def test_list_verification_checks_returns_list():
    response = client.get("/verification-checks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)