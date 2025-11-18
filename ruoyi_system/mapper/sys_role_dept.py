# -*- coding: utf-8 -*-
# @Author  : YY

from typing import List

from sqlalchemy import delete, func, insert, select
from ruoyi_admin.ext import db
from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_system.domain.entity import SysRoleDept
from ruoyi_system.domain.po import SysRoleDeptPo


class SysRoleDeptMapper:
    
    """
    部门与角色相关联的数据访问层
    """

    @classmethod
    @Transactional(db.session)
    def batch_role_dept(cls, role_dept_list: List[SysRoleDept]) -> int:
        """
        批量新增角色部门信息

        Args:
            role_dept_list (List[SysRoleDept]): 角色部门列表
        
        Returns:
            int: 操作影响的行数
        """
        role_dept_list = [
            row.model_dump(
                exclude_none=True,
                exclude_unset=True,
            ) for row in role_dept_list]
        stmt = insert(SysRoleDeptPo).values(role_dept_list)
        return db.session.execute(stmt).rowcount
    
    @classmethod
    @Transactional(db.session)
    def delete_role_dept_by_role_id(cls, role_id: int) -> int:
        """
        根据角色ID，删除角色和部门关联数据

        Args:
            role_id (int): 角色ID
        
        Returns:
            int: 操作影响的行数
        """
        stmt = delete(SysRoleDeptPo).where(SysRoleDeptPo.role_id == role_id)
        return db.session.execute(stmt).rowcount

    @classmethod
    @Transactional(db.session)
    def delete_role_dept(cls, role_ids: List[int]) -> int:
        """
        批量删除角色部门关联信息

        Args:
            role_ids (List[int]): 多个角色ID
        
        Returns:
            int: 操作影响的行数
        """
        stmt = delete(SysRoleDeptPo).where(SysRoleDeptPo.role_id.in_(role_ids))
        return db.session.execute(stmt).rowcount
        
    @classmethod
    def select_count_role_dept_by_dept_id(cls, dept_id: int) -> int:
        """
        查询部门使用的角色数量

        Args:
            dept_id (int): 部门ID
        
        Returns:
            int: 角色数量
        """
        stmt = select(func.count()).select_from(SysRoleDeptPo) \
            .where(SysRoleDeptPo.dept_id == dept_id)
        return db.session.execute(stmt).scalar_one_or_none() or 0

    @classmethod
    def select_dept_ids_by_role_id(cls, role_id: int) -> List[int]:
        """
        查询角色下的部门ID列表

        Args:
            role_id (int): 角色ID

        Returns:
            List[int]: 部门ID列表
        """
        stmt = select(SysRoleDeptPo.dept_id) \
            .where(SysRoleDeptPo.role_id == role_id)
        return db.session.execute(stmt).scalars().all()

