# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_hall.py
# @Time    : 

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class MuseumHall(BaseEntity):
    """
    展厅信息表对象
    """
    # 展厅ID
    hall_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="展厅ID"),
        ExcelField(name="展厅ID")
    ]
    # 展厅名称
    hall_name: Annotated[
        Optional[str],
        Field(default=None, description="展厅名称"),
        VoField(query=True),
        ExcelField(name="展厅名称")
    ]
    # 位置
    location: Annotated[
        Optional[str],
        Field(default=None, description="位置"),
        ExcelField(name="位置")
    ]
    # 所属博物馆ID
    museum_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属博物馆ID"),
        VoField(query=True),
        ExcelField(name="所属博物馆ID")
    ]
    # 状态（0正常 1停用）
    status: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="状态（0正常 1停用）"),
        VoField(query=True),
        ExcelField(name="状态（0正常 1停用）")
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

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")