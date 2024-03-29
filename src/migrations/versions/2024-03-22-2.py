"""one more change in deposits table

Revision ID: 67b390707d34
Revises: 353b545593c6
Create Date: 2024-03-22 21:03:53.750740

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "67b390707d34"
down_revision: Union[str, None] = "353b545593c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
