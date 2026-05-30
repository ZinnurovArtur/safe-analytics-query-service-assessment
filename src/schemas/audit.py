from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AuditEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    group_by: str
    filter_query: dict[str, str] = Field(default_factory=dict)
    suppression_triggered: bool
