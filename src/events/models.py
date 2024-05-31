from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Text, Date, BIGINT
from src.database import metadata

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
    Column('user_id', BIGINT, ForeignKey('user.id'), nullable=False),
    Column('event_id', Integer, ForeignKey('event.id'), nullable=False),
    Column('reg_date', TIMESTAMP, nullable=False),
    Column('status', Boolean, nullable=False, default=True),
    Column('was', Boolean, nullable=False, default=False)
)