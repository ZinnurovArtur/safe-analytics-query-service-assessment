"""Tests for API behaviour."""

from fastapi.testclient import TestClient
from config import get_settings
from main import app
from utils.dataset import load_dataset

app.state.dataset = load_dataset(get_settings().CSV_PATH)

client = TestClient(app)


def test_query_endpoint_success():
    """Valid group_by returns 200 with a dict of group counts."""
    response = client.post("/query", json={"group_by": "department"})

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_query_endpoint_missing_group_by():
    """Omitting group_by fails schema validation before reaching the handler."""
    response = client.post("/query", json={})

    assert response.status_code == 422


def test_query_endpoint_invalid_group_by():
    """A column that doesn't exist in the dataset returns 400."""
    response = client.post("/query", json={"group_by": "unknown"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid group_by field: unknown"


def test_query_endpoint_invalid_filter():
    """A filter key that doesn't exist in the dataset returns 400."""
    response = client.post(
        "/query",
        json={"group_by": "department", "filter": {"unknown_column": "London"}},
    )

    assert response.status_code == 400
    assert "Invalid filter field" in response.json()["detail"]


def test_query_endpoint_with_filter():
    """Filtering by a valid column returns 200 with a dict."""
    response = client.post(
        "/query",
        json={"group_by": "department", "filter": {"location": "London"}},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_group_by_restricted_column_returns_403():
    """Grouping by an identifying column like 'name' is blocked with 403."""
    response = client.post("/query", json={"group_by": "name"})

    assert response.status_code == 403
    assert "name" in response.json()["detail"]


def test_filter_by_restricted_column_returns_403():
    """Filtering by an identifying column like 'name' is blocked with 403."""
    response = client.post(
        "/query",
        json={
            "group_by": "department",
            "filter": {"name": "Alice", "location": "London"},
        },
    )

    assert response.status_code == 403
    assert "name" in response.json()["detail"]
