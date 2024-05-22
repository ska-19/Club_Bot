from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, Date

from src.user_profile.models import user
from src.database import Base, metadata

club = Table(
    'club', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner', Integer, ForeignKey('user.id'), nullable=False),
    Column('name', String(255), nullable=False),
    Column('dest', Text),
    Column('photo', Text),  # link
    Column('bio', Text),
    Column('links', Text),  # links to social media
    Column('date_created', Date),
    Column('date_joined', TIMESTAMP, nullable=False),
    Column('comfort_time', Text),  # meeting time
    Column('channel_link', String(255), nullable=False),
    Column('uid', String(255), nullable=False),
    # TODO: add achievements, currency, prizes, etc.
)
