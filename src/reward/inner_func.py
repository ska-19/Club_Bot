from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.reward.models import reward, user_x_reward
from src.database import get_async_session
from src.events.models import event
from src.events.inner_func import error, error404u, error404c, error404uc

error404ad = {
    "status": "error",
    "data": "Admin not found",
    "details": None
}

error404ac = {
    "status": "error",
    "data": "Reward not found in club",
    "details": None
}

error404p = {
    "status": "error",
    "data": "User has no permission to create/update reward",
    "details": None
}

error404r = {
    "status": "error",
    "data": "Reward not found",
    "details": None

}

error404re = {
    "status": "error",
    "data": "User already has this reward",
    "details": None
}


async def get_reward_by_id(
        reward_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(reward).where(reward.c.id == reward_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "Reward not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_all_user_by_reward_id(
        reward_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_reward).where(user_x_reward.c.reward_id == reward_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            return "Users not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_all_reward_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_reward).where(user_x_reward.c.user_id == user_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            return "Rewards not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_reward_user(
        reward_id: int,
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_reward).where(user_x_reward.c.reward_id == reward_id).where(user_x_reward.c.user_id == user_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if data:
            return "User already has this reward"
        else:
            return "Good"
    except Exception:
        raise HTTPException(status_code=500, detail=error)
