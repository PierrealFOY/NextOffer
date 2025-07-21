"""Merge reset_password into baseline

Revision ID: 9b5ba979ba5e
Revises: 74ae8350aa5f, e13925fd0572
Create Date: 2025-07-16 11:19:14.239492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b5ba979ba5e'
down_revision: Union[str, None] = ('74ae8350aa5f', 'e13925fd0572')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
