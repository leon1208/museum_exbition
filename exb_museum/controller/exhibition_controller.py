
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
from exb_museum.domain.entity import Exhibition
from exb_museum.service.exhibition_service import ExhibitionService

from .. import reg

exhibition_service = ExhibitionService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@reg.api.route('/exb_museum/exbition/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:exbition:list'))
@JsonSerializer()
def exbition_list(dto: Exhibition):
    """查询展览信息表列表"""
    exhibition_entity = Exhibition()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_entity, attr):
            setattr(exhibition_entity, attr, getattr(dto, attr))
    exbitions = exhibition_service.select_exhibition_list(exhibition_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=exbitions)


@reg.api.route('/exb_museum/exbition/<int:exhibitionId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:query'))
@JsonSerializer()
def get_exbition(exhibition_id: int):
    """获取展览信息表详细信息"""
    exhibition_entity = exhibition_service.select_exhibition_by_id(exhibition_id)
    return AjaxResponse.from_success(data=exhibition_entity)


@reg.api.route('/exb_museum/exbition', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:add'))
@Log(title='展览信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_exbition(dto: Exhibition):
    """新增展览信息表"""
    exhibition_entity = Exhibition()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_entity, attr):
            setattr(exhibition_entity, attr, getattr(dto, attr))
    result = exhibition_service.insert_exhibition(exhibition_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/exbition', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:edit'))
@Log(title='展览信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_exbition(dto: Exhibition):
    """修改展览信息表"""
    exhibition_entity = Exhibition()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_entity, attr):
            setattr(exhibition_entity, attr, getattr(dto, attr))
    result = exhibition_service.update_exhibition(exhibition_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@reg.api.route('/exb_museum/exbition/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:remove'))
@Log(title='展览信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_exbition(ids: str):
    """删除展览信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = exhibition_service.delete_exhibition_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@reg.api.route('/exb_museum/exbition/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:export'))
@Log(title='展览信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_exbition(dto: Exhibition):
    """导出展览信息表列表"""
    exhibition_entity = Exhibition()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_entity, attr):
            setattr(exhibition_entity, attr, getattr(dto, attr))
    _clear_page_context()
    exhibition_entity.page_num = None
    exhibition_entity.page_size = None
    exbitions = exhibition_service.select_exhibition_list(exhibition_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Exhibition)
    return excel_util.export_response(exbitions, "展览信息表数据")

@reg.api.route('/exb_museum/exbition/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def exhibition_import_template():
    """下载展览信息表导入模板"""
    excel_util = ExcelUtil(Exhibition)
    return excel_util.import_template_response(sheetname="展览信息表数据")

@reg.api.route('/exb_museum/exbition/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:exbition:import'))
@Log(title='展览信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def exhibition_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入展览信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(Exhibition)
    exbition_list = excel_util.import_file(file, sheetname="展览信息表数据")
    msg = exhibition_service.import_exhibition(exbition_list, update_support)
    return AjaxResponse.from_success(msg=msg)