
from fastapi.testclient import TestClient
from app.main import app, _users

client = TestClient(app)


def setup_function():
    _users.clear()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["service"] == "user-service"


def test_create_and_get_user():
    res = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert res.status_code == 201
    user = res.json()
    assert user["name"] == "Alice"

    res2 = client.get(f"/users/{user['id']}")
    assert res2.status_code == 200
    assert res2.json()["email"] == "alice@example.com"


def test_list_users():
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    res = client.get("/users")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_delete_user():
    res = client.post("/users", json={"name": "Carol", "email": "carol@example.com"})
    uid = res.json()["id"]
    del_res = client.delete(f"/users/{uid}")
    assert del_res.status_code == 204
    assert client.get(f"/users/{uid}").status_code == 404


def test_get_not_found():
    res = client.get("/users/9999")
    assert res.status_code == 404
