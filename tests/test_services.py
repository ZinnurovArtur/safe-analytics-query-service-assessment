"""Tests for suppression and filtering logic."""

from schemas.dataset import Dataset
from schemas.query import QueryRequest
from api.query.services import run_query


SAMPLE = Dataset(
    columns=["department", "location"],
    rows=[
        {"department": "Engineering", "location": "London"},
        {"department": "Engineering", "location": "London"},
        {"department": "Engineering", "location": "London"},
        {"department": "HR",          "location": "London"},
        {"department": "HR",          "location": "London"},
        {"department": "HR",          "location": "London"},
        {"department": "Executive",   "location": "London"},   # count=1, below threshold
        {"department": "Engineering", "location": "Manchester"},
    ],
)


def test_suppression_applied_below_threshold():
    """Groups below the threshold are replaced with 'suppressed'."""
    result = run_query(SAMPLE, QueryRequest(group_by="department"), threshold=3)

    assert result.groups["Engineering"] == 4
    assert result.groups["HR"] == 3
    assert result.groups["Executive"] == "suppressed"
    assert result.suppression_triggered is True


def test_no_suppression_when_threshold_is_one():
    """With threshold=1 every group has at least 1 row so nothing is hidden."""
    result = run_query(SAMPLE, QueryRequest(group_by="department"), threshold=1)

    assert all(isinstance(v, int) for v in result.groups.values())
    assert result.suppression_triggered is False


def test_filter_reduces_results():
    """Only Manchester rows are kept; Engineering's single row is suppressed."""
    result = run_query(
        SAMPLE,
        QueryRequest(group_by="department", filter={"location": "Manchester"}),
        threshold=3,
    )

    assert result.groups == {"Engineering": "suppressed"}


def test_filter_no_match_returns_empty():
    """A filter value that matches nothing returns an empty dict."""
    result = run_query(
        SAMPLE,
        QueryRequest(group_by="department", filter={"location": "Atlantis"}),
        threshold=3,
    )

    assert result.groups == {}
