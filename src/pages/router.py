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
from src.events.schemas import EventReg, EventUpdate
from src.user_club.router import get_clubs_by_user, get_balance, get_users_in_club
from src.user_club.inner_func import get_role
from src.events.router import get_event_club, get_check_rec, reg_event, event_disreg, get_event, update_event
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
    calc_exp = lambda x: (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10), math.floor(
        10 * (x - 5 * (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) * (
                (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) + 1)) / (
                (math.floor((-5 + math.sqrt(25 + 20 * x)) / 10)) + 1)))
    user_data['full_xp'] = calc_exp(user_data['xp'])[0]
    user_data['xp_percent'] = calc_exp(user_data['xp'])[1]
    # achievements = await get_achievement_by_user(user_data['id'], session)
    # user_data['achievement'] = achievements['data']
    return templates.TemplateResponse("profile_user.html", {"request": request, "user_info": user_data})


@router.put("/profile_user/{user_id}")
async def update_profile_user(
        user_id: int,
        user_update: UserUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    user = await update_profile(user_id, user_update, session)
    return {"message": "Profile updated successfully", "user": user}


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
    for event in events:
        event_id = event['id']
        event['reg'] = await get_check_rec(event_id, user_data['id'], session)
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


@router.post("/main_user/{user_id}")
async def register_event(
        event_reg: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    reg = await reg_event(event_reg, session)
    return {"message": "Event Reg successfully", "reg_event": reg}


@router.put("/main_user/{user_id}")
async def update_main_event(
        user_id: int,
        event_update: EventUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    event_id = event_update.club_id
    user_clubs = await get_clubs_by_user(user_id, session)
    club_info = dict(user_clubs['data'][0])
    event_update.club_id = club_info['id']
    ev = await get_event(event_id, session)
    event_update.host_id = ev['data'].get('host_id')
    event = await update_event(event_id, event_update, session)
    return {"message": "Event updated successfully", "event": event}


@router.delete("/main_user/{user_id}")
async def deregister_event(
        EventReg: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    disreg = await event_disreg(EventReg.user_id, EventReg.event_id, session)
    return {"message": "Event Disreg successfully", "disreg_event": disreg}


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
    user_info_in_club = next((item for item in users if item['username'] == user_data['username']), None)
    user_data['role'] = user_info_in_club['role']
    club_info['xp'] = 0
    return templates.TemplateResponse("club_user.html", {
        "request": request,
        "user_info": user_data,
        "club_info": club_info,
        "users": users
    })
