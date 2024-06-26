"""fix int

Revision ID: c3a31fa293bc
Revises: f152506022f7
Create Date: 2024-05-31 00:12:09.479948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3a31fa293bc'
down_revision: Union[str, None] = 'f152506022f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('photo', sa.Text(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('club_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_x_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('club_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('club_x_user', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('event_reg', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('mentorship', 'club_id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('user', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=False)
    op.alter_column('user_x_achievement', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_x_achievement', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('user', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=False)
    op.alter_column('mentorship', 'club_id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('event_reg', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('club_x_user', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_table('user_x_product')
    op.drop_table('product')
    # ### end Alembic commands ###