from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, Text, Date
from src.database import metadata

club = Table(
    'club', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner', Integer, ForeignKey('user.id'), nullable=False),
    Column('name', String(255), nullable=False),
    Column('dest', Text),
    Column('photo', Text),
    Column('bio', Text),
    Column('links', Text),
    Column('date_created', Date),
    Column('date_joined', TIMESTAMP, nullable=False),
    Column('comfort_time', Text),
    Column('channel_link', String(255), nullable=False),
    Column('uid', String(255), nullable=False),
)
