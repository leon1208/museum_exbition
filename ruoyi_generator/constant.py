# 代码生成常量信息

class GenConstants:
    # 单表（增删改查）
    TPL_CRUD = "crud"

    # 树表（增删改查）
    TPL_TREE = "tree"

    # 主子表（增删改查）
    TPL_SUB = "sub"

    # 数据库字符串类型
    COLUMNTYPE_STR = ['char', 'varchar', 'nvarchar', 'varchar2']

    # 数据库文本类型
    COLUMNTYPE_TEXT = ['tinytext', 'text', 'mediumtext', 'longtext']

    # 数据库时间类型
    COLUMNTYPE_TIME = ['datetime', 'time', 'date', 'timestamp']

    # 数据库数字类型
    COLUMNTYPE_NUMBER = ['tinyint', 'smallint', 'mediumint', 'int', 'number', 'integer',
                         'bigint', 'float', 'double', 'decimal']

    # BO对象 不需要添加的字段
    COLUMNNAME_NOT_ADD = ["create_by", "create_time", "del_flag", "update_by",
                          "update_time"]

    # BO对象 不需要编辑的字段
    COLUMNNAME_NOT_EDIT = ["create_by", "create_time", "del_flag", "update_by",
                           "update_time"]

    # VO对象 不需要显示的列表字段
    COLUMNNAME_NOT_LIST = ["create_by", "create_time", "del_flag", "update_by",
                           "update_time"]

    # BO对象 不需要查询的字段
    COLUMNNAME_NOT_QUERY = ["create_by", "create_time", "del_flag", "update_by",
                            "update_time", "remark"]

    # Entity基类字段
    BASE_ENTITY = ["createBy", "createTime", "updateBy", "updateTime", "remark"]

    # Tree基类字段
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors"]

    # 文本框
    HTML_INPUT = "input"

    # 文本域
    HTML_TEXTAREA = "textarea"

    # 下拉框
    HTML_SELECT = "select"

    # 单选框
    HTML_RADIO = "radio"

    # 复选框
    HTML_CHECKBOX = "checkbox"

    # 日期控件
    HTML_DATETIME = "datetime"

    # 图片上传控件
    HTML_IMAGE_UPLOAD = "imageUpload"

    # 文件上传控件
    HTML_FILE_UPLOAD = "fileUpload"

    # 富文本控件
    HTML_EDITOR = "editor"

    # 字符串类型
    TYPE_STRING = "String"

    # 整型
    TYPE_INTEGER = "Integer"

    # 长整型
    TYPE_LONG = "Long"

    # 浮点型
    TYPE_DOUBLE = "Double"

    # 高精度计算类型
    TYPE_BIGDECIMAL = "BigDecimal"

    # 时间类型
    TYPE_DATE = "Date"

    # 模糊查询
    QUERY_LIKE = "LIKE"

    # 相等查询
    QUERY_EQ = "EQ"

    # 需要
    REQUIRE = "1"