# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_mapper.py
# @Time    : 2025-12-23 09:24:49

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_system.domain.po import SysDeptPo
from exb_museum.domain.entity import Museum
from exb_museum.domain.po import MuseumPo

class MuseumMapper:
    """博物馆信息表Mapper"""

    @staticmethod
    def select_museum_list(museum: Museum) -> List[Museum]:
        """
        查询博物馆信息表列表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            List[museum]: 博物馆信息表列表
        """
        # 构建查询条件
        stmt = select(MuseumPo).join(SysDeptPo, MuseumPo.dept_id == SysDeptPo.dept_id)
        if museum.museum_name:
            stmt = stmt.where(MuseumPo.museum_name.like("%" + str(museum.museum_name) + "%"))
        if museum.address:
            stmt = stmt.where(MuseumPo.address.like("%" + str(museum.address) + "%"))
        if museum.status is not None:
            stmt = stmt.where(MuseumPo.status == museum.status)
        if museum.app_id:
            stmt = stmt.where(MuseumPo.app_id == museum.app_id)

        if "criterian_meta" in g and g.criterian_meta.scope is not None:
            stmt = stmt.where(g.criterian_meta.scope)
        
        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt

        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        result = db.session.execute(stmt).scalars().all()
        return [Museum.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_museum_by_id(museum_id: int) -> Museum:
        """
        根据ID查询博物馆信息表

        Args:
            museum_id (int): 博物馆ID

        Returns:
            museum: 博物馆信息表对象
        """
        result = db.session.get(MuseumPo, museum_id)
        return Museum.model_validate(result) if result else None


    @staticmethod
    def select_museum_by_app_id(app_id: str) -> Museum:
        """
        根据小程序AppID查询博物馆信息表

        Args:
            app_id (str): 小程序AppID

        Returns:
            Museum: 博物馆信息表对象
        """
        result = db.session.execute(
            select(MuseumPo).where(MuseumPo.app_id == app_id)
        ).scalar_one_or_none()
        return Museum.model_validate(result) if result else None


    @staticmethod
    def insert_museum(museum: Museum) -> int:
        """
        新增博物馆信息表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = MuseumPo()
        new_po.museum_id = museum.museum_id
        new_po.museum_name = museum.museum_name
        new_po.address = museum.address
        new_po.description = museum.description
        new_po.status = museum.status
        new_po.del_flag = museum.del_flag or 0
        new_po.create_by = museum.create_by
        new_po.create_time = museum.create_time or now
        new_po.update_by = museum.update_by
        new_po.update_time = museum.update_time or now
        new_po.remark = museum.remark
        new_po.app_id = museum.app_id
        new_po.dept_id = museum.dept_id
        db.session.add(new_po)

        db.session.flush()
        museum.museum_id = new_po.museum_id
        return 1

    
    @staticmethod
    def update_museum(museum: Museum) -> int:
        """
        修改博物馆信息表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            int: 更新的记录数
        """
        
        existing = db.session.get(MuseumPo, museum.museum_id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.museum_name = museum.museum_name
        existing.address = museum.address
        existing.description = museum.description
        existing.status = museum.status
        existing.del_flag = museum.del_flag
        existing.update_by = museum.update_by
        existing.update_time = museum.update_time or now
        existing.remark = museum.remark
        existing.app_id = museum.app_id
        existing.dept_id = museum.dept_id
        return 1

    @staticmethod
    def delete_museum_by_ids(ids: List[int]) -> int:
        """
        批量删除博物馆信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(MuseumPo).where(MuseumPo.museum_id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount