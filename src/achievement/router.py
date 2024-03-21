from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.achievement.models import achievement
from src.achievement.schemas import AddAchievement, UpdateAchievement

router = APIRouter(
    prefix="/achievement",
    tags=["achievement"]
)


@router.post("/add_achievement")
async def add_achievement(
        new_data: AddAchievement,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_achievement")
async def get_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/update_achievement")
async def update_achievement(
        achievement_id: int,
        new_data: UpdateAchievement,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/add_achievement_to_user")
async def add_to_user(
        user_id: int,
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_users_by_achievement")
async def get_by_achievement(
        achievement_id: int,
        ssession: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_achievement_by_user")
async def get_by_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass
