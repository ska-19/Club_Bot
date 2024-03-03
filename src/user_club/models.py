from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.user_profile.models import user
from src.database import Base, metadata

club_x_user = Table(
    'club_x_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('clubot_bd.club.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('role', String(255), nullable=False),
    Column('date_joined', TIMESTAMP, nullable=False)
)