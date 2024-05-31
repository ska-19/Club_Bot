from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text, BIGINT

from src.user_profile.models import user
from src.database import Base, metadata

product = Table(
    'product', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('price', Integer, nullable=False),
    Column('description', Text),
    Column('quantity', Integer, nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
)

user_x_product = Table(
    'user_x_product', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', BIGINT, ForeignKey('user.id'), nullable=False),
    Column('product_id', Integer, ForeignKey('product.id'), nullable=False),
    Column('date', TIMESTAMP, nullable=False),
    Column('status', Text, nullable=False, default='request'),
)