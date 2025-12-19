"""加入菜单

Revision ID: 94950978f132
Revises: d1a929936dac
Create Date: 2025-12-19 09:13:43.332591

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.mysql import insert


# revision identifiers, used by Alembic.
revision: str = '94950978f132'
down_revision: Union[str, Sequence[str], None] = 'd1a929936dac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 使用SQLAlchemy Core的table对象
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 插入AI实验主菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2025,
        menu_name='AI实验',
        parent_id=0,
        order_num=4,
        path='aicrawl',
        component=None,
        query=None,
        is_frame=1,
        is_cache=0,
        menu_type='M',
        visible='0',
        status='0',
        perms=None,
        icon='code',
        create_by='admin',
        create_time='2025-12-11 13:23:16',
        update_by='',
        update_time=None,
        remark=''
    )
    
    # 使用MySQL的on_duplicate_key_update实现upsert
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        query=insert_stmt.inserted.query,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入截屏实验子菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2026,
        menu_name='截屏实验',
        parent_id=2025,
        order_num=0,
        path='screenshot',
        component='aicrawl/screenshot/index',
        query=None,
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='aicrawl:screenshot',
        icon='dict',
        create_by='admin',
        create_time='2025-12-11 13:24:41',
        update_by='admin',
        update_time='2025-12-11 13:31:21',
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        query=insert_stmt.inserted.query,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入转MD实验子菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2027,
        menu_name='转MD实验',
        parent_id=2025,
        order_num=1,
        path='web2md',
        component='aicrawl/web2md/index',
        query=None,
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='aicrawl:web2md',
        icon='druid',
        create_by='admin',
        create_time='2025-12-19 08:44:13',
        update_by='admin',
        update_time='2025-12-19 08:44:51',
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        query=insert_stmt.inserted.query,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)


def downgrade() -> None:
    """Downgrade schema."""
    # 使用SQLAlchemy ORM删除插入的菜单数据
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 删除子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2026, 2027])))
    
    # 删除主菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2025))