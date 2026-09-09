import pytest
from fastapi.testclient import TestClient

from main import app
from services.expenseServices import expenses
from services.tripServices import trips


@pytest.fixture(autouse=True)
def clean_database():
    trips.delete_many({})
    expenses.delete_many({})
    yield
    trips.delete_many({})
    expenses.delete_many({})


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def trip_payload():
    return {
        "trip_id": 101,
        "name": "Weekend trip",
        "start_date": "2026-09-01T10:00:00",
        "end_date": "2026-09-05T10:00:00",
        "destination": "Paris",
        "List_of_friends": ["Alex", "Sam"],
    }


def expense_payload():
    return {
        "trip_id": 101,
        "title": "Dinner",
        "amount": 42.50,
        "paid_by": "Alex",
        "shared_with": ["Alex", "Sam"],
        "timestamp": "2026-09-02T19:00:00",
        "note": "Shared dinner",
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Application Working Successfully"}


def test_trip_crud(client):
    created = client.post("/trips/", json=trip_payload())
    assert created.status_code == 201
    assert created.json()["trip_id"] == 101
    assert created.json()["id"]

    retrieved = client.get("/trips/101")
    assert retrieved.status_code == 200
    assert retrieved.json()["name"] == "Weekend trip"

    updated = client.put("/trips/101", json={"name": "Long weekend"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Long weekend"

    deleted = client.delete("/trips/101")
    assert deleted.status_code == 200
    assert deleted.json() == {"message": "Trip details deleted"}
    assert client.get("/trips/101").status_code == 404


def test_expense_crud_and_trip_filter(client):
    created = client.post("/expenses/", json=expense_payload())
    assert created.status_code == 201
    expense_id = created.json()["id"]

    filtered = client.get("/expenses/trip/101")
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
    assert filtered.json()[0]["id"] == expense_id

    retrieved = client.get(f"/expenses/{expense_id}")
    assert retrieved.status_code == 200
    assert retrieved.json()["title"] == "Dinner"

    updated = client.put(f"/expenses/{expense_id}", json={"amount": 50})
    assert updated.status_code == 200
    assert updated.json()["amount"] == 50

    deleted = client.delete(f"/expenses/{expense_id}")
    assert deleted.status_code == 200
    assert deleted.json()["message"]
    assert client.get(f"/expenses/{expense_id}").status_code == 404


@pytest.mark.parametrize(
    "path, method, payload",
    [
        ("/trips/999", "get", None),
        ("/expenses/not-an-object-id", "get", None),
        ("/expenses/", "post", {"trip_id": 0}),
    ],
)
def test_invalid_requests_return_client_errors(client, path, method, payload):
    response = getattr(client, method)(path, json=payload) if payload else getattr(client, method)(path)

    assert 400 <= response.status_code < 500