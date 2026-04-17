
from fastapi.testclient import TestClient
from app.main import app, _products

client = TestClient(app)


def setup_function():
    _products.clear()


def test_health():
    res = client.get("/health")
    assert res.json()["service"] == "product-service"


def test_create_product():
    res = client.post("/products", json={"name": "Widget", "price": 9.99, "stock": 100})
    assert res.status_code == 201
    assert res.json()["name"] == "Widget"


def test_list_products():
    client.post("/products", json={"name": "Gadget", "price": 19.99})
    res = client.get("/products")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_not_found():
    res = client.get("/products/9999")
    assert res.status_code == 404
