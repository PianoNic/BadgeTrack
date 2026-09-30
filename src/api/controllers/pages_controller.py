from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(include_in_schema=False)

_TEMPLATES = Path(__file__).resolve().parents[3] / "templates"


@router.get("/")
async def index() -> FileResponse:
    return FileResponse(_TEMPLATES / "index.html")


@router.get("/about")
async def about() -> FileResponse:
    return FileResponse(_TEMPLATES / "about.html")
