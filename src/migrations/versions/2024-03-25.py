"""Changes in Targets table

Revision ID: 1a07f592692e
Revises: c1902ae50b9d
Create Date: 2024-03-25 14:14:10.530107

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a07f592692e"
down_revision: Union[str, None] = "c1902ae50b9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("targets", sa.Column("status", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("targets", "status")
    # ### end Alembic commands ###