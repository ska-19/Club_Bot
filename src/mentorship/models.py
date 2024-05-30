from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, BIGINT

from src.user_profile.models import user
from src.club.models import club
from src.database import Base, metadata


mentorship = Table(
    'mentorship', metadata,
    Column('id', Integer, primary_key=True),
    Column('mentor_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('mentee_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('club_id', BIGINT, ForeignKey('club.id'), nullable=False),
    # Column('start_date', TIMESTAMP, nullable=False),
    # Column('end_date', TIMESTAMP, nullable=False)
)
