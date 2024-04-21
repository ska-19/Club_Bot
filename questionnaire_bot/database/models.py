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


class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    choosing_knew_interest_clubs: Mapped[int] = mapped_column(Integer, default=0)
    choosing_readiness_new_meetings: Mapped[int] = mapped_column(Integer, default=0)
    choosing_expectations: Mapped[int] = mapped_column(Integer, default=0)
    choosing_meeting_format: Mapped[int] = mapped_column(Integer, default=0)
    choosing_hobbies: Mapped[str] = mapped_column(String(255), default='')
    tell_hobbies: Mapped[str] = mapped_column(Text, default='')
    tell_expectations: Mapped[str] = mapped_column(Text, default='')
    choosing_stay_in_touch: Mapped[int] = mapped_column(Integer, default=0)
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id')


# class Category(Base):
#     __tablename__ = 'categories'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(25))


# class Item(Base):
#     __tablename__ = 'items'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     description: Mapped[str] = mapped_column(String(128))
#     price: Mapped[str] = mapped_column(String(10))
#     category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


# class Basket(Base):
#     __tablename__ = 'basket'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     item: Mapped[int] = mapped_column(ForeignKey('items.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# questionnaire = Table(
#     'questionnaire', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', Integer),
#     Column('choosing_knew_interest_clubs', Integer),
#     Column('choosing_readiness_new_meetings', Integer),
#     Column('choosing_expectations', Integer),
#     Column('choosing_meeting_format', Integer),
#     Column('choosing_hobbies', String(255)),
#     Column('tell_hobbies', Text),
#     Column('tell_expectations', Text),
#     Column('choosing_stay_in_touch', Integer),
# )