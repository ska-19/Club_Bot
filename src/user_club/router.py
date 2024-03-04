from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_club.models import club_x_user
from src.user_club.schemas import UserJoin, UpdateRole, UserDisjoin


router = APIRouter(
    prefix="/join",
    tags=["join"]
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
    "data": "This user already in this club",
    "details": None
}

success = {
    "status": "success",
    "data": None,
    "details": None
}


# внутренняя функция, принимает user_id и club_id возвращает rec_id
# перед вызовом обязательно проверить существоание записи (check_rec)
async def get_rec_id(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    try:
        query = select(club_x_user).where(club_x_user.c.user_id == user_id and club_x_user.c.club_id == club_id)
        result = await session.execute(query)
        data = result.mappings().first()

        return data['id']
    except Exception:
        raise HTTPException(status_code=500, detail=error)


# внутренняя функция, принимает user_id и club_id, возвращает true, если такой записи нет, false иначе
async def check_rec(
        user_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(club_x_user).where(club_x_user.c.user_id == user_id and club_x_user.c.club_id == club_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return True
        else:
            return False
    except Exception:
        raise HTTPException(status_code=500, detail=error)


# принимает джейсон вида UserJoin
# 200 + success, если все хорошо
# 409 если такая запись уже существует
# 500 если внутрення ошибка сервера
@router.post("/join_club")
async def join_to_the_club(
        join_data: UserJoin,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        join_dict = join_data.dict()
        if not await check_rec(join_dict['user_id'], join_dict['club_id'], session):
            raise HTTPException(status_code=409, detail=error409)

        join_dict['date_joined'] = datetime.utcnow()
        stmt = insert(club_x_user).values(**join_dict)
        await session.execute(stmt)
        await session.commit()

        return success
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


# принимает джейсон вида UserJoin
# 200 + success, если все хорошо
# 409 если такая запись уже существует
# 500 если внутрення ошибка сервера
@router.post("/disjoin_club")
async def disjoin_club(
        data: UserDisjoin,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        data_dict = data.dic()
        if await check_rec(data_dict['user_id'], data_dict['club_id'], session):
            raise HTTPException(status_code=404, detail=error404)

        rec_id = await get_rec_id(data_dict['user_id'], data_dict['club_id'], session)
        stmt = delete(club_x_user).where(club_x_user.c.id == rec_id)
        await session.execute(stmt)
        await session.commit()

        return success
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


@router.post("/role_upgrade")
async def role_update(
        new_role: UpdateRole,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_role_dict = new_role.dict()
        if await check_rec(new_role_dict['user_id'], new_role_dict['club_id'], session):
            raise HTTPException(status_code=404, detail=error404)

        rec_id = await get_rec_id(new_role_dict['user_id'], new_role_dict['club_id'], session)
        stmt = update(club_x_user).where(club_x_user.c.id == rec_id).values(role=role_update.role)
        await session.execute(stmt)
        await session.commit()

        return success
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_users_in_club")
async def get_users_in_club(
        user_id: int,  # TODO: write schema
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/get_users_with_role")
async def get_users_with_role(
        user_id: int,  # TODO: write schema
        club_id: int,
        role: str,
        session: AsyncSession = Depends(get_async_session)
):
    pass


