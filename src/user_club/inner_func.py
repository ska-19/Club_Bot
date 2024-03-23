from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club_x_user


error = {
    "status": "error",
    "data": None,
    "details": None
}


async def get_rec_id(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    """ Возвращает id записи в таблице club_x_user, внутренняя функция

        Note: перед вызовом обязательно проверить существоание записи (check_rec)

        :param user_id:
        :param club_id:
        :return: rec_id (int)

    """
    try:
        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()

        return data['id']
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_rec(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Проверяет существование записи в таблице club_x_user, внутренняя функция

        :param user_id:
        :param club_id:
        :return:
            True если записи нет.
            False если запись есть.

    """
    try:
        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)