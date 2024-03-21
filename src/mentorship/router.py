from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.mentorship.models import mentorship
from src.mentorship.schemas import NewMentorship


router = APIRouter(
    prefix="/mentorship",
    tags=["mentorship"]
)


@router.post("/add_mentorship")
async def add_mentorship(
        new_mentorship: NewMentorship,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_mentor")
async def get_mentor(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_mentee")
async def get_mentee(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/update_mentorship")
async def update_mentorship():
    pass
