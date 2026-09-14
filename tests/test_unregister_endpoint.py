from fastapi.testclient import TestClient

from src.app import app, activities


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"
    activity = activities[activity_name]

    if email not in activity["participants"]:
        activity["participants"].append(email)

    try:
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email},
        )

        assert response.status_code == 200
        body = response.json()
        assert "Removed" in body["message"]
        assert email not in activity["participants"]
    finally:
        if email in activity["participants"]:
            activity["participants"].remove(email)
