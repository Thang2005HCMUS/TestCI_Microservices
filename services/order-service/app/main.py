from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Order Service", version="1.0.0")

_orders: Dict[int, dict] = {}
_counter = 0


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]


class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    status: str = "pending"


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@app.get("/orders")
def list_orders():
    return list(_orders.values())


@app.post("/orders", response_model=Order, status_code=201)
def create_order(payload: OrderCreate):
    global _counter
    _counter += 1
    order = {"id": _counter, "status": "pending", **payload.model_dump()}
    _orders[_counter] = order
    return order


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in _orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return _orders[order_id]


@app.patch("/orders/{order_id}/status")
def update_status(order_id: int, status: str):
    if order_id not in _orders:
        raise HTTPException(status_code=404, detail="Order not found")
    _orders[order_id]["status"] = status
    return _orders[order_id]
