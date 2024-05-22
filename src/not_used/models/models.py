from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Text

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255), nullable=False),  # tg handler
    Column('mentor', Boolean, nullable=False, default=False),  
    Column('email', String(255)),
    Column('password', String(255), nullable=False),  # tg_id
    Column('name', String(255), nullable=False),  # tg name
    Column('surname', String(255), nullable=False),  # tg surname
    Column('dob', TIMESTAMP),
    Column('tel', String(255)),
    Column('date_joined', TIMESTAMP, nullable=False),
    Column('photo', Text),  # link
    Column('comfort_time', Text),  # meeting time
    Column('course', String(255)),
    Column('faculty', String(255)),
    Column('links', Text),  # links to social media
    Column('bio', Text)
)

club = Table(
    'club', metadata,
    Column('id', Integer, primary_key=True),
    Column('owner', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('name', String(255), nullable=False),
    Column('dest', Text),
    Column('photo', Text),  # link
    Column('bio', Text),
    Column('links', Text),  # links to social media
    Column('date_created', TIMESTAMP),
    Column('date_joined', TIMESTAMP, nullable=False),
    Column('comfort_time', Text)  # meeting time
    # TODO: add achievements, currency, prizes, etc.
)

club_x_user = Table(
    'club_x_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('clubot_bd.club.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('role', String(255), nullable=False),
    Column('date_joined', TIMESTAMP, nullable=False)
)

event = Table(
    'event', metadata,
    Column('id', Integer, primary_key=True),
    Column('club_id', Integer, ForeignKey('clubot_bd.club.id'), nullable=False),
    Column('host_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('date', TIMESTAMP, nullable=False),
    Column('sinopsis', Text, nullable=False),
    Column('contact', String(255), nullable=False),
    Column('speaker', String(255), nullable=False)
)

event_reg = Table(
    'event_reg', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('event_id', Integer, ForeignKey('clubot_bd.event.id'), nullable=False),
    Column('confirm', Boolean, nullable=False, default=False),  
    Column('reg_date', TIMESTAMP, nullable=False)
)

mentorship = Table(
    'mentorship', metadata,
    Column('id', Integer, primary_key=True),
    Column('mentor_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('mentee_id', Integer, ForeignKey('clubot_bd.users.id'), nullable=False),
    Column('club_id', Integer, ForeignKey('clubot_bd.club.id'), nullable=False),
    Column('start_date', TIMESTAMP, nullable=False),
    Column('end_date', TIMESTAMP, nullable=False)
)

achievement = Table(
    'reward', metadata,
    Column('id', Integer, primary_key=True),
    Column('info', Text)
)

user_x_achievement = Table(
    'user_x_achievement', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('achievement_id', Integer, ForeignKey('reward.id'), nullable=False),
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
    Column('meet_date', TIMESTAMP, nullable=False),
    Column('info', Text)
)