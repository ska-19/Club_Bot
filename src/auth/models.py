from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.database import Base, metadata

user = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255), nullable=False),  # mail
    Column('mentor', Boolean, nullable=False, default=False),
    Column('email', String(255)), # tg handler
    # Column('password', String(255), nullable=False),  # tg_id
    Column('name', String(255), nullable=False),  # tg name
    Column('surname', String(255), nullable=False),  # tg surname
    # Column('dob', TIMESTAMP),
    Column('tel', String(255)),
    # Column('date_joined', TIMESTAMP, nullable=False, default=datetime.utcnow()),
    Column('photo', Text),  # link
    Column('comfort_time', Text),  # meeting time
    Column('course', String(255)),
    Column('faculty', String(255)),
    Column('links', Text),  # links to social media
    Column('bio', Text),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)  # tg handler
    mentor = Column(Boolean, nullable=False, default=False)
    email = Column(String(255))
    # Column('password', String(255), nullable=False),  # tg_id
    name = Column(String(255), nullable=False)  # tg name
    surname = Column(String(255), nullable=False)  # tg surname
    # dob = Column(TIMESTAMP)
    tel = Column(String(255))
    # date_joined = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    photo = Column(Text)  # link
    comfort_time = Column(Text)  # meeting time
    course = Column(String(255))
    faculty = Column(String(255))
    links = Column(Text)  # links to social media
    bio = Column(Text)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)