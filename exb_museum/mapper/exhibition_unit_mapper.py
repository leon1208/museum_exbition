# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_unit_mapper.py
# @Time    : 

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import ExhibitionUnit
from exb_museum.domain.po.exhibition_unit_po import ExhibitionUnitPo

class ExhibitionUnitMapper:
    """展览单元信息表Mapper"""

    @staticmethod
    def select_exhibition_unit_list(exhibition_unit: ExhibitionUnit) -> List[ExhibitionUnit]:
        """
        查询展览单元信息表列表

        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象

        Returns:
            List[ExhibitionUnit]: 展览单元信息表列表
        """
        # 构建查询条件
        stmt = select(ExhibitionUnitPo)

        if exhibition_unit.unit_name:
            stmt = stmt.where(ExhibitionUnitPo.unit_name.like("%" + str(exhibition_unit.unit_name) + "%"))

        if exhibition_unit.exhibition_id is not None:
            stmt = stmt.where(ExhibitionUnitPo.exhibition_id == exhibition_unit.exhibition_id)

        if exhibition_unit.unit_type is not None:
            stmt = stmt.where(ExhibitionUnitPo.unit_type == exhibition_unit.unit_type)

        if exhibition_unit.hall_id is not None:
            stmt = stmt.where(ExhibitionUnitPo.hall_id == exhibition_unit.hall_id)

        if exhibition_unit.section:
            stmt = stmt.where(ExhibitionUnitPo.section.like("%" + str(exhibition_unit.section) + "%"))

        if exhibition_unit.status is not None:
            stmt = stmt.where(ExhibitionUnitPo.status == exhibition_unit.status)

        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt
        
        stmt = stmt.order_by(ExhibitionUnitPo.exhibition_id, ExhibitionUnitPo.section, ExhibitionUnitPo.sort_order)

        result = db.session.execute(stmt).scalars().all()
        return [ExhibitionUnit.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_exhibition_unit_by_id(unit_id: int) -> ExhibitionUnit:
        """
        根据ID查询展览单元信息表

        Args:
            unit_id (int): 展览单元ID

        Returns:
            ExhibitionUnit: 展览单元信息表对象
        """
        result = db.session.get(ExhibitionUnitPo, unit_id)
        return ExhibitionUnit.model_validate(result) if result else None
    

    @staticmethod
    def insert_exhibition_unit(exhibition_unit: ExhibitionUnit) -> int:
        """
        新增展览单元信息表

        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = ExhibitionUnitPo()
        new_po.unit_name = exhibition_unit.unit_name
        new_po.exhibition_id = exhibition_unit.exhibition_id
        new_po.exhibit_label = exhibition_unit.exhibit_label
        new_po.guide_text = exhibition_unit.guide_text
        new_po.unit_type = exhibition_unit.unit_type
        new_po.hall_id = exhibition_unit.hall_id
        new_po.section = exhibition_unit.section
        new_po.sort_order = exhibition_unit.sort_order
        new_po.collections = exhibition_unit.collections
        new_po.status = exhibition_unit.status
        new_po.del_flag = exhibition_unit.del_flag
        new_po.create_by = exhibition_unit.create_by
        new_po.create_time = exhibition_unit.create_time or now
        new_po.update_by = exhibition_unit.update_by
        new_po.update_time = exhibition_unit.update_time or now
        new_po.remark = exhibition_unit.remark
        db.session.add(new_po)
        db.session.flush()  # 刷新以获取自动生成的ID
        exhibition_unit.unit_id = new_po.unit_id
        return 1

    
    @staticmethod
    def update_exhibition_unit(exhibition_unit: ExhibitionUnit) -> int:
        """
        修改展览单元信息表

        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象

        Returns:
            int: 更新的记录数
        """
        existing = db.session.get(ExhibitionUnitPo, exhibition_unit.unit_id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.unit_name = exhibition_unit.unit_name
        existing.exhibition_id = exhibition_unit.exhibition_id
        existing.exhibit_label = exhibition_unit.exhibit_label
        existing.guide_text = exhibition_unit.guide_text
        existing.unit_type = exhibition_unit.unit_type
        existing.hall_id = exhibition_unit.hall_id
        existing.section = exhibition_unit.section
        existing.sort_order = exhibition_unit.sort_order
        existing.collections = exhibition_unit.collections
        existing.status = exhibition_unit.status
        existing.del_flag = exhibition_unit.del_flag
        existing.create_by = exhibition_unit.create_by
        existing.create_time = exhibition_unit.create_time
        existing.update_by = exhibition_unit.update_by
        existing.update_time = exhibition_unit.update_time or now
        existing.remark = exhibition_unit.remark
        return 1

    @staticmethod
    def delete_exhibition_unit_by_ids(ids: List[int]) -> int:
        """
        批量删除展览单元信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(ExhibitionUnitPo).where(ExhibitionUnitPo.unit_id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount

    @staticmethod
    def get_max_sort_order_by_exhibition_and_section(exhibition_id: int, section: str) -> int:
        """
        获取指定展览和章节下的最大排序值
    
        Args:
            exhibition_id (int): 展览ID
            section (str): 章节
    
        Returns:
            int: 最大排序值
        """
        from sqlalchemy import func
        stmt = select(func.max(ExhibitionUnitPo.sort_order)).where(
            ExhibitionUnitPo.exhibition_id == exhibition_id
        )
        if section:
            stmt = stmt.where(ExhibitionUnitPo.section == section)
        else:
            stmt = stmt.where(ExhibitionUnitPo.section.is_(None))
        
        result = db.session.execute(stmt).scalar()
        return result if result is not None else 0

    @staticmethod
    def update_sort_order(unit_id: int, sort_order: int) -> int:
        """
        更新展览单元排序
        
        Args:
            unit_id (int): 展览单元ID
            sort_order (int): 排序值
            
        Returns:
            int: 更新的记录数
        """
        stmt = (
            update(ExhibitionUnitPo)
            .where(ExhibitionUnitPo.unit_id == unit_id)
            .values(sort_order=sort_order, update_time=datetime.now())
        )
        result = db.session.execute(stmt)
        return result.rowcount

    @staticmethod
    def select_exhibition_units_by_exhibition_and_section(exhibition_id: int, section: str) -> List[ExhibitionUnit]:
        """
        根据展览ID和章节查询所有展览单元，按排序值升序排列
        
        Args:
            exhibition_id (int): 展览ID
            section (str): 章节
            
        Returns:
            List[ExhibitionUnit]: 展览单元列表
        """
        stmt = (
            select(ExhibitionUnitPo)
            .where(
                ExhibitionUnitPo.exhibition_id == exhibition_id,
                ExhibitionUnitPo.section == section,
                ExhibitionUnitPo.del_flag == 0
            )
            .order_by(ExhibitionUnitPo.sort_order.asc(), ExhibitionUnitPo.unit_id.asc())
        )
        results = db.session.execute(stmt).scalars().all()
        return [ExhibitionUnit.model_validate(po) for po in results]