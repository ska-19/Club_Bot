from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_profile.models import user
from src.user_profile.schemas import UserUpdate, UserCreate
from src.user_profile.inner_func import get_user_by_id

router = APIRouter(
    prefix="/user_profile",
    tags=["user_profile"]
)

error = {
    "status": "error",
    "data": None,
    "details": None
}

error404 = {
    "status": "error",
    "data": "User not found",
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
        user_dict['achievments'] = {'first': 0, 'second': 0, 'third': 0}
        user_dict['date_joined'] = datetime.utcnow()
        user_dict['dob'] = date.today()

        # password = user_dict.pop("password")
        # user_dict["hashed_password"] = password  # TODO: add hash password
        stmt = insert(user).values(**user_dict)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": user_dict,  # TODO: how return UserRead schemas
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

        :param user_id:
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


@router.get("/get_attr")
async def get_user_attr(
        user_id: int,
        col: str,
        session: AsyncSession = Depends(get_async_session)):
    """Получает данные пользователя по его id и атрибуту

        :param user_id:
        :param col:
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
            "data": data[col],
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
    """Обновляет данные пользователя

       :param user_id:
       :param update_data:
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
            name=update_data.name,
            surname=update_data.surname,
            email=update_data.email,
            tel=update_data.tel,
            photo=update_data.photo,
            comfort_time=update_data.comfort_time,
            course=update_data.course,
            faculty=update_data.faculty,
            links=update_data.links,
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


@router.post("/update_xp")
async def update_xp(
        user_id: int,
        update_xp: int,
        session: AsyncSession = Depends(get_async_session)):
    """Обновляет xp пользователя

        :param user_id:
        :param update_xp: на сколько надо изменить xp
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
            xp=data['xp'] + update_xp
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_user_by_id(user_id, session)
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


@router.post("/update_achievment")
async def update_achievment(
        user_id: int,
        achievment: str,
        session: AsyncSession = Depends(get_async_session)):
    """Обновляет достижение пользователя (не работает, вроде Кирилл взял на себя очивки)

        :param user_id:
        :param achievment:
        :return:
            200 + джейсон со всеми данными, если все хорошо.
            404 если такого юзера нет.
            500 если внутрення ошибка сервера.

    """
    try:
        data = await get_user_by_id(user_id, session)
        if data == "User not found":
            raise ValueError
        data['achievment'][achievment] = 1
        stmt = update(user).where(user.c.id == user_id).values(
            achievment=data['achievment']
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
