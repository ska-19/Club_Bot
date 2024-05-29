from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.market.models import product, user_x_product
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


@router.post("/add_product")
async def add_product(
        new_data: AddProduct,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        print('a')
        if await get_user_by_id(new_data.admin_id, session) == "User not found":
            raise ValueError('404u')
        if await get_club_by_id(new_data.club_id, session) == "Club not found":
            raise ValueError('404c')
        role = await get_role(new_data.admin_id, new_data.club_id, session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            product_dict = new_data.model_dump()

            query = insert(product).values(name=product_dict['name'],
                                          price=product_dict['price'],
                                          description=product_dict['description'],
                                          photo=product_dict['photo'],
                                          quantity=product_dict['quantity'],
                                          rating=product_dict['rating'],
                                          club_id=new_data.club_id)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": product_dict,
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404u':
            print('market/add_product 404u')
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404c':
            print('market/add_product 404c')
            raise HTTPException(status_code=404, detail=error404c)
        if str(e) == '404uc':
            print('market/add_product 404uc')
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '404p':
            print('market/add_product 404p')
            raise HTTPException(status_code=404, detail=error404p)
    finally:
        await session.rollback()


@router.post("/update_product")
async def update_product(
        new_data: UpdateProduct,
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
            product_dict = new_data.model_dump()

            query = update(product).where(product.c.id == new_data.id).values(name=product_dict['name'],
                                          price=product_dict['price'],
                                          description=product_dict['description'],
                                          photo=product_dict['photo'],
                                          quantity=product_dict['quantity'],
                                          rating=product_dict['rating'],
                                          club_id=new_data.club_id)
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": product_dict,
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
    finally:
        await session.rollback()



@router.get("/get_product")
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
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
        if str(e) == '404p':
            raise HTTPException(status_code=404, detail=error404r)
    except Exception:
        raise HTTPException(status_code=500, detail=error)



@router.post("/buy_product")
async def buy_product(
        product_id: int,
        user_id: int,
        count: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        if await get_product_by_id(product_id, session) == "Product not found":
            raise ValueError('404pr')
        prod = await get_product_by_id(product_id, session)
        if await check_rec(user_id, prod['club_id'], session):
            raise ValueError('404uc')
        if not await check_transaction_count(user_id, product_id, count, session):
            raise ValueError('404pc')
        if not await check_transaction_balance(user_id, product_id, count, session):
            raise ValueError('404pb')

        query = insert(user_x_product).values(user_id=user_id,
                                              product_id=product_id,
                                              count=count,
                                              club_id=prod['club_id'],
                                              date=datetime.utcnow())
        await session.execute(query)
        await session.commit()

        usr = await get_user_by_id(user_id, session)
        query = update(club_x_user).where((club_x_user.c.user_id == user_id) &
                                          (club_x_user.c.club_id == prod['club_id'])).values(
            balance=usr['balance'] - prod['price'] * count
        )
        await session.execute(query)
        await session.commit()

        query = update(product).where(product.c.id == product_id).values(
            count=prod['count'] - count
        )
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": {'user_id': user_id,
                     'product_id': product_id,
                     'count': count,
                     'date': datetime.utcnow(),
                     'status': 'request'},
            "details": None
        }

    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404pr':
            raise HTTPException(status_code=404, detail=error404pr)
        if str(e) == '404uc':
            raise HTTPException(status_code=404, detail=error404uc)
        if str(e) == '404pb':
            raise HTTPException(status_code=404, detail=error404pb)
        if str(e) == '404pc':
            raise HTTPException(status_code=404, detail=error404pc)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()


@router.post("/get_all_request")
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
    finally:
        await session.rollback()



@router.post("/accept_request")
async def accept_request(
        admin_id: int,
        user_x_product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(admin_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_user_x_product_by_id(user_x_product_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        role = await get_role(admin_id, data['club_id'], session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            query = update(user_x_product).where(user_x_product.c.id == user_x_product_id).values(status='accept')
            await session.execute(query)
            await session.commit()

            return {
                "status": "success",
                "data": {'user_id': data['user_id'],
                         'product_id': data['product_id'],
                         'count': data['count'],
                         'date': data['date'],
                         'status': 'accept'},
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404up':
            raise HTTPException(status_code=404, detail=error404req)
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


@router.post("/reject_request_admin")
async def reject_request_admin(
        admin_id: int,
        user_x_product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(admin_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_user_x_product_by_id(user_x_product_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        role = await get_role(admin_id, data['club_id'], session)
        if role == "User not in the club":
            raise ValueError('404uc')
        if role == "admin" or role == "owner":
            query = update(user_x_product).where(user_x_product.c.id == user_x_product_id).values(status='reject')
            await session.execute(query)
            await session.commit()

            query = update(product).where(product.c.id == data['product_id']).values(count=data['count'])
            await session.execute(query)
            await session.commit()

            prod = await get_product_by_id(data['product_id'], session)
            query = update(club_x_user).where((club_x_user.c.user_id == data['user_id']) &
                                                (club_x_user.c.club_id == data['club_id'])).values(
                    balance=club_x_user.c.balance + data['count'] * prod['price']
                )

            return {
                "status": "success",
                "data": {'user_id': data['user_id'],
                         'product_id': data['product_id'],
                         'count': data['count'],
                         'date': data['date'],
                         'status': 'admin_reject'},
                "details": None
            }
        else:
            raise ValueError('404p')
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404up':
            raise HTTPException(status_code=404, detail=error404req)
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



@router.post("/reject_request_user")
async def reject_request_user(
        user_id: int,
        user_x_product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        data = await get_user_x_product_by_id(user_x_product_id, session)
        if data == "Request not found":
            raise ValueError('404req')
        if data['user_id'] != user_id:
            raise ValueError('403u')
        if data['status'] != 'request':
            raise ValueError('403s')
        query = update(user_x_product).where(user_x_product.c.id == user_x_product_id).values(status='reject')
        await session.execute(query)
        await session.commit()

        query = update(product).where(product.c.id == data['product_id']).values(count=data['count'])
        await session.execute(query)
        await session.commit()

        prod = await get_product_by_id(data['product_id'], session)
        query = update(club_x_user).where((club_x_user.c.user_id == data['user_id']) &
                                          (club_x_user.c.club_id == data['club_id'])).values(
            balance=club_x_user.c.balance + data['count'] * prod['price']
        )

        return {
            "status": "success",
            "data": {'user_id': data['user_id'],
                     'product_id': data['product_id'],
                     'count': data['count'],
                     'date': data['date'],
                     'status': 'user_reject'},
            "details": None
        }
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
        if str(e) == '404up':
            raise HTTPException(status_code=404, detail=error404req)
        if str(e) == '403u':
            raise HTTPException(status_code=403, detail=error403u)
        if str(e) == '403s':
            raise HTTPException(status_code=403, detail=error403)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()



@router.post("/get_user_history")
async def get_user_history(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if await get_user_by_id(user_id, session) == "User not found":
            raise ValueError('404u')
        query = select(user_x_product).where(user_x_product.c.user_id == user_id)
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
    except ValueError as e:
        if str(e) == '404u':
            raise HTTPException(status_code=404, detail=error404u)
    except Exception:
        raise HTTPException(status_code=500, detail=error)
    finally:
        await session.rollback()




