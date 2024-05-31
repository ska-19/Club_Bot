"""fix int 2

Revision ID: 16a73dcc3b5c
Revises: d80e0a573246
Create Date: 2024-05-31 21:25:42.721380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a73dcc3b5c'
down_revision: Union[str, None] = 'd80e0a573246'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('club', 'owner',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('club', 'owner',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###