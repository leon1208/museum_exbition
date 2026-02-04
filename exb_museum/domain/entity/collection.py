# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: collection.py
# @Time    : 2026-01-08 11:23:01

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class Collection(BaseEntity):
    """
    藏品信息表对象
    """
    # 藏品ID
    collection_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="藏品ID"),
        ExcelField(name="藏品ID")
    ]
    # 藏品名
    collection_name: Annotated[
        Optional[str],
        Field(default=None, description="藏品名"),
        VoField(query=True),
        ExcelField(name="藏品名")
    ]
    # 类型
    collection_type: Annotated[
        Optional[str],
        Field(default=None, description="类型"),
        VoField(query=True),
        ExcelField(name="类型")
    ]
    # 尺寸
    size_info: Annotated[
        Optional[str],
        Field(default=None, description="尺寸"),
        ExcelField(name="尺寸")
    ]
    # 材质
    material: Annotated[
        Optional[str],
        Field(default=None, description="材质"),
        ExcelField(name="材质")
    ]
    # 年代
    age: Annotated[
        Optional[str],
        Field(default=None, description="年代"),
        ExcelField(name="年代")
    ]
    # 作者
    author: Annotated[
        Optional[str],
        Field(default=None, description="作者"),
        ExcelField(name="作者")
    ]
    # 藏品简介
    description: Annotated[
        Optional[str],
        Field(default=None, description="藏品简介"),
        ExcelField(name="藏品简介")
    ]
    # 所属展览
    exhibition_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属展览"),
        VoField(query=True),
        ExcelField(name="所属展览")
    ]
    # 所属博物馆
    museum_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属博物馆"),
        VoField(query=True),
        ExcelField(name="所属博物馆")
    ]
    # 状态
    status: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="状态"),
        VoField(query=True),
        ExcelField(name="状态", dict_type="sys_normal_disable")
    ]
    # 删除标志
    del_flag: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="删除标志"),
        ExcelField(name="删除标志")
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