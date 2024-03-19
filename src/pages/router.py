from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/profile_base")
def get_profile_base(request: Request):
    return templates.TemplateResponse("profile_base.html", {"request": request})


@router.get("/profile_user")
def get_profile_user(request: Request):
    return templates.TemplateResponse("profile_user.html", {"request": request})
