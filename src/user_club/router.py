from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club_x_user
from src.user_profile.models import user
from src.club.models import club
from src.user_club.schemas import UserJoin, UpdateRole, User, UpdateBalance
from src.user_profile.inner_func import get_user_by_id
from src.club.inner_func import get_club_by_id
from src.user_club.inner_func import get_role, get_rec_id, check_rec, get_users_by_dict, make_main, make_not_main, \
    error, error404u, error404c, error404uc, success

router = APIRouter(
    prefix="/join",
    tags=["join"]
)

error404s = {
    "status": "error",
    "data": "Users not found",
    "details": None
}

error409 = {
    "status": "error",
    "data": "This user already in this club",
    "details": None
}


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
        join_dict['is_main'] = False
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


@router.get("/get_balance")
async def get_balance(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает баланс пользователя в клубе

           :param
           :return:
               200 + success, если все хорошо.
               404 + error404uc, если пользователь не состоит в клубе.
               404 + error404u, если пользователь не найден.
               404 + error404c, если клуб не найден.
               500 если внутрення ошибка сервера.

        """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        if await check_rec(user_id, club_id, session):
            raise ValueError('404')

        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == club_id))
        result = await session.execute(query)
        data = result.mappings().first()

        return {
            "status": "success",
            "data": data['balance'],
            "details": None
        }

    except ValueError as e:
        if str(e) == '404':
            raise HTTPException(status_code=404, detail=error404uc)
        elif str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception as e:
        raise HTTPException(status_code=500, detail=error)


@router.post("/disjoin_club")
async def disjoin_club(
        data: User,
        session: AsyncSession = Depends(get_async_session)
):
    """ Удаляет запись о присоединении пользователя к клубу

       :param data: джейсон вида User
       :return:
           200 + success, если все хорошо.
           404 + error404uc, если пользователь не состоит в клубе.
           404 + error404u, если пользователь не найден.
           404 + error404c, если клуб не найден.
           500 если внутрення ошибка сервера.

    """
    try:
        data_dict = data.dict()
        if await get_user_by_id(data_dict['user_id '], session) == "User not found":  # TODO: вот здесь падает
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
        user_id: int,
        club_id: int,
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
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        if await check_rec(user_id, club_id, session):
            raise ValueError('404uc')
        rec_id = await get_rec_id(user_id, club_id, session)

        role = await get_role(user_id, club_id, session)

        if role == 'admin':
            stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(role='member')
        elif role == 'member':
            stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(role='admin')

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


@router.post("/update_balance")
async def update_balance(
        new_balance: UpdateBalance,
        session: AsyncSession = Depends(get_async_session)
):
    """ Обновляет баланс пользователя в клубе

       :param new_balance: джейсон вида UpdateBalance
       :return:
           200 + success, если все хорошо.
           404 + error404uc, если пользователь не состоит в клубе.
           404 + error404u, если пользователь не найден.
           404 + error404c, если клуб не найден.
           500 если внутрення ошибка сервера.

    """
    try:
        new_balance_dict = new_balance.dict()
        if await get_user_by_id(new_balance_dict['user_id'], session) == "User not found":
            raise ValueError('404u')

        if await get_club_by_id(new_balance_dict['club_id'], session) == "Club not found":
            raise ValueError('404c')

        if await check_rec(new_balance_dict['user_id'], new_balance_dict['club_id'], session):
            raise ValueError('404uc')

        rec_id = await get_rec_id(new_balance_dict['user_id'], new_balance_dict['club_id'], session)

        query = select(club_x_user).where(
            (club_x_user.c.user_id == new_balance_dict['user_id']) &
            (club_x_user.c.club_id == new_balance_dict['club_id']))
        result = await session.execute(query)
        data = result.mappings().first()

        stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(
            balance=data['balance'] + new_balance.plus_balance
        )
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

       :param club_id
       :return:
           200 + джейсон со списком всех пользователей, если все хорошо.
           404 + error404c, если клуб не найден.
           404 + error404s, если таких пользователей нет.
           500 если внутрення ошибка сервера.

    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        join = club_x_user.join(user, club_x_user.c.user_id == user.c.id)
        query = select(user.c.username, club_x_user.c.role, club_x_user.c.date_joined).select_from(join).where(
            club_x_user.c.club_id == club_id)

        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404s')

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

        :param user_id
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


@router.post('/new_main')
async def new_main(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Делает клуб главным

               :param user_id
               :param club_id
               :return:
                   200 + success
                   404 + error404u, если пользователь не найден.
                   404 + error404c, если клубов у пользователя нет.
                   404 + error404uc, если пользователя нет в этом клубе
                   500 если внутрення ошибка сервера.

           """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')
        if await check_rec(user_id, club_id, session):
            raise ValueError('404uc')

        data = await get_clubs_by_user(user_id, session)
        clubs = data['data']
        for club in clubs:
            await make_not_main(user_id, club['id'], session)

        await make_main(user_id, club_id, session)

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


@router.post('/get_main')
async def get_main_club(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает главный клуб пользователя

           :param user_id
           :return:
               200 + джейсон с главным клубом
               404 + error404u, если пользователь не найден.
               404 + error404c, если клубов у пользователя нет.
               500 если внутрення ошибка сервера.

       """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        query = select(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.is_main == True)
        )

        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            query = select(club_x_user).where(club_x_user.c.user_id == user_id)
            result = await session.execute(query)
            data = result.mappings().all()

        if not data:
            raise ValueError('404')

        return {
            "status": "success",
            "data": data[0],
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        else:
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
