from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.user_profile.models import user
from src.database import Base, metadata

achievement = Table(
    'achievement', metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(255), nullable=False),
    Column('info', Text),
    Column('pic', Text)
)

user_x_achievement = Table(
    'user_x_achievement', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('achievement_id', Integer, ForeignKey('achievement.id'), nullable=False),
    Column('date', TIMESTAMP, nullable=False)
)