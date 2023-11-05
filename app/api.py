from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates

from app.db import init
from app.models.responses import BadRequest, BadRequestResponseModel
from app.routers import boardings, decklists


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init()
    yield


api = FastAPI(
    title="Decklists and Boardings API",
    description="This is a tool to generate decklists and boarding guides for Magic: The Gathering. It is currently in development.",
    version="alpha",
    lifespan=lifespan,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestResponseModel},
    },
)
templates = Jinja2Templates(directory="app/templates")


# exception handler for pydantic value errors
@api.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return BadRequest(str(exc))


api.include_router(boardings.router)
api.include_router(decklists.router)


# Serve a static HTML Frontend
@api.get("/", include_in_schema=False)
async def root(request: Request):
    content = {
        "request": request,
        "title": "Boarding Guide Generator",
        "heading": "Decklist and Boarding Guide Generator",
        "paragraph": "This is a tool to generate decklists and boarding guides for Magic: The Gathering. It is currently in development.",
        "swagger_url": "/docs",
    }
    return templates.TemplateResponse("index.html", content)
