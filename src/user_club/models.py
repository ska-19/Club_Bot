from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, BIGINT

from src.user_profile.models import user
from src.club.models import club
from src.database import Base, metadata

club_x_user = Table(
    'club_x_user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('user_id', BIGINT, ForeignKey('user.id'), nullable=False),
    Column('role', String(255), nullable=False),
    Column('date_joined', TIMESTAMP, nullable=False),
    Column('balance', Integer, nullable=False),
    Column('is_main', Boolean, nullable=False)
)
