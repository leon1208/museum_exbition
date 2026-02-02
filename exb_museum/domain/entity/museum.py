# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum.py
# @Time    : 2025-12-23 09:24:49

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class Museum(BaseEntity):
    """
    博物馆信息表对象
    """
    # 博物馆ID
    museum_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="博物馆ID"),
        ExcelField(name="博物馆ID")
    ]
    # 博物馆名称
    museum_name: Annotated[
        Optional[str],
        Field(default=None, description="博物馆名称"),
        VoField(query=True),
        ExcelField(name="博物馆名称")
    ]
    # 博物馆地址
    address: Annotated[
        Optional[str],
        Field(default=None, description="博物馆地址"),
        VoField(query=True),
        ExcelField(name="博物馆地址")
    ]
    # 博物馆简介
    description: Annotated[
        Optional[str],
        Field(default=None, description="博物馆简介"),
        ExcelField(name="博物馆简介")
    ]
    # 状态（0正常 1停用）
    status: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="状态（0正常 1停用）"),
        VoField(query=True),
        ExcelField(name="状态（0正常 1停用）", dict_type="sys_yes_no")
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
    # 小程序AppID
    app_id: Annotated[
        Optional[str],
        Field(default=None, description="小程序AppID"),
        VoField(query=True),
        ExcelField(name="小程序AppID")
    ]
    # 小程序AppSecret
    app_secret: Annotated[
        Optional[str],
        Field(default=None, description="小程序AppSecret"),
        ExcelField(name="小程序AppSecret")
    ]
    # 所属部门ID
    dept_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属部门ID"),
        ExcelField(name="所属部门ID")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")