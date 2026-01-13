# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_unit.py
# @Time    : 

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class ExhibitionUnit(BaseEntity):
    """
    展览单元信息表对象
    """
    # 展览单元ID
    unit_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="展览单元ID"),
        ExcelField(name="展览单元ID")
    ]
    # 单元名称
    unit_name: Annotated[
        Optional[str],
        Field(default=None, description="单元名称"),
        VoField(query=True),
        ExcelField(name="单元名称")
    ]
    # 所属展览ID
    exhibition_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所属展览ID"),
        VoField(query=True),
        ExcelField(name="所属展览ID")
    ]
    # 展签
    exhibit_label: Annotated[
        Optional[str],
        Field(default=None, description="展签"),
        ExcelField(name="展签")
    ]
    # 导览词
    guide_text: Annotated[
        Optional[str],
        Field(default=None, description="导览词"),
        ExcelField(name="导览词")
    ]
    # 类型(0展品单元 1文字单元 2多媒体单元)
    unit_type: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="类型(0展品单元 1文字单元 2多媒体单元)"),
        VoField(query=True),
        ExcelField(name="类型(0展品单元 1文字单元 2多媒体单元)")
    ]
    # 所在展厅ID
    hall_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="所在展厅ID"),
        VoField(query=True),
        ExcelField(name="所在展厅ID")
    ]
    # 所属章节
    section: Annotated[
        Optional[str],
        Field(default=None, description="所属章节"),
        VoField(query=True),
        ExcelField(name="所属章节")
    ]
    # 顺序
    sort_order: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=0, description="顺序"),
        ExcelField(name="顺序")
    ]
    # 关联藏品ID列表(JSON数组存储，仅展品单元类型使用)
    collections: Annotated[
        Optional[str],
        Field(default=None, description="关联藏品ID列表(JSON数组存储，仅展品单元类型使用)"),
        ExcelField(name="关联藏品ID列表")
    ]
    # 是否复制藏品媒体至展览单元
    copy_collection_media: Annotated[
        Optional[bool],
        Field(default=False, description="是否复制藏品媒体至展览单元"),
        ExcelField(name="是否复制藏品媒体至展览单元")
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