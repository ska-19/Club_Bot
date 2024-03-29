"""db creation

Revision ID: bb1e9ae4e5e0
Revises: 
Create Date: 2024-03-05 14:18:48.934017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb1e9ae4e5e0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('mentor', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('surname', sa.String(length=255), nullable=False),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('tel', sa.String(length=255), nullable=True),
    sa.Column('date_joined', sa.TIMESTAMP(), nullable=False),
    sa.Column('photo', sa.Text(), nullable=True),
    sa.Column('comfort_time', sa.Text(), nullable=True),
    sa.Column('course', sa.String(length=255), nullable=True),
    sa.Column('faculty', sa.String(length=255), nullable=True),
    sa.Column('links', sa.Text(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('club',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('dest', sa.Text(), nullable=True),
    sa.Column('photo', sa.Text(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('links', sa.Text(), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=True),
    sa.Column('date_joined', sa.TIMESTAMP(), nullable=False),
    sa.Column('comfort_time', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('club_x_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('club_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.Column('date_joined', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('club_id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(), nullable=False),
    sa.Column('sinopsis', sa.Text(), nullable=False),
    sa.Column('contact', sa.String(length=255), nullable=False),
    sa.Column('speaker', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.ForeignKeyConstraint(['host_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_reg',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('confirm', sa.Boolean(), nullable=False),
    sa.Column('reg_date', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_reg')
    op.drop_table('event')
    op.drop_table('club_x_user')
    op.drop_table('club')
    op.drop_table('user')
    # ### end Alembic commands ###