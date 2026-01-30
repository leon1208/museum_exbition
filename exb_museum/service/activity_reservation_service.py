# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: activity_reservation_service.py
# @Time    : 2026-01-29

from typing import List
from ruoyi_common.utils import security_util
from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_admin.ext import db
from exb_museum.domain.entity.activity_reservation import ActivityReservation
from exb_museum.domain.entity.activity import Activity
from exb_museum.domain.entity.wx_user import WxUser
from exb_museum.service.activity_service import ActivityService
from exb_museum.mapper.activity_reservation_mapper import ActivityReservationMapper


class ActivityReservationService:
    """活动预约表服务类"""

    def select_activity_reservation_list(self, activity_reservation: ActivityReservation) -> List[ActivityReservation]:
        """
        查询活动预约表列表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            List[ActivityReservation]: 活动预约表列表
        """
        return ActivityReservationMapper.select_activity_reservation_list(activity_reservation)

    
    def select_activity_reservation_by_id(self, reservation_id: int) -> ActivityReservation:
        """
        根据ID查询活动预约表

        Args:
            reservation_id (int): 预约ID

        Returns:
            ActivityReservation: 活动预约表对象
        """
        return ActivityReservationMapper.select_activity_reservation_by_id(reservation_id)
    

    def select_activity_reservation_by_activity_and_user(self, activity_id: int, wx_user_id: int) -> ActivityReservation:
        """
        根据活动ID和微信用户ID查询预约记录

        Args:
            activity_id (int): 活动ID
            wx_user_id (int): 微信用户ID

        Returns:
            ActivityReservation: 活动预约表对象
        """
        return ActivityReservationMapper.select_activity_reservation_by_activity_and_user(activity_id, wx_user_id)


    @Transactional(db.session)
    def insert_activity_reservation(self, activity_reservation: ActivityReservation) -> int:
        """
        新增活动预约表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            int: 插入的记录数
        """
        # 设置创建人
        # activity_reservation.create_by_user(security_util.get_username())
        # activity_reservation.update_by_user(security_util.get_username()) 
        return ActivityReservationMapper.insert_activity_reservation(activity_reservation)

    @Transactional(db.session)    
    def update_activity_reservation(self, activity_reservation: ActivityReservation) -> int:
        """
        修改活动预约表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        # activity_reservation.update_by_user(security_util.get_username())
        return ActivityReservationMapper.update_activity_reservation(activity_reservation)

    @Transactional(db.session)
    def delete_activity_reservation_by_ids(self, ids: List[int]) -> int:
        """
        批量删除活动预约表

        Args:
            ids (List[int]): 预约ID列表

        Returns:
            int: 删除的记录数
        """
        return ActivityReservationMapper.delete_activity_reservation_by_ids(ids)

    @Transactional(db.session)
    def delete_activity_reservation_by_id(self, reservation_id: int) -> int:
        """
        根据ID删除活动预约表

        Args:
            reservation_id (int): 预约ID

        Returns:
            int: 删除的记录数
        """
        ## 更新活动报名人数

        # 先查询预约记录
        activity_reservation = self.select_activity_reservation_by_id(reservation_id)
        if not activity_reservation:
            return 0
        
        # 获取活动对象
        activity_service = ActivityService()
        activity = activity_service.select_activity_by_id(activity_reservation.activity_id)
        if not activity:
            return 0

        result = ActivityReservationMapper.delete_activity_reservation_by_id(reservation_id)
        if result > 0:
            # 更新活动报名人数
            activity_service.update_activity_register_count(activity)
        return result

    @Transactional(db.session)
    def add_activity_reservation(self, activity_id: int, wx_user_id: int, phone_number: str) -> str:
        """
        微信端新增活动预约表

        Args:
            activity_reservation (ActivityReservation): 活动预约表对象

        Returns:
            str: 预约结果
        """

        # 检查活动是否存在
        activity_service = ActivityService()
        activity = activity_service.select_activity_by_id(activity_id)
        if not activity:
            return '活动不存在'
        
        # 检查是否已预约过该活动
        existing_reservation = self.select_activity_reservation_by_activity_and_user(
            activity_id, wx_user_id
        )
        if existing_reservation:
            return '您已经预约过该活动，无需重复预约'
        
        # 检查活动是否已达到最大报名人数
        if activity.max_registration and activity.registration_count >= activity.max_registration:
            return '该活动报名人数已达上限'
        
        # 创建预约记录
        activity_reservation = ActivityReservation()
        activity_reservation.activity_id = activity_id
        activity_reservation.wx_user_id = wx_user_id
        activity_reservation.phone_number = phone_number
        
        result = self.insert_activity_reservation(activity_reservation)
        if result > 0:
            # 更新活动报名人数
            activity_service.update_activity_register_count(activity)
            return '预约成功'
        
        return '预约失败,请联系管理员'
 
    @Transactional(db.session)
    def cancel_activity_reservation(self, reservation_id: int, wx_user_id: int) -> str:
        """
        微信端取消活动预约表

        Args:
            reservation_id (int): 预约ID
            wx_user_id (int): 微信用户ID

        Returns:
            str: 取消结果
        """
        reservation = self.select_activity_reservation_by_id(reservation_id)
        if not reservation:
            return '预约记录不存在'
        
        # 检查预约记录是否属于当前用户
        if reservation.wx_user_id != wx_user_id:
            return '无权限操作他人预约记录'
        
        # 先获取活动信息用于更新报名人数
        activity_service = ActivityService()
        activity = activity_service.select_activity_by_id(reservation.activity_id)
        
        result = self.delete_activity_reservation_by_id(reservation_id)
        if result > 0:
            # 更新活动报名人数
            activity_service.update_activity_register_count(activity)
            return '取消预约成功'
        return '取消预约失败,请联系管理员'
