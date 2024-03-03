from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.club.models import club
from src.club.schemas import ClubUpdate, ClubCreate

router = APIRouter(
    prefix="/club",
    tags=["club"]
)

error = {
    "status": "error",
    "data": None,
    "details": None
}

error404 = {
    "status": "error",
    "data": "Club not found",
    "details": None
}

error409 = {
    "status": "error",
    "data": "Club with the same name already exists",
    "details": None
}


async def get_club_by_id(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(club).where(club.c.id == club_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "Club not found"

        return data
    except Exception:
        return None


# внутренняя функция, принимает имя клуба, возвращает true, если клуба с таким именем нет, false иначе
async def check_leg_name(
        club_name: str,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    try:
        query = select(club).where(club.c.name == club_name)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)


# принимает джейсон вида ClubCreate
# 200 + джейсон со всеми данными, если все хорошо
# 409 если клуб с таким именем уже существует
# 500 если внутрення ошибка сервера
@router.post("/create_club")
async def create_club(
        new_club: ClubCreate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        club_dict = new_club.dict()
        if not await check_leg_name(club_dict['name'], session):
            raise HTTPException(status_code=409, detail=error409)

        stmt = insert(club).values(**club_dict)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": club_dict,  # TODO: how return ClubRead schemas
            "details": None
        }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


# принимает club_id
# 200 + джейсон со всеми данными, если все хорошо
# 404 если такого клуба нет
# 500 если внутрення ошибка сервера
@router.get("/get_club")
async def get_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_club_by_id(club_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "Club not found":
            raise HTTPException(status_code=404, detail=error404)
        return {
            "status": "success",
            "data": data,
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail=error)


# принимает club_id и джейсон вида ClubUpdate
# 200 + джейсон со всеми данными(обновленными), если все хорошо
# 404 если такого клуба нет
# 409 если клуб с таким именем уже существует
# 500 если внутрення ошибка сервера
@router.post("/update_club")
async def update_club(
        club_id: int,
        update_data: ClubUpdate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_club_by_id(club_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "Club not found":
            raise HTTPException(status_code=404, detail=error404)
        if not await check_leg_name(update_data.name, session):
            raise HTTPException(status_code=409, detail=error409)

        stmt = update(club).where(club.c.id == club_id).values(
            name=update_data.name,
            dest=update_data.dest,
            photo=update_data.photo,
            bio=update_data.bio,
            links=update_data.links,
            comfort_time=update_data.comfort_time
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_club_by_id(club_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "Club not found":
            raise HTTPException(status_code=404, detail=error404)
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)