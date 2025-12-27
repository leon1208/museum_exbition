"""新增博物馆菜单

Revision ID: fe298ac25d08
Revises: 28c4bdcbbcaa
Create Date: 2025-12-27 15:10:23.364531

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.mysql import insert
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe298ac25d08'
down_revision: Union[str, Sequence[str], None] = '28c4bdcbbcaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 使用SQLAlchemy Core的table对象
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 插入场馆管理主菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2029,
        menu_name='场馆管理',
        parent_id=0,
        order_num=10,
        path='exb_museum',
        is_frame=1,
        is_cache=0,
        menu_type='M',
        visible='0',
        status='0',
        icon='tab',
        create_by='admin',
        create_time='2025-12-23 09:22:40',
        update_by='admin',
        update_time='2025-12-23 09:24:03',
        remark=''
    )
    
    # 使用MySQL的on_duplicate_key_update实现upsert
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表子菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2030,
        menu_name='博物馆信息表',
        parent_id=2029,
        order_num=1,
        path='museum',
        component='exb_museum/museum/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='exb_museum:museum:list',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='博物馆信息表菜单'
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2031,
        menu_name='博物馆信息表查询',
        parent_id=2030,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:query',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2032,
        menu_name='博物馆信息表新增',
        parent_id=2030,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:add',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2033,
        menu_name='博物馆信息表修改',
        parent_id=2030,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:edit',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2034,
        menu_name='博物馆信息表删除',
        parent_id=2030,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:remove',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2035,
        menu_name='博物馆信息表导出',
        parent_id=2030,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:export',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
        update_by=insert_stmt.inserted.update_by,
        update_time=insert_stmt.inserted.update_time,
        remark=insert_stmt.inserted.remark
    )
    
    op.execute(upsert_stmt)
    
    # 插入博物馆信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2036,
        menu_name='博物馆信息表导入',
        parent_id=2030,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:museum:import',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        menu_name=insert_stmt.inserted.menu_name,
        parent_id=insert_stmt.inserted.parent_id,
        order_num=insert_stmt.inserted.order_num,
        path=insert_stmt.inserted.path,
        component=insert_stmt.inserted.component,
        is_frame=insert_stmt.inserted.is_frame,
        is_cache=insert_stmt.inserted.is_cache,
        menu_type=insert_stmt.inserted.menu_type,
        visible=insert_stmt.inserted.visible,
        status=insert_stmt.inserted.status,
        perms=insert_stmt.inserted.perms,
        icon=insert_stmt.inserted.icon,
        create_by=insert_stmt.inserted.create_by,
        create_time=insert_stmt.inserted.create_time,
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
    
    # 删除按钮菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2031, 2032, 2033, 2034, 2035, 2036])))
    
    # 删除子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2030))
    
    # 删除主菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2029))