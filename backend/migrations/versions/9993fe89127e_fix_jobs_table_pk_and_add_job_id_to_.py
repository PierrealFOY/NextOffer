"""Fix jobs table PK and add job_id to child tables

Revision ID: 9993fe89127e
Revises: 3de30c133d32
Create Date: 2025-08-26 16:54:57.580155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9993fe89127e'
down_revision: Union[str, None] = '3de30c133d32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
