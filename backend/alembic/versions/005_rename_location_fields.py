"""Rename latitude/longitude to lat/lng

Revision ID: 005
Revises: 004
Create Date: 2025-01-31

"""

from typing import Sequence, Union

from alembic import op

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("pizzeria", "latitude", new_column_name="lat")
    op.alter_column("pizzeria", "longitude", new_column_name="lng")


def downgrade() -> None:
    op.alter_column("pizzeria", "lat", new_column_name="latitude")
    op.alter_column("pizzeria", "lng", new_column_name="longitude")
