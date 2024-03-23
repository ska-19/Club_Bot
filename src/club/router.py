from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.club.models import club
from src.club.schemas import ClubUpdate, ClubCreate
from src.user_profile.router import get_user_by_id

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
        raise HTTPException(status_code=500, detail=error)


async def check_leg_name(
        club_name: str,
        session: AsyncSession = Depends(get_async_session)) -> bool:
    """ Проверяет существует ли клуб с таким именем, внутренняя функция

    :param club_name:
    :return:
        True - если клуба с таким именем нет.
        False - если клуб с таким именем существует.

    """
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


@router.post("/create_club")
async def create_club(
        new_club: ClubCreate,
        session: AsyncSession = Depends(get_async_session)):
    """ Создаёт новый клуб

    :param new_club: джейсон вида ClubCreate
    :return:
        200 + джейсон со всеми данными, если все хорошо.
        404 если owner (=user_id) не существует.
        409 если клуб с таким именем уже существует.
        500 если внутрення ошибка сервера.

    """
    try:
        club_dict = new_club.dict()
        if await get_user_by_id(club_dict['owner'], session) == "User not found":
            raise ValueError('404u')

        if not await check_leg_name(club_dict['name'], session):
            raise ValueError('409')

        club_dict['date_joined'] = datetime.utcnow()
        stmt = insert(club).values(**club_dict)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": club_dict,  # TODO: how return ClubRead schemas
            "details": None
        }
    except ValueError as e:
        if str(e) == '409':
            raise HTTPException(status_code=409, detail=error409)
        else:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "User not found",
                "details": None
                 })
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_club")
async def get_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Получает данные клуба по его id

    :param club_id:
    :return:
        200 + джейсон со всеми данными, если все хорошо.
        404 если такого клуба нет.
        500 если внутрення ошибка сервера.

    """
    try:
        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.post("/update_club")
async def update_club(
        club_id: int,
        update_data: ClubUpdate,
        session: AsyncSession = Depends(get_async_session)):
    """ Обновляет данные клуба по его id

    :param club_id:
    :param update_data: джейсон вида ClubUpdate
    :return:
        200 + джейсон со всеми данными(обновленными), если все хорошо.
        404 если такого клуба нет.
        409 если клуб с таким именем уже существует.
        500 если внутрення ошибка сервера.

    """
    try:
        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError('404')
        if not await check_leg_name(update_data.name, session):
            raise ValueError('409')

        stmt = update(club).where(club.c.id == club_id).values(
            name=update_data.name,
            dest=update_data.dest,
            photo=update_data.photo,
            bio=update_data.bio,
            links=update_data.links,
            comfort_time=update_data.comfort_time,
            date_created=update_data.date_created
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError('404')
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404':
            raise HTTPException(status_code=404, detail=error404)
        else:
            raise HTTPException(status_code=409, detail=error409)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
