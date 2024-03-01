from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user_profile.models import user
from src.user_profile.schemas import UserUpdate, UserCreate

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


async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            data = "User not found"

        return data
    except Exception:
        return None


# принимает джейсон вида UserCreate, возвращает все поля, которые уже заполненны (комментарии что есть что в
# schemas), возвращает 200 и все поля user если все хорошо и 500 ошибку если не получилось создать
# если в каком то поле возвращается string значит это поле пустое

@router.post("/create")
async def create_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        user_dict = new_user.dict()
        data = await get_user_by_id(user_dict['id'], session)
        if data != "User not found":
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": "User already exist",
                "details": None
            })

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
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


# принимает user_id, возвращает 404 если пользователь не найден, 500 если что то пошло не по плану, 200 и все
# поля user если все хорошо

@router.get("/get_user")
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_user_by_id(user_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "User not found":
            raise HTTPException(status_code=500, detail=error404)
        else:
            return {
                "status": "success",
                "data": data,
                "details": None
            }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)

# принимает user_id, возвращает 404 если пользователь не найден, 500 если что то пошло не по плану, 200 и конкретный
# аттрибут user если все хорошо

@router.get("/get_attr")
async def get_user_attr(
        user_id: int,
        col: str,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_user_by_id(user_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "User not found":
            raise HTTPException(status_code=500, detail=error404)
        else:
            return {
                "status": "success",
                "data": data[col],
                "details": None
            }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


# принимает user_id и джейсон вида UserUpdate, возвращает 404 если пользователь не найден, 500 если что то пошло не
# по плану, 200 и все поля user если все хорошо

@router.post("/update")
async def update_profile(
        user_id: int,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_user_by_id(user_id, session)
        if data is None:
            raise HTTPException(status_code=500, detail=error)
        elif data == "User not found":
            raise HTTPException(status_code=500, detail=error404)
        else:
            stmt = update(user).where(user.c.id == user_id).values(
                username=update_data.username,
                name=update_data.name,
                surname=update_data.surname,
                email=update_data.email,
                tel=update_data.tel,
                photo=update_data.photo,
                comfort_time=update_data.comfort_time,
                course=update_data.course,
                faculty=update_data.faculty,
                links=update_data.links,
                bio=update_data.bio
            )
            await session.execute(stmt)
            await session.commit()

            data = await get_user_by_id(user_id, session)
            if data is None:
                return error
            elif data == "User not found":
                return error404
            else:
                return {
                    "status": "success",
                    "data": data,
                    "details": None
                }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)
