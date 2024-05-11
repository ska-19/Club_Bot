from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.reward.models import reward, user_x_reward, club_x_reward
from src.reward.schemas import AddRewardClub, UpdateRewardClub, AddRewardUser
from src.reward.inner_func import *
from src.user_club.inner_func import check_rec, get_role
from src.user_profile.inner_func import get_user_by_id
from src.club.inner_func import get_club_by_id

router = APIRouter(
    prefix="/reward",
    tags=["reward"]
)


@router.post("/add_reward")
async def add_reward(
        new_data: AddRewardClub,
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
            reward_dict = new_data.model_dump()

            query = insert(reward).values(info=reward_dict['info'],
                                          exp=reward_dict['exp'])
            result = await session.execute(query)
            await session.commit()
            query = insert(club_x_reward).values(club_id=new_data.club_id,
                                                      reward_id=result.inserted_primary_key[0],
                                                      context=None)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": reward_dict,
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


@router.get("/get_reward")
async def get_reward(
        reward_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        data = await get_reward_by_id(reward_id, session)
        if data == "Reward not found":
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


@router.post("/update_reward")
async def update_reward(
        reward_id: int,
        new_data: UpdateRewardClub,
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
            query = update(reward).where(reward.c.id == reward_id).values(info=new_data.info,
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


@router.post("/add_reward_to_user")
async def add_to_user(
        new_data: AddRewardUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(new_data.admin_id, session) == "User not found":
            raise ValueError('404ad')
        if await get_user_by_id(new_data.user_id, session) == "User not found":
            raise ValueError('404u')
        query = select(club_x_reward).where(club_x_reward.c.id == new_data.club_x_reward_id)
        result = await session.execute(query)
        data = result.mappings().first()
        if not data:
            raise ValueError('404ac')
        role = await get_role(new_data.admin_id, data['club_id'], session)
        if role == "owner" or role == "admin":
            query = insert(user_x_reward).values(user_id=new_data.user_id,
                                                 reward_id=data['reward_id'],
                                                 context=None)
            await session.execute(query)
            await session.commit()
            return_data = {
                "admin_id": new_data.admin_id,
                "user_id": new_data.user_id,
                "reward_id": data['reward_id'],
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


@router.get("/get_users_by_reward")
async def get_by_reward(
        reward_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_reward_by_id(reward_id, session) == "Reward not found":
            raise ValueError('404a')
        data = await get_all_user_by_reward_id(reward_id, session)
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



@router.get("/get_reward_by_user")
async def get_by_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_all_reward_by_user_id(user_id, session)
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