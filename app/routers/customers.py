from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/customers", tags=["customers"])

# Temporary in-memory storage (we’ll replace with a database next)
CUSTOMERS: dict[int, "Customer"] = {}
NEXT_ID = 1


class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class Customer(CustomerCreate):
    id: int


@router.get("/", response_model=list[Customer])
def list_customers():
    return list(CUSTOMERS.values())


@router.post("/", response_model=Customer, status_code=201)
def create_customer(payload: CustomerCreate):
    global NEXT_ID
    customer = Customer(id=NEXT_ID, **payload.model_dump())
    CUSTOMERS[NEXT_ID] = customer
    NEXT_ID += 1
    return customer


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, payload: CustomerCreate):
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    updated = Customer(id=customer_id, **payload.model_dump())
    CUSTOMERS[customer_id] = updated
    return updated


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    del CUSTOMERS[customer_id]
    return {"deleted": True, "id": customer_id}