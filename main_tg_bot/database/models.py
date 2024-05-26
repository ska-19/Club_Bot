import os
from dotenv import load_dotenv

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'),
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
