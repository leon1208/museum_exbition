"""增加展厅对象和多媒体对象的菜单权限

Revision ID: fe73c6994479
Revises: aa09f01c20aa
Create Date: 2026-02-03 10:02:00.582602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert



# revision identifiers, used by Alembic.
revision: str = 'fe73c6994479'
down_revision: Union[str, Sequence[str], None] = 'aa09f01c20aa'
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
    
    # 首先查找博物馆模块的父菜单ID (通常是2029)
    # 插入展厅信息表菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2060,
        menu_name='展厅信息表',
        parent_id=2029,  # 假设博物馆模块的父菜单ID是2029
        order_num=5,
        path='hall',
        component='exb_museum/hall/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='1',
        status='0',
        perms='exb_museum:hall:list',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='展厅信息表菜单'
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展厅信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2061,
        menu_name='展厅信息表查询',
        parent_id=2060,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:query',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展厅信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2062,
        menu_name='展厅信息表新增',
        parent_id=2060,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:add',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展厅信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2063,
        menu_name='展厅信息表修改',
        parent_id=2060,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:edit',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入展厅信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2064,
        menu_name='展厅信息表删除',
        parent_id=2060,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:remove',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )

    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
        
    # 插入展厅信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2065,
        menu_name='展厅信息表导出',
        parent_id=2060,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:export',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)

    # 插入展厅信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2066,
        menu_name='展厅信息表导入',
        parent_id=2060,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:hall:import',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )

    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表菜单（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2067,
        menu_name='多媒体信息表',
        parent_id=2029,  # 假设博物馆模块的父菜单ID是2029
        order_num=6,
        path='media',
        component='exb_museum/media/index',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='1',
        status='0',
        perms='exb_museum:media:list',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark='多媒体信息表菜单'
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表查询按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2068,
        menu_name='多媒体信息表查询',
        parent_id=2067,
        order_num=1,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:query',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表新增按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2069,
        menu_name='多媒体信息表新增',
        parent_id=2067,
        order_num=2,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:add',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表修改按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2070,
        menu_name='多媒体信息表修改',
        parent_id=2067,
        order_num=3,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:edit',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表删除按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2071,
        menu_name='多媒体信息表删除',
        parent_id=2067,
        order_num=4,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:remove',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )

    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)
    
    # 插入多媒体信息表导出按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2072,
        menu_name='多媒体信息表导出',
        parent_id=2067,
        order_num=5,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:export',
        icon='#',
        create_by='admin',
        create_time=sa.func.sysdate(),
        update_by='',
        update_time=None,
        remark=''
    )
    
    upsert_stmt = upsert(insert_stmt)
    op.execute(upsert_stmt)

    # 插入多媒体信息表导入按钮（Upsert操作）
    insert_stmt = insert(menu_table).values(
        menu_id=2073,
        menu_name='多媒体信息表导入',
        parent_id=2067,
        order_num=6,
        path='#',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='exb_museum:media:import',
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

    # 删除多媒体按钮菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2068, 2069, 2070, 2071, 2072, 2073])))
    
    # 删除多媒体子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2067))
    
    # 删除展厅按钮菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id.in_([2061, 2062, 2063, 2064, 2065, 2066])))
    
    # 删除展厅子菜单
    op.execute(menu_table.delete().where(menu_table.c.menu_id == 2060))
