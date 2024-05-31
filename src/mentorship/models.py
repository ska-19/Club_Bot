from sqlalchemy import Table, Column, Integer, ForeignKey, BIGINT

from src.database import metadata


mentorship = Table(
    'mentorship', metadata,
    Column('id', Integer, primary_key=True),
    Column('mentor_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('mentee_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('club_id', BIGINT, ForeignKey('club.id'), nullable=False),
)
