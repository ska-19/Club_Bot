from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club_x_user
from src.user_profile.models import user
from src.club.models import club
from src.user_club.schemas import UserJoin, UpdateRole, UserDisjoin
from src.user_profile.router import get_user_by_id
from src.club.router import get_club_by_id

router = APIRouter(
    prefix="/join",
    tags=["join"]
)

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

error404s = {
    "status": "error",
    "data": "Users not found",
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

error409 = {
    "status": "error",
    "data": "This user already in this club",
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
        session: AsyncSession = Depends(get_async_session)
):
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

        if not data:
            return True
        else:
            return False
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


@router.post("/join_club")
async def join_to_the_club(
        join_data: UserJoin,
        session: AsyncSession = Depends(get_async_session)
):
    """ Присоединяет пользователя к клубу

    :param join_data: джейсон вида UserJoin
    :return:
        200 + success, если все хорошо.
        404 + error404u, если пользователь не найден.
        404 + error404c, если клуб не найден.
        409 если такая запись уже существует.
        500 если внутрення ошибка сервера.

    Note: error404u и error404c имена переменных с джейсонами-ошибками.

    """
    try:
        join_dict = join_data.dict()
        if await get_user_by_id(join_dict['user_id'], session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(join_dict['club_id'], session) == "Club not found":
            raise ValueError('404c')

        if not await check_rec(join_dict['user_id'], join_dict['club_id'], session):
            raise ValueError('409')

        join_dict['date_joined'] = datetime.utcnow()
        stmt = insert(club_x_user).values(**join_dict)
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        elif str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        else:
            raise HTTPException(status_code=409, detail=error409)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/disjoin_club")
async def disjoin_club(
        data: UserDisjoin,
        session: AsyncSession = Depends(get_async_session)
):
    """ Удаляет запись о присоединении пользователя к клубу

    :param data: джейсон вида UserDisjoin
    :return:
        200 + success, если все хорошо.
        404 + error404uc, если пользователь не состоит в клубе.
        404 + error404u, если пользователь не найден.
        404 + error404c, если клуб не найден.
        500 если внутрення ошибка сервера.

    """
    try:
        data_dict = data.dict()
        if await get_user_by_id(data_dict['user_id '], session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(data_dict['club_id'], session) == "Club not found":
            raise ValueError('404c')

        if await check_rec(data_dict['user_id'], data_dict['club_id'], session):
            raise ValueError('404')

        rec_id = await get_rec_id(data_dict['user_id'], data_dict['club_id'], session)
        stmt = delete(club_x_user).where(club_x_user.c.id == rec_id)
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404':
            raise HTTPException(status_code=404, detail=error404uc)
        elif str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/role_update")
async def role_update(
        new_role: UpdateRole,
        session: AsyncSession = Depends(get_async_session)
):
    """ Обновляет роль пользователя в клубе

    :param new_role: джейсон вида UpdateRole
    :return:
        200 + success, если все хорошо.
        404 + error404uc, если пользователь не состоит в клубе.
        404 + error404u, если пользователь не найден.
        404 + error404c, если клуб не найден.
        500 если внутрення ошибка сервера.

    """
    try:
        new_role_dict = new_role.dict()
        if await get_user_by_id(new_role_dict['user_id'], session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(new_role_dict['club_id'], session) == "Club not found":
            raise ValueError('404c')

        if await check_rec(new_role_dict['user_id'], new_role_dict['club_id'], session):
            raise ValueError('404uc')

        rec_id = await get_rec_id(new_role_dict['user_id'], new_role_dict['club_id'], session)
        stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(role=new_role.role)
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        elif str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_users_in_club")
async def get_users_in_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает список пользователей в клубе

    :param club_id:
    :return:
        200 + джейсон со списком всех пользователей, если все хорошо.
        404 + error404c, если клуб не найден.
        404 + error404s, если таких пользователей нет.
        500 если внутрення ошибка сервера.

    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        query = select(club_x_user).where(club_x_user.c.club_id == club_id)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404s')

        data = await get_users_by_dict(data, session)

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404s':
            raise HTTPException(status_code=404, detail=error404s)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_users_with_role")
async def get_users_with_role(
        club_id: int,
        role: str,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает список пользователей в клубе с определенной ролью

    :param club_id:
    :param role:
    :return:
        200 + джейсон со cписком всех пользователей с этой ролью, если все хорошо.
        404 + error404c, если клуб не найден.
        404 + error404s, если таких пользователей нет.
        500 если внутрення ошибка сервера.

    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        query = select(club_x_user).where(
            (club_x_user.c.club_id == club_id) &
            (club_x_user.c.role == role))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404s')

        data = await get_users_by_dict(data, session)

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404s':
            raise HTTPException(status_code=404, detail=error404s)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_clubs_by_user")
async def get_clubs_by_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает список клубов, в которых состоит пользователь

    :param user_id:
    :return:
        200 + джейсон со cписком всех клубой, в которых состоит пользователь, если все хорошо.
        404 + error404u, если пользователь не найден.
        404 если таких клубов нет.
        500 если внутрення ошибка сервера.

    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        query = select(club_x_user).where(club_x_user.c.user_id == user_id)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404s')

        clubs_ids = [item['club_id'] for item in data]
        query = select(club).where(club.c.id.in_(clubs_ids))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise Exception

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404s':
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "Clubs not found",
                "details": None
            })
        else:
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
