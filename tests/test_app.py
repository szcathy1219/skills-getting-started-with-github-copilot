import os
import sys

# make sure the src/ folder is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_activities_returns_all():
    # Arrange
    # (reset is handled by autouse fixture)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # check for a couple of known activities
    assert "Chess Club" in response.json()
    assert "Gym Class" in response.json()


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in app.activities[activity]["participants"]
    assert "Signed up" in response.json().get("message", "")


def test_signup_nonexistent_activity():
    # Arrange
    email = "foo@bar.com"
    activity = "Nonexistent"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_signed():
    # Arrange
    activity = "Chess Club"
    existing = app.activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    participant = app.activities[activity]["participants"][0]
    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": participant}
    )
    # Assert
    assert response.status_code == 200
    assert participant not in app.activities[activity]["participants"]
    assert "Removed" in response.json().get("message", "")


def test_remove_nonexistent_activity():
    # Arrange
    activity = "NoActivity"
    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": "someone@x.com"}
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "ghost@mergington.edu"
    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
