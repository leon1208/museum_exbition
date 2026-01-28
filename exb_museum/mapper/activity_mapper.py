# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: activity_mapper.py
# @Time    : 2024-12-19 10:30:00

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import Activity
from exb_museum.domain.po import ActivityPo


class ActivityMapper:
    """活动信息表Mapper"""

    @staticmethod
    def select_activity_list(activity: Activity) -> List[Activity]:
        """
        查询活动信息表列表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            List[Activity]: 活动信息表列表
        """
        # 构建查询条件
        stmt = select(ActivityPo)

        if activity.activity_name:
            stmt = stmt.where(ActivityPo.activity_name.like("%" + str(activity.activity_name) + "%"))

        if activity.activity_type:
            stmt = stmt.where(ActivityPo.activity_type.like("%" + str(activity.activity_type) + "%"))

        if activity.location:
            stmt = stmt.where(ActivityPo.location.like("%" + str(activity.location) + "%"))

        if activity.museum_id is not None:
            stmt = stmt.where(ActivityPo.museum_id == activity.museum_id)

        if activity.presenter:
            stmt = stmt.where(ActivityPo.presenter.like("%" + str(activity.presenter) + "%"))

        if activity.target_audience:
            stmt = stmt.where(ActivityPo.target_audience.like("%" + str(activity.target_audience) + "%"))

        if activity.status is not None:
            stmt = stmt.where(ActivityPo.status == activity.status)

        if activity.del_flag is not None:
            stmt = stmt.where(ActivityPo.del_flag == activity.del_flag)

        stmt = stmt.where(ActivityPo.del_flag != 1)  # 只查询未删除的记录

        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt

        result = db.session.execute(stmt).scalars().all()
        return [Activity.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_activity_by_id(activity_id: int) -> Activity:
        """
        根据ID查询活动信息表

        Args:
            activity_id (int): 活动ID

        Returns:
            Activity: 活动信息表对象
        """
        result = db.session.get(ActivityPo, activity_id)
        return Activity.model_validate(result) if result else None
    

    @staticmethod
    def insert_activity(activity: Activity) -> int:
        """
        新增活动信息表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = ActivityPo()
        new_po.activity_id = activity.activity_id
        new_po.activity_name = activity.activity_name
        new_po.introduction = activity.introduction
        new_po.activity_type = activity.activity_type
        new_po.target_audience = activity.target_audience
        new_po.location = activity.location
        new_po.activity_start_time = activity.activity_start_time
        new_po.activity_end_time = activity.activity_end_time
        new_po.registration_count = activity.registration_count or 0
        new_po.max_registration = activity.max_registration or 0
        new_po.presenter = activity.presenter
        new_po.museum_id = activity.museum_id
        new_po.status = activity.status
        new_po.del_flag = activity.del_flag or 0
        new_po.create_by = activity.create_by
        new_po.create_time = activity.create_time or now
        new_po.update_by = activity.update_by
        new_po.update_time = activity.update_time or now
        new_po.remark = activity.remark
        db.session.add(new_po)
        
        db.session.flush()
        activity.activity_id = new_po.activity_id
        return 1

    
    @staticmethod
    def update_activity(activity: Activity) -> int:
        """
        修改活动信息表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            int: 更新的记录数
        """
        
        existing = db.session.get(ActivityPo, activity.activity_id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.activity_name = activity.activity_name
        existing.introduction = activity.introduction
        existing.activity_type = activity.activity_type
        existing.target_audience = activity.target_audience
        existing.location = activity.location
        existing.activity_start_time = activity.activity_start_time
        existing.activity_end_time = activity.activity_end_time
        existing.registration_count = activity.registration_count
        existing.max_registration = activity.max_registration
        existing.presenter = activity.presenter
        existing.museum_id = activity.museum_id
        existing.status = activity.status
        existing.del_flag = activity.del_flag
        existing.create_by = activity.create_by
        existing.create_time = activity.create_time
        existing.update_by = activity.update_by
        existing.update_time = activity.update_time or now
        existing.remark = activity.remark
        return 1

    @staticmethod
    def delete_activity_by_ids(ids: List[int]) -> int:
        """
        批量删除活动信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(ActivityPo).where(ActivityPo.activity_id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount