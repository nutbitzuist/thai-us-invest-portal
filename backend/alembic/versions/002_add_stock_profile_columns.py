"""Add stock profile columns

Revision ID: 002_add_stock_profile
Revises: 001_initial
Create Date: 2026-01-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_stock_profile'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to stocks table
    op.add_column('stocks', sa.Column('ceo', sa.String(255)))
    op.add_column('stocks', sa.Column('employees', sa.Integer()))
    op.add_column('stocks', sa.Column('headquarters', sa.String(255)))
    op.add_column('stocks', sa.Column('founded_year', sa.Integer()))
    op.add_column('stocks', sa.Column('analysis_data', sa.Text()))


def downgrade() -> None:
    op.drop_column('stocks', 'ceo')
    op.drop_column('stocks', 'employees')
    op.drop_column('stocks', 'headquarters')
    op.drop_column('stocks', 'founded_year')
    op.drop_column('stocks', 'analysis_data')
