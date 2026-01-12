# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_hall_po.py
# @Time    : 

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class MuseumHallPo(db.Model):
    """
    展厅信息表PO对象
    """
    __tablename__ = 'exb_museum_hall'
    __table_args__ = {'comment': '展厅信息表'}
    
    hall_id: Mapped[int] = mapped_column(
        'hall_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='展厅ID'
    )
    hall_name: Mapped[Optional[str]] = mapped_column(
        'hall_name',
        String(200),
        nullable=False,
        comment='展厅名称'
    )
    location: Mapped[Optional[str]] = mapped_column(
        'location',
        String(500),
        nullable=True,
        comment='位置'
    )
    museum_id: Mapped[Optional[int]] = mapped_column(
        'museum_id',
        BigInteger,
        nullable=False,
        comment='所属博物馆ID'
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