# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition.py
# @Time    : 2026-01-08 08:54:20

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class Exhibition(BaseEntity):
    """
    展览信息表对象
    """
    # 展览ID
    exhibition_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="展览ID"),
        ExcelField(name="展览ID")
    ]
    # 展名
    exhibition_name: Annotated[
        Optional[str],
        Field(default=None, description="展名"),
        VoField(query=True),
        ExcelField(name="展名")
    ]
    # 展览简介
    description: Annotated[
        Optional[str],
        Field(default=None, description="展览简介"),
        ExcelField(name="展览简介")
    ]
    # 所属博物馆ID
    museum_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属博物馆ID"),
        VoField(query=True),
        ExcelField(name="所属博物馆ID")
    ]
    # 展厅
    hall: Annotated[
        Optional[str],
        Field(default=None, description="展厅"),
        ExcelField(name="展厅")
    ]
    # 展览开始时间
    start_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="展览开始时间"),
        ExcelField(name="展览开始时间")
    ]
    # 展览结束时间
    end_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="展览结束时间"),
        ExcelField(name="展览结束时间")
    ]
    # 主办单位
    organizer: Annotated[
        Optional[str],
        Field(default=None, description="主办单位"),
        VoField(query=True),
        ExcelField(name="主办单位")
    ]
    # 展览类型（0长期 1临时）
    exhibition_type: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="展览类型（0长期 1临时）"),
        VoField(query=True),
        ExcelField(name="展览类型（0长期 1临时）")
    ]
    # 内容标签
    content_tags: Annotated[
        Optional[str],
        Field(default=None, description="内容标签"),
        ExcelField(name="内容标签")
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