from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.club.models import club
from src.club.schemas import ClubUpdate, ClubCreate
from src.user_profile.inner_func import get_user_by_id
from src.user_club.router import join_to_the_club, get_users_in_club, disjoin_club
from src.user_club.schemas import UserJoin, User
from src.club.inner_func import get_club_by_id, check_leg_name

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


@router.post("/create_club")
async def create_club(
        new_club: ClubCreate,
        session: AsyncSession = Depends(get_async_session)):
    """ Создаёт новый клуб  !!!важно вызвать

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
        owner = club_dict["owner"]
        stmt = insert(club).values(**club_dict).returning(club.c.id)
        result = await session.execute(stmt)
        await session.commit()

        id = result.fetchone()[0]
        userjoin = UserJoin(club_id=id, user_id=owner, role='owner')
        await join_to_the_club(userjoin, session)
        club_dict['id'] = id
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


@router.get("/get_channel_link")
async def get_club_link(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Получает ссылку на канал клуба по его id

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
            "data": data['channel_link'],
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
            date_created=update_data.date_created,
            channel_link=update_data.channel_link
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



@router.post("/delete_club")
async def delete_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Удаляет клуб по его id

        :param club_id:
        :return:
            200 + джейсон со всеми данными, если все хорошо.
            404 если такого клуба нет.
            500 если внутрення ошибка сервера.

    """
    try:
        print(club_id)
        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError("404")
        usrs = await get_users_in_club(club_id, session)
        usrs = usrs['data']
        for u in usrs:
            user = User(user_id=u['user_id'], club_id=club_id)
            await disjoin_club(user, session)
        query = delete(club).where(club.c.id == club_id)

        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
