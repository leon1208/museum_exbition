"""增加小程序app_id

Revision ID: 773850cad82d
Revises: fe298ac25d08
Create Date: 2026-01-06 10:57:32.234517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '773850cad82d'
down_revision: Union[str, Sequence[str], None] = 'fe298ac25d08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 为exb_museum表添加app_id字段
    op.add_column('exb_museum', sa.Column('app_id', mysql.VARCHAR(length=50), nullable=True, comment='小程序AppID'))
    

def downgrade() -> None:
    """Downgrade schema."""
    # 删除exb_museum表的app_id字段
    op.drop_column('exb_museum', 'app_id')