from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CSV_PATH: Path = Path("/Users/arturzinnurov/Documents/safe-analytics-query-service-assessment/data/employees.csv")
    SUPPRESSION_THRESHOLD: int = 3
    AUDIT_LOG_PATH: Path = Path("logs/audit.log")

    class Config:
        extra = "ignore"
