from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.randomcoffee.models import randomcoffee
from src.randomcoffee.schemas import NewCoffee


router = APIRouter(
    prefix="/club",
    tags=["club"]
)


@router.post("/add_coffee")
async def add_coffee(
        new_coffee: NewCoffee,
        session: AsyncSession = Depends(get_async_session)
):
    pass
