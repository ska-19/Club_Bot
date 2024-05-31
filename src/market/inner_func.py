from fastapi import Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.market.models import product, user_x_product
from src.database import get_async_session
from src.errors import *
from src.user_club.inner_func import get_user_balance


async def get_product_by_id(
        product_id: int,
        session: AsyncSession
):
    try:
        query = select(product).where(product.c.id == product_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "Product not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_transaction_count(
        user_id: int,
        product_id: int,
        count: int,
        session: AsyncSession
):
    try:
        prod = await get_product_by_id(product_id, session)
        if prod['count'] < count:
            return False

        return True
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def check_transaction_balance(
        user_id: int,
        product_id: int,
        session: AsyncSession
):
    try:
        prod = await get_product_by_id(product_id, session)
        balance = await get_user_balance(user_id, prod['club_id'], session)
        if balance < prod['price']:
            return False

        return True
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_user_x_product_by_id(
        user_x_product_id: int,
        session: AsyncSession
):
    try:
        query = select(user_x_product).where(user_x_product.c.id == user_x_product_id)
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "Request not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)


async def get_rec_market(
        user_id: int,
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user_x_product).where(
            (user_x_product.c.user_id == user_id) &
            (user_x_product.c.product_id == product_id)
        ).order_by(desc(user_x_product.c.date))
        result = await session.execute(query)
        data = result.mappings().first()

        if not data:
            return "Request not found"
        return data
    except Exception:
        raise HTTPException(status_code=500, detail=error)

