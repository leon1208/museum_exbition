"""增加藏品信息表菜单

Revision ID: 057f04c42df5
Revises: 5e64c48932c8
Create Date: 2026-01-08 11:34:03.254779

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.mysql import insert
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '057f04c42df5'
down_revision: Union[str, Sequence[str], None] = '5e64c48932c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 使用SQLAlchemy Core的table对象
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 插入藏品信息表子菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2044,
        menu_name='藏品信息表',
        parent_id=2029,
        order_num=3,
        path='collection',
        component='exb_museum/collection/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='exb_museum:collection:list',
        icon='icon',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='藏品信息表菜单'
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
    
    # 插入藏品信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2045,
        menu_name='藏品信息表查询',
        parent_id=2044,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:query',
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
    
    # 插入藏品信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2046,
        menu_name='藏品信息表新增',
        parent_id=2044,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:add',
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
    
    # 插入藏品信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2047,
        menu_name='藏品信息表修改',
        parent_id=2044,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:edit',
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
    
    # 插入藏品信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2048,
        menu_name='藏品信息表删除',
        parent_id=2044,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:remove',
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
    
    # 插入藏品信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2049,
        menu_name='藏品信息表导出',
        parent_id=2044,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:export',
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
    
    # 插入藏品信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2050,
        menu_name='藏品信息表导入',
        parent_id=2044,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:collection:import',
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
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2045, 2046, 2047, 2048, 2049, 2050])))
    
    # 删除子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2044))