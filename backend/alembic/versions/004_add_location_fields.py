"""Add location fields to pizzeria

Revision ID: 004
Revises: 003
Create Date: 2025-01-31

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("pizzeria", sa.Column("lat", sa.Float(), nullable=True))
    op.add_column("pizzeria", sa.Column("lng", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("pizzeria", "lng")
    op.drop_column("pizzeria", "lat")
