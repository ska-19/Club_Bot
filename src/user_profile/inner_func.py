from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_profile.models import user


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


async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if not data:
            return "User not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


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
