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
from exb_museum.domain.entity import Activity
from exb_museum.service.activity_service import ActivityService

from .. import reg

activity_service = ActivityService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@reg.api.route('/exb_museum/activity/list', methods=['GET'])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:activity:list'))
@JsonSerializer()
def list_activities(dto: Activity):
    """查询活动信息表列表"""
    activity_entity = Activity()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(activity_entity, attr):
            setattr(activity_entity, attr, getattr(dto, attr))
    activities = activity_service.select_activity_list(activity_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=activities)


@reg.api.route('/exb_museum/activity/<int:activityId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:activity:query'))
@JsonSerializer()
def get_activity(activity_id: int):
    """获取活动信息表详细信息"""
    activity_entity = activity_service.select_activity_by_id(activity_id)
    return AjaxResponse.from_success(data=activity_entity)


@reg.api.route('/exb_museum/activity', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:activity:add'))
@Log(title='活动信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_activity(dto: Activity):
    """新增活动信息表"""
    activity_entity = Activity()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(activity_entity, attr):
            setattr(activity_entity, attr, getattr(dto, attr))
    result = activity_service.insert_activity(activity_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/activity', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:activity:edit'))
@Log(title='活动信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_activity(dto: Activity):
    """修改活动信息表"""
    activity_entity = Activity()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(activity_entity, attr):
            setattr(activity_entity, attr, getattr(dto, attr))
    result = activity_service.update_activity(activity_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')


@reg.api.route('/exb_museum/activity/<int:activityId>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:activity:remove'))
@Log(title='活动信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def remove_activity(activity_id: int):
    """删除活动信息表"""
    result = activity_service.delete_activity_by_id(activity_id)
    if result > 0:
        return AjaxResponse.from_success(msg='删除成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')


@reg.api.route('/exb_museum/activity', methods=['DELETE'])
@QueryValidator()
@PreAuthorize(HasPerm('exb_museum:activity:remove'))
@Log(title='活动信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def batch_remove_activities():
    """批量删除活动信息表"""
    activity_ids_str = getattr(g.criterian_obj, 'activityIds', None)
    if activity_ids_str is None:
        return AjaxResponse.from_error(msg='请选择要删除的数据')
    
    activity_ids = [int(id) for id in activity_ids_str.split(',')]
    result = activity_service.batch_delete_activity(activity_ids)
    if result > 0:
        return AjaxResponse.from_success(msg=f'已成功删除{result}条数据')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')


@reg.api.route('/exb_museum/activity/export', methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm('exb_museum:activity:export'))
@Log(title='活动信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_activities():
    """导出活动信息表"""
    activity_entity = Activity()
    for attr in g.criterian_obj.model_fields.keys():
        if hasattr(activity_entity, attr) and getattr(g.criterian_obj, attr) is not None:
            setattr(activity_entity, attr, getattr(g.criterian_obj, attr))

    # 清除分页上下文，防止分页参数影响查询
    _clear_page_context()

    activities = activity_service.select_activity_list(activity_entity)
    excel_util = ExcelUtil(Activity)
    return excel_util.export_excel_response(activities, "活动信息表数据")


@reg.api.route('/exb_museum/activity/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def activity_import_template():
    """下载活动信息表导入模板"""
    excel_util = ExcelUtil(Activity)
    return excel_util.import_template_response(sheetname="活动信息表数据")


@reg.api.route('/exb_museum/activity/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:activity:import'))
@Log(title='活动信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def activity_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入活动信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(Activity)
    activity_list = excel_util.import_file(file, sheetname="活动信息表数据")
    msg = activity_service.import_activity(activity_list, update_support)
    return AjaxResponse.from_success(msg=msg)