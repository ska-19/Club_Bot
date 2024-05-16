import math
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.database import get_async_session
from src.user_profile.router import update_profile
from src.user_profile.inner_func import get_user_by_id
from src.user_profile.router import get_user
from src.user_profile.schemas import UserUpdate
from src.user_club.router import get_clubs_by_user, get_balance, get_users_in_club
from src.user_club.inner_func import get_role
from src.events.router import get_event_club
from src.achievement.router import get_achievement_by_user

router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="src/templates")


# Функции для взаимодействия со страницами профиля
@router.get("/profile_base")
def get_profile_base(request: Request):
    return templates.TemplateResponse("profile_base.html", {"request": request})


@router.get("/profile_user/{user_id}")
async def get_profile_user(
        request: Request,
        user_info=Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_data = dict(user_info['data'])
    achievements = await get_achievement_by_user(user_data['id'], session)
    calc_exp = lambda x: (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10), math.floor(
        10 * (x - 5 * (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) * ((math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) + 1)) / (
                    (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) + 1)))
    user_data['full_xp'] = calc_exp(user_data['xp'])[0]
    user_data['xp_percent'] = calc_exp(user_data['xp'])[1]
    user_data['achievement'] = achievements['data']
    return templates.TemplateResponse("profile_user.html", {"request": request, "user_info": user_data})


@router.post("/profile_user/{user_id}")
async def update_profile_user(
        user_id: int,
        request: Request,
        user_update: UserUpdate,
        user_info=Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    await update_profile(user_id, user_update, session)
    return RedirectResponse(url=f"/pages/profile_user/{user_id}")


# Функции для взаимодействия со страницами "Главное"
@router.get("/main_base")
def get_main_base(request: Request):
    return templates.TemplateResponse("main_base.html", {"request": request})


@router.get("/main_user/{user_id}")
async def get_main_user(
        request: Request,
        user_info=Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_data = dict(user_info['data'])
    user_clubs = await get_clubs_by_user(user_data['id'], session)
    club_info = dict(user_clubs['data'][0])
    user_x_club_info_role = await get_role(user_data['id'], club_info['id'], session)
    user_x_club_info_balance = await get_balance(user_data['id'], club_info['id'], session)
    event_data = await get_event_club(club_info['id'], session)
    event_info = event_data['data']
    events = [dict(event) for event in event_info]
    club_info['xp'] = 0
    user_x_club_info = {
        'role': user_x_club_info_role,
        'balance': user_x_club_info_balance['data']
    }
    return templates.TemplateResponse("main_user.html", {
        "request": request,
        "user_info": user_data,
        "club_info": club_info,
        "user_x_club_info": user_x_club_info,
        "events": events
    })


# Функции для взаимодействия со страницами "О клубе"
@router.get("/club_base")
def get_club_base(request: Request):
    return templates.TemplateResponse("club_base.html", {"request": request})


@router.get("/club_user/{user_id}")
async def get_club_user(
        request: Request,
        user_info=Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_data = dict(user_info['data'])
    user_clubs = await get_clubs_by_user(user_data['id'], session)
    club_info = dict(user_clubs['data'][0])
    users_in_club = await get_users_in_club(club_info['id'], session)
    users = users_in_club['data']
    club_info['xp'] = 0
    return templates.TemplateResponse("club_user.html", {
        "request": request,
        "user_info": user_data,
        "club_info": club_info,
        "users": users
    })