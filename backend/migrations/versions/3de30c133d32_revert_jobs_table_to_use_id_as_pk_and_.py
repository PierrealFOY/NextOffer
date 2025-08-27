"""Revert jobs table to use id as PK and remove external_id

Revision ID: 3de30c133d32
Revises: 28e35235201f
Create Date: 2025-08-26 16:36:13.552877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3de30c133d32'
down_revision: Union[str, None] = '28e35235201f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Supprimer les contraintes FK existantes si elles existent
    with op.batch_alter_table("liked_jobs") as batch_op:
        try:
            batch_op.drop_constraint("fk_liked_jobs_job_uuid_jobs", type_="foreignkey")
        except Exception:
            pass
    with op.batch_alter_table("seen_jobs") as batch_op:
        try:
            batch_op.drop_constraint("fk_seen_jobs_job_uuid_jobs", type_="foreignkey")
        except Exception:
            pass
    with op.batch_alter_table("applied_jobs") as batch_op:
        try:
            batch_op.drop_constraint("fk_applied_jobs_job_uuid_jobs", type_="foreignkey")
        except Exception:
            pass

    # 2. Supprimer external_id dans jobs si elle existe
    with op.batch_alter_table("jobs") as batch_op:
        try:
            batch_op.drop_column("external_id")
        except Exception:
            pass

    # 3. S'assurer que job_id est string dans les tables enfants
    with op.batch_alter_table("liked_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.String(), existing_type=sa.Integer(), nullable=True)
    with op.batch_alter_table("seen_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.String(), existing_type=sa.Integer(), nullable=True)
    with op.batch_alter_table("applied_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.String(), existing_type=sa.Integer(), nullable=True)

    # 4. Créer de nouvelles contraintes FK
    op.create_foreign_key(None, 'liked_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key(None, 'seen_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key(None, 'applied_jobs', 'jobs', ['job_id'], ['id'])
