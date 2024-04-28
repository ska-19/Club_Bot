from fastapi import APIRouter
from sqlalchemy import select, insert, update, delete

from datetime import datetime

from src.club.inner_func import get_club_by_id
from src.events.schemas import EventCreate, EventUpdate, EventReg
from src.user_club.inner_func import check_rec, get_role
from src.events.inner_func import *
from src.user_profile.inner_func import get_user_by_id

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/create_event")
async def create_event(
        new_event: EventCreate,
        session: AsyncSession = Depends(get_async_session)):
    """ Создаёт новое событие

            :param new_event: джейсон вида EventCreate
            :return:
                200 + джейсон со всеми данными, если все хорошо.
                404 + error404u если owner (=user_id) не существует.
                404 + error404c если такой клуб не найден
                404 + error404uc если пользователь не состоит в клубе
                403 + error403 если нет доступа у пользователя для такого запроса
                409 если клуб с таким именем уже существует.
                500 если внутрення ошибка сервера.

    """
    try:
        if await get_user_by_id(new_event.host_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(new_event.club_id, session) == "Club not found":
            raise ValueError('404c')

        role = await get_role(new_event.host_id, new_event.club_id, session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            event_dict = new_event.model_dump()
            query = insert(event).values(**event_dict)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": event_dict,
                "details": None
            }
        else:
            raise ValueError('403')
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '403':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_event")
async def get_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ выдает данные о событии по id

               :param event_id
               :return:
                   принимает event_id
                   200 + джейсон со всеми данными, если все хорошо
                   404 + error404e если события с таким id нет
                   500 если внутрення ошибка сервера
    """
    try:
        data = await get_event_by_id(event_id, session)
        if data == "Event not found":
            raise ValueError('404e')
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404e':
            raise HTTPException(status_code=404, detail=error404e)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.post("/update_event")
async def update_event(
        event_id: int,
        update_data: EventUpdate,
        session: AsyncSession = Depends(get_async_session)):
    """ Изменяет событие

                :param
                    event_id
                    update_data: джейсон вида EventUpdate
                :return:
                    200 + джейсон со всеми данными, если все хорошо.
                    404 + error404u если owner (=user_id) не существует.
                    404 + error404c если такой клуб не найден
                    404 + error404e если события с таким id нет
                    403 + error403 если нет доступа у пользователя для такого запроса
                    409 если клуб с таким именем уже существует.
                    500 если внутрення ошибка сервера.

    """
    try:
        data = await get_event_by_id(event_id, session)
        if data == "Event not found":
            raise ValueError('404e')
        if await get_user_by_id(update_data.host_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(update_data.club_id, session) == "Club not found":
            raise ValueError('404c')
        if update_data.host_id != data['host_id']:
            raise ValueError('403')

        event_dict = update_data.model_dump()
        query = update(event).where(event.c.id == event_id).values(**event_dict)
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": event_dict,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404e':
            raise HTTPException(status_code=404, detail=error404e)
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '403':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/event_reg")
async def reg_event(
        data: EventReg,
        session: AsyncSession = Depends(get_async_session)):
    """ регистрирует пользователя на событие

               :param data: джейсон вида EventReg
               :return:
                  200 + джейсон со всеми данными, если все хорошо.
                  404 + error404u если owner (=user_id) не существует.
                  404 + error404e если события с таким id нет
                  404 + error404uc если пользователь не состоит в клубе
                  500 - внутренняя ошибка сервера

    """
    try:
        if await get_user_by_id(data.user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_event_by_id(data.event_id, session) == "Event not found":
            raise ValueError('404e')
        club_id = await get_club_id_by_event_id(data.event_id, session)
        if await check_rec(data.user_id, club_id, session):
            raise ValueError('404uc')
        event_dict = data.model_dump()
        event_dict['reg_date'] = datetime.utcnow()
        query = insert(event_reg).values(**event_dict)
        await session.execute(query)

        await session.commit()

        return {
            "status": "success",
            "data": event_dict,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404e':
            raise HTTPException(status_code=404, detail=error404e)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_event_club")
async def get_event_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ выдает данные о событиях в клубе по id

               :param event_id
               :return:
                   200 + джейсон со всеми данными, если все хорошо.
                   404 + error404с если клуб не найден
                   500 если внутрення ошибка сервера
    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')
        data = await get_all_event_club(club_id, session)
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/event_disreg")
async def event_disreg(
        user_id: int,
        event_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ отменяет регистрацию пользователя на событие

               :param
                  user_id
                  event_id
               :return:
                  200 + джейсон со всеми данными, если все хорошо.
                  404 + error404u если owner (=user_id) не существует.
                  404 + error404e если события с таким id нет
                  404 + error404eu если пользователь не регистрировался на событие
                  500 - внутренняя ошибка сервера

    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_event_by_id(event_id, session) == "Event not found":
            raise ValueError('404e')
        print('here')
        if not await check_rec_event(user_id, event_id, session):
            raise ValueError('404eu')

        query = select(event_reg).where(
            (event_reg.c.user_id == user_id) &
            (event_reg.c.event_id == event_id))
        result = await session.execute(query)
        data = result.mappings().first()

        query = delete(event_reg).where(
            (event_reg.c.user_id == user_id) &
            (event_reg.c.event_id == event_id))
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404e':
            raise HTTPException(status_code=404, detail=error404e)
        if str(e) == '404eu':
            raise HTTPException(status_code=404, detail=error404eu)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/delete_event")
async def delete_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ удаляет событие

              :param event_id
              :return:
                 200 + джейсон со всеми данными, если все хорошо.
                 404 + error404e если события с таким id нет
                 500 - внутренняя ошибка сервера

       """
    try:
        data = await get_event_by_id(event_id, session)
        if data == "Event not found":
            raise ValueError('404e')

        query = delete(event).where(event.c.id == event_id)
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404e':
            raise HTTPException(status_code=404, detail=error404e)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()