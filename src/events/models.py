from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, Date

from src.user_profile.models import user
from src.club.models import club
from src.database import Base, metadata

event = Table(
    'event', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('host_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('date', Date, nullable=False),
    Column('sinopsis', Text, nullable=False),
    Column('contact', String(255), nullable=False),
    Column('speaker', String(255), nullable=False),
    Column('reward', Integer, nullable=False)
)

event_reg = Table(
    'event_reg', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('event_id', Integer, ForeignKey('event.id'), nullable=False),
    # Column('confirm', Boolean, nullable=False, default=False),
    Column('reg_date', TIMESTAMP, nullable=False),
    Column('status', Boolean, nullable=False, default=True),
    Column('was', Boolean, nullable=False, default=False)
)