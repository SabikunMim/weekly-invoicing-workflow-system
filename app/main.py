from fastapi import FastAPI

app = FastAPI(
    title="Weekly Invoicing Workflow System",
    description="Backend system for tracking clients, weekly invoice records, exceptions, and reconciliation checks.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Weekly Invoicing Workflow System API",
        "status": "running",
    }