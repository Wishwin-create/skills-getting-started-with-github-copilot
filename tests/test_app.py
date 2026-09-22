from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Soccer Team"
    email = "student@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert delete_response.status_code == 200
    payload = delete_response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_unknown_email_returns_error():
    activity_name = "Soccer Team"
    email = "missing@example.com"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
