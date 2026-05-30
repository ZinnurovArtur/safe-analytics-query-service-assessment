from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CSV_PATH: Path
    SUPPRESSION_THRESHOLD: int = 3
    AUDIT_LOG_PATH: Path

    class Config:
        env_file = "../.env"
        extra = "ignore"
