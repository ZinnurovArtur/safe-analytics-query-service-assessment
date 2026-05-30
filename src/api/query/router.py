from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.query.services import run_query
from config import Settings
from schemas.audit import AuditEntry
from schemas.query import QueryRequest
from utils.audit import write_audit

router = APIRouter(tags=["Query"])

config = Settings()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/query")
async def query(request: Request, body: QueryRequest):
    dataset = request.app.state.dataset

    if body.group_by not in dataset.columns:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid group_by field: {body.group_by}"},
        )

    if body.filter:
        invalid_keys = [k for k in body.filter if k not in dataset.columns]
        if invalid_keys:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid filter field(s): {', '.join(invalid_keys)}"},
            )

    result = run_query(dataset, body, config.SUPPRESSION_THRESHOLD)

    write_audit(
        config.AUDIT_LOG_PATH,
        AuditEntry(
            group_by=body.group_by,
            filters=body.filter or {},
            suppression_triggered=result.suppression_triggered,
        ),
    )

    return result.groups
