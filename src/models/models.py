from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255), nullable=False),
    Column('mentor', Boolean, nullable=False),
    Column('info', Text)
)

club = Table(
    'club', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('info', Text)
)

club_x_user = Table(
    'club_x_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('role', String(255), nullable=False),
    Column('info', Text)
)

event = Table(
    'event', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('host_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('info', Text)
)

event_reg = Table(
    'event_reg', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('event_id', Integer, ForeignKey('event.id'), nullable=False),
    Column('info', Text)
)

mentorship = Table(
    'mentorship', metadata,
    Column('id', Integer, primary_key=True),
    Column('mentor_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('mentee_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('info', Text)
)

achievement = Table(
    'achievement', metadata,
    Column('id', Integer, primary_key=True),
    Column('info', Text)
)

user_x_achievement = Table(
    'user_x_achievement', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('achievement_id', Integer, ForeignKey('achievement.id'), nullable=False),
    Column('info', Text)
)

questionnaire = Table(
    'questionnaire', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('info', Text)
)

randomcoffee = Table(
    'randomcoffee', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id1', Integer, ForeignKey('users.id'), nullable=False),
    Column('user_id2', Integer, ForeignKey('users.id'), nullable=False),
    Column('club_id', Integer, ForeignKey('club.id'), nullable=False),
    Column('info', Text)
)