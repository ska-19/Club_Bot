from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, Date, JSON, BIGINT

from src.database import Base, metadata

user = Table(
    'user', metadata,
    Column('id', BIGINT, primary_key=True, autoincrement=False),  # tg id
    Column('username', String(255), nullable=False),  # tg username (handler)
    Column('mentor', Boolean, nullable=False, default=False),
    Column('email', String(255)),
    # Column('password', String(255), nullable=False),
    Column('name', String(255), nullable=False),  # tg name
    Column('surname', String(255), nullable=False),  # tg surname
    Column('dob', Date),
    Column('tel', String(255)),
    Column('date_joined', TIMESTAMP, nullable=False, default=datetime.utcnow()),
    Column('photo', Text),  # ссылка на фото
    Column('comfort_time', Text),  # удобное время для встреч
    Column('course', String(255)),
    Column('faculty', String(255)),
    Column('links', Text),  # ссылки на соц сети
    Column('bio', Text),  # о себе
    # Column("hashed_password", String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),

    Column('xp', Integer, default=0, nullable=False),
    Column('city', String, nullable=False),
    Column('education', String, nullable=False),
    # Column('achievments', JSON)
)
