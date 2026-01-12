# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_unit_po.py
# @Time    : 

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db

class ExhibitionUnitPo(db.Model):
    """
    展览单元信息表PO对象
    """
    __tablename__ = 'exb_exhibition_unit'
    __table_args__ = {'comment': '展览单元信息表'}
    
    unit_id: Mapped[int] = mapped_column(
        'unit_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='展览单元ID'
    )
    unit_name: Mapped[Optional[str]] = mapped_column(
        'unit_name',
        String(500),
        nullable=False,
        comment='单元名称'
    )
    exhibition_id: Mapped[Optional[int]] = mapped_column(
        'exhibition_id',
        BigInteger,
        nullable=False,
        comment='所属展览ID'
    )
    exhibit_label: Mapped[Optional[str]] = mapped_column(
        'exhibit_label',
        Text,
        nullable=True,
        comment='展签'
    )
    guide_text: Mapped[Optional[str]] = mapped_column(
        'guide_text',
        Text,
        nullable=True,
        comment='导览词'
    )
    unit_type: Mapped[Optional[int]] = mapped_column(
        'unit_type',
        mysql.TINYINT,
        nullable=False,
        comment='类型(0展品单元 1文字单元 2多媒体单元)'
    )
    hall_id: Mapped[Optional[int]] = mapped_column(
        'hall_id',
        BigInteger,
        nullable=True,
        comment='所在展厅ID'
    )
    section: Mapped[Optional[str]] = mapped_column(
        'section',
        String(255),
        nullable=True,
        comment='所属章节'
    )
    sort_order: Mapped[Optional[int]] = mapped_column(
        'sort_order',
        Integer,
        nullable=False,
        default=0,
        comment='顺序'
    )
    collections: Mapped[Optional[str]] = mapped_column(
        'collections',
        JSON,
        nullable=True,
        comment='关联藏品ID列表(JSON数组存储，仅展品单元类型使用)'
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