from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.achievement.models import achievement, user_x_achievement, club_x_achievement
from src.achievement.schemas import AddAchievementClub, UpdateAchievementClub, AddAchievementUser
from src.achievement.inner_func import *
from src.user_club.inner_func import check_rec, get_role
from src.user_profile.inner_func import get_user_by_id
from src.club.inner_func import get_club_by_id

router = APIRouter(
    prefix="/achievement",
    tags=["achievement"]
)


@router.post("/add_achievement")
async def add_achievement(
        new_data: AddAchievementClub,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(new_data.admin_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(new_data.club_id, session) == "Club not found":
            raise ValueError('404c')
        role = await get_role(new_data.admin_id, new_data.club_id, session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            achievement_dict = new_data.model_dump()

            query = insert(achievement).values(info=achievement_dict['info'],
                                               exp=achievement_dict['exp'])
            result = await session.execute(query)
            await session.commit()
            query = insert(club_x_achievement).values(club_id=new_data.club_id,
                                                      achievement_id=result.inserted_primary_key[0],
                                                      context=None)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": achievement_dict,
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '404p':
            raise HTTPException(status_code=404, detail=error404p)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_achievement")
async def get_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        data = await get_achievement_by_id(achievement_id, session)
        if data == "Achievement not found":
            raise ValueError('404a')
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404a':
            raise HTTPException(status_code=404, detail=error404a)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.post("/update_achievement")
async def update_achievement(
        achievement_id: int,
        new_data: UpdateAchievementClub,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(new_data.admin_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(new_data.club_id, session) == "Club not found":
            raise ValueError('404c')
        role = await get_role(new_data.admin_id, new_data.club_id, session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            query = update(achievement).where(achievement.c.id == achievement_id).values(info=new_data.info,
                                                                                         exp=new_data.exp)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": new_data.dict(),
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '404p':
            raise HTTPException(status_code=404, detail=error404p)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/add_achievement_to_user")
async def add_to_user(
        new_data: AddAchievementUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(new_data.admin_id, session) == "User not found":
            raise ValueError('404ad')
        if await get_user_by_id(new_data.user_id, session) == "User not found":
            raise ValueError('404u')
        query = select(club_x_achievement).where(club_x_achievement.c.id == new_data.club_x_achievement_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if not data:
            raise ValueError('404ac')
        role = await get_role(new_data.admin_id, data['club_id'], session)
        if role == "owner" or role == "admin":
            query = insert(user_x_achievement).values(user_id=new_data.user_id,
                                                      achievement_id=data['achievement_id'],
                                                      context=None)
            await session.execute(query)
            await session.commit()
            return_data = {
                "admin_id": new_data.admin_id,
                "user_id": new_data.user_id,
                "achievement_id": data['achievement_id'],
                "club_id": data['club_id'],

            }
            return {
                "status": "success",
                "data": return_data,
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404ad':
            raise HTTPException(status_code=404, detail=error404ad)
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404ac':
            raise HTTPException(status_code=404, detail=error404ac)
        if str(e) == '404p':
            raise HTTPException(status_code=404, detail=error404p)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_users_by_achievement")
async def get_by_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_achievement_by_id(achievement_id, session) == "Achievement not found":
            raise ValueError('404a')
        data = await get_all_user_by_achievement_id(achievement_id, session)
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404a':
            raise HTTPException(status_code=404, detail=error404a)
    except Exception:
        raise HTTPException(status_code=500, detail=error)



@router.get("/get_achievement_by_user")
async def get_by_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_all_achievement_by_user_id(user_id, session)
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


#TODO: добавить удаление ачивок и возможность получить все ачивки в клубе