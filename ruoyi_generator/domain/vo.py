from ruoyi_generator.domain.entity import GenTable, GenTableColumn
from ruoyi_common.base.model import BaseEntity


class GenTableVO(BaseEntity):
    """
    代码生成业务表
    """
    def __init__(self):
        self.table_id = None
        self.table_name = None
        self.table_comment = None
        self.sub_table_name = None
        self.sub_table_fk_name = None
        self.class_name = None
        self.tpl_category = None
        self.package_name = None
        self.module_name = None
        self.business_name = None
        self.function_name = None
        self.function_author = None
        self.gen_type = None
        self.gen_path = None
        self.options = None
        self.create_by = None
        self.create_time = None
        self.update_by = None
        self.update_time = None
        self.remark = None
        # 子表信息
        self.sub_table = None
        # 表列信息
        self.columns = []
        # 主键信息
        self.pk_column = None
        # 表列字段字符串组，英文逗号分隔
        self.column_field_str = None
        
    @staticmethod
    def from_entity(entity: GenTable):
        vo = GenTableVO()
        vo.table_id = entity.table_id
        vo.table_name = entity.table_name
        vo.table_comment = entity.table_comment
        vo.sub_table_name = entity.sub_table_name
        vo.sub_table_fk_name = entity.sub_table_fk_name
        vo.class_name = entity.class_name
        vo.tpl_category = entity.tpl_category
        vo.package_name = entity.package_name
        vo.module_name = entity.module_name
        vo.business_name = entity.business_name
        vo.function_name = entity.function_name
        vo.function_author = entity.function_author
        vo.gen_type = entity.gen_type
        vo.gen_path = entity.gen_path
        vo.options = entity.options
        vo.create_by = entity.create_by
        vo.create_time = entity.create_time
        vo.update_by = entity.update_by
        vo.update_time = entity.update_time
        vo.remark = entity.remark
        return vo


class GenTableColumnVO(BaseEntity):
    """
    代码生成业务列
    """
    def __init__(self):
        self.column_id = None
        self.table_id = None
        self.column_name = None
        self.column_comment = None
        self.column_type = None
        self.java_type = None
        self.java_field = None
        self.is_pk = None
        self.is_increment = None
        self.is_required = None
        self.is_insert = None
        self.is_edit = None
        self.is_list = None
        self.is_query = None
        self.query_type = None
        self.html_type = None
        self.dict_type = None
        self.sort = None
        self.create_by = None
        self.create_time = None
        self.update_by = None
        self.update_time = None
        self.remark = None
        
    @staticmethod
    def from_entity(entity: GenTableColumn):
        vo = GenTableColumnVO()
        vo.column_id = entity.column_id
        vo.table_id = entity.table_id
        vo.column_name = entity.column_name
        vo.column_comment = entity.column_comment
        vo.column_type = entity.column_type
        vo.java_type = entity.java_type
        vo.java_field = entity.java_field
        vo.is_pk = entity.is_pk
        vo.is_increment = entity.is_increment
        vo.is_required = entity.is_required
        vo.is_insert = entity.is_insert
        vo.is_edit = entity.is_edit
        vo.is_list = entity.is_list
        vo.is_query = entity.is_query
        vo.query_type = entity.query_type
        vo.html_type = entity.html_type
        vo.dict_type = entity.dict_type
        vo.sort = entity.sort
        vo.create_by = entity.create_by
        vo.create_time = entity.create_time
        vo.update_by = entity.update_by
        vo.update_time = entity.update_time
        vo.remark = entity.remark
        return vo
