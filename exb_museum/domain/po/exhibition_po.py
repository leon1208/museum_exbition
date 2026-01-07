# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_po.py
# @Time    : 2025-01-05

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class ExhibitionPo(db.Model):
    """
    展览信息表PO对象
    """
    __tablename__ = 'exb_exhibition'
    __table_args__ = {'comment': '展览信息表'}
    
    exhibition_id: Mapped[int] = mapped_column(
        'exhibition_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='展览ID'
    )
    exhibition_name: Mapped[Optional[str]] = mapped_column(
        'exhibition_name',
        String(500),
        nullable=False,
        comment='展名'
    )
    description: Mapped[Optional[str]] = mapped_column(
        'description',
        Text,
        nullable=True,
        comment='展览简介'
    )
    museum_id: Mapped[Optional[int]] = mapped_column(
        'museum_id',
        BigInteger,
        nullable=False,
        comment='所属博物馆ID'
    )
    hall: Mapped[Optional[str]] = mapped_column(
        'hall',
        String(100),
        nullable=True,
        comment='展厅'
    )
    start_time: Mapped[Optional[datetime]] = mapped_column(
        'start_time',
        DateTime,
        nullable=False,
        comment='展览开始时间'
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(
        'end_time',
        DateTime,
        nullable=False,
        comment='展览结束时间'
    )
    organizer: Mapped[Optional[str]] = mapped_column(
        'organizer',
        String(500),
        nullable=True,
        comment='主办单位'
    )
    exhibition_type: Mapped[Optional[int]] = mapped_column(
        'exhibition_type',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='展览类型（0长期 1临时）'
    )
    content_tags: Mapped[Optional[str]] = mapped_column(
        'content_tags',
        String(500),
        nullable=True,
        comment='内容标签'
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