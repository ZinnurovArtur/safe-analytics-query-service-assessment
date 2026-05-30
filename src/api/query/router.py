from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from api.query.services import run_query
from schemas.audit import AuditEntry
from schemas.query import QueryRequest
from config import Settings, get_settings
from utils.audit import write_audit

router = APIRouter(tags=["Query"])


@router.post("/query")
async def query(
    request: Request, body: QueryRequest, settings: Settings = Depends(get_settings)
):
    dataset = request.app.state.dataset

    if body.group_by not in dataset.columns:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid group_by field: {body.group_by}"},
        )

    if body.filter_query:
        invalid_keys = [k for k in body.filter_query if k not in dataset.columns]
        if invalid_keys:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"Invalid filter field(s): {', '.join(invalid_keys)}"
                },
            )

    query_result = run_query(dataset, body, settings.SUPPRESSION_THRESHOLD)

    write_audit(
        settings.AUDIT_LOG_PATH,
        AuditEntry(
            group_by=body.group_by,
            filter_query=body.filter_query or {},
            suppression_triggered=query_result.suppression_triggered,
        ),
    )

    return query_result.groups
