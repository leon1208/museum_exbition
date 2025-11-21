# -*- coding: utf-8 -*-
# @Author  : YY

from typing import List, Literal, Optional

from ruoyi_common.constant import UserConstants
from ruoyi_common.domain.entity import SysRole
from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_common.exception import ServiceException
from ruoyi_common.utils import security_util as SecurityUtil
from ruoyi_system.domain.entity import SysRoleDept, SysRoleMenu, SysUserRole
from ruoyi_system.mapper import SysRoleDeptMapper,SysRoleMenuMapper, \
                                SysUserRoleMapper,SysRoleMapper
from ruoyi_system.service.sys_dept import SysDeptService
from ruoyi_framework.descriptor.datascope import DataScope
from ruoyi_admin.ext import db


class SysRoleService:
    
    @classmethod
    @DataScope(dept=True)
    def select_role_list(cls, query:SysRole) -> List[SysRole]:
        """
        根据条件，查询角色数据

        Args:
            query (SysRole): 包含查询条件的传输对象

        Returns:
            List[SysRole]: 角色列表

        """
        return SysRoleMapper.select_role_list(query)

    @classmethod
    def select_role_all(cls) -> List[SysRole]:
        """
        查询所有角色数据

        Args:
            query (SysRole): 包含查询条件的传输对象

        Returns:
            List[SysRole]: 角色列表

        """
        return SysRoleMapper.select_role_all()
    
    @classmethod
    def select_roles_by_user_id(cls, user_id:int) -> List[SysRole]:
        """
        根据用户ID查询角色列表

        Args:
            user_id(int): 用户ID

        Returns:
            List[SysRole]: 角色列表
        """
        eos: List[SysRole] = SysRoleMapper.select_role_permission_by_user_id(user_id)
        scoped_roles: List[SysRole] = cls.select_role_list(None)
        for role in scoped_roles:
            if role.role_id in [eo.role_id for eo in eos]:
                role.flag = True
        return scoped_roles

    @classmethod
    def select_role_permission_by_user_id(cls, user_id:int) -> List[str]:
        """
        根据用户ID，查询角色权限

        Args:
            user_id(int): 用户ID

        Returns:
            List[str]: 角色权限列表
        """
        eos = SysRoleMapper.select_role_permission_by_user_id(user_id)
        permset = set()
        for eo in eos:
            permset = permset | set(eo.role_key.strip().split(","))
        return list(permset)

    @classmethod
    def select_role_list_by_user_id(cls, user_id:int) -> List[SysRole]:
        """
        根据用户ID，查询角色选择框列表

        Args:
            user_id(int): 用户ID

        Returns:
            List[SysRole]: 角色选择框列表
        """
        user_eos:List[SysRole] = SysRoleMapper. \
            select_role_permission_by_user_id(user_id)
        eos:List[SysRole] = cls.select_role_list(SysRole())
        for eo in eos:
            for user_eo in user_eos:
                if eo.role_id == user_eo.role_id:
                    eo.flag = True
                    break
        return eos

    @classmethod
    def select_role_by_id(cls, role_id:int) -> Optional[SysRole]:
        """
        根据角色ID，查询角色

        Args:
            role_id(int): 角色ID

        Returns:
            SysRole: 角色信息
        """
        role = SysRoleMapper.select_role_by_id(role_id)
        if role:
            role.menu_ids = SysRoleMenuMapper.select_menu_ids_by_role_id(role_id)
            role.dept_ids = list(SysDeptService.select_dept_list_by_role_id(role_id)) \
                if role.data_scope == "2" else []
        return role
    
    @classmethod
    def check_role_name_unique(cls, role: SysRole) -> Literal['0', '1']:
        """
        校验角色名称是否唯一
        
        Args:
            role(SysRole): 角色信息

        Returns:
            Literal['0', '1'] : 唯一性校验结果, 0:唯一, 1:不唯一
        """
        eo:SysRole = SysRoleMapper.check_role_name_unique(role.role_name)
        if eo and eo.role_id != role.role_id:
            return UserConstants.NOT_UNIQUE
        return UserConstants.UNIQUE

    @classmethod
    def check_role_key_unique(cls, role: SysRole) -> Literal['0', '1']:
        """校验角色权限是否唯一
        
        Args:
            role(SysRole): 角色信息

        Returns:
            Literal['0', '1'] : 唯一性校验结果, 0:唯一, 1:不唯一
        """
        eo: SysRole = SysRoleMapper.check_role_key_unique(role.role_key)
        if eo and eo.role_id != role.role_id:
            return UserConstants.NOT_UNIQUE
        return UserConstants.UNIQUE

    @classmethod
    def check_role_allowed(cls, role: SysRole):
        """
        校验角色是否允许操作
        
        Args:
            role(SysRole): 角色信息

        Raises:
            ServiceException: 超级管理员角色不允许操作
        """
        if role and role.role_id and role.is_admin():
            raise ServiceException("不允许操作超级管理员角色")
    
    @classmethod    
    def check_role_data_scope(cls, role_id: int):
        """
        校验角色是否有数据权限
        
        Args:
            role_id(int): 角色ID

        Raises:
            ServiceException: 超级管理员角色不允许操作
        """
        if not SecurityUtil.is_admin(SecurityUtil.get_user_id()):
            role = SysRole(role_id=role_id)
            roles: List[SysRole] = cls.select_role_list(role)
            if not roles:
                raise ServiceException("没有权限访问角色数据")

    @classmethod
    def count_user_role_by_role_id(cls, role_id:int) -> int:
        """
        通过角色ID查询角色使用数量

        Args:
            role_id(int): 角色ID

        Returns:
            int: 角色使用数量
        """
        return SysRoleMapper.count_user_role_by_role_id(role_id)

    @classmethod
    @Transactional(db.session)
    def insert_role(cls, role:SysRole) -> int:
        """
        新增角色信息
        
        Args:
            role(SysRole): 角色信息

        Returns:
            int: 新增角色ID
        """
        last_id = SysRoleMapper.insert_role(role)
        role.role_id = last_id
        return cls.insert_role_menu(role)

    @classmethod
    @Transactional(db.session)
    def update_role(cls, role:SysRole) -> bool:
        """
        修改保存角色信息

        Args:
            role(SysRole): 角色信息
        
        Returns:
            bool: 修改结果
        """
        SysRoleMapper.update_role(role)
        SysRoleMenuMapper.delete_role_menu_by_role_id(role.role_id)
        return cls.insert_role_menu(role) > 0

    @classmethod
    @Transactional(db.session)
    def update_role_status(cls, role:SysRole) -> bool:
        """
        修改角色状态

        Args:
            role(SysRole): 角色信息
        
        Returns:
            bool: 修改结果
        """
        return SysRoleMapper.update_role(role) > 0

    @classmethod
    @Transactional(db.session)
    def auth_data_scope(cls, role:SysRole) -> bool:
        """
        修改数据权限信息

        Args:
            role(SysRole): 角色信息
        
        Returns:
            bool: 修改结果（True 表示成功）
        """
        # 1. 先更新角色本身的数据范围等信息
        SysRoleMapper.update_role(role)
        # 2. 清理原有角色-部门关联
        SysRoleDeptMapper.delete_role_dept_by_role_id(role.role_id)
        # 3. 只有“自定义数据权限”(通常为 '2') 时才维护角色-部门表
        # 其他类型的数据范围（全部、本部门、本部门及以下、仅本人）都不需要 sys_role_dept 记录
        if role.data_scope == "2" and role.dept_ids:
            num = cls.insert_role_dept(role)
            return num > 0
        # 非自定义范围，即使没有部门记录也视为成功
        return True
    
    @classmethod
    @Transactional(db.session)
    def insert_role_menu(cls, role: SysRole) -> int:
        """
        新增角色菜单信息

        Args:
            role(SysRole): 角色信息

        Returns:
            int: 新增角色菜单数量
        """
        menus = []
        for menu_id in role.menu_ids:
            menu = SysRoleMenu(role_id=role.role_id, menu_id=menu_id)
            menus.append(menu)
        if len(menus) > 0:
            SysRoleMenuMapper.batch_role_menu(menus)
        return len(menus)
    
    @classmethod
    @Transactional(db.session)
    def insert_role_dept(cls, role: SysRole):
        """
        新增角色部门信息

        Args:
            role(SysRole): 角色信息

        Returns:
            int: 新增角色部门数量
        """
        depts = []
        for dept_id in role.dept_ids:
            dept = SysRoleDept(role_id=role.role_id, dept_id=dept_id)
            depts.append(dept)
        if len(depts) > 0:
            SysRoleDeptMapper.batch_role_dept(depts)
        return len(depts)
        
    @classmethod
    @Transactional(db.session)
    def delete_role_by_id(cls, role_id:int) -> bool:
        """
        通过角色ID删除角色

        Args:
            role_id(int): 角色ID

        Returns:
            bool: 删除结果
        """
        SysRoleMenuMapper.delete_role_menu_by_role_id(role_id)
        SysRoleDeptMapper.delete_role_dept_by_role_id(role_id)
        return SysRoleMapper.delete_role_by_id(role_id)  > 0

    @classmethod
    @Transactional(db.session)
    def delete_role_by_ids(cls, role_ids:List[int]) -> bool:
        """
        批量删除角色信息

        Args:
            role_ids(List[int]): 角色ID列表

        Returns:
            bool: 删除结果
        """
        for role_id in role_ids:
            cls.check_role_allowed(SysRole(role_id=role_id))
            # cls.check_role_data_scope(role_id) # todo
            role: SysRole = cls.select_role_by_id(role_id)
            if cls.count_user_role_by_role_id(role_id) > 0:
                raise ServiceException("角色{}已分配用户，不能删除".format(role.role_name))
        SysRoleMenuMapper.delete_role_menu(role_ids)
        SysRoleDeptMapper.delete_role_dept(role_ids)
        return SysRoleMapper.delete_role_by_ids(role_ids) > 0

    @classmethod
    @Transactional(db.session)
    def delete_auth_user(cls, user_role:SysUserRole) -> bool:
        """
        取消授权用户角色

        Args:
            user_role(SysUserRole): 用户角色信息

        Returns:
            bool: 取消授权结果
        """
        return SysUserRoleMapper.delete_user_role_info(user_role) > 0

    @classmethod
    @Transactional(db.session)
    def delete_auth_users(cls, role_id, user_ids) -> bool:
        """
        批量取消授权用户角色

        Args:
            role_id(int): 角色ID
            user_ids(List[int]): 用户ID列表

        Returns:
            bool: 取消授权结果
        """
        return SysUserRoleMapper.delete_user_role_infos(role_id, user_ids) > 0

    @classmethod
    @Transactional(db.session)
    def insert_auth_users(cls, role_id, user_ids) -> bool:
        """
        批量选择授权用户角色

        Args:
            role_id(int): 角色ID
            user_ids(List[int]): 用户ID列表

        Returns:
            bool: 选择授权结果
        """
        user_roles = [SysUserRole(user_id=user_id, role_id=role_id) \
            for user_id in user_ids]
        num = SysUserRoleMapper.batch_user_role(user_roles)
        return num > 0
    

