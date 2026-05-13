import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Remove if already exists (cleanup)
    client.delete(f"/activities/{activity}/signup?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Remove participant
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Remove again (should fail)
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_nonexistent_activity():
    response = client.delete("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
