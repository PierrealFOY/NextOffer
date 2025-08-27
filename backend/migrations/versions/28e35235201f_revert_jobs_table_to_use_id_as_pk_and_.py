"""Revert jobs table to use id as PK and remove external_id

Revision ID: 28e35235201f
Revises: 9b5ba979ba5e
Create Date: 2025-08-26 16:30:34.093386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28e35235201f'
down_revision: Union[str, None] = '9b5ba979ba5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # jobs table
    op.add_column('jobs', sa.Column('id', sa.Integer(), primary_key=True))
    op.drop_column('jobs', 'external_id')

    # tables enfants
    op.add_column('liked_jobs', sa.Column('job_id', sa.Integer(), nullable=True))
    op.add_column('seen_jobs', sa.Column('job_id', sa.Integer(), nullable=True))
    op.add_column('applied_jobs', sa.Column('job_id', sa.Integer(), nullable=True))

    # clés étrangères
    op.create_foreign_key(None, 'liked_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key(None, 'seen_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key(None, 'applied_jobs', 'jobs', ['job_id'], ['id'])

def downgrade() -> None:
    op.drop_constraint(None, 'liked_jobs', type_='foreignkey')
    op.drop_constraint(None, 'seen_jobs', type_='foreignkey')
    op.drop_constraint(None, 'applied_jobs', type_='foreignkey')
    
    op.drop_column('liked_jobs', 'job_id')
    op.drop_column('seen_jobs', 'job_id')
    op.drop_column('applied_jobs', 'job_id')

    op.add_column('jobs', sa.Column('external_id', sa.String(), nullable=True))
    op.drop_column('jobs', 'id')
