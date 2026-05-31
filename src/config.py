from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CSV_PATH: Path = Path("data/employees.csv")
    SUPPRESSION_THRESHOLD: int = 3
    RESTRICTED_FIELDS: list[str] = ["name", "employee_id"]
    AUDIT_LOG_PATH: Path = Path("logs/audit.log")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
