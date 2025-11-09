# -*- coding: utf-8 -*-
# @Author  : YY

from flask import request

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_generator.controller import gen
from ruoyi_generator.domain.entity import GenTableColumn
from ruoyi_generator.domain.po import GenTableColumnPO
from ruoyi_generator.service.column_service import GenTableColumnService

gen_table_column_service = GenTableColumnService()


@gen.route('/column/gen/<int:tableId>', methods=["GET"])
@PathValidator()
@PreAuthorize(HasPerm('tool:gen:list'))
@JsonSerializer()
def gen_column_list(tableId: int):
    """
    查询代码生成字段列表
    """
    rows, total = gen_table_column_service.select_gen_table_column_list_by_table_id(tableId)
    return TableResponse(rows=rows, total=total)


@gen.route('/column/<int:columnId>', methods=["GET"])
@PathValidator()
@PreAuthorize(HasPerm('tool:gen:query'))
@JsonSerializer()
def get_column(columnId: int):
    """
    查询代码生成字段详细信息
    """
    column = gen_table_column_service.select_gen_table_column_by_id(columnId)
    return AjaxResponse.from_success(data=column)


@gen.route('/column', methods=["POST"])
@BodyValidator()
@PreAuthorize(HasPerm('tool:gen:add'))
@JsonSerializer()
def add_column(dto: GenTableColumn):
    """
    新增代码生成字段
    """
    result = gen_table_column_service.insert_gen_table_column(dto)
    if result:
        return AjaxResponse.from_success(msg="新增成功")
    else:
        return AjaxResponse.from_error(msg="新增失败")


@gen.route('/column/<int:columnId>', methods=["PUT"])
@BodyValidator()
@PreAuthorize(HasPerm('tool:gen:edit'))
@JsonSerializer()
def update_column(dto: GenTableColumn):
    """
    修改代码生成字段
    """
    result = gen_table_column_service.update_gen_table_column(dto)
    if result:
        return AjaxResponse.from_success(msg="修改成功")
    else:
        return AjaxResponse.from_error(msg="修改失败")


@gen.route('/column/<columnIds>', methods=["DELETE"])
@PathValidator()
@PreAuthorize(HasPerm('tool:gen:remove'))
@JsonSerializer()
def delete_column(columnIds: str):
    """
    删除代码生成字段
    """
    try:
        ids = [int(i) for i in columnIds.split(',')]
        result = gen_table_column_service.delete_gen_table_column_by_ids(ids)
        if result:
            return AjaxResponse.from_success(msg="删除成功")
        else:
            return AjaxResponse.from_error(msg="删除失败")
    except Exception as e:
        return AjaxResponse.from_error(msg=f"删除失败: {str(e)}")