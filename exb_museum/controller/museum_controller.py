
from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from exb_museum.domain.entity import Museum
from exb_museum.service.museum_service import MuseumService

from .. import reg

museum_service = MuseumService()

def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@reg.api.route('/exb_museum/museum/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:museum:list'))
@JsonSerializer()
def museum_list(dto: Museum):
    """查询博物馆信息表列表"""
    museum_entity = Museum()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(museum_entity, attr):
            setattr(museum_entity, attr, getattr(dto, attr))
    museums = museum_service.select_museum_list(museum_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=museums)


@reg.api.route('/exb_museum/museum/<int:museumId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:museum:query'))
@JsonSerializer()
def get_museum(museum_id: int):
    """获取博物馆信息表详细信息"""
    museum_entity = museum_service.select_museum_by_id(museum_id)
    return AjaxResponse.from_success(data=museum_entity)


@reg.api.route('/exb_museum/museum', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:museum:add'))
@Log(title='博物馆信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_museum(dto: Museum):
    """新增博物馆信息表"""
    museum_entity = Museum()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(museum_entity, attr):
            setattr(museum_entity, attr, getattr(dto, attr))
    result = museum_service.insert_museum(museum_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/museum', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:museum:edit'))
@Log(title='博物馆信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_museum(dto: Museum):
    """修改博物馆信息表"""
    museum_entity = Museum()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(museum_entity, attr):
            setattr(museum_entity, attr, getattr(dto, attr))
    result = museum_service.update_museum(museum_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@reg.api.route('/exb_museum/museum/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:museum:remove'))
@Log(title='博物馆信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_museum(ids: str):
    """删除博物馆信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = museum_service.delete_museum_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@reg.api.route('/exb_museum/museum/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('exb_museum:museum:export'))
@Log(title='博物馆信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_museum(dto: Museum):
    """导出博物馆信息表列表"""
    museum_entity = Museum()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(museum_entity, attr):
            setattr(museum_entity, attr, getattr(dto, attr))
    _clear_page_context()
    museum_entity.page_num = None
    museum_entity.page_size = None
    museums = museum_service.select_museum_list(museum_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Museum)
    return excel_util.export_response(museums, "博物馆信息表数据")

@reg.api.route('/exb_museum/museum/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def museum_import_template():
    """下载博物馆信息表导入模板"""
    excel_util = ExcelUtil(Museum)
    return excel_util.import_template_response(sheetname="博物馆信息表数据")

@reg.api.route('/exb_museum/museum/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:museum:import'))
@Log(title='博物馆信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def museum_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入博物馆信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(Museum)
    museum_list = excel_util.import_file(file, sheetname="博物馆信息表数据")
    msg = museum_service.import_museum(museum_list, update_support)
    return AjaxResponse.from_success(msg=msg)