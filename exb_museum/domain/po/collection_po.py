# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: collection_po.py
# @Time    : 2025-01-05

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class CollectionPo(db.Model):
    """
    藏品信息表PO对象
    """
    __tablename__ = 'exb_collection'
    __table_args__ = {'comment': '藏品信息表'}
    
    collection_id: Mapped[int] = mapped_column(
        'collection_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='藏品ID'
    )
    collection_name: Mapped[Optional[str]] = mapped_column(
        'collection_name',
        String(500),
        nullable=False,
        comment='藏品名'
    )
    collection_type: Mapped[Optional[str]] = mapped_column(
        'collection_type',
        String(50),
        nullable=False,
        comment='类型(油画、书法、瓷器等)'
    )
    size_info: Mapped[Optional[str]] = mapped_column(
        'size_info',
        String(200),
        nullable=True,
        comment='尺寸'
    )
    material: Mapped[Optional[str]] = mapped_column(
        'material',
        String(100),
        nullable=True,
        comment='材质'
    )
    age: Mapped[Optional[str]] = mapped_column(
        'age',
        String(100),
        nullable=True,
        comment='年代'
    )
    author: Mapped[Optional[str]] = mapped_column(
        'author',
        String(100),
        nullable=True,
        comment='作者'
    )
    description: Mapped[Optional[str]] = mapped_column(
        'description',
        Text,
        nullable=True,
        comment='藏品简介'
    )
    exhibition_id: Mapped[Optional[int]] = mapped_column(
        'exhibition_id',
        BigInteger,
        nullable=True,
        comment='所属展览ID'
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