from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_exception_item_successfully():
    client_response = client.post("/clients", json={
        "name": "Sean Test Client",
        "email": "client@example.com",
        "client_type": "group",
        "billing_frequency": "weekly",
        "notes": "Client used for exception testing",
    })

    client_id = client_response.json()["id"]

    invoice_response = client.post("/invoice-records", json={
        "client_id": client_id,
        "week_start": "2026-06-13",
        "week_end": "2026-06-19",
        "service_description": "Weekly group activity billing",
        "amount": 450.00,
        "status": "pending",
        "notes": "Needs calendar verification",
    })

    invoice_record_id = invoice_response.json()["id"]

    response = client.post("/exceptions", json={
        "invoice_record_id": invoice_record_id,
        "issue_type": "missing_calendar_record",
        "description": "Calendar activity is missing for this invoice record.",
        "severity": "high",
        "status": "open",
        "needs_sean_review": True,
        "notes": "Confirm with Sean before sending invoice.",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["invoice_record_id"] == invoice_record_id
    assert data["issue_type"] == "missing_calendar_record"
    assert data["needs_sean_review"] is True


def test_create_exception_requires_existing_invoice_record():
    response = client.post("/exceptions", json={
        "invoice_record_id": 999,
        "issue_type": "pricing_mismatch",
        "description": "Invoice amount does not match expected pricing.",
        "severity": "medium",
        "status": "open",
        "needs_sean_review": True,
        "notes": None,
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice record not found"


def test_list_exception_items_returns_list():
    response = client.get("/exceptions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)