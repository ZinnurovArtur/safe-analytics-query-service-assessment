from fastapi import APIRouter
from .query.router import router as query_router

main_router = APIRouter()
main_router.include_router(query_router)
