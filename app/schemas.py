from datetime import date
from typing import Optional

from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    client_type: str
    billing_frequency: str = "weekly"
    notes: Optional[str] = None


class Client(ClientCreate):
    id: int


class InvoiceRecordCreate(BaseModel):
    client_id: int
    week_start: date
    week_end: date
    service_description: str
    amount: float
    status: str = "pending"
    notes: Optional[str] = None


class InvoiceRecord(InvoiceRecordCreate):
    id: int

class ExceptionItemCreate(BaseModel):
    invoice_record_id: int
    issue_type: str
    description: str
    severity: str = "medium"
    status: str = "open"
    needs_sean_review: bool = False
    notes: Optional[str] = None


class ExceptionItem(ExceptionItemCreate):
    id: int