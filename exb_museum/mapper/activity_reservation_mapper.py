# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: activity_reservation_mapper.py
# @Time    : 2026-01-29

from typing import List
from sqlalchemy import select, delete
from ruoyi_admin.ext import db
from exb_museum.domain.po.activity_reservation_po import ActivityReservationPo
from exb_museum.domain.entity.activity_reservation import ActivityReservation
from datetime import datetime
from flask import g


class ActivityReservationMapper:
    """活动预约表Mapper"""

    @staticmethod
    def select_activity_reservation_list(activity_reservation: ActivityReservation) -> List[ActivityReservation]:
        """
        查询活动预约表列表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            List[ActivityReservation]: 活动预约表列表
        """
        # 构建查询条件
        stmt = select(ActivityReservationPo)
        
        if activity_reservation.reservation_id:
            stmt = stmt.where(ActivityReservationPo.reservation_id == activity_reservation.reservation_id)
        if activity_reservation.activity_id:
            stmt = stmt.where(ActivityReservationPo.activity_id == activity_reservation.activity_id)
        if activity_reservation.wx_user_id:
            stmt = stmt.where(ActivityReservationPo.wx_user_id == activity_reservation.wx_user_id)
        if activity_reservation.phone_number:
            stmt = stmt.where(ActivityReservationPo.phone_number.like("%" + str(activity_reservation.phone_number) + "%"))
        if activity_reservation.create_time:
            stmt = stmt.where(ActivityReservationPo.create_time >= activity_reservation.create_time)
        if activity_reservation.update_time:
            stmt = stmt.where(ActivityReservationPo.update_time >= activity_reservation.update_time)

        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt

        stmt = stmt.order_by(ActivityReservationPo.registration_time.desc())
        result = db.session.execute(stmt).scalars().all()
        return [ActivityReservation.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_activity_reservation_by_id(reservation_id: int) -> ActivityReservation:
        """
        根据ID查询活动预约表

        Args:
            reservation_id (int): 预约ID

        Returns:
            ActivityReservation: 活动预约表对象
        """
        result = db.session.get(ActivityReservationPo, reservation_id)
        return ActivityReservation.model_validate(result) if result else None


    @staticmethod
    def select_activity_reservation_by_activity_and_user(activity_id: int, wx_user_id: int) -> ActivityReservation:
        """
        根据活动ID和微信用户ID查询预约记录

        Args:
            activity_id (int): 活动ID
            wx_user_id (int): 微信用户ID

        Returns:
            ActivityReservation: 活动预约表对象
        """
        result = db.session.execute(
            select(ActivityReservationPo).where(
                ActivityReservationPo.activity_id == activity_id,
                ActivityReservationPo.wx_user_id == wx_user_id,
                ActivityReservationPo.del_flag == 0
            )
        ).scalar_one_or_none()
        return ActivityReservation.model_validate(result) if result else None


    @staticmethod
    def insert_activity_reservation(activity_reservation: ActivityReservation) -> int:
        """
        新增活动预约表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = ActivityReservationPo()
        new_po.reservation_id = activity_reservation.reservation_id
        new_po.activity_id = activity_reservation.activity_id
        new_po.wx_user_id = activity_reservation.wx_user_id
        new_po.registration_time = activity_reservation.registration_time or now
        new_po.phone_number = activity_reservation.phone_number
        new_po.del_flag = activity_reservation.del_flag or 0
        new_po.create_by = activity_reservation.create_by
        new_po.create_time = activity_reservation.create_time or now
        new_po.update_by = activity_reservation.update_by
        new_po.update_time = activity_reservation.update_time or now
        new_po.remark = activity_reservation.remark
        db.session.add(new_po)
        
        db.session.flush()
        activity_reservation.reservation_id = new_po.reservation_id
        return 1

    
    @staticmethod
    def update_activity_reservation(activity_reservation: ActivityReservation) -> int:
        """
        修改活动预约表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            int: 更新的记录数
        """
        
        existing = db.session.get(ActivityReservationPo, activity_reservation.reservation_id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.activity_id = activity_reservation.activity_id
        existing.wx_user_id = activity_reservation.wx_user_id
        existing.registration_time = activity_reservation.registration_time
        existing.phone_number = activity_reservation.phone_number
        existing.del_flag = activity_reservation.del_flag
        existing.update_by = activity_reservation.update_by
        existing.update_time = activity_reservation.update_time or now
        existing.remark = activity_reservation.remark
        return 1

    @staticmethod
    def delete_activity_reservation_by_ids(ids: List[int]) -> int:
        """
        批量删除活动预约表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(ActivityReservationPo).where(ActivityReservationPo.reservation_id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount

    @staticmethod
    def delete_activity_reservation_by_id(reservation_id: int) -> int:
        """
        根据ID删除活动预约表

        Args:
            reservation_id (int): 预约ID

        Returns:
            int: 删除的记录数
        """
        stmt = delete(ActivityReservationPo).where(ActivityReservationPo.reservation_id == reservation_id)
        result = db.session.execute(stmt)
        return result.rowcount
