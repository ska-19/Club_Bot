from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.user_profile.models import user
from src.club.models import club
from src.database import Base, metadata


randomcoffee = Table(
    'randomcoffee', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id1', Integer, ForeignKey('user.id'), nullable=False),
    Column('user_id2', Integer, ForeignKey('user.id'), nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('meet_date', TIMESTAMP, nullable=False),
    Column('info', Text)
)