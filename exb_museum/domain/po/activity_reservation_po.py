# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: activity_reservation_po.py
# @Time    : 2026-01-29

from typing import Optional
from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, Text, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from ruoyi_admin.ext import db
import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql


class ActivityReservationPo(db.Model):
    """
    活动预约表PO对象
    """
    __tablename__ = 'exb_activity_reservation'
    __table_args__ = (
        UniqueConstraint('activity_id', 'wx_user_id', name='uk_activityid_wxuserid'),
        {'comment': '活动预约表'},
    )
    
    # 预约ID
    reservation_id: Mapped[int] = mapped_column(
        'reservation_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='预约ID'
    )
    # 活动ID
    activity_id: Mapped[int] = mapped_column(
        'activity_id',
        BigInteger,
        nullable=False,
        comment='活动ID'
    )
    # 微信用户ID
    wx_user_id: Mapped[int] = mapped_column(
        'wx_user_id',
        BigInteger,
        nullable=False,
        comment='微信用户ID'
    )
    # 报名时间
    registration_time: Mapped[Optional[datetime]] = mapped_column(
        'registration_time',
        DateTime,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='报名时间'
    )
    # 手机号码
    phone_number: Mapped[Optional[str]] = mapped_column(
        'phone_number',
        String(20),
        nullable=True,
        comment='手机号码'
    )
    # 删除标志（0存在 1删除）
    del_flag: Mapped[Optional[int]] = mapped_column(
        'del_flag',
        mysql.TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment='删除标志（0存在 1删除）'
    )
    # 创建者
    create_by: Mapped[Optional[str]] = mapped_column(
        'create_by',
        String(64),
        nullable=True,
        comment='创建者'
    )
    # 创建时间
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='创建时间'
    )
    # 更新者
    update_by: Mapped[Optional[str]] = mapped_column(
        'update_by',
        String(64),
        nullable=True,
        comment='更新者'
    )
    # 更新时间
    update_time: Mapped[Optional[datetime]] = mapped_column(
        'update_time',
        DateTime,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        comment='更新时间'
    )
    # 备注
    remark: Mapped[Optional[str]] = mapped_column(
        'remark',
        String(500),
        nullable=True,
        comment='备注'
    )
