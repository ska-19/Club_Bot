from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club
from src.user_club.schemas import UserJoin


router = APIRouter(
    prefix="/join",
    tags=["join"]
)


@router.post("/join_club")
async def join_to_the_club(
        join_data: UserJoin,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/disjoin_club")
async def disjoin_club(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/role_upgrade")
async def role_update(
        user_id: int,
        club_id: int,
        update_role: str,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_users_in_club")
async def get_users_in_club(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_users_with_role")
async def get_users_with_role(
        user_id: int,
        club_id: int,
        role: str,
        session: AsyncSession = Depends(get_async_session)
):
    pass


