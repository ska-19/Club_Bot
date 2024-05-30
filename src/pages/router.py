import math
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.database import get_async_session
from src.user_profile.router import update_profile
from src.user_profile.router import get_user, update_links_profile
from src.user_profile.schemas import UserUpdate
from src.club.schemas import FoundUid
from src.club.router import search, get_club
from src.events.schemas import EventReg, EventUpdate, EventCreate
from src.events.router import get_event_club, get_check_rec, reg_event, event_disreg, get_event, update_event, \
    create_event, get_users_by_event, end_event
from src.user_club.router import get_clubs_by_user, get_balance, get_users_in_club, disjoin_club, role_update, \
    get_main_club, new_main, join_to_the_club
from src.user_club.inner_func import get_role
from src.user_club.schemas import User, UserJoin
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
    print(1)
    user_data['full_xp'] = calc_exp(user_data['xp'])[0]
    user_data['xp_percent'] = calc_exp(user_data['xp'])[1]
    # achievements = await get_achievement_by_user(user_data['id'], session)
    # user_data['achievement'] = achievements['data']
    user_clubs = await get_main_club(user_data['id'], session)
    print(1)
    if user_clubs['status'] == "success":
        user_data['exist_clubs'] = 1
    else:
        user_data['exist_clubs'] = 0
    print(user_data)
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
    blank_link = FoundUid(uid="")
    await update_links_profile(user_info['data']['id'], blank_link, session)
    user_data = dict(user_info['data'])
    club_info_data = await get_main_club(user_data['id'], session)
    club_info = dict(club_info_data['data'])
    user_x_club_info_role = await get_role(user_data['id'], club_info['id'], session)
    user_x_club_info_balance = await get_balance(user_data['id'], club_info['id'], session)
    event_data = await get_event_club(club_info['id'], session)
    if event_data['data'] != "Event not found":
        user_data['exist_events'] = 1
        events = [dict(event) for event in event_data['data']]
        for event in events:
            event_id = event['id']
            event['reg'] = await get_check_rec(event_id, user_data['id'], session)
    else:
        user_data['exist_events'] = 0
        events = []
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


@router.post("/main_user/{user_id}/1")
async def register_event(
        event_reg: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    reg = await reg_event(event_reg, session)
    return {"message": "Event Reg successfully", "reg_event": reg}


@router.post("/main_user/{user_id}/2")
async def create_new_event(
        event_cre: EventCreate,
        session: AsyncSession = Depends(get_async_session)
):
    club = await get_main_club(event_cre.club_id, session)
    event_cre.club_id = club['data']['id']
    create = await create_event(event_cre, session)
    return {"message": "Event Reg successfully", "New event!": create}


@router.put("/main_user/{user_id}")
async def update_main_event(
        user_id: int,
        event_update: EventUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    event_id = event_update.club_id
    main_club_data = await get_main_club(user_id, session)
    main_club = dict(main_club_data['data'])
    event_update.club_id = main_club['id']
    ev = await get_event(event_id, session)
    event_update.host_id = ev['data'].get('host_id')
    event_update.name = ev['data'].get('name')
    event = await update_event(event_id, event_update, session)
    return {"message": "Event updated successfully", "event": event}


@router.delete("/main_user/{user_id}")
async def deregister_event(
        event_reg: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    disreg = await event_disreg(event_reg.user_id, event_reg.event_id, session)
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
    main_club_data = await get_main_club(user_data['id'], session)
    main_club = dict(main_club_data['data'])
    users_in_club = await get_users_in_club(main_club['id'], session)
    users = users_in_club['data']
    user_info_in_club = next((item for item in users if item['username'] == user_data['username']), None)
    user_data['role'] = user_info_in_club['role']
    main_club['xp'] = 0
    return templates.TemplateResponse("club_user.html", {
        "request": request,
        "user_info": user_data,
        "club_info": main_club,
        "users": users
    })


@router.put("/club_user/{user_id}")
async def update_role(
        update_user: User,
        session: AsyncSession = Depends(get_async_session)
):
    main_club_data = await get_main_club(update_user.user_id, session)
    main_club = dict(main_club_data['data'])
    update_user.club_id = main_club['id']
    new_role_user = await role_update(update_user.user_id, update_user.club_id, session)
    return {"message": "Update role user successfully", "update_user": new_role_user}


@router.delete("/club_user/{user_id}")
async def kick_club_user(
        kick_user: User,
        session: AsyncSession = Depends(get_async_session)
):
    main_club_data = await get_main_club(kick_user.user_id, session)
    main_club = dict(main_club_data['data'])

    kick_user.club_id = main_club['id']
    kicked_user = await disjoin_club(kick_user, session)
    return {"message": "Kick user successfully", "kick_user": kicked_user}


# Функции для поиска других клубов
@router.get("/search_base")
def get_search_base(request: Request):
    return templates.TemplateResponse("search_base.html", {"request": request})


@router.get("/search_user/{user_id}")
async def get_search_user(
        request: Request,
        user_id: int,
        user_info=Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_data = dict(user_info['data'])
    main_club = await get_main_club(user_data['id'], session)
    if main_club['status'] == "success":
        user_data['exist_main_club'] = 1
        main_club_data = dict(main_club['data'])
    else:
        user_data['exist_main_club'] = 0
        main_club_data = {}
    user_clubs = await get_clubs_by_user(user_data['id'], session)
    if user_clubs['status'] == 'fail':
        clubs_data = []
        user_data['exist_clubs'] = 0
    else:
        clubs_data_with_main = user_clubs['data']
        user_data['exist_clubs'] = 1
        if user_data['exist_main_club'] == 0:
            clubs_data = [club for club in clubs_data_with_main if club["name"] != main_club_data["name"]]
        else:
            clubs_data = [club for club in clubs_data_with_main]
    # if user_clubs['status'] == 'success' and len(user_clubs['data']) > 1:
    #     clubs_data_with_main = user_clubs['data']
    #     user_data['exist_clubs'] = 1
    #     clubs_data = [club for club in clubs_data_with_main if club["name"] != main_club_data["name"]]
    # else:
    #     clubs_data = []
    #     user_data['exist_clubs'] = 0
    uid_last_search = user_data['links']  # последний поисковой запрос данного юзера, изначально ""
    if uid_last_search == "":
        found_club_data = {"id": 0}
    else:
        search_club = await search(uid_last_search, session)
        found_club_data = search_club['data']
    return templates.TemplateResponse("search_user.html", {
        "request": request,
        "user_info": user_data,
        "found_club": found_club_data,
        "main_club": main_club_data,
        "clubs": clubs_data,
    })


@router.post("/search_user/{user_id}")
async def join_club(
        join_data: UserJoin,
        session: AsyncSession = Depends(get_async_session)
):
    join = await join_to_the_club(join_data, session)
    new_main_club = await new_main(join_data.user_id, join_data.club_id, session)
    return {"message": "Event Reg successfully", "new join club": new_main_club}


@router.put("/search_user/{user_id}/1")
async def found_club(
        user_id: int,
        last_search: FoundUid,
        session: AsyncSession = Depends(get_async_session)
):
    update_last_search = await update_links_profile(user_id, last_search, session)
    return {"message": "Event updated successfully", "new last search": update_last_search}


@router.put("/search_user/{user_id}/2")
async def change_main_club(
        changed_main_club: User,
        session: AsyncSession = Depends(get_async_session)
):
    new_main_club = await new_main(changed_main_club.user_id, changed_main_club.club_id, session)
    return {"message": "Event updated successfully", "new main club": new_main_club}


@router.delete("/search_user/{user_id}")
async def leave_club(
        user_club: User,
        session: AsyncSession = Depends(get_async_session)
):
    disjoin = await disjoin_club(user_club, session)
    return {"message": "Event Disreg successfully", "leave from club": disjoin}

# Функции для завершения событий
@router.get("/endevent_base")
def get_endevent_base(request: Request):
    return templates.TemplateResponse("endevent_base.html", {"request": request})


@router.get("/endevent_user/{user_id}/{event_id}")
async def get_endevent_user(
        request: Request,
        users=Depends(get_users_by_event),
        session: AsyncSession = Depends(get_async_session)
):
    print(users)
    return templates.TemplateResponse("endevent_user.html", {
        "request": request,
        "users": users,
        "user_id": user_id
    })
