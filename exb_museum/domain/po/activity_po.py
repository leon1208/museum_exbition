# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: activity_po.py
# @Time    : 2024-12-19 10:30:00

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db


class ActivityPo(db.Model):
    """
    活动信息表PO对象
    """
    __tablename__ = 'exb_activity'
    __table_args__ = {'comment': '活动信息表'}
    
    # 活动ID
    activity_id: Mapped[int] = mapped_column(
        'activity_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='活动ID'
    )
    # 活动名称
    activity_name: Mapped[Optional[str]] = mapped_column(
        'activity_name',
        String(255),
        nullable=False,
        comment='活动名称'
    )
    # 活动介绍
    introduction: Mapped[Optional[str]] = mapped_column(
        'introduction',
        Text,
        nullable=True,
        comment='活动介绍'
    )
    # 活动类型
    activity_type: Mapped[Optional[str]] = mapped_column(
        'activity_type',
        String(100),
        nullable=False,
        comment='活动类型(讲座/表演/手工/其他等)'
    )
    # 活动对象
    target_audience: Mapped[Optional[str]] = mapped_column(
        'target_audience',
        String(255),
        nullable=False,
        server_default=sa.text("'不限'"),
        comment='活动对象'
    )
    # 活动地点
    location: Mapped[Optional[str]] = mapped_column(
        'location',
        String(255),
        nullable=False,
        comment='活动地点'
    )
    # 活动开始时间
    activity_start_time: Mapped[Optional[datetime]] = mapped_column(
        'activity_start_time',
        DateTime,
        nullable=False,
        comment='活动开始时间'
    )
    # 活动结束时间
    activity_end_time: Mapped[Optional[datetime]] = mapped_column(
        'activity_end_time',
        DateTime,
        nullable=True,
        comment='活动结束时间'
    )
    # 报名人数
    registration_count: Mapped[Optional[int]] = mapped_column(
        'registration_count',
        Integer,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='报名人数'
    )
    # 最大报名人数
    max_registration: Mapped[Optional[int]] = mapped_column(
        'max_registration',
        Integer,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='最大报名人数'
    )
    # 主讲人或表演团
    presenter: Mapped[Optional[str]] = mapped_column(
        'presenter',
        String(255),
        nullable=True,
        comment='主讲人或表演团队'
    )
    # 所属博物馆ID
    museum_id: Mapped[Optional[int]] = mapped_column(
        'museum_id',
        BigInteger,
        nullable=True,
        comment='所属博物馆ID'
    )
    # 状态（0正常 1停用）
    status: Mapped[Optional[int]] = mapped_column(
        'status',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='状态（0正常 1停用）'
    )
    # 删除标志（0存在 1删除）
    del_flag: Mapped[Optional[int]] = mapped_column(
        'del_flag',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
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
        server_default=sa.text('CURRENT_TIMESTAMP'),
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
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        comment='更新时间'
    )
    # 备注
    remark: Mapped[Optional[str]] = mapped_column(
        'remark',
        String(500),
        nullable=True,
        comment='备注'
    )