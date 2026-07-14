from fastapi import FastAPI, HTTPException

from app.schemas import Client, ClientCreate

app = FastAPI(
    title="Weekly Invoicing Workflow System",
    description="Backend system for tracking clients, weekly invoice records, exceptions, and reconciliation checks.",
    version="0.1.0",
)

clients: list[Client] = []
next_client_id = 1


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
        **client_data.model_dump()
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