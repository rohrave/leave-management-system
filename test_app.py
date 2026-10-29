import pytest
import app as app_module


@pytest.fixture
def client():
    app_module.leave_requests.clear()
    app_module.next_id = 1
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Leave Management System" in response.data


def test_apply_leave(client):
    response = client.post(
        "/apply",
        data={"name": "Test Employee", "reason": "Personal work", "days": "2"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test Employee" in response.data
    assert b"Pending" in response.data


def test_approve_leave(client):
    client.post("/apply", data={"name": "A", "reason": "Test", "days": "1"})
    response = client.post("/approve/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Approved" in response.data


def test_reject_leave(client):
    client.post("/apply", data={"name": "B", "reason": "Test", "days": "1"})
    response = client.post("/reject/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Rejected" in response.data


def test_invalid_days(client):
    response = client.post(
        "/apply",
        data={"name": "Test", "reason": "Test", "days": "0"},
    )
    assert response.status_code == 400
