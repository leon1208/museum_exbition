"""增加展览信息表菜单

Revision ID: 5e64c48932c8
Revises: 7c2e504df7e5
Create Date: 2026-01-08 09:36:23.625673

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.mysql import insert
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e64c48932c8'
down_revision: Union[str, Sequence[str], None] = '7c2e504df7e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 使用SQLAlchemy Core的table对象
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 插入展览信息表子菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2037,
        menu_name='展览信息表',
        parent_id=2029,
        order_num=1,
        path='exhibition',
        component='exb_museum/exhibition/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:list',
        icon='education',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='展览信息表菜单'
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
    
    # 获取刚插入的菜单ID作为父ID
    # 由于MySQL中LAST_INSERT_ID()不能直接在SQLAlchemy中使用，我们手动指定ID
    
    # 插入展览信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2038,
        menu_name='展览信息表查询',
        parent_id=2037,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:query',
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
    
    # 插入展览信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2039,
        menu_name='展览信息表新增',
        parent_id=2037,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:add',
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
    
    # 插入展览信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2040,
        menu_name='展览信息表修改',
        parent_id=2037,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:edit',
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
    
    # 插入展览信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2041,
        menu_name='展览信息表删除',
        parent_id=2037,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:remove',
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
    
    # 插入展览信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2042,
        menu_name='展览信息表导出',
        parent_id=2037,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:export',
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
    
    # 插入展览信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2043,
        menu_name='展览信息表导入',
        parent_id=2037,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:exhibition:import',
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
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2038, 2039, 2040, 2041, 2042, 2043])))
    
    # 删除子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2037))