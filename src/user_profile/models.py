from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, Date, JSON, BIGINT
from src.database import metadata

user = Table(
    'user', metadata,
    Column('id', BIGINT, primary_key=True, autoincrement=False),
    Column('username', String(255), nullable=False),
    Column('mentor', Boolean, nullable=False, default=False),
    Column('email', String(255)),
    Column('name', String(255), nullable=False),
    Column('surname', String(255), nullable=False),
    Column('dob', Date),
    Column('tel', String(255)),
    Column('date_joined', TIMESTAMP, nullable=False, default=datetime.utcnow()),
    Column('photo', Text),
    Column('comfort_time', Text),
    Column('course', String(255)),
    Column('faculty', String(255)),
    Column('links', Text),
    Column('bio', Text),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
    Column('xp', Integer, default=0, nullable=False),
    Column('city', String, nullable=False),
    Column('education', String, nullable=False),
)
