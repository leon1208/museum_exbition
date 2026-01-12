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
from exb_museum.domain.entity import ExhibitionUnit
from exb_museum.service.exhibition_unit_service import ExhibitionUnitService

from .. import reg

exhibition_unit_service = ExhibitionUnitService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@reg.api.route('/exb_museum/unit/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:unit:list'))
@JsonSerializer()
def exhibition_unit_list(dto: ExhibitionUnit):
    """查询展览单元信息表列表"""
    exhibition_unit_entity = ExhibitionUnit()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_unit_entity, attr):
            setattr(exhibition_unit_entity, attr, getattr(dto, attr))
    exhibition_units = exhibition_unit_service.select_exhibition_unit_list(exhibition_unit_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=exhibition_units)


@reg.api.route('/exb_museum/unit/<int:unitId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:unit:query'))
@JsonSerializer()
def get_exhibition_unit(unit_id: int):
    """获取展览单元信息表详细信息"""
    exhibition_unit_entity = exhibition_unit_service.select_exhibition_unit_by_id(unit_id)
    return AjaxResponse.from_success(data=exhibition_unit_entity)


@reg.api.route('/exb_museum/unit', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:unit:add'))
@Log(title='展览单元信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_exhibition_unit(dto: ExhibitionUnit):
    """新增展览单元信息表"""
    exhibition_unit_entity = ExhibitionUnit()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_unit_entity, attr):
            setattr(exhibition_unit_entity, attr, getattr(dto, attr))
    result = exhibition_unit_service.insert_exhibition_unit(exhibition_unit_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/unit', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:unit:edit'))
@Log(title='展览单元信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_exhibition_unit(dto: ExhibitionUnit):
    """修改展览单元信息表"""
    exhibition_unit_entity = ExhibitionUnit()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_unit_entity, attr):
            setattr(exhibition_unit_entity, attr, getattr(dto, attr))
    result = exhibition_unit_service.update_exhibition_unit(exhibition_unit_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@reg.api.route('/exb_museum/unit/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:unit:remove'))
@Log(title='展览单元信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_exhibition_unit(ids: str):
    """删除展览单元信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = exhibition_unit_service.delete_exhibition_unit_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@reg.api.route('/exb_museum/unit/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('exb_museum:unit:export'))
@Log(title='展览单元信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_exhibition_unit(dto: ExhibitionUnit):
    """导出展览单元信息表列表"""
    exhibition_unit_entity = ExhibitionUnit()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_unit_entity, attr):
            setattr(exhibition_unit_entity, attr, getattr(dto, attr))
    _clear_page_context()
    exhibition_unit_entity.page_num = None
    exhibition_unit_entity.page_size = None
    exhibition_units = exhibition_unit_service.select_exhibition_unit_list(exhibition_unit_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(ExhibitionUnit)
    return excel_util.export_response(exhibition_units, "展览单元信息表数据")

@reg.api.route('/exb_museum/unit/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def exhibition_unit_import_template():
    """下载展览单元信息表导入模板"""
    excel_util = ExcelUtil(ExhibitionUnit)
    return excel_util.import_template_response(sheetname="展览单元信息表数据")

@reg.api.route('/exb_museum/unit/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:unit:import'))
@Log(title='展览单元信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def exhibition_unit_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入展览单元信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(ExhibitionUnit)
    exhibition_unit_list = excel_util.import_file(file, sheetname="展览单元信息表数据")
    msg = exhibition_unit_service.import_exhibition_unit(exhibition_unit_list, update_support)
    return AjaxResponse.from_success(msg=msg)