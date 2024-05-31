from sqlalchemy import Integer, String, Text, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from bot_instance import SQL_URL_RC

engine = create_async_engine(url=SQL_URL_RC,
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    questionnaire_counter: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_knew_interest_clubs: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_readiness_new_meetings: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_expectations: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_meeting_format: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_zodiac_signs: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_personality_type: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_gender: Mapped[int] = mapped_column(Integer, default=-1)
    choosing_hobbies: Mapped[str] = mapped_column(String(255), default='')
    tell_hobbies: Mapped[str] = mapped_column(Text, default='')
    tell_what_do_you_do: Mapped[str] = mapped_column(Text, default='')
    tell_expectations: Mapped[str] = mapped_column(Text, default='')
    choosing_stay_in_touch: Mapped[int] = mapped_column(Integer, default=-1)
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
