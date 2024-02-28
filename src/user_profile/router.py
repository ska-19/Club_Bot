from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import user, User
from src.auth.schemas import UserUpdate

router = APIRouter(
    prefix="/user_profile",
    tags=["user_profile"]
)

error_get = {
    "status": "error",
    "data": None,
    "details": None
}

error_post = {
    "status": "error"
}


@router.get("/get_user")
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        resp = result.mappings().first()
        if resp:
            return {
                "status": "success",
                "data": resp,
                "details": None
            }
        else:
            raise HTTPException(status_code=500, detail=error_get)
    except Exception:
        raise HTTPException(status_code=500, detail=error_get)


@router.get("/get_column")
async def get_user_column(
        user_id: int,
        col: str,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        resp = result.mappings().first()
        if resp:
            return {
                "status": "success",
                "data": resp[col],
                "details": None
            }
        else:
            raise HTTPException(status_code=500, detail=error_get)
    except Exception:
        raise HTTPException(status_code=500, detail=error_get)


@router.post("/update")
async def update_profile(
        user_id: int,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        resp = result.scalars().first()

        if not resp:
            raise HTTPException(status_code=404, detail="User not found")

        update_data_dict = update_data.dict(exclude_unset=True)
        not_changed = ['email', 'password', 'is_active', 'is_superuser', 'is_verified']
        for key, value in update_data_dict.items():
            if key not in not_changed and value != "string":
                setattr(resp, key, value)

        try:
            session.add(resp)
            await session.commit()
            return {"message": "success"}
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=500, detail=error_post)