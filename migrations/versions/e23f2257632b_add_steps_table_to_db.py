import sqlmodel

"""Add steps table to db

Revision ID: e23f2257632b
Revises: c714a5949cd3
Create Date: 2024-11-04 02:02:23.555306

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e23f2257632b"
down_revision: Union[str, None] = "c714a5949cd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notebookstep",
        sa.Column("step_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("notebook_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("modified_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["notebook_id"],
            ["notebook.id"],
        ),
        sa.PrimaryKeyConstraint("step_id"),
    )
    op.create_index(
        op.f("ix_notebookstep_step_id"), "notebookstep", ["step_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notebookstep_step_id"), table_name="notebookstep")
    op.drop_table("notebookstep")
    # ### end Alembic commands ###
