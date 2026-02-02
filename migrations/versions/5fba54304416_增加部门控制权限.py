"""增加部门控制权限

Revision ID: 5fba54304416
Revises: 227d75fbd92a
Create Date: 2026-02-02 09:27:25.868635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '5fba54304416'
down_revision: Union[str, Sequence[str], None] = '227d75fbd92a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 定义冲突处理策略：当主键冲突时更新记录
def create_upsert_statement(insert_stmt):
    """Create an upsert statement for the department table."""
    return insert_stmt.on_duplicate_key_update(
        parent_id=insert_stmt.inserted.parent_id,
        ancestors=insert_stmt.inserted.ancestors,
        dept_name=insert_stmt.inserted.dept_name,
        order_num=insert_stmt.inserted.order_num,
        leader=insert_stmt.inserted.leader,
        phone=insert_stmt.inserted.phone,
        email=insert_stmt.inserted.email,
        status=insert_stmt.inserted.status,
        del_flag=insert_stmt.inserted.del_flag,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time
    )

def upgrade() -> None:
    """Upsert department data."""
    # 导入SysDeptPo模型
    from ruoyi_system.domain.po import SysDeptPo
    dept_table = SysDeptPo.__table__
    
    # 创建upsert语句
    insert_stmt = insert(dept_table).values(
        dept_id=200,
        parent_id=0,
        ancestors='0',
        dept_name='展慧管理',
        order_num=1,
        leader='leeon',
        phone='18988888888',
        email='189@189.cn',
        status='0',
        del_flag='0',
        create_by='admin',
        create_time=datetime.strptime('2026-02-02 00:00:00', '%Y-%m-%d %H:%M:%S'),
        update_by='',
        update_time=None
    )
    # 创建upsert语句
    upsert_stmt = create_upsert_statement(insert_stmt)    
    # 执行upsert操作
    op.execute(upsert_stmt)

    
    insert_stmt = insert(dept_table).values(
        dept_id=201,
        parent_id=200,
        ancestors='0,200',
        dept_name='博物馆管理组',
        order_num=0,
        leader='leeon',
        phone='18988888888',
        email='189@189.cn',
        status='0',
        del_flag='0',
        create_by='admin',
        create_time=datetime.strptime('2026-02-02 00:00:00', '%Y-%m-%d %H:%M:%S'),
        update_by='',
        update_time=None
    )
    # 创建upsert语句
    upsert_stmt = create_upsert_statement(insert_stmt)    
    # 执行upsert操作
    op.execute(upsert_stmt)

    insert_stmt = insert(dept_table).values(
        dept_id=202,
        parent_id=201,
        ancestors='0,200,201',
        dept_name='在线演示博物馆',
        order_num=0,
        leader='leeon',
        phone='18988888888',
        email='189@189.cn',
        status='0',
        del_flag='0',
        create_by='admin',
        create_time=datetime.strptime('2026-02-02 00:00:00', '%Y-%m-%d %H:%M:%S'),
        update_by='',
        update_time=None
    )
    # 创建upsert语句
    upsert_stmt = create_upsert_statement(insert_stmt)    
    # 执行upsert操作
    op.execute(upsert_stmt)

    insert_stmt = insert(dept_table).values(
        dept_id=203,
        parent_id=201,
        ancestors='0,200,201',
        dept_name='浦东历史博物馆',
        order_num=1,
        leader='leeon',
        phone='18988888888',
        email='189@189.cn',
        status='0',
        del_flag='0',
        create_by='admin',
        create_time=datetime.strptime('2026-02-02 00:00:00', '%Y-%m-%d %H:%M:%S'),
        update_by='',
        update_time=None
    )
    # 创建upsert语句
    upsert_stmt = create_upsert_statement(insert_stmt)    
    # 执行upsert操作
    op.execute(upsert_stmt)    

def downgrade() -> None:
    """Remove department data with dept_id=200."""
    from ruoyi_system.domain.po import SysDeptPo
    dept_table = SysDeptPo.__table__
    
    # 删除指定的部门记录
    delete_stmt = dept_table.delete().where(dept_table.c.dept_id.in_([200, 201, 202, 203]))
    op.execute(delete_stmt)