from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.achievement.models import achievement, user_x_achievement


error = {
    "status": "error",
    "data": None,
    "details": None
}


async def get_achievement_by_id(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(achievement).where(achievement.c.id == achievement_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Achievement not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_rec_id(
        user_id: int,
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)) -> int:
    """ Возвращает id записи в таблице user_x_achievementv, внутренняя функция

        Note: перед вызовом обязательно проверить существоание записи (check_rec)

        :param
            user_id:
            achievement_id:
        :return:
            rec_id (int)
            500 + error если внутренняя ошибка сервера
    """
    try:
        query = select(user_x_achievement).where(
            (user_x_achievement.c.user_id == user_id) &
            (user_x_achievement.c.achievement_id == achievement_id))
        result = await session.execute(query)
        data = result.mappings().first()

        return data['id']
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_rec(
        user_id: int,
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Проверяет существование записи в таблице club_x_user, внутренняя функция

        :param
            user_id:
            achievement_id:
        :return:
            True если записи нет.
            False если запись есть.
            500 + error если внутренняя ошибка сервера
    """
    try:
        query = select(user_x_achievement).where(
            (user_x_achievement.c.user_id == user_id) &
            (user_x_achievement.c.achievement_id == achievement_id))
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)