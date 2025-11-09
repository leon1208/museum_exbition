from typing import Optional, List, Annotated
from datetime import datetime
from ruoyi_common.base.model import BaseEntity
from pydantic import ConfigDict, field_validator, model_validator, Field, BeforeValidator
from ruoyi_common.utils.base import DateUtil
from pydantic import BaseModel
from ruoyi_common.base.transformer import to_datetime
import json


class GenTable(BaseEntity):
    """
    代码生成业务表
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders = {
            datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS) if v else None
        }
    )

    table_id: Optional[int] = Field(None, alias='tableId')
    table_name: Optional[str] = Field(None, alias='tableName')
    table_comment: Optional[str] = Field(None, alias='tableComment')
    sub_table_name: Optional[str] = Field(None, alias='subTableName')
    sub_table_fk_name: Optional[str] = Field(None, alias='subTableFkName')
    class_name: Optional[str] = Field(None, alias='className')
    tpl_category: Optional[str] = Field("crud", alias='tplCategory')
    package_name: Optional[str] = Field(None, alias='packageName')
    module_name: Optional[str] = Field(None, alias='moduleName')
    business_name: Optional[str] = Field(None, alias='businessName')
    function_name: Optional[str] = Field(None, alias='functionName')
    function_author: Optional[str] = Field(None, alias='functionAuthor')
    gen_type: Optional[str] = Field("0", alias='genType')
    gen_path: Optional[str] = Field("/", alias='genPath')
    options: Optional[str] = Field("{}", alias='options')
    create_by: Optional[str] = Field("", alias='createBy')
    create_time: Optional[datetime] = Field(None, alias='createTime')
    update_by: Optional[str] = Field("", alias='updateBy')
    update_time: Optional[datetime] = Field(None, alias='updateTime')
    remark: Optional[str] = None
    columns: Optional[List['GenTableColumn']] = None
    pk_column: Optional['GenTableColumn'] = Field(None, alias='pkColumn')
    # 添加tree相关字段
    tree_name: Optional[str] = Field(None, alias='treeName')
    tree_code: Optional[str] = Field(None, alias='treeCode')
    tree_parent_code: Optional[str] = Field(None, alias='treeParentCode')
    # 分页参数
    page_num: Optional[int] = Field(None, alias='pageNum')
    page_size: Optional[int] = Field(None, alias='pageSize')

    @model_validator(mode='after')
    def process_options(self):
        # 解析options字段以设置tree相关属性
        if self.options and isinstance(self.options, str):
            try:
                options_dict = json.loads(self.options)
                self.tree_name = options_dict.get('treeName')
                self.tree_code = options_dict.get('treeCode')
                self.tree_parent_code = options_dict.get('treeParentCode')
            except Exception:
                pass
        return self

    def model_dump(self, **kwargs):
        # 确保使用别名导出
        kwargs.setdefault('by_alias', True)
        kwargs.setdefault('exclude_none', False)  # 确保包含所有字段
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs):
        # 确保使用别名导出为JSON
        kwargs.setdefault('by_alias', True)
        kwargs.setdefault('exclude_none', False)  # 确保包含所有字段
        return super().model_dump_json(**kwargs)


class GenTableColumn(BaseEntity):
    """
    代码生成业务列
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders = {
            datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS) if v else None
        },
        extra = "forbid"
    )

    column_id: Optional[int] = Field(None, alias='columnId')
    table_id: Optional[int] = Field(None, alias='tableId')
    column_name: Optional[str] = Field(None, alias='columnName')
    column_comment: Optional[str] = Field(None, alias='columnComment')
    column_type: Optional[str] = Field(None, alias='columnType')
    java_type: Optional[str] = Field(None, alias='javaType')
    java_field: Optional[str] = Field(None, alias='javaField')
    is_pk: Optional[str] = Field("0", alias='isPk')
    is_increment: Optional[str] = Field("0", alias='isIncrement')
    is_required: Optional[str] = Field("0", alias='isRequired')
    is_insert: Optional[str] = Field("1", alias='isInsert')
    is_edit: Optional[str] = Field("1", alias='isEdit')
    is_list: Optional[str] = Field("1", alias='isList')
    is_query: Optional[str] = Field("1", alias='isQuery')
    query_type: Optional[str] = Field("EQ", alias='queryType')
    html_type: Optional[str] = Field(None, alias='htmlType')
    dict_type: Optional[str] = Field("", alias='dictType')
    sort: Optional[int] = None
    create_by: Optional[str] = Field("", alias='createBy')
    create_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = Field(None, alias='createTime')
    update_by: Optional[str] = Field("", alias='updateBy')
    update_time: Optional[Annotated[datetime, BeforeValidator(to_datetime())]] = Field(None, alias='updateTime')
    remark: Optional[str] = None
    # 分页参数
    page_num: Optional[int] = Field(None, alias='pageNum')
    page_size: Optional[int] = Field(None, alias='pageSize')

    def model_dump(self, **kwargs):
        # 确保使用别名导出
        kwargs.setdefault('by_alias', True)
        kwargs.setdefault('exclude_none', False)  # 确保包含所有字段
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs):
        # 确保使用别名导出为JSON
        kwargs.setdefault('by_alias', True)
        kwargs.setdefault('exclude_none', False)  # 确保包含所有字段
        return super().model_dump_json(**kwargs)

# 为了解决前向引用问题，需要在类定义后更新类型注释
GenTable.model_rebuild()
GenTableColumn.model_rebuild()
