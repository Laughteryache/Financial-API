"""Changed deposits table

Revision ID: 353b545593c6
Revises: 719fa5942c2b
Create Date: 2024-03-22 19:40:05.584290

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "353b545593c6"
down_revision: Union[str, None] = "719fa5942c2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
