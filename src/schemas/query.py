from pydantic import BaseModel, ConfigDict


class QueryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_by": "department",
                "filter_query": {"location": "London"},
            }
        }
    )

    group_by: str
    filter_query: dict[str, str] | None = None


class QueryResult(BaseModel):
    groups: dict[str, int | str]
    suppression_triggered: bool
