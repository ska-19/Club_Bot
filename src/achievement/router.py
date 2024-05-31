from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.achievement.models import achievement, user_x_achievement
from src.user_profile.inner_func import get_user_by_id
from src.user_profile.models import user
from src.achievement.inner_func import get_achievement_by_id, get_rec_id, check_rec, error


router = APIRouter(
    prefix="/achievement",
    tags=["achievement"]
)

success = {
    "status": "success",
    "data": None,
    "details": None
}

error404a = {
    "status": "error",
    "data": 'Achievment not found',
    "details": None
}

error404u = {
    "status": "error",
    "data": 'User not found',
    "details": None
}

error404ua = {
    "status": "error",
    "data": 'This user has not this achievement',
    "details": None
}


@router.post("/add_achievement_to_user")
async def add_to_user(
        user_id: int,
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Выдает пользователю ачивку

       :param
           user_id
           achievement_id
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404a, если ачивка не найдена.
           409 если такая запись уже существует.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_achievement_by_id(achievement_id, session) == "Achievement not found":
            raise ValueError('404a')
        if check_rec(user_id, achievement_id, session):
            raise ValueError('409')

        ach = {
            'user_id': user_id,
            'achievement_id': achievement_id,
            'date': datetime.utcnow()
        }

        stmt = insert(user_x_achievement).values(**ach)
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        elif str(e) == '409':
            raise HTTPException(status_code=409, detail={
                "status": "error",
                "data": 'This user already has this achievement',
                "details": None
            })
        else:
            raise HTTPException(status_code=404,  detail=error404a)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/remove_achievement_to_user")
async def remove_from_user(
        user_id: int,
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Удаляет запись о выдаче ачивки

      :param
          user_id
          achievement_id
      :return:
          200 + success, если все хорошо.
          404 + error404ua, если у пользователя нет этой ачивки.
          404 + error404u, если пользователь не найден.
          404 + error404a, если ачивка не найдена.
          500 если внутрення ошибка сервера.
   """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_achievement_by_id(achievement_id, session) == "Achievement not found":
            raise ValueError('404a')
        if await check_rec(user_id, achievement_id, session):
            raise ValueError('404')

        rec_id = await get_rec_id(user_id, achievement_id, session)
        stmt = delete(user_x_achievement).where(user_x_achievement.c.id == rec_id)
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        elif str(e) == '404a':
            raise HTTPException(status_code=404, detail=error404a)
        else:
            raise HTTPException(status_code=404, detail=error404ua)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_users_by_achievement")
async def get_by_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Возвращает список пользователей с ачивкой

       :param achievement_id
       :return:
           200 + джейсон со списком всех пользователей, если все хорошо.
           404 + error404a, если ачивка не найдена.
           404, если таких пользователей нет.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_achievement_by_id(achievement_id, session) == "Achievement not found":
            raise ValueError('404a')

        join = user_x_achievement.join(user, user_x_achievement.c.user_id == user.c.id)
        query = (select(user, user_x_achievement.c.date)
                 .select_from(join)
                 .where(user_x_achievement.c.achievement_id == achievement_id))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404')

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404':
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "Users not found",
                "details": None
            })
        else:
            raise HTTPException(status_code=404, detail=error404a)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_achievement_by_user")
async def get_achievement_by_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ Возвращает список ачивок, которые есть у пользователя

       :param user_id
       :return:
           200 + джейсон со cписком всех ачивок, которые есть у пользователя, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 если таких ачивок нет.
           500 если внутрення ошибка сервера.

   """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        query = (select(user_x_achievement)
                 .where(user_x_achievement.c.user_id == user_id))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404')

        ach_ids = [item['achievement_id'] for item in data]
        query = (select(achievement)
                 .where(achievement.c.id.in_(ach_ids)))
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
        if str(e) == '404':
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "Achievements not found",
                "details": None
            })
        else:
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
