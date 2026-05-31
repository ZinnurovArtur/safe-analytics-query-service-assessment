"""Tests for audit entry structure."""

import json

from schemas.audit import AuditEntry


def test_audit_entry_has_expected_fields():
    """All required fields are present and hold the correct values."""
    entry = AuditEntry(
        group_by="department",
        filter_query={"location": "London"},
        suppression_triggered=True,
    )

    data = entry.model_dump()

    assert data["group_by"] == "department"
    assert data["filter_query"] == {"location": "London"}
    assert data["suppression_triggered"] is True
    assert "timestamp" in data


def test_audit_entry_serialises_to_valid_json():
    """Entry can be dumped to JSON and parsed back without losing data."""
    entry = AuditEntry(group_by="location", filter_query={}, suppression_triggered=False)

    parsed = json.loads(entry.model_dump_json())

    assert parsed["group_by"] == "location"
    assert parsed["suppression_triggered"] is False
