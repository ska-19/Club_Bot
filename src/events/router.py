from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.events.models import club
from src.events.schemas import EventCreate, EventUpdate, EventReg

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post("/create_event")
async def create_event(
        new_event: EventCreate,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_event")
async def get_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/update_event")
async def update_event(
        event_is: int,
        update_data: EventUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/event_reg")
async def event_reg(
        data: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    pass
