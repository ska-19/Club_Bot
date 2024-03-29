from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.mentorship.models import mentorship
from src.mentorship.schemas import NewMentorship
from src.mentorship.inner_func import get_mentorship_by_id, check_leg_mentorship, error, error404


router = APIRouter(
    prefix="/mentorship",
    tags=["mentorship"]
)


@router.post("/add_mentorship")
async def add_mentorship(
        new_mentorship: NewMentorship,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        mentorship_dict = new_mentorship.dict()
        query = insert(mentorship).values(
            mentor_id=mentorship_dict['mentor_id'],
            mentee_id=mentorship_dict['mentee_id'],
            club_id=mentorship_dict['club_id']
        )

        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": mentorship_dict,
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_mentor")
async def get_mentor(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(mentorship.mentor_id).where(
            mentorship.c.mentee_id == user_id,
            mentorship.c.club_id == club_id
        )
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Mentor not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_mentees")
async def get_mentees(
        mentor_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(mentorship.mentee_id).where(
            mentorship.c.mentor_id == mentor_id,
            mentorship.c.club_id == club_id
        )
        result = await session.execute(query)
        data = result.mappings()

        if not data:
            data = "Mentees not found"

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.post("/update_mentorship")
async def update_mentorship(
        mentorship_id: int,
        update_data: NewMentorship,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        data = await get_mentorship_by_id(mentorship_id, session)
        if data == "Mentorship not found":
            raise ValueError('404m')

        if not check_leg_mentorship(update_data.mentor_id, update_data.mentee_id, update_data.club_id, session):
            raise ValueError('404d')

        query = update(mentorship).where(mentorship.c.mentorship_id == mentorship_id).values(
            mentor_id=update_data.mentor_id,
            mentee_id=update_data.mentee_id,
            club_id=update_data.club_id
        )

        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404m':
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "Mentorship not found",
                "details": None
            })
        elif str(e) == '404d':
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "Mentorship with such data already exists",
                "details": None
            })
        else:
            raise HTTPException(status_code=404, detail=error404)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()

