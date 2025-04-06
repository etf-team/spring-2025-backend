"""Initial

Revision ID: fb0d9328f639
Revises: 
Create Date: 2025-04-06 08:09:13.231419

"""
from typing import Sequence, Union

import fastapi_storages.integrations.sqlalchemy
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fb0d9328f639'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_config',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('power_price', sa.Numeric(), nullable=False),
    sa.Column('power_price_net', sa.Numeric(), nullable=False),
    sa.Column('comes_into_force_from', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category_price_info_file',
    sa.Column('file', fastapi_storages.integrations.sqlalchemy.FileType(storage=None), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comes_into_force_from', sa.Date(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('power_hours_ats_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('hour', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('power_hours_net',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('include_hours', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('comes_info_force_from', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('power_hours_net')
    op.drop_table('power_hours_ats_record')
    op.drop_table('category_price_info_file')
    op.drop_table('application_config')
    # ### end Alembic commands ###
