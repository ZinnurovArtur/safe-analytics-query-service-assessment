from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_by": "department",
                "filter": {"location": "London"},
            }
        }
    )
    group_by: str
    filter_query: dict[str, str] | None = Field(default=None, alias="filter")


class QueryResult(BaseModel):
    groups: dict[str, int | str]
    suppression_triggered: bool
