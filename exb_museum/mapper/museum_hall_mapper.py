# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_hall_mapper.py
# @Time    : 

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import MuseumHall
from exb_museum.domain.po.museum_hall_po import MuseumHallPo

class MuseumHallMapper:
    """展厅信息表Mapper"""

    @staticmethod
    def select_museum_hall_list(museum_hall: MuseumHall) -> List[MuseumHall]:
        """
        查询展厅信息表列表

        Args:
            museum_hall (MuseumHall): 展厅信息表对象

        Returns:
            List[MuseumHall]: 展厅信息表列表
        """
        try:
            # 构建查询条件
            stmt = select(MuseumHallPo)

            if museum_hall.hall_name:
                stmt = stmt.where(MuseumHallPo.hall_name.like("%" + str(museum_hall.hall_name) + "%"))

            if museum_hall.museum_id is not None:
                stmt = stmt.where(MuseumHallPo.museum_id == museum_hall.museum_id)

            if museum_hall.location:
                stmt = stmt.where(MuseumHallPo.location.like("%" + str(museum_hall.location) + "%"))

            if museum_hall.status is not None:
                stmt = stmt.where(MuseumHallPo.status == museum_hall.status)

            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [MuseumHall.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询展厅信息表列表出错: {e}")
            return []

    
    @staticmethod
    def select_museum_hall_by_id(hall_id: int) -> MuseumHall:
        """
        根据ID查询展厅信息表

        Args:
            hall_id (int): 展厅ID

        Returns:
            MuseumHall: 展厅信息表对象
        """
        try:
            result = db.session.get(MuseumHallPo, hall_id)
            return MuseumHall.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询展厅信息表出错: {e}")
            return None
    

    @staticmethod
    def insert_museum_hall(museum_hall: MuseumHall) -> int:
        """
        新增展厅信息表

        Args:
            museum_hall (MuseumHall): 展厅信息表对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = MuseumHallPo()
            new_po.hall_name = museum_hall.hall_name
            new_po.location = museum_hall.location
            new_po.museum_id = museum_hall.museum_id
            new_po.status = museum_hall.status
            new_po.del_flag = museum_hall.del_flag
            new_po.create_by = museum_hall.create_by
            new_po.create_time = museum_hall.create_time or now
            new_po.update_by = museum_hall.update_by
            new_po.update_time = museum_hall.update_time or now
            new_po.remark = museum_hall.remark
            db.session.add(new_po)
            db.session.commit()
            museum_hall.hall_id = new_po.hall_id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增展厅信息表出错: {e}")
            return 0

    
    @staticmethod
    def update_museum_hall(museum_hall: MuseumHall) -> int:
        """
        修改展厅信息表

        Args:
            museum_hall (MuseumHall): 展厅信息表对象

        Returns:
            int: 更新的记录数
        """
        try:
            existing = db.session.get(MuseumHallPo, museum_hall.hall_id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.hall_name = museum_hall.hall_name
            existing.location = museum_hall.location
            existing.museum_id = museum_hall.museum_id
            existing.status = museum_hall.status
            existing.del_flag = museum_hall.del_flag
            existing.create_by = museum_hall.create_by
            existing.create_time = museum_hall.create_time
            existing.update_by = museum_hall.update_by
            existing.update_time = museum_hall.update_time or now
            existing.remark = museum_hall.remark
            db.session.commit()
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"修改展厅信息表出错: {e}")
            return 0

    @staticmethod
    def delete_museum_hall_by_ids(ids: List[int]) -> int:
        """
        批量删除展厅信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(MuseumHallPo).where(MuseumHallPo.hall_id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除展厅信息表出错: {e}")
            return 0