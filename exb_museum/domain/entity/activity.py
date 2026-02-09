# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: activity.py
# @Time    : 2024-12-19 10:30:00

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class Activity(BaseEntity):
    """
    活动信息表对象
    """
    # 活动ID
    activity_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="活动ID"),
        ExcelField(name="活动ID")
    ]
    # 活动名称
    activity_name: Annotated[
        Optional[str],
        Field(default=None, description="活动名称"),
        VoField(query=True),
        ExcelField(name="活动名称")
    ]
    # 活动介绍
    introduction: Annotated[
        Optional[str],
        Field(default=None, description="活动介绍"),
        ExcelField(name="活动介绍")
    ]
    # 活动类型
    activity_type: Annotated[
        Optional[str],
        Field(default=None, description="活动类型"),
        VoField(query=True),
        ExcelField(name="活动类型")
    ]
    # 活动对象
    target_audience: Annotated[
        Optional[str],
        Field(default=None, description="活动对象"),
        ExcelField(name="活动对象")
    ]
    # 活动地点
    location: Annotated[
        Optional[str],
        Field(default=None, description="活动地点"),
        VoField(query=True),
        ExcelField(name="活动地点")
    ]
    # 活动时间
    activity_start_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="活动开始时间"),
        ExcelField(name="活动开始时间")
    ]
    # 活动结束时间
    activity_end_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="活动结束时间"),
        ExcelField(name="活动结束时间")
    ]
    # 报名人数
    registration_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=0, description="报名人数"),
        ExcelField(name="报名人数")
    ]
    # 最大报名人数
    max_registration: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=0, description="最大报名人数"),
        ExcelField(name="最大报名人数")
    ]
    # 主讲人或表演团
    presenter: Annotated[
        Optional[str],
        Field(default=None, description="主讲人或表演团队"),
        ExcelField(name="主讲人或表演团队")
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
        ExcelField(name="状态", dict_type="sys_normal_disable")
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
    
    def can_register(self) -> bool:
        """判断是否可以注册"""
        return (
            self.status == 0 
            and self.activity_start_time 
            and self.activity_start_time > datetime.now()
            and self.registration_count < self.max_registration
        )

    def get_status_display(self) -> str:
        """获取状态显示文本"""
        return "即将开始" if self.activity_start_time > datetime.now() else "已经结束" if self.status == 0 else "已经取消"

    def get_formatted_time(self) -> str:
        """获取格式化的时间显示"""
        return f"{self.activity_start_time.strftime('%y年%m月%d日 %H:%M') if self.activity_start_time else ''}{self.activity_end_time.strftime(' 至 %H:%M') if self.activity_end_time else ''}"