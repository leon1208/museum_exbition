# -*- coding: utf-8 -*-
# @Author  : Assistant AI
# @FileName: wx_user.py
# @Time    : 2025-12-24

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class WxUser(BaseEntity):
    """
    微信用户对象
    """

    # 主键ID
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="主键ID"),
        ExcelField(name="主键ID")
    ]
    # 微信应用ID
    app_id: Annotated[
        Optional[str],
        Field(default=None, description="微信应用ID"),
        VoField(query=True),
        ExcelField(name="微信应用ID")
    ]
    # 微信用户OpenID
    open_id: Annotated[
        Optional[str],
        Field(default=None, description="微信用户OpenID"),
        VoField(query=True),
        ExcelField(name="微信用户OpenID")
    ]
    # 微信用户UnionID
    union_id: Annotated[
        Optional[str],
        Field(default=None, description="微信用户UnionID"),
        ExcelField(name="微信用户UnionID")
    ]
    # 微信用户SessionKey
    session_key: Annotated[
        Optional[str],
        Field(default=None, description="微信用户SessionKey"),
        VoField(query=True),
        ExcelField(name="微信用户SessionKey")
    ]
    # 头像URL
    avatar_url: Annotated[
        Optional[str],
        Field(default=None, description="头像URL"),
        ExcelField(name="头像URL")
    ]
    # 昵称
    nickname: Annotated[
        Optional[str],
        Field(default=None, description="昵称"),
        ExcelField(name="昵称")
    ]
    # 状态（0正常 1禁用）
    status: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="状态（0正常 1禁用）"),
        VoField(query=True),
        ExcelField(name="状态（0正常 1禁用）", dict_type="sys_common_status")
    ]
    # 删除标志（0存在 1删除）
    del_flag: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="删除标志（0存在 1删除）"),
        ExcelField(name="删除标志（0存在 1删除）")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        ExcelField(name="创建时间")
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

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")