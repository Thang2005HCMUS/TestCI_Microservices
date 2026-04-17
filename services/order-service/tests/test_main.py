from fastapi.testclient import TestClient
from app.main import app, _orders

client = TestClient(app)


def setup_function():
    _orders.clear()


def test_health():
    assert client.get("/health").json()["service"] == "order-service"


def test_create_order():
    payload = {"user_id": 1, "items": [{"product_id": 10, "quantity": 2}]}
    res = client.post("/orders", json=payload)
    assert res.status_code == 201
    assert res.json()["status"] == "pending"


def test_get_order():
    payload = {"user_id": 2, "items": [{"product_id": 5, "quantity": 1}]}
    order_id = client.post("/orders", json=payload).json()["id"]
    res = client.get(f"/orders/{order_id}")
    assert res.status_code == 200
    assert res.json()["user_id"] == 2


def test_update_status():
    payload = {"user_id": 3, "items": [{"product_id": 7, "quantity": 3}]}
    order_id = client.post("/orders", json=payload).json()["id"]
    res = client.patch(f"/orders/{order_id}/status", params={"status": "shipped"})
    assert res.json()["status"] == "shipped"


def test_order_not_found():
    assert client.get("/orders/9999").status_code == 404
