from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.club.models import club


error = {
    "status": "error",
    "data": None,
    "details": None
}


async def get_club_by_id(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(club).where(club.c.id == club_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Club not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_club_by_uid(
        club_uid: str,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(club).where(club.c.uid == club_uid)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Club not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_leg_name(
        club_name: str,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    """ Проверяет существует ли клуб с таким именем, внутренняя функция

       :param club_name:
       :return:
           True - если клуба с таким именем нет.
           False - если клуб с таким именем существует.

    """
    try:
        query = select(club).where(club.c.name == club_name)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)
