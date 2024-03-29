from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.database import get_async_session
from src.user_profile.router import get_user_by_id, update_profile
from src.user_profile.schemas import UserUpdate
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


@router.put("/profile_user/{user_id}")
async def update_profile_user(
        user_id: int,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        await update_profile(user_id, update_data, session)
        return RedirectResponse(url=f"/pages/profile_user/{user_id}")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/main_base")
def get_main_base(request: Request):
    return templates.TemplateResponse("main_base.html", {"request": request})


@router.get("/main_user/{id}")
def get_main_user(request: Request):
    pass


@router.get("/club_base")
def get_club_base(request: Request):
    return templates.TemplateResponse("club_base.html", {"request": request})


@router.get("/club_user/{user_id}")
def get_club_user(request: Request):
    pass