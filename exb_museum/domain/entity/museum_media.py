# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exb_museum_media.py
# @Time    : 2025-12-24 10:46:49

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class MuseumMedia(BaseEntity):
    """
    博物馆多媒体表对象
    """
    # 多媒体ID
    media_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="多媒体ID"),
        VoField(query=True),
        ExcelField(name="多媒体ID")
    ]
    # 博物馆ID
    museum_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="博物馆ID"),
        VoField(query=True),
        ExcelField(name="博物馆ID")
    ]
    # 媒体类型（1图片 2视频 3音频）
    media_type: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="媒体类型（1图片 2视频 3音频）"),
        VoField(query=True),
        ExcelField(name="媒体类型（1图片 2视频 3音频）")
    ]
    # 媒体名称
    media_name: Annotated[
        Optional[str],
        Field(default=None, description="媒体名称"),
        VoField(query=True),
        ExcelField(name="媒体名称")
    ]
    # 媒体URL
    media_url: Annotated[
        Optional[str],
        Field(default=None, description="媒体URL"),
        VoField(query=True),
        ExcelField(name="媒体URL")
    ]
    # 封面图（视频封面/音频封面）
    cover_url: Annotated[
        Optional[str],
        Field(default=None, description="封面图（视频封面/音频封面）"),
        VoField(query=True),
        ExcelField(name="封面图（视频封面/音频封面）")
    ]
    # 时长（秒，视频/音频）
    duration: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="时长（秒，视频/音频）"),
        VoField(query=True),
        ExcelField(name="时长（秒，视频/音频）")
    ]
    # 排序号（越小越靠前）
    sort: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="排序号（越小越靠前）"),
        VoField(query=True),
        ExcelField(name="排序号（越小越靠前）")
    ]
    # 文件大小
    size: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="文件大小"),
        VoField(query=True),
        ExcelField(name="文件大小")
    ]
    # 是否封面（0否 1是）
    is_cover: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="是否封面（0否 1是）"),
        VoField(query=True),
        ExcelField(name="是否封面（0否 1是）")
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
        VoField(query=True),
        ExcelField(name="删除标志（0存在 1删除）")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        VoField(query=True),
        ExcelField(name="创建时间")
    ]
    # 更新时间
    update_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="更新时间"),
        VoField(query=True),
        ExcelField(name="更新时间")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")