from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, Text, BIGINT

from src.database import metadata

achievement = Table(
    'achievement', metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(255), nullable=False),
    Column('info', Text),
    Column('pic', Text)
)

user_x_achievement = Table(
    'user_x_achievement', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', BIGINT, ForeignKey('user.id'), nullable=False),
    Column('achievement_id', Integer, ForeignKey('achievement.id'), nullable=False),
    Column('date', TIMESTAMP, nullable=False)
)