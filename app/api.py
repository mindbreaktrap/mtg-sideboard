from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.db import init
from app.models.responses import BadRequest
from app.routers import boardings, decklists


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init()
    yield


api = FastAPI(lifespan=lifespan)


# exception handler for pydantic value errors
@api.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return BadRequest(str(exc))


api.include_router(boardings.router)
api.include_router(decklists.router)
