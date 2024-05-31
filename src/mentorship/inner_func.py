from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.mentorship.models import mentorship


error = {
    "status": "error",
    "data": None,
    "details": None
}

error404 = {
    "status": "error",
    "data": "User not found",
    "details": None
}


async def get_mentorship_by_id(
        mentorship_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(mentorship).where(mentorship.c.mentorship_id == mentorship_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Mentorship not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_leg_mentorship(
        mentor_id: int,
        mentee_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    """ Проверяет существует ли менторство с таким ментором и пользователем, внутренняя функция

           :param mentor_id
           :param mentee_id
           :param club_id
           :return:
               True - если менторства с такими данными нет.
               False - если менторство с такими данными существует.

        """
    try:
        query = select(mentorship).where(
            mentorship.c.mentor_id == mentor_id,
            mentorship.c.mentee_id == mentee_id,
            mentorship.c.club_id == club_id
        )
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)