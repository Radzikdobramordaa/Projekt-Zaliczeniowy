from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Currency Rates API is running"
    }

def test_get_currencies():

    response = client.get("/currencies")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_get_years():

    response = client.get("/currencies/years")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_get_by_date():

    response = client.get(
        "/currencies/date/2026-06-09"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )