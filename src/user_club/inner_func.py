from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club_x_user
from src.user_profile.models import user
from src.user_profile.inner_func import get_user_by_id
from src.club.inner_func import get_club_by_id


error = {
    "status": "error",
    "data": None,
    "details": None
}

error404u = {
    "status": "error",
    "data": "User not found",
    "details": None
}

error404c = {
    "status": "error",
    "data": "Club not found",
    "details": None
}

error404uc = {
    "status": "error",
    "data": "This user not in this club",
    "details": None
}

success = {
    "status": "success",
    "data": None,
    "details": None
}


async def get_rec_id(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    """ Возвращает id записи в таблице club_x_user, внутренняя функция

        Note: перед вызовом обязательно проверить существоание записи (check_rec)

        :param user_id:
        :param club_id:
        :return: rec_id (int)

    """
    try:
        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()

        return data['id']
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_rec(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Проверяет существование записи в таблице club_x_user, внутренняя функция

        :param user_id:
        :param club_id:
        :return:
            True если записи нет.
            False если запись есть.

    """
    try:
        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()
        print(data)
        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)


# внутреняя функция, принимает user_id и club_id, возвращает роль пользователя в клубе
async def get_role( #TODO: мб сделать ее внешней
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    if await check_rec(user_id, club_id, session):
        return "User not in the club"
    try:
        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "User not found"

        return data['role']
    except Exception:
        raise HTTPException(status_code=500, detail=error)


# внутрення функция для получения списка юзеров по списку словарей, содержащих user_id
# при вызове функции обязательно проверить что data является списком словарей с полем user_id и он не пуст
async def get_users_by_dict(
        data,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user_ids = [item['user_id'] for item in data]
        query = select(user).where(user.c.id.in_(user_ids))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise Exception

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


 # внутреняя функция, принимает user_id и club_id, возвращает роль пользователя в клубе


async def get_role(  # TODO: мб сделать ее внешней
            user_id: int,
            club_id: int,
            session: AsyncSession = Depends(get_async_session)
    ):
        if await check_rec(user_id, club_id, session):
            return "User not in the club"
        try:
            query = select(club_x_user).where(
                (club_x_user.c.user_id == user_id) &
                (club_x_user.c.club_id == club_id))
            result = await session.execute(query)
            data = result.mappings().first()

            if not data:
                return "User not found"

            return data['role']
        except Exception:
            raise HTTPException(status_code=500, detail=error)


async def get_users_by_dict(
        data,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает список пользователей по списку словарей, содержащих user_id, внутренняя функция

       Note: перед вызовом обязательно проверить что data является списком словарей с полем user_id и он не пуст

       :param data:
       :return:

    """
    try:
        user_ids = [item['user_id'] for item in data]
        query = select(user).where(user.c.id.in_(user_ids))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise Exception

        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def make_main(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        rec_id = await get_rec_id(user_id, club_id, session)

        stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(is_main=True)

        await session.execute(stmt)
        await session.commit()

        return success
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


async def make_not_main(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        rec_id = await get_rec_id(user_id, club_id, session)

        stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(is_main=False)

        await session.execute(stmt)
        await session.commit()

        return success
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
