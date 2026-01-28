# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: wx_user_mapper.py
# @Time    : 2025-12-24

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import WxUser
from exb_museum.domain.po import WxUserPo

class WxUserMapper:
    """微信用户表Mapper"""

    @staticmethod
    def select_wx_user_list(wx_user: WxUser) -> List[WxUser]:
        """
        查询微信用户表列表

        Args:
            wx_user (WxUser): 微信用户表对象

        Returns:
            List[WxUser]: 微信用户表列表
        """
        # 构建查询条件
        stmt = select(WxUserPo)
        if wx_user.app_id:
            stmt = stmt.where(WxUserPo.app_id == wx_user.app_id)
        if wx_user.open_id:
            stmt = stmt.where(WxUserPo.open_id.like("%" + str(wx_user.open_id) + "%"))
        if wx_user.union_id:
            stmt = stmt.where(WxUserPo.union_id.like("%" + str(wx_user.union_id) + "%"))
        if wx_user.nickname:
            stmt = stmt.where(WxUserPo.nickname.like("%" + str(wx_user.nickname) + "%"))
        if wx_user.status is not None:
            stmt = stmt.where(WxUserPo.status == wx_user.status)

        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt

        result = db.session.execute(stmt).scalars().all()
        return [WxUser.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_wx_user_by_id(id: int) -> WxUser:
        """
        根据ID查询微信用户表

        Args:
            id (int): 主键ID

        Returns:
            WxUser: 微信用户表对象
        """
        result = db.session.get(WxUserPo, id)
        return WxUser.model_validate(result) if result else None


    @staticmethod
    def select_wx_user_by_app_id_and_open_id(app_id: str, open_id: str) -> WxUser:
        """
        根据小程序AppID和OpenID查询微信用户表

        Args:
            app_id (str): 小程序AppID
            open_id (str): 微信用户OpenID

        Returns:
            WxUser: 微信用户表对象
        """
        result = db.session.execute(
            select(WxUserPo).where(
                WxUserPo.app_id == app_id,
                WxUserPo.open_id == open_id
            )
        ).scalar_one_or_none()
        return WxUser.model_validate(result) if result else None


    @staticmethod
    def select_wx_user_by_open_id(open_id: str) -> WxUser:
        """
        根据OpenID查询微信用户表

        Args:
            open_id (str): 微信用户OpenID

        Returns:
            WxUser: 微信用户表对象
        """
        result = db.session.execute(
            select(WxUserPo).where(WxUserPo.open_id == open_id)
        ).scalar_one_or_none()
        return WxUser.model_validate(result) if result else None


    @staticmethod
    def insert_wx_user(wx_user: WxUser) -> int:
        """
        新增微信用户表

        Args:
            wx_user (WxUser): 微信用户表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = WxUserPo()
        new_po.id = wx_user.id
        new_po.app_id = wx_user.app_id
        new_po.open_id = wx_user.open_id
        new_po.union_id = wx_user.union_id
        new_po.session_key = wx_user.session_key
        new_po.avatar_url = wx_user.avatar_url
        new_po.nickname = wx_user.nickname
        new_po.status = wx_user.status or 0
        new_po.del_flag = wx_user.del_flag or 0
        new_po.create_time = wx_user.create_time or now
        new_po.update_time = wx_user.update_time or now
        new_po.remark = wx_user.remark
        db.session.add(new_po)

        db.session.flush()
        wx_user.id = new_po.id
        return 1

    
    @staticmethod
    def update_wx_user(wx_user: WxUser) -> int:
        """
        修改微信用户表

        Args:
            wx_user (WxUser): 微信用户表对象

        Returns:
            int: 更新的记录数
        """
        
        existing = db.session.get(WxUserPo, wx_user.id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.app_id = wx_user.app_id
        existing.open_id = wx_user.open_id
        existing.union_id = wx_user.union_id
        existing.session_key = wx_user.session_key
        existing.avatar_url = wx_user.avatar_url
        existing.nickname = wx_user.nickname
        existing.status = wx_user.status or 0
        existing.del_flag = wx_user.del_flag or 0
        existing.update_time = wx_user.update_time or now
        existing.remark = wx_user.remark
        return 1

    @staticmethod
    def delete_wx_user_by_ids(ids: List[int]) -> int:
        """
        批量删除微信用户表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(WxUserPo).where(WxUserPo.id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount