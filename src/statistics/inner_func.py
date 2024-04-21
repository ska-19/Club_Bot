from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from src.database import get_async_session
from src.user_club.inner_func import get_role
from src.events.models import event_reg, event


error = {
    "status": "error",
    "data": None,
    "details": None
}

error404uc = {
    "status": "error",
    "data": "This user not in this club",
    "details": None
}

error404u = {
    "status": "error",
    "data": "User not found",
    "details": None
}


async def validation(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    """ Проверяет пользователя на то, является ли он владельцем клуба

           :return:
               true, если является.
               false, если не является.
               404 + error404uc, если пользователь не состоит в клубе.
               404 + error404u, если пользователь не найден.
               500 если внутрення ошибка сервера.

           Note: error404u и error404c имена переменных с джейсонами-ошибками.

        """
    try:
        role = await get_role(user_id, club_id, session)
        if role == 'User not in the club':
            raise ValueError('404uc')
        elif role == 'User not found':
            raise ValueError('404u')
        if role == 'owner':
            return True
        return False
    except ValueError as e:
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        else:
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_event_valid(
        club_id: int,
        event_id: int,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    """ Проверяет есть ли такое событие

              :param:
                    user_id: int
                    club_id: int
              :return:
                  true, если есть.
                  false, если нет.
                  500 если внутрення ошибка сервера.

              Note: error404u и error404c имена переменных с джейсонами-ошибками.

           """
    try:
        join = event_reg.join(event, event_reg.c.event_id == event.c.id)
        query = (select(event_reg.c.event_id, event.c.club)
                 .select_from(join)
                 .where((event_reg.c.event_id == event_id) &
                        (event.c.club == club_id)))

        result = await session.execute(query)
        data = result.mappings().first()

        if data:
            return True
        return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)