"""fix product 2

Revision ID: d80e0a573246
Revises: 0919de7e0883
Create Date: 2024-05-31 04:58:12.555492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd80e0a573246'
down_revision: Union[str, None] = '0919de7e0883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_x_product', sa.Column('date', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_x_product', 'date')
    # ### end Alembic commands ###