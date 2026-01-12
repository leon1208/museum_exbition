# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_mapper.py
# @Time    : 2026-01-08 08:54:20

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import Exhibition
from exb_museum.domain.po import ExhibitionPo

class ExhibitionMapper:
    """展览信息表Mapper"""

    @staticmethod
    def select_exhibition_list(exhibition: Exhibition) -> List[Exhibition]:
        """
        查询展览信息表列表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            List[exhibition]: 展览信息表列表
        """
        try:
            # 构建查询条件
            stmt = select(ExhibitionPo)


            if exhibition.exhibition_name:
                stmt = stmt.where(ExhibitionPo.exhibition_name.like("%" + str(exhibition.exhibition_name) + "%"))

            if exhibition.sections:
                stmt = stmt.where(ExhibitionPo.sections.like("%" + str(exhibition.sections) + "%"))

            if exhibition.museum_id is not None:
                stmt = stmt.where(ExhibitionPo.museum_id == exhibition.museum_id)

            if exhibition.hall:
                stmt = stmt.where(ExhibitionPo.hall.like("%" + str(exhibition.hall) + "%"))

            if exhibition.organizer:
                stmt = stmt.where(ExhibitionPo.organizer.like("%" + str(exhibition.organizer) + "%"))

            if exhibition.exhibition_type is not None:
                stmt = stmt.where(ExhibitionPo.exhibition_type == exhibition.exhibition_type)

            if exhibition.content_tags:
                stmt = stmt.where(ExhibitionPo.content_tags.like("%" + str(exhibition.content_tags) + "%"))

            if exhibition.status is not None:
                stmt = stmt.where(ExhibitionPo.status == exhibition.status)


            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [Exhibition.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询展览信息表列表出错: {e}")
            return []

    
    @staticmethod
    def select_exhibition_by_id(exhibition_id: int) -> Exhibition:
        """
        根据ID查询展览信息表

        Args:
            exhibition_id (int): 展览ID

        Returns:
            exhibition: 展览信息表对象
        """
        try:
            result = db.session.get(ExhibitionPo, exhibition_id)
            return Exhibition.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询展览信息表出错: {e}")
            return None
    

    @staticmethod
    def insert_exhibition(exhibition: Exhibition) -> int:
        """
        新增展览信息表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = ExhibitionPo()
            new_po.exhibition_id = exhibition.exhibition_id
            new_po.exhibition_name = exhibition.exhibition_name
            new_po.description = exhibition.description
            new_po.museum_id = exhibition.museum_id
            new_po.hall = exhibition.hall
            new_po.start_time = exhibition.start_time
            new_po.end_time = exhibition.end_time
            new_po.organizer = exhibition.organizer
            new_po.exhibition_type = exhibition.exhibition_type
            new_po.content_tags = exhibition.content_tags
            new_po.sections = exhibition.sections
            new_po.status = exhibition.status
            new_po.del_flag = exhibition.del_flag
            new_po.create_by = exhibition.create_by
            new_po.create_time = exhibition.create_time or now
            new_po.update_by = exhibition.update_by
            new_po.update_time = exhibition.update_time or now
            new_po.remark = exhibition.remark
            db.session.add(new_po)
            db.session.commit()
            exhibition.exhibition_id = new_po.exhibition_id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增展览信息表出错: {e}")
            return 0

    
    @staticmethod
    def update_exhibition(exhibition: Exhibition) -> int:
        """
        修改展览信息表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            int: 更新的记录数
        """
        try:
            
            existing = db.session.get(ExhibitionPo, exhibition.exhibition_id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.exhibition_name = exhibition.exhibition_name
            existing.description = exhibition.description
            existing.museum_id = exhibition.museum_id
            existing.hall = exhibition.hall
            existing.start_time = exhibition.start_time
            existing.end_time = exhibition.end_time
            existing.organizer = exhibition.organizer
            existing.exhibition_type = exhibition.exhibition_type
            existing.content_tags = exhibition.content_tags
            existing.sections = exhibition.sections
            existing.status = exhibition.status
            existing.del_flag = exhibition.del_flag
            existing.create_by = exhibition.create_by
            existing.create_time = exhibition.create_time
            existing.update_by = exhibition.update_by
            existing.update_time = exhibition.update_time or now
            existing.remark = exhibition.remark
            db.session.commit()
            return 1
            
        except Exception as e:
            db.session.rollback()
            print(f"修改展览信息表出错: {e}")
            return 0

    @staticmethod
    def delete_exhibition_by_ids(ids: List[int]) -> int:
        """
        批量删除展览信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(ExhibitionPo).where(ExhibitionPo.exhibition_id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除展览信息表出错: {e}")
            return 0