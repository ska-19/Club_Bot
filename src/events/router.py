from fastapi import APIRouter
from sqlalchemy import insert, update

from datetime import datetime

from src.club.inner_func import get_club_by_id
from src.events.schemas import EventCreate, EventUpdate, EventReg, Data
from src.user_club.inner_func import check_rec, get_role
from src.events.inner_func import *
from src.user_profile.inner_func import get_user_by_id
from src.user_club.schemas import UpdateBalance
from src.user_club.router import update_balance
from src.user_profile.models import user


router = APIRouter(
    prefix="/events",
    tags=["events"]
)

error404s = {
    "status": "error",
    "data": "Users not found",
    "details": None
}


@router.get("/check_rec")
async def get_check_rec(
        event_id: int,
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        if not await check_rec_event(user_id=user_id, event_id=event_id, session=session):
            return False
        return True
    except Exception:
        raise HTTPException(status_code=500, detail=error)


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
            query = insert(event).values(**event_dict).returning(event.c.id)
            result = await session.execute(query)
            await session.commit()

            id = result.fetchone()[0]
            RegEvent = EventReg(user_id=new_event.host_id, event_id=id)
            await reg_event(RegEvent, session)

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

               :param event_id: int
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

                :param event_id: int
                :param update_data: джейсон вида EventUpdate
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
        if await (check_rec_event(data.user_id, data.event_id, session)):
            raise ValueError('409')

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
        if str(e) == '409':
            raise HTTPException(status_code=409, detail=error409)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_event_club")
async def get_event_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ выдает данные о событиях в клубе по id

               :param club_id: int
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

               :param user_id: int
               :param event_id: int
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


@router.post("/delete_event") #TODO: пофиксить удаление
async def delete_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)):
    """ удаляет событие

              :param event_id: int
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


@router.post('/end_event')
async def end_event(
        event_id: int,
        data: Data,
        session: AsyncSession = Depends(get_async_session)
):
    """ завершает событие. выдает опыт и монеты участникам, которые пришли и админ составу, очищает event_reg и удаляет событие
        список пользователлей должен поступать в формате json (смотри схему Data, на самом деле json в jsone с ключем k), где ключ - стинговое значение user_id, а значение - 0/1 в зависимости от посещения

                 :param event_id: int
                 :param data: Data
                 :return:
                    200 + джейсон со всеми данными, если все хорошо.
                    404 + error404e если события с таким id нет
                    500 - внутренняя ошибка сервера

          """
    try:
        users = data.dict()['users']
        data = await get_event_by_id(event_id, session)

        if data == "Event not found":
            raise ValueError('404e')

        reward = data['reward']
        club_id = await get_club_id_by_event_id(event_id, session)
        await adm_boost(event_id, session)
        for user_id, perm in users.items():
            if perm:
                updatebalance = UpdateBalance(club_id=club_id, user_id=user_id, plus_balance=reward)
                await update_balance(updatebalance, session)
                await update_xp(int(user_id), 50, session)
        await clean(event_id, session)
        await delete_event(event_id, session)
    except ValueError:
        raise HTTPException(status_code=404, detail=error404e)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_users_by_event")
async def get_users_by_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_event_by_id(event_id, session) == "Event not found":
            raise ValueError('404e')

        join = event_reg.join(user, event_reg.c.user_id == user.c.id)
        query = select(user.c.id, user.c.username, user.c.name, user.c.surname, event_reg.c.reg_date).select_from(join).where(event_reg.c.event_id == event_id).order_by(user.c.surname)

        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            raise ValueError('404s')

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404s':
            raise HTTPException(status_code=404, detail=error404s)
        else:
            raise HTTPException(status_code=404, detail=error404e)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
