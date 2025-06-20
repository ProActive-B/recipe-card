from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app
from app.api import get_session
from app import models

from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(engine)


def override_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_session
client = TestClient(app)


def test_create_job(monkeypatch):
    def fake_delay(job_id: str):
        return None

    monkeypatch.setattr("app.tasks.process_video.delay", fake_delay)
    response = client.post("/api/job", params={"url": "https://youtu.be/123", "target_lang": "en"})
    assert response.status_code == 200
    assert "job_id" in response.json()
