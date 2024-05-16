from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.events.models import event, event_reg

error = {
    "status": "error",
    "data": None,
    "details": None
}

error404u = {
    "status": "error",
    "data": "User not found",
    "details": None
}

error404e = {
    "status": "error",
    "data": "Event not found",
    "details": None
}

error404c = {
    "status": "error",
    "data": "Club not found",
    "details": None
}

error404uc = {
    "status": "error",
    "data": "This user not in this club",
    "details": None
}

error403 = {
    "status": "error",
    "data": "Forbidden",
    "details": None
}

error404eu = {
    "status": "error",
    "data": "User has not registration in this event",
    "details": None
}

# внутреняя функция принимает для соблюдения преемственности с club
async def get_event_by_id(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event).where(event.c.id == event_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if not data:
            data = "Event not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_all_event_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event).where(event.c.club_id == club_id)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            data = "Event not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_rec_event(
        user_id: int,
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event_reg).where(
            (event_reg.c.user_id == user_id) &
            (event_reg.c.id == event_id))
        result = await session.execute(query)
        data = result.mappings().first()

        if data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_club_id_by_event_id(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event).where(event.c.id == event_id)
        result = await session.execute(query)
        data = result.mappings().first()

        return data['club_id']
    except Exception:
        raise HTTPException(status_code=500, detail=error)