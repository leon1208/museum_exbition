# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: activity_reservation.py
# @Time    : 2026-01-29

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class ActivityReservation(BaseEntity):
    """
    活动预约对象
    """

    # 预约ID
    reservation_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="预约ID"),
        ExcelField(name="预约ID")
    ]
    # 活动ID
    activity_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="活动ID"),
        VoField(query=True),
        ExcelField(name="活动ID")
    ]
    # 微信用户ID
    wx_user_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="微信用户ID"),
        VoField(query=True),
        ExcelField(name="微信用户ID")
    ]
    # 报名时间
    registration_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="报名时间"),
        ExcelField(name="报名时间")
    ]
    # 手机号码
    phone_number: Annotated[
        Optional[str],
        Field(default=None, description="手机号码"),
        ExcelField(name="手机号码")
    ]
    # 删除标志（0存在 1删除）
    del_flag: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="删除标志（0存在 1删除）"),
        ExcelField(name="删除标志（0存在 1删除）")
    ]
    # 创建者
    create_by: Annotated[
        Optional[str],
        Field(default=None, description="创建者"),
        ExcelField(name="创建者")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        ExcelField(name="创建时间")
    ]
    # 更新者
    update_by: Annotated[
        Optional[str],
        Field(default=None, description="更新者"),
        ExcelField(name="更新者")
    ]
    # 更新时间
    update_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="更新时间"),
        ExcelField(name="更新时间")
    ]
    # 备注
    remark: Annotated[
        Optional[str],
        Field(default=None, description="备注"),
        ExcelField(name="备注")
    ]
    # 微信用户昵称
    nickname: Annotated[
        Optional[str],
        Field(default=None, description="微信用户昵称"),
        ExcelField(name="微信用户昵称")
    ]
    # 微信用户头像
    avatar_url: Annotated[
        Optional[str],
        Field(default=None, description="微信用户头像"),
        ExcelField(name="微信用户头像")
    ]