# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: exb_museum_media_po.py
# @Time    : 2025-12-24 10:46:49

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class MuseumMediaPo(db.Model):
    """
    博物馆多媒体表PO对象
    """
    __tablename__ = 'exb_museum_media'
    __table_args__ = (
        Index('idx_object_type_id', 'object_type', 'object_id', unique=True),
        {'comment': '博物馆多媒体表'})
    
    media_id: Mapped[int] = mapped_column(
        'media_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='多媒体ID'
    )
    object_type: Mapped[Optional[str]] = mapped_column(
        'object_type',
        String(50),
        nullable=False,
        comment='对象类型（museum, exhibition, collection等）'
    )
    object_id: Mapped[Optional[int]] = mapped_column(
        'object_id',
        BigInteger,
        nullable=False,
        comment='关联对象ID'
    )
    media_type: Mapped[Optional[int]] = mapped_column(
        'media_type',
        mysql.TINYINT,
        nullable=False,
        comment='媒体类型（1图片 2视频 3音频）'
    )
    media_name: Mapped[Optional[str]] = mapped_column(
        'media_name',
        String(255),
        nullable=False,
        comment='媒体名称'
    )
    media_url: Mapped[Optional[str]] = mapped_column(
        'media_url',
        String(500),
        nullable=False,
        comment='媒体URL'
    )
    cover_url: Mapped[Optional[str]] = mapped_column(
        'cover_url',
        String(500),
        nullable=True,
        comment='封面图（视频封面/音频封面）'
    )
    duration: Mapped[Optional[int]] = mapped_column(
        'duration',
        Integer,
        nullable=True,
        comment='时长（秒，视频/音频）'
    )
    sort: Mapped[Optional[int]] = mapped_column(
        'sort',
        Integer,
        nullable=False,
        comment='排序号（越小越靠前）'
    )
    size: Mapped[Optional[int]] = mapped_column(
        'size',
        Integer,
        nullable=True,
        comment='文件大小'
    )
    is_cover: Mapped[Optional[int]] = mapped_column(
        'is_cover',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='是否封面（0否 1是）'
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
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP'),
        comment='创建时间'
    )
    update_time: Mapped[Optional[datetime]] = mapped_column(
        'update_time',
        DateTime,
        nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        comment='更新时间'
    )