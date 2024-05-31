from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_profile.models import user
from src.user_profile.schemas import UserUpdate, UserCreate
from src.user_profile.inner_func import get_user_by_id, error404
from src.user_club.router import get_clubs_by_user, disjoin_club
from src.user_club.schemas import User
from src.club.schemas import FoundUid

router = APIRouter(
    prefix="/user_profile",
    tags=["user_profile"]
)

error = {
    "status": "error",
    "data": None,
    "details": None
}

error409 = {
    "status": "error",
    "data": "User already exists",
    "details": None
}


@router.post("/create_user")
async def create_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    """ Создаёт нового пользователя

        :param new_user: джейсон вида UserCreat
        :return:
            200 + джейсон со всеми данными(которые уже заполненны (комментарии что есть что в schemas)), если все хорошо.
            409 если юзер с таким именем уже существует.
            500 если внутрення ошибка сервера.
            если в каком то поле возвращается string значит это поле пустое.

    """
    try:
        user_dict = new_user.dict()
        data = await get_user_by_id(user_dict['id'], session)
        if data != "User not found":
            raise ValueError
        user_dict['is_active'] = True
        user_dict['is_superuser'] = False
        user_dict['is_verified'] = False
        user_dict['mentor'] = False
        user_dict['email'] = 'string'
        user_dict['tel'] = 'string'
        user_dict['photo'] = 'string'
        user_dict['comfort_time'] = 'string'
        user_dict['course'] = 'string'
        user_dict['faculty'] = 'string'
        user_dict['links'] = 'string'
        user_dict['bio'] = 'string'
        user_dict['education'] = 'string'
        user_dict['city'] = 'string'
        user_dict['xp'] = 0
        user_dict['date_joined'] = datetime.utcnow()
        user_dict['dob'] = date.today()

        stmt = insert(user).values(**user_dict)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": user_dict,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=409, detail=error409)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_user")
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Получает данные пользователя по его id

        :param user_id: int
        :return:
            200 + джейсон со всеми данными, если все хорошо.
            404 если такого юзера нет.
            500 если внутрення ошибка сервера.

    """
    try:
        data = await get_user_by_id(user_id, session)
        if data == "User not found":
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


@router.post("/update_create_user")
async def update_create_profile(
        update_data: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Обновляет данные пользователя (для тг бота)

       :param update_data: UserCreate
       :return:
           200 + джейсон со всеми данными, если все хорошо.
           404 если такого юзера нет.
           500 если внутрення ошибка сервера.

    """
    try:
        update_data = dict(update_data)
        data = await get_user_by_id(update_data['id'], session)
        if data == "User not found":
            raise ValueError
        stmt = update(user).where(user.c.id == update_data['id']).values(
            username=update_data['username'],
            name=update_data['name'],
            surname=update_data['surname']
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_user_by_id(update_data['id'], session)
        if data == "User not found":
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
    finally:
        await session.rollback()


@router.post("/update_links_user")
async def update_links_profile(
        user_id: int,
        update_data: FoundUid,
        session: AsyncSession = Depends(get_async_session)):
    """Обновляет данные пользователя (только линкс)

       :param user_id: int
       :param update_data: FoundUid
       :return:
           200 + джейсон со всеми данными, если все хорошо.
           404 если такого юзера нет.
           500 если внутрення ошибка сервера.

    """
    try:
        data = await get_user_by_id(user_id, session)
        if data == "User not found":
            raise ValueError
        stmt = update(user).where(user.c.id == user_id).values(
            links=update_data.uid
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_user_by_id(user_id, session)
        if data == "User not found":
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
    finally:
        await session.rollback()


@router.post("/update_user")
async def update_profile(
        user_id: int,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_async_session)):
    """Обновляет данные пользователя (для веб аппа)

       :param user_id: int
       :param update_data: UserUpdate
       :return:
           200 + джейсон со всеми данными, если все хорошо.
           404 если такого юзера нет.
           500 если внутрення ошибка сервера.

    """
    try:
        data = await get_user_by_id(user_id, session)
        if data == "User not found":
            raise ValueError
        stmt = update(user).where(user.c.id == user_id).values(
            bio=update_data.bio,
            dob=update_data.dob,
            education=update_data.education,
            city=update_data.city
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_user_by_id(user_id, session)
        if data == "User not found":
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
    finally:
        await session.rollback()


@router.post("/delete_user")
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """Удаляет пользователя

        :param user_id: int
        :return:
            200 + джейсон со всеми данными, если все хорошо.
            404 если такого юзера нет.
            500 если внутрення ошибка сервера.

    """
    try:
        data = await get_user_by_id(user_id, session)
        if data == "User not found":
            raise ValueError("404")
        clubs = await get_clubs_by_user(user_id, session)
        clubs_data = clubs['data']
        for club in clubs_data:
            user_data = User(user_id=user_id, club_id=club['id'])
            await disjoin_club(user_data, session)
        stmt = user.delete().where(user.c.id == user_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
