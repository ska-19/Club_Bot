from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import insert, update

from src.user_profile.inner_func import update_xp
from src.market.schemas import AddProduct, UpdateProduct
from src.market.inner_func import *
from src.user_club.inner_func import check_rec, get_role
from src.user_profile.inner_func import get_user_by_id
from src.club.inner_func import get_club_by_id
from src.user_club.models import club_x_user

router = APIRouter(
    prefix="/market",
    tags=["market"]
)

success = {
    "status": "success",
    "data": None,
    "details": None
}


@router.post("/add_product")
async def add_product(
        new_data: AddProduct,
        session: AsyncSession = Depends(get_async_session)
):
    """ Создает товар в магазине

       :param new_data: джейсон вида AddProduct
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404c, если клуб не найден.
           404 + error404uc, если пользователь не состоит в клубе.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(new_data.user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(new_data.club_id, session) == "Club not found":
            raise ValueError('404c')
        if await check_rec(new_data.user_id, new_data.club_id, session):
            raise ValueError('404uc')
        product_dict = new_data.model_dump()

        query = insert(product).values(
            name=product_dict['name'],
            price=product_dict['price'],
            description=product_dict['description'],
            quantity=product_dict['quantity'],
            club_id=product_dict['club_id'])
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": product_dict,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/update_product")
async def update_product(
        new_data: UpdateProduct,
        session: AsyncSession = Depends(get_async_session)
):
    """ Изменяет товар в магазине

       :param new_data: джейсон вида UpdateProduct
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404c, если клуб не найден.
           404 + error404uc, если пользователь не состоит в клубе.
           404 + error404pr, если товар не найден
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(new_data.user_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_product_by_id(new_data.id, session)
        if await get_club_by_id(data['club_id'], session) == "Club not found":
            raise ValueError('404c')
        if await check_rec(new_data.user_id, data['club_id'], session):
            raise ValueError('404uc')
        if await get_product_by_id(new_data.id, session) == "Product not found":
            raise ValueError('404pr')
        product_dict = new_data.model_dump()

        query = update(product).where(product.c.id == product_dict['id']).values(
            name=product_dict['name'],
            price=product_dict['price'],
            description=product_dict['description'],
            quantity=product_dict['quantity'])
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": product_dict,
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '404pr':
            raise HTTPException(status_code=404, detail=error404pr)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_product")
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает товар по id

       :param product_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404pr, если товар не найден
           500 если внутрення ошибка сервера.
    """
    try:
        data = await get_product_by_id(product_id, session)
        if data == "Product not found":
            raise ValueError('404pr')
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=error404pr)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.post("/buy_product")
async def buy_product(
        product_id: int,
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Создает заявку на покупку товара

       :param user_id: int
       :param product_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404pr, если товар не найден
           403 + error403pb, если недостаточно денег для покупки
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_product_by_id(product_id, session) == "Product not found":
            raise ValueError('404pr')
        prod = await get_product_by_id(product_id, session)
        if not await check_transaction_balance(user_id, product_id, session):
            raise ValueError('403pb')

        stmt = insert(user_x_product).values(
            user_id=user_id,
            product_id=product_id,
            status='request',
            date=datetime.utcnow())

        await session.execute(stmt)
        await session.commit()

        stmt = update(club_x_user).where(
            (club_x_user.c.user_id == user_id) &
            (club_x_user.c.club_id == prod['club_id'])).values(
            balance=club_x_user.c.balance - prod['price'])
        await session.execute(stmt)
        await session.commit()

        stmt = update(product).where(product.c.id == product_id).values(
            quantity=prod['quantity'] - 1
        )
        await session.execute(stmt)
        await session.commit()

        await update_xp(user_id, 100, session)

        return success

    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404pr':
            raise HTTPException(status_code=404, detail=error404pr)
        if str(e) == '403pb':
            raise HTTPException(status_code=403, detail=error403pb)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get("/get_all_request")
async def get_all_request(
        admin_id: int,
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(admin_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')
        role = await get_role(admin_id, club_id, session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            query = select(user_x_product).where((user_x_product.c.club_id == club_id) &
                                                 (user_x_product.c.status == 'request'))
            result = await session.execute(query)
            data = result.mappings().all()

            if not data:
                return {
                    "status": "success",
                    "data": None,
                    "details": None
                }

            return {
                "status": "success",
                "data": data,
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


@router.post("/accept_request")
async def accept_request(
        rec_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Одобряет заявку на покупку товара

      :param rec_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404req, если заявка не найдена
           403 + error403, если заявка уже одобрена/отклонена
           500 если внутрення ошибка сервера.
    """
    try:
        data = await get_user_x_product_by_id(rec_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        if data['status'] != 'request':
            raise ValueError('403s')

        stmt = update(user_x_product).where(user_x_product.c.id == data['id']).values(status='accept')
        await session.execute(stmt)
        await session.commit()

        return success
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404req':
            raise HTTPException(status_code=404, detail=error404req)
        if str(e) == '403s':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/reject_request_admin")
async def reject_request_admin(
        rec_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Отклоняет заявку на покупку товара со стороны администрации

       :param rec_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404req, если заявка не найдена
           403 + error403, если заявка уже одобрена/отклонена
           500 если внутрення ошибка сервера.
    """
    try:
        data = await get_user_x_product_by_id(rec_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        if data['status'] != 'request':
            raise ValueError('403s')

        stmt = update(user_x_product).where(user_x_product.c.id == data['id']).values(status='reject')
        await session.execute(stmt)
        await session.commit()

        data_product = await get_product_by_id(data['product_id'], session)
        stmt = update(product).where(product.c.id == data['product_id']).values(quantity=data_product['quantity'] + 1)
        await session.execute(stmt)
        await session.commit()

        stmt = update(club_x_user).where(
            (club_x_user.c.user_id == data['user_id']) &
            (club_x_user.c.club_id == data_product['club_id'])).values(
            balance=club_x_user.c.balance + data_product['price'])
        await session.execute(stmt)
        await session.commit()

        await update_xp(data['user_id'], -75, session)

        return success

    except ValueError as e:
        if str(e) == '404req':
            raise HTTPException(status_code=404, detail=error404req)
        if str(e) == '403s':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/reject_request_user")
async def reject_request_user(
        rec_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Отклоняет заявку на покупку товара со стороны пользователя

       :param rec_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           404 + error404req, если заявка не найдена
           403 + error403, если заявка уже одобрена/отклонена
           500 если внутрення ошибка сервера.
        """
    try:
        data = await get_user_x_product_by_id(rec_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        if data['status'] != 'request':
            raise ValueError('403s')

        stmt = update(user_x_product).where(user_x_product.c.id == data['id']).values(status='reject')
        await session.execute(stmt)
        await session.commit()

        data_product = await get_product_by_id(data['product_id'], session)
        stmt = update(product).where(product.c.id == data['product_id']).values(quantity=data_product['quantity'] + 1)
        await session.execute(stmt)
        await session.commit()

        stmt = update(club_x_user).where(
            (club_x_user.c.user_id == data['user_id']) &
            (club_x_user.c.club_id == data_product['club_id'])).values(
            balance=club_x_user.c.balance + data_product['price'])
        await session.execute(stmt)
        await session.commit()

        await update_xp(data['user_id'], -100, session)

        return success
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404req':
            raise HTTPException(status_code=404, detail=error404req)
        if str(e) == '403s':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post('/delete_item')
async def delete_product(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Удаляет товар из магазина (лениво)

       :param product_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404pr, если товар не найден
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_product_by_id(product_id, session) == "Product not found":
            raise ValueError('404pr')
        stmt = update(product).where(product.c.id == product_id).values(quantity=-1)
        await session.execute(stmt)
        await session.commit()
    except ValueError:
        raise HTTPException(status_code=404, detail=error404pr)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.get('/get_item_by_club')
async def get_items_by_club(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает все товары в клубе

       :param club_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404pr, если товар не найден
           404 + error404c, если клуб не найден.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')
        query = select(product).where(product.c.club_id == club_id)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            return {
                "status": "fail",
                "data": None,
                "details": None
            }

        return {
            "status": "success",
            "data": data,
            "details": None
        }

    except ValueError:
        raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_user_history_active")
async def get_user_history_active(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает активные заявки пользователя

       :param user_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        join = user_x_product.join(product, user_x_product.c.product_id == product.c.id)
        query = select(product, user_x_product).select_from(join).where(
            (user_x_product.c.user_id == user_id) &
            (user_x_product.c.status == 'request')).order_by(user_x_product.c.date)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            return {
                "status": "fail",
                "data": None,
                "details": None
            }

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_user_history_close")
async def get_user_history_close(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает одобренные/отклоненные заявки пользователя

       :param user_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404u, если пользователь не найден.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')

        join = user_x_product.join(product, user_x_product.c.product_id == product.c.id)
        query = select(product, user_x_product).select_from(join).where(
            (user_x_product.c.user_id == user_id) &
            (user_x_product.c.status != 'request')).order_by(desc(user_x_product.c.date))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            return {
                "status": "fail",
                "data": None,
                "details": None
            }

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_admin_history_active")
async def get_admin_history_active(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает активные заявки пользователей клуба

       :param club_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404c, если клуб не найден.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        join = user_x_product.join(product, user_x_product.c.product_id == product.c.id)
        query = select(product, user_x_product).select_from(join).where(
            (product.c.club_id == club_id) &
            (user_x_product.c.status == 'request')).order_by(user_x_product.c.date)
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            return {
                "status": "fail",
                "data": None,
                "details": None
            }

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)


@router.get("/get_admin_history_close")
async def get_admin_history_close(
        club_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """ Возвращает одобренные/отклоненные заявки пользователей клуба

       :param user_id: int
       :return:
           200 + success, если все хорошо.
           404 + error404c, если клуб не найден.
           500 если внутрення ошибка сервера.
    """
    try:
        if await get_club_by_id(club_id, session) == "Club not found":
            raise ValueError('404c')

        join = user_x_product.join(product, user_x_product.c.product_id == product.c.id)
        query = select(product, user_x_product).select_from(join).where(
            (product.c.club_id == club_id) &
            (user_x_product.c.status != 'request')).order_by(desc(user_x_product.c.date))
        result = await session.execute(query)
        data = result.mappings().all()

        if not data:
            return {
                "status": "fail",
                "data": None,
                "details": None
            }

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=error404c)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
