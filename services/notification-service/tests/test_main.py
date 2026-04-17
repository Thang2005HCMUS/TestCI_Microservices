from fastapi.testclient import TestClient
from app.main import app, _notifications

client = TestClient(app)


def setup_function():
    _notifications.clear()


def test_health():
    assert client.get("/health").json()["service"] == "notification-service"


def test_send_email():
    payload = {
        "recipient": "user@example.com",
        "subject": "Order shipped",
        "body": "Your order is on the way!",
        "channel": "email",
    }
    res = client.post("/notify", json=payload)
    assert res.status_code == 202
    assert res.json()["delivered"] is True or "id" in res.json()


def test_send_sms():
    payload = {
        "recipient": "+84901234567",
        "subject": "OTP",
        "body": "Your OTP is 123456",
        "channel": "sms",
    }
    res = client.post("/notify", json=payload)
    assert res.status_code == 202


def test_list_notifications():
    client.post("/notify", json={
        "recipient": "a@b.com", "subject": "Hi", "body": "Hello", "channel": "push"
    })
    res = client.get("/notifications")
    assert res.status_code == 200
    assert len(res.json()) >= 1
