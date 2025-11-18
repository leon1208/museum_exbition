# -*- coding: utf-8 -*-
# @Author  : YY

from typing import List
from sqlalchemy import delete, func, insert, select

from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_system.domain.entity import SysRoleMenu
from ruoyi_admin.ext import db
from ruoyi_system.domain.po import SysRoleMenuPo


class SysRoleMenuMapper:
    
    """
    角色与菜单相关联的数据访问层
    """
    
    @classmethod
    def select_menu_ids_by_role_id(cls, role_id: int) -> List[int]:
        """
        查询角色下的菜单ID列表

        Args:
            role_id: 角色ID

        Returns:
            菜单ID列表
        """
        stmt = select(SysRoleMenuPo.menu_id) \
            .where(SysRoleMenuPo.role_id == role_id)
        return db.session.execute(stmt).scalars().all()
    
    @classmethod
    def check_menu_exist_role(cls, menu_id: int) -> int:
        """
        查询菜单下的菜单数量
        
        Args:
            menu_id: 菜单ID
        
        Returns:
            角色数量
        """
        stmt = select(func.count()).select_from(SysRoleMenuPo) \
            .where(SysRoleMenuPo.menu_id == menu_id)
        return db.session.execute(stmt).scalar() or 0

    @classmethod
    @Transactional(db.session)
    def delete_role_menu_by_role_id(cls, role_id: int) -> int:
        """
        删除角色下的关联菜单
        
        Args:
            role_id: 角色ID
        
        Returns:
            删除的行数
        """
        stmt = delete(SysRoleMenuPo) \
            .where(SysRoleMenuPo.role_id == role_id)
        return db.session.execute(stmt).rowcount

    @classmethod
    @Transactional(db.session)
    def delete_role_menu(cls, ids: List[int]) -> int:
        """
        批量删除角色下的关联菜单
        
        Args:
            ids: 角色ID列表
        
        Returns:
            删除的行数
        """
        stmt = delete(SysRoleMenuPo) \
            .where(SysRoleMenuPo.role_id.in_(ids))
        return db.session.execute(stmt).rowcount

    @classmethod
    @Transactional(db.session)
    def batch_role_menu(cls, role_menu_list: List[SysRoleMenu]) -> int:
        """
        批量新增角色菜单信息
        
        Args:
            role_menu_list: 角色菜单列表
        
        Returns:
            新增的行数
        """
        role_menu_list = [
            row.model_dump(
                exclude_none=True,
                exclude_unset=True    
            ) for row in role_menu_list]
        stmt = insert(SysRoleMenuPo).values(role_menu_list)
        return db.session.execute(stmt).rowcount
