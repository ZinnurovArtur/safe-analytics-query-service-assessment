from pydantic import BaseModel


class QueryRequest(BaseModel):
    group_by: str
    filter: dict[str, str] | None = None


class QueryResult(BaseModel):
    groups: dict[str, int | str]
    suppression_triggered: bool
