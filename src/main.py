from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import main_router
from config import settings
from utils.dataset import load_dataset


"""
The lifespan context manager is used to load the dataset and the config.

Args:
    app: The FastAPI app.

Returns:
    A lifespan context manager.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.dataset = load_dataset(settings.CSV_PATH)
    yield


app = FastAPI(title="Safe Analytics Query Service", lifespan=lifespan)

app.include_router(main_router)
