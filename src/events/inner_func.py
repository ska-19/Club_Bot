from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.events.models import event, event_reg
from src.user_club.router import update_balance, get_users_with_role
from src.user_club.schemas import UpdateBalance
from src.user_profile.router import update_xp

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

error409 = {
    "status": "error",
    "data": "User already registr in this event",
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
        query = select(event).where(event.c.club_id == club_id).order_by(event.c.date)
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
            (event_reg.c.event_id == event_id))
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


async def clean(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(event_reg).where(event_reg.c.event_id == event_id)
        await session.execute(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


async def adm_boost(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        event = await get_event_by_id(event_id, session)
        reward = event['reward']
        club_id = await get_club_id_by_event_id(event_id, session)
        admin = await get_users_with_role(club_id, 'admin', session)
        owner = await get_users_with_role(club_id, 'owner', session)
        admins = [admin['data'],
                  owner['data']]
        for admin in admins:
            updatebalance = UpdateBalance(club_id=club_id, user_id=admin[0]['id'], plus_balance=reward)
            await update_balance(updatebalance, session)
            await update_xp(admin[0]['id'], 50, session)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
