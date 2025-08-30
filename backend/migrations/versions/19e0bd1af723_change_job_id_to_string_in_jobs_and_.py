"""change job_id to string in jobs and child tables

Revision ID: 19e0bd1af723
Revises: 9993fe89127e
Create Date: 2025-08-26 17:03:57.182793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e0bd1af723'
down_revision: Union[str, None] = '9993fe89127e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Supprimer les FK existantes
    op.drop_constraint("fk_liked_jobs_job_id_jobs", "liked_jobs", type_="foreignkey")
    op.drop_constraint("fk_seen_jobs_job_id_jobs", "seen_jobs", type_="foreignkey")
    op.drop_constraint("fk_applied_jobs_job_id_jobs", "applied_jobs", type_="foreignkey")

    # 2. Convertir jobs.id en String
    with op.batch_alter_table("jobs") as batch_op:
        batch_op.alter_column("id",
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              nullable=False)

    # 3. Convertir job_id dans les tables enfants en String
    with op.batch_alter_table("liked_jobs") as batch_op:
        batch_op.alter_column("job_id",
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              nullable=True)
    with op.batch_alter_table("seen_jobs") as batch_op:
        batch_op.alter_column("job_id",
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              nullable=True)
    with op.batch_alter_table("applied_jobs") as batch_op:
        batch_op.alter_column("job_id",
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              nullable=True)

    # 4. Re-créer les FK
    op.create_foreign_key("fk_liked_jobs_job_id_jobs", "liked_jobs", "jobs", ["job_id"], ["id"])
    op.create_foreign_key("fk_seen_jobs_job_id_jobs", "seen_jobs", "jobs", ["job_id"], ["id"])
    op.create_foreign_key("fk_applied_jobs_job_id_jobs", "applied_jobs", "jobs", ["job_id"], ["id"])



def downgrade() -> None:
    # Supprimer les FK
    with op.batch_alter_table("liked_jobs") as batch_op:
        batch_op.drop_constraint("fk_liked_jobs_job_id_jobs", type_="foreignkey")
    with op.batch_alter_table("seen_jobs") as batch_op:
        batch_op.drop_constraint("fk_seen_jobs_job_id_jobs", type_="foreignkey")
    with op.batch_alter_table("applied_jobs") as batch_op:
        batch_op.drop_constraint("fk_applied_jobs_job_id_jobs", type_="foreignkey")

    # Revenir au type Integer
    with op.batch_alter_table("liked_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.Integer(), existing_type=sa.String(), nullable=True)
    with op.batch_alter_table("seen_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.Integer(), existing_type=sa.String(), nullable=True)
    with op.batch_alter_table("applied_jobs") as batch_op:
        batch_op.alter_column("job_id", type_=sa.Integer(), existing_type=sa.String(), nullable=True)

    # Re-créer les contraintes FK originales
    op.create_foreign_key("fk_liked_jobs_job_id_jobs", 'liked_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key("fk_seen_jobs_job_id_jobs", 'seen_jobs', 'jobs', ['job_id'], ['id'])
    op.create_foreign_key("fk_applied_jobs_job_id_jobs", 'applied_jobs', 'jobs', ['job_id'], ['id'])


