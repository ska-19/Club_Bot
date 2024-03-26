from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.achievement.models import achievement, user_x_achievement
from src.database import get_async_session
from src.events.models import event
from src.events.inner_func import error, error404u, error404c, error404uc, error404p

error404a = {
    "status": "error",
    "data": "Achievement not found",
    "details": None
}

error404ad = {
    "status": "error",
    "data": "Admin not found",
    "details": None
}

error404ac = {
    "status": "error",
    "data": "Achievement not found in club",
    "details": None
}


async def get_achievement_by_id(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(achievement).where(achievement.c.id == achievement_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "Achievement not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_all_user_by_achievement_id(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_achievement).where(user_x_achievement.c.achievement_id == achievement_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            return "Users not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_all_achievement_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_achievement).where(user_x_achievement.c.user_id == user_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            return "Achievements not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)
