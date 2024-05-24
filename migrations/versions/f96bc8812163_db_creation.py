"""db creation

Revision ID: f96bc8812163
Revises: 
Create Date: 2024-05-24 13:26:54.490903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f96bc8812163'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('club', 'uid')
    op.drop_column('club_x_user', 'is_main')
    op.alter_column('event', 'date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.drop_column('event', 'reward')
    op.add_column('event_reg', sa.Column('confirm', sa.Boolean(), nullable=False))
    op.drop_column('event_reg', 'status')
    op.drop_column('event_reg', 'was')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event_reg', sa.Column('was', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('event_reg', sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('event_reg', 'confirm')
    op.add_column('event', sa.Column('reward', sa.INTEGER(), autoincrement=False, nullable=False))
    op.alter_column('event', 'date',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.add_column('club_x_user', sa.Column('is_main', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('club', sa.Column('uid', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
