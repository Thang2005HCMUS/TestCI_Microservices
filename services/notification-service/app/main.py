from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Notification Service", version="1.0.0")

# Mock: store sent notifications in memory
_notifications: List[dict] = []


class NotificationRequest(BaseModel):
    recipient: str
    subject: str
    body: str
    channel: str = "email"   # email | sms | push

def NewMethod():
    return 23
@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}


@app.post("/notify", status_code=202)
def send_notification(payload: NotificationRequest):
    """Mock-send a notification (no real sending)."""
    record = {
        "id": len(_notifications) + 1,
        "delivered": True,
        **payload.model_dump(),
    }
    _notifications.append(record)
    return {"message": "Notification queued", "id": record["id"]}


@app.get("/notifications")
def list_notifications():
    return _notifications
