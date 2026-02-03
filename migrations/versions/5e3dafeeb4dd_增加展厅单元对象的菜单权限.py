"""增加展厅单元对象的菜单权限

Revision ID: 5e3dafeeb4dd
Revises: fe73c6994479
Create Date: 2026-02-03 12:44:22.477146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert


# revision identifiers, used by Alembic.
revision: str = '5e3dafeeb4dd'
down_revision: Union[str, Sequence[str], None] = 'fe73c6994479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upsert(insert_stmt):
    return insert_stmt.on_duplicate_key_update(
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

def upgrade() -> None:
    """Upgrade schema."""
    # 使用SQLAlchemy Core的table对象
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__
    
    # 插入展览单元信息表菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2074,
        menu_name='展览单元信息表',
        parent_id=2029,  # 假设博物馆模块的父菜单ID是2029
        order_num=7,
        path='unit',
        component='exb_museum/unit/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='1',
        status='0',
        perms='exb_museum:unit:list',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='展览单元信息表菜单'
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展览单元信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2075,
        menu_name='展览单元信息表查询',
        parent_id=2074,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:query',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展览单元信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2076,
        menu_name='展览单元信息表新增',
        parent_id=2074,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:add',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展览单元信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2077,
        menu_name='展览单元信息表修改',
        parent_id=2074,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:edit',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展览单元信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2078,
        menu_name='展览单元信息表删除',
        parent_id=2074,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:remove',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )

    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展览单元信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2079,
        menu_name='展览单元信息表导出',
        parent_id=2074,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:export',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)

    # 插入展览单元信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2080,
        menu_name='展览单元信息表导入',
        parent_id=2074,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:unit:import',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )

    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)

def downgrade() -> None:
    """Downgrade schema."""
    # 使用SQLAlchemy ORM删除插入的菜单数据
    from ruoyi_system.domain.po import SysMenuPo
    menu_table = SysMenuPo.__table__

    # 删除展览单元按钮菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2075, 2076, 2077, 2078, 2079, 2080])))
    
    # 删除展览单元子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2074))