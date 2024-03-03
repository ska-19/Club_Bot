from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.events.models import club, event
from src.events.schemas import EventCreate, EventUpdate, EventReg
from src.club.router import error,  error404, error409

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

# внутренняя функция, принимает дату, возвращает true, если события в этот день нет, false иначе
# async def check_date_conflict(
#         date: str,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         query = select(event).where(event.c.date == date)
#         result = await session.execute(query)
#         data = result.mappings().first()
#
#         if not data:
#             return True
#         else:
#             return False
#     except Exception:
#         return False

# принимает json вида EventCreate
# 200 - успешно создано, возвращает json со всеми данными
# 409 - Событие с такой датой уже существует
# 500 - ошибка сервера
@router.post("/create_event")
async def create_event(
        new_event: EventCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # if not await check_date_conflict(new_event.date):
        #     raise HTTPException(status_code=409, detail=error409)
        query = insert(event).values(
            club_id=new_event.club_id,
            host_id=new_event.host_id,
            # date=new_event.date,
            sinopsis=new_event.sinopsis,
            contact=new_event.contact,
            speaker=new_event.speaker
        )
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": new_event.model_dump(),
            "details": None
        }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)


# принимает event_id
# 200 + джейсон со всеми данными, если все хорошо
# 404 если события с таким id нет
# 500 если внутрення ошибка сервера

@router.get("/get_event")
async def get_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event).where(event.c.id == event_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            raise HTTPException(status_code=404, detail=error404)
    except Exception:
        raise HTTPException(status_code=500, detail=error)

# принимает event_id
# 200 + джейсон со всеми данными, если все хорошо
# 404 если события с таким id нет
# 500 если внутрення ошибка сервера

@router.post("/update_event")
async def update_event(
        event_id: int,
        update_data: EventUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(event).where(event.c.id == event_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            raise HTTPException(status_code=404, detail=error404)
        # if not await check_date_conflict(update_data.date):
        #     raise HTTPException(status_code=409, detail=error409)
        query = update(event).where(event.c.id == event_id).values(
            club_id=update_data.club_id,
            host_id=update_data.host_id,
            # date=update_data.date,
            sinopsis=update_data.sinopsis,
            contact=update_data.contact,
            speaker=update_data.speaker
        )
        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": update_data.model_dump(),
            "details": None
        }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)

# принимает json вида EventReg
# 200 - успешно создано, возвращает json со всеми данными
# 500 - ошибка сервера
@router.post("/event_reg")
async def event_reg(
        data: EventReg,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = insert(event_reg).values(
            user_id=data.user_id,
            event_id=data.event_id,
            confirm=data.confirm,
            # reg_date=data.reg_date
        )
        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": data.model_dump(),
            "details": None
        }
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=error)
