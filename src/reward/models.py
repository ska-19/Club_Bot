from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.user_profile.models import user
from src.database import Base, metadata

reward = Table(
    'reward', metadata,
    Column('id', Integer, primary_key=True),
    Column('info', Text),
    Column('exp', Integer),
)

user_x_reward = Table(
    'user_x_reward', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('reward_id', Integer, ForeignKey('reward.id'), nullable=False),
    Column('context', Text)
)

club_x_reward = Table(
    'club_x_reward', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('reward_id', Integer, ForeignKey('reward.id'), nullable=False),
    Column('context', Text)
)