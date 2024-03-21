from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.questionnaire.models import questionnaire
from src.questionnaire.schemas import AddQuestionnaire, UpdateQuestionnaire

router = APIRouter(
    prefix="/questionnaire",
    tags=["questionnaire"]
)


@router.post("/add_questionnaire")
async def add_questionnaire(
        new_data: AddQuestionnaire,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_questionnaire")
async def get_questionnaire(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/update_questionnaire")
async def update_questionnaire(
        user_id: int,
        update_data: UpdateQuestionnaire,
        session: AsyncSession = Depends(get_async_session)
):
    pass
