from fastapi import FastAPI, HTTPException

from app.schemas import Client, ClientCreate, InvoiceRecord, InvoiceRecordCreate

app = FastAPI(
    title="Weekly Invoicing Workflow System",
    description="Backend system for tracking clients, weekly invoice records, exceptions, and reconciliation checks.",
    version="0.1.0",
)

clients: list[Client] = []
next_client_id = 1

invoice_records: list[InvoiceRecord] = []
next_invoice_record_id = 1


@app.get("/")
def root():
    return {
        "message": "Weekly Invoicing Workflow System API",
        "status": "running",
    }


@app.post("/clients", response_model=Client, status_code=201)
def create_client(client_data: ClientCreate):
    global next_client_id

    client = Client(
        id=next_client_id,
        **client_data.model_dump(),
    )

    clients.append(client)
    next_client_id += 1

    return client


@app.get("/clients", response_model=list[Client])
def list_clients():
    return clients


@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: int):
    for client in clients:
        if client.id == client_id:
            return client

    raise HTTPException(status_code=404, detail="Client not found")


@app.post("/invoice-records", response_model=InvoiceRecord, status_code=201)
def create_invoice_record(invoice_data: InvoiceRecordCreate):
    global next_invoice_record_id

    client_exists = any(client.id == invoice_data.client_id for client in clients)

    if not client_exists:
        raise HTTPException(status_code=404, detail="Client not found")

    invoice_record = InvoiceRecord(
        id=next_invoice_record_id,
        **invoice_data.model_dump(),
    )

    invoice_records.append(invoice_record)
    next_invoice_record_id += 1

    return invoice_record


@app.get("/invoice-records", response_model=list[InvoiceRecord])
def list_invoice_records():
    return invoice_records