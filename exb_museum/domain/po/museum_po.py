# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_po.py
# @Time    : 2025-12-23 09:24:49

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class MuseumPo(db.Model):
    """
    博物馆信息表PO对象
    """
    __tablename__ = 'exb_museum'
    __table_args__ = {'comment': '博物馆信息表'}
    museum_id: Mapped[int] = mapped_column(
        'museum_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='博物馆ID'
    )
    museum_name: Mapped[Optional[str]] = mapped_column(
        'museum_name',
        String(200),
        nullable=False,
        comment='博物馆名称'
    )
    address: Mapped[Optional[str]] = mapped_column(
        'address',
        String(500),
        nullable=True,
        comment='博物馆地址'
    )
    description: Mapped[Optional[str]] = mapped_column(
        'description',
        Text,
        nullable=True,
        comment='博物馆简介'
    )
    status: Mapped[Optional[int]] = mapped_column(
        'status',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='状态（0正常 1停用）'
    )
    del_flag: Mapped[Optional[int]] = mapped_column(
        'del_flag',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='删除标志（0存在 1删除）'
    )
    create_by: Mapped[Optional[str]] = mapped_column(
        'create_by',
        String(64),
        nullable=True,
        comment='创建者'
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP'),
        comment='创建时间'
    )
    update_by: Mapped[Optional[str]] = mapped_column(
        'update_by',
        String(64),
        nullable=True,
        comment='更新者'
    )
    update_time: Mapped[Optional[datetime]] = mapped_column(
        'update_time',
        DateTime,
        nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        comment='更新时间'
    )
    remark: Mapped[Optional[str]] = mapped_column(
        'remark',
        String(500),
        nullable=True,
        comment='备注'
    )
    app_id: Mapped[Optional[str]] = mapped_column(
        'app_id',
        String(50),
        nullable=True,
        comment='小程序AppID'
    )
    app_secret: Mapped[Optional[str]] = mapped_column(
        'app_secret',
        String(100),
        nullable=True,
        comment='小程序AppSecret'
    )