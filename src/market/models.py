from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

from src.user_profile.models import user
from src.database import Base, metadata

product = Table(
    'product', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('price', Integer, nullable=False),
    Column('description', Text),
    Column('photo', Text),
    Column('quantity', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
)