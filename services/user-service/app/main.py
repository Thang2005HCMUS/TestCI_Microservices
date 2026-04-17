from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="User Service", version="1.0.0")

# In-memory store (no DB needed for CI practice)
_users: Dict[int, dict] = {}
_counter = 0


class UserCreate(BaseModel):
    name: str
    email: str


class User(UserCreate):
    id: int

def f():
    return 1
@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}


@app.get("/users")
def list_users():
    return list(_users.values())


@app.post("/users", response_model=User, status_code=201)
def create_user(payload: UserCreate):
    global _counter
    _counter += 1
    user = {"id": _counter, **payload.model_dump()}
    _users[_counter] = user
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="User not found")
    return _users[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="User not found")
    del _users[user_id]
