from fastapi import APIRouter, Depends, Request, HTTPException
from api.query.services import run_query
from schemas.audit import AuditEntry
from schemas.query import QueryRequest
from config import Settings, get_settings
from utils.audit import write_audit

router = APIRouter(tags=["Query"])


@router.post("/query")
async def query(
    request: Request, body: QueryRequest, settings: Settings = Depends(get_settings)
) -> dict[str, int | str]:
    """
    Run an aggregation query against the loaded dataset.

    Validates the request fields against known dataset columns before delegating
    to the service layer. Suppression is applied by the service based on the
    configured threshold. Every request - including those that trigger suppression
    - is recorded in the audit log.
    """
    dataset = request.app.state.dataset

    # Reject unknown group_by columns before doing any work.
    if body.group_by not in dataset.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid group_by field: {body.group_by}",
        )

    # Reject filter keys that don't correspond to a real column.
    if body.filter_query:
        invalid_keys = [k for k in body.filter_query if k not in dataset.columns]
        if invalid_keys:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid filter field(s): {', '.join(invalid_keys)}",
            )

    query_result = run_query(dataset, body, settings.SUPPRESSION_THRESHOLD)

    # Write the audit entry regardless of whether suppression was triggered.
    write_audit(
        settings.AUDIT_LOG_PATH,
        AuditEntry(
            group_by=body.group_by,
            filter_query=body.filter_query or {},
            suppression_triggered=query_result.suppression_triggered,
        ),
    )

    return query_result.groups
