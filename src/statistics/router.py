import os
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import tempfile

from src.database import get_async_session
from src.user_club.models import club_x_user
from src.user_profile.models import user
from src.events.models import event_reg, event
from src.events.inner_func import get_event_by_id
from src.club.inner_func import get_club_by_id
from src.statistics.inner_func import error, error404uc, error404u, validation, check_event_valid


router = APIRouter(
    prefix="/statitics",
    tags=["statistics"]
)

error403 = {
    "status": "error",
    "data": "Forbidden",
    "details": None
}

error404ec = {
    "status": "error",
    "data": "This event not in this club",
    "details": None
}


@router.get("/get_club_statistics")
async def get_users_in_club_xlsx(
        user_id: int,
        club_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)):
    """ Возвращает статистику пользователей клуба в формате xlsx

               :param:
                    user_id: int
                    club_id: int
               :return:
                   200 ссылка на скачивание файла.
                   403 + error403, если нет доступа.
                   404 + error404u, если пользователь не найден.
                   500 если внутрення ошибка сервера.

            """
    try:
        if not await validation(user_id, club_id, session):
            raise HTTPException(status_code=403, detail=error403)

        join = club_x_user.join(user, club_x_user.c.user_id == user.c.id)
        query = select(user.c.username, club_x_user.c.role, club_x_user.c.date_joined).select_from(join).where(
            club_x_user.c.club_id == club_id)

        result = await session.execute(query)
        df = pd.DataFrame(result.mappings().all())

        if not df:
            raise ValueError('404u')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            df.to_excel(tmp.name, index=False)
            tmp_path = tmp.name

        background_tasks.add_task(os.unlink, tmp_path)

        return FileResponse(tmp_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='club_statistics.xlsx')
    except ValueError:
        raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_event_statistics")
async def get_users_in_event_xlsx(
        user_id: int,
        club_id: int,
        event_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)):
    """ Возвращает статистику ивента внутри клуба в формате xlsx

                  :param:
                       user_id: int
                       club_id: int
                       event_id: int
                  :return:
                      200 ссылка на скачивание файла.
                      403 + error403, если нет доступа.
                      404 + error404ec, если в клубе нет такого события.
                      404 + error404u, если пользователь не найден.
                      500 если внутрення ошибка сервера.

               """
    try:
        if not await validation(user_id, club_id, session):
            raise ValueError('403')
        if not await check_event_valid(club_id, event_id, session):
            raise ValueError('404ec')

        join = event_reg.join(user, event_reg.c.user_id == user.c.id)
        query = select(user.c.username, event_reg.c.role, event_reg.c.date_joined).select_from(join).where(
            event_reg.c.event_id == event_id)

        result = await session.execute(query)
        df = pd.DataFrame(result.mappings().all())

        if not df:
            raise ValueError('404u')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            df.to_excel(tmp.name, index=False)
            tmp_path = tmp.name

        background_tasks.add_task(os.unlink, tmp_path)

        data = await get_event_by_id(event_id, session)
        name_event = data['id']
        # поменять в бд, добавить название события
        data = await get_club_by_id(club_id, session)
        name_club = data['name']

        return FileResponse(tmp_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            filename=f'{name_club}_{name_event}.xlsx')
    except ValueError as e:
        if str(e) == '403':
            raise HTTPException(status_code=403, detail=error403)
        elif str(e) == '404ec':
            raise HTTPException(status_code=404, detail=error404ec)
        else:
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_events_statistics")
async def get_users_in_club_events_xlsx(
        user_id: int,
        club_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)):
    """ Возвращает статистику всех ивентов внутри клуба в формате xlsx

                     :param:
                          user_id: int
                          club_id: int
                     :return:
                         200 ссылка на скачивание файла.
                         403 + error403, если нет доступа.
                         404 + error404u, если пользователь не найден.
                         500 если внутрення ошибка сервера.

                  """
    try:
        if not await validation(user_id, club_id, session):
            raise ValueError('403')

        join = (event
                .join(event_reg, event.c.id == event_reg.c.event_id)
                .join(user, event_reg.c.user_id == user.c.id))

        query = (select(event.c.id, event.c.date, event_reg.c.user_id, event_reg.c.confirm, event_reg.c.reg_date, user)
                 .select_from(join)
                 .where(event.c.club_id == club_id))

        result = await session.execute(query)
        df = pd.DataFrame(result.mappings().all())

        if not df:
            raise ValueError('404u')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            df.to_excel(tmp.name, index=False)
            tmp_path = tmp.name

        background_tasks.add_task(os.unlink, tmp_path)

        data = await get_club_by_id(club_id, session)
        name_club = data['name']

        return FileResponse(tmp_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            filename=f'{name_club}_events.xlsx')
    except ValueError as e:
        if str(e) == '403':
            raise HTTPException(status_code=403, detail=error403)
        else:
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
