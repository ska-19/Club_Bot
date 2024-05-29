from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_profile.models import user


error = {
    "status": "error",
    "data": None,
    "details": None
}


async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if not data:
            return "User not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)