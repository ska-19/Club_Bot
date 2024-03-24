from datetime import datetime

from src.club.schemas import ClubUpdate, ClubCreate
from src.user_profile.router import get_user_by_id
from src.club.inner_func import *

router = APIRouter(
    prefix="/club",
    tags=["club"]
)

# принимает джейсон вида ClubCreate
# 200 + джейсон со всеми данными, если все хорошо
# 404 если owner (=user_id) не существует
# 409 если клуб с таким именем уже существует
# 500 если внутрення ошибка сервера
@router.post("/create_club")
async def create_club(
        new_club: ClubCreate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        club_dict = new_club.dict()
        if await get_user_by_id(club_dict['owner'], session) == "User not found":
            raise ValueError('404u')

        if not await check_leg_name(club_dict['name'], session):
            raise ValueError('409')

        club_dict['date_joined'] = datetime.utcnow()
        stmt = insert(club).values(**club_dict)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": club_dict,  # TODO: how return ClubRead schemas
            "details": None
        }
    except ValueError as e:
        if str(e) == '409':
            raise HTTPException(status_code=409, detail=error409)
        else:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": "User not found",
                "details": None
                 })
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


# принимает club_id
# 200 + джейсон со всеми данными, если все хорошо
# 404 если такого клуба нет
# 500 если внутрення ошибка сервера
@router.get("/get_club")
async def get_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
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


# принимает club_id и джейсон вида ClubUpdate
# 200 + джейсон со всеми данными(обновленными), если все хорошо
# 404 если такого клуба нет
# 409 если клуб с таким именем уже существует
# 500 если внутрення ошибка сервера
@router.post("/update_club") #TODO: мб стоит еще проверять что именно овнер или админ пытается чет поменять в клубе
async def update_club(
        club_id: int,
        update_data: ClubUpdate,
        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError('404')
        if not await check_leg_name(update_data.name, session):
            raise ValueError('409')

        stmt = update(club).where(club.c.id == club_id).values(
            name=update_data.name,
            dest=update_data.dest,
            photo=update_data.photo,
            bio=update_data.bio,
            links=update_data.links,
            comfort_time=update_data.comfort_time,
            date_created=update_data.date_created
        )
        await session.execute(stmt)
        await session.commit()

        data = await get_club_by_id(club_id, session)
        if data == "Club not found":
            raise ValueError('404')
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404':
            raise HTTPException(status_code=404, detail=error404)
        else:
            raise HTTPException(status_code=409, detail=error409)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()
