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
from exb_museum.domain.entity import MuseumHall
from exb_museum.service.museum_hall_service import MuseumHallService

from .. import reg

museum_hall_service = MuseumHallService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@reg.api.route('/exb_museum/hall/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:hall:list'))
@JsonSerializer()
def exhibition_hall_list(dto: MuseumHall):
    """查询展厅信息表列表"""
    exhibition_hall_entity = MuseumHall()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_hall_entity, attr):
            setattr(exhibition_hall_entity, attr, getattr(dto, attr))
    museum_halls = museum_hall_service.select_museum_hall_list(exhibition_hall_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=museum_halls)


@reg.api.route('/exb_museum/hall/<int:hallId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:hall:query'))
@JsonSerializer()
def get_exhibition_hall(hall_id: int):
    """获取展厅信息表详细信息"""
    exhibition_hall_entity = museum_hall_service.select_museum_hall_by_id(hall_id)
    return AjaxResponse.from_success(data=exhibition_hall_entity)


@reg.api.route('/exb_museum/hall', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:hall:add'))
@Log(title='展厅信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_exhibition_hall(dto: MuseumHall):
    """新增展厅信息表"""
    exhibition_hall_entity = MuseumHall()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_hall_entity, attr):
            setattr(exhibition_hall_entity, attr, getattr(dto, attr))
    result = museum_hall_service.insert_museum_hall(exhibition_hall_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/hall', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:hall:edit'))
@Log(title='展厅信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_exhibition_hall(dto: MuseumHall):
    """修改展厅信息表"""
    exhibition_hall_entity = MuseumHall()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_hall_entity, attr):
            setattr(exhibition_hall_entity, attr, getattr(dto, attr))
    result = museum_hall_service.update_museum_hall(exhibition_hall_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@reg.api.route('/exb_museum/hall/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:hall:remove'))
@Log(title='展厅信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_exhibition_hall(ids: str):
    """删除展厅信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = museum_hall_service.delete_museum_hall_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@reg.api.route('/exb_museum/hall/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('exb_museum:hall:export'))
@Log(title='展厅信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_exhibition_hall(dto: MuseumHall):
    """导出展厅信息表列表"""
    exhibition_hall_entity = MuseumHall()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(exhibition_hall_entity, attr):
            setattr(exhibition_hall_entity, attr, getattr(dto, attr))
    _clear_page_context()
    exhibition_hall_entity.page_num = None
    exhibition_hall_entity.page_size = None
    exhibition_halls = museum_hall_service.select_museum_hall_list(exhibition_hall_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(MuseumHall)
    return excel_util.export_response(exhibition_halls, "展厅信息表数据")

@reg.api.route('/exb_museum/hall/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def exhibition_hall_import_template():
    """下载展厅信息表导入模板"""
    excel_util = ExcelUtil(MuseumHall)
    return excel_util.import_template_response(sheetname="展厅信息表数据")

@reg.api.route('/exb_museum/hall/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:hall:import'))
@Log(title='展厅信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def exhibition_hall_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入展厅信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(MuseumHall)
    exhibition_hall_list = excel_util.import_file(file, sheetname="展厅信息表数据")
    msg = museum_hall_service.import_museum_hall(exhibition_hall_list, update_support)
    return AjaxResponse.from_success(msg=msg)