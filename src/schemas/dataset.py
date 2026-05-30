from pydantic import BaseModel


class Dataset(BaseModel):
    rows: list[dict[str, str]]
    columns: set[str]

