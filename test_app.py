import os
os.environ["DEMO_MODE"] = "true"
os.environ.pop("GEMINI_API_KEY", None)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_generate_demo_plan():
    response = client.post(
        "/generate-workout",
        data={
            "username": "Test User",
            "user_id": "TEST001",
            "age": "25",
            "weight": "60",
            "goal": "General wellness",
            "intensity": "Low",
        },
    )
    assert response.status_code == 200
    assert "7-Day Wellness Plan" in response.text or "Updated Workout Plan" in response.text
