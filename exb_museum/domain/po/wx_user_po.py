# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: wx_user_po.py
# @Time    : 2025-12-24

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from ruoyi_admin.ext import db


class WxUserPo(db.Model):
    """
    微信用户表PO对象
    """
    __tablename__ = 'exb_wx_user'
    __table_args__ = (
        UniqueConstraint('app_id', 'open_id', name='uk_appid_openid'),
        {'comment': '微信用户表'},
    )

    id: Mapped[int] = mapped_column(
        'id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='主键ID'
    )

    app_id: Mapped[str] = mapped_column(
        'app_id',
        String(64),
        nullable=False,
        comment='微信应用ID'
    )

    open_id: Mapped[str] = mapped_column(
        'open_id',
        String(64),
        nullable=False,
        comment='微信用户OpenID'
    )

    union_id: Mapped[Optional[str]] = mapped_column(
        'union_id',
        String(64),
        nullable=True,
        comment='微信用户UnionID'
    )

    session_key: Mapped[Optional[str]] = mapped_column(
        'session_key',
        String(128),
        nullable=True,
        comment='微信用户SessionKey'
    )

    avatar_url: Mapped[Optional[str]] = mapped_column(
        'avatar_url',
        Text,
        nullable=True,
        comment='头像URL'
    )

    nickname: Mapped[Optional[str]] = mapped_column(
        'nickname',
        String(100),
        nullable=True,
        comment='昵称'
    )

    status: Mapped[Optional[int]] = mapped_column(
        'status',
        mysql.TINYINT,
        nullable=False,
        server_default=sa.text("'0'"),
        comment='状态（0正常 1禁用）'
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

    remark: Mapped[Optional[str]] = mapped_column(
        'remark',
        String(500),
        nullable=True,
        comment='备注'
    )