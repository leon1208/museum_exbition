from typing import Optional, List, Annotated
from datetime import datetime
from ruoyi_common.base.model import BaseEntity
from pydantic import ConfigDict, model_validator, BeforeValidator
from ruoyi_common.utils.base import DateUtil
from ruoyi_common.base.transformer import to_datetime
from sqlalchemy import CHAR, DateTime, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column
from ruoyi_admin.ext import db


class GenTablePo(db.Model):
    __tablename__ = 'gen_table'
    __table_args__ = {'comment': '代码生成业务表'}

    table_id: Mapped[int] = mapped_column(BIGINT(20), primary_key=True, comment='编号')
    table_name: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("''"), comment='表名称')
    table_comment: Mapped[Optional[str]] = mapped_column(String(500), server_default=text("''"), comment='表描述')
    sub_table_name: Mapped[Optional[str]] = mapped_column(String(64), comment='关联子表的表名')
    sub_table_fk_name: Mapped[Optional[str]] = mapped_column(String(64), comment='子表关联的外键名')
    class_name: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("''"), comment='实体类名称')
    tpl_category: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("'crud'"), comment='使用的模板')
    package_name: Mapped[Optional[str]] = mapped_column(String(100), comment='生成包路径')
    module_name: Mapped[Optional[str]] = mapped_column(String(30), comment='生成模块名')
    business_name: Mapped[Optional[str]] = mapped_column(String(30), comment='生成业务名')
    function_name: Mapped[Optional[str]] = mapped_column(String(50), comment='生成功能名')
    function_author: Mapped[Optional[str]] = mapped_column(String(50), comment='生成功能作者')
    gen_type: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'0'"), comment='生成代码方式（0zip压缩包 1自定义路径）')
    gen_path: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("'/'"), comment='生成路径（不填默认项目路径）')
    options: Mapped[Optional[str]] = mapped_column(String(1000), comment='其它生成选项')
    create_by: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''"), comment='创建者')
    create_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='创建时间')
    update_by: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''"), comment='更新者')
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='更新时间')
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment='备注')


class GenTableColumnPo(db.Model):
    __tablename__ = 'gen_table_column'
    __table_args__ = {'comment': '代码生成业务列'}

    column_id: Mapped[int] = mapped_column(BIGINT(20), primary_key=True, comment='编号')
    table_id: Mapped[Optional[int]] = mapped_column(BIGINT(20), comment='归属表编号')
    column_name: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("''"), comment='列名称')
    column_comment: Mapped[Optional[str]] = mapped_column(String(500), server_default=text("''"), comment='列描述')
    column_type: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("''"), comment='列类型')
    java_type: Mapped[Optional[str]] = mapped_column(String(500), server_default=text("''"), comment='JAVA类型')
    java_field: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("''"), comment='JAVA字段名')
    is_pk: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'0'"), comment='是否主键（1是）')
    is_increment: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'0'"), comment='是否自增（1是）')
    is_required: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'0'"), comment='是否必填（1是）')
    is_insert: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'1'"), comment='是否为插入字段（1是）')
    is_edit: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'1'"), comment='是否编辑字段（1是）')
    is_list: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'1'"), comment='是否列表字段（1是）')
    is_query: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'1'"), comment='是否查询字段（1是）')
    query_type: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("'EQ'"), comment='查询方式（等于、不等于、大于、小于、范围）')
    html_type: Mapped[Optional[str]] = mapped_column(String(200), comment='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')
    dict_type: Mapped[Optional[str]] = mapped_column(String(200), server_default=text("''"), comment='字典类型')
    sort: Mapped[Optional[int]] = mapped_column(INTEGER(4), server_default=text("'0'"), comment='排序')
    create_by: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''"), comment='创建者')
    create_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='创建时间')
    update_by: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''"), comment='更新者')
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='更新时间')
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment='备注')


class GenTablePO(BaseEntity):
    """
    代码生成业务表
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders = {
            datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS) if v else None
        },
        extra = "ignore"
    )
    
    table_id: Optional[int] = None
    table_name: Optional[str] = None
    table_comment: Optional[str] = None
    sub_table_name: Optional[str] = None
    sub_table_fk_name: Optional[str] = None
    class_name: Optional[str] = None
    tpl_category: Optional[str] = None
    package_name: Optional[str] = None
    module_name: Optional[str] = None
    business_name: Optional[str] = None
    function_name: Optional[str] = None
    function_author: Optional[str] = None
    gen_type: Optional[str] = None
    gen_path: Optional[str] = None
    options: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = None
    update_by: Optional[str] = None
    update_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = None
    remark: Optional[str] = None
    columns: Optional[List['GenTableColumnPO']] = None
    pk_column: Optional[dict] = None
    params: Optional[dict] = None
    # 添加tree相关字段
    tree_name: Optional[str] = None
    tree_code: Optional[str] = None
    tree_parent_code: Optional[str] = None
    # 分页参数
    page_num: Optional[int] = None
    page_size: Optional[int] = None


class GenTableColumnPO(BaseEntity):
    """
    代码生成业务列
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders = {
            datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS) if v else None
        },
        extra = "ignore"
    )
    
    column_id: Optional[int] = None
    table_id: Optional[int] = None
    column_name: Optional[str] = None
    column_comment: Optional[str] = None
    column_type: Optional[str] = None
    java_type: Optional[str] = None
    java_field: Optional[str] = None
    is_pk: Optional[str] = None
    is_increment: Optional[str] = None
    is_required: Optional[str] = None
    is_insert: Optional[str] = None
    is_edit: Optional[str] = None
    is_list: Optional[str] = None
    is_query: Optional[str] = None
    query_type: Optional[str] = "EQ"
    html_type: Optional[str] = None
    dict_type: Optional[str] = ""
    sort: Optional[int] = None
    create_by: Optional[str] = ""
    create_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = None
    update_by: Optional[str] = ""
    update_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = None
    remark: Optional[str] = None
    # 分页参数
    page_num: Optional[int] = None
    page_size: Optional[int] = None
