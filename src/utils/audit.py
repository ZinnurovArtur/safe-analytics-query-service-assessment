import logging
from pathlib import Path

from schemas.audit import AuditEntry

logger = logging.getLogger(__name__)


def write_audit(path: Path, entry: AuditEntry) -> None:
    """
    Write an audit entry and save to the JSON format as the log file.

    Args:
        path: The path to the audit log file.
        entry: The audit entry to write.

    Returns:
        None
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

    except Exception:
        logger.exception("Failed to write audit log")
