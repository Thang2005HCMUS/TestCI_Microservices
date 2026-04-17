from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Product Service", version="1.0.0")

_products: Dict[int, dict] = {}
_counter = 0

def cal(l):
    return sum(l)
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0


class Product(ProductCreate):
    id: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}


@app.get("/products")
def list_products():
    return list(_products.values())


@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate):
    global _counter
    _counter += 1
    product = {"id": _counter, **payload.model_dump()}
    _products[_counter] = product
    return product


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    return _products[product_id]
