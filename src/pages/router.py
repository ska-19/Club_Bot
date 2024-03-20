from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.user_profile.router import get_user_by_id
from src.club.router import get_club_by_id

router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/profile_base")
def get_profile_base(request: Request):
    return templates.TemplateResponse("profile_base.html", {"request": request})


@router.get("/profile_user/{user_id}")
def get_profile_user(request: Request, user_info=Depends(get_user_by_id)):
    return templates.TemplateResponse("profile_user.html", {"request": request, "user_info": user_info})


@router.get("/main_base")
def get_profile_base(request: Request):
    return templates.TemplateResponse("profile_base.html", {"request": request})


@router.get("/main_user/{id}") # тут id из club_user
def get_profile_user(request: Request, user_info=Depends()):  # а тут что в депендс?
    return templates.TemplateResponse("profile_user.html", {"request": request})


@router.get("/main_base")
def get_profile_base(request: Request):
    return templates.TemplateResponse("profile_base.html", {"request": request})


@router.get("/main_user/{club_id}")
def get_profile_user(request: Request, user_info=Depends(get_club_by_id)):  # а тут что в депендс?
    return templates.TemplateResponse("profile_user.html", {"request": request})
