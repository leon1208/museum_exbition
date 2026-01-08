
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
from exb_museum.domain.entity import Collection
from exb_museum.service.collection_service import CollectionService


from .. import reg

collection_service = CollectionService()

def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@reg.api.route('/exb_museum/collection/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('exb_museum:collection:list'))
@JsonSerializer()
def collection_list(dto: Collection):
    """查询藏品信息表列表"""
    collection_entity = Collection()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(collection_entity, attr):
            setattr(collection_entity, attr, getattr(dto, attr))
    collections = collection_service.select_collection_list(collection_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=collections)


@reg.api.route('/exb_museum/collection/<int:collectionId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:collection:query'))
@JsonSerializer()
def get_collection(collection_id: int):
    """获取藏品信息表详细信息"""
    collection_entity = collection_service.select_collection_by_id(collection_id)
    return AjaxResponse.from_success(data=collection_entity)


@reg.api.route('/exb_museum/collection', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:collection:add'))
@Log(title='藏品信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_collection(dto: Collection):
    """新增藏品信息表"""
    collection_entity = Collection()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(collection_entity, attr):
            setattr(collection_entity, attr, getattr(dto, attr))
    result = collection_service.insert_collection(collection_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@reg.api.route('/exb_museum/collection', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('exb_museum:collection:edit'))
@Log(title='藏品信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_collection(dto: Collection):
    """修改藏品信息表"""
    collection_entity = Collection()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(collection_entity, attr):
            setattr(collection_entity, attr, getattr(dto, attr))
    result = collection_service.update_collection(collection_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@reg.api.route('/exb_museum/collection/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('exb_museum:collection:remove'))
@Log(title='藏品信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_collection(ids: str):
    """删除藏品信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = collection_service.delete_collection_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@reg.api.route('/exb_museum/collection/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('exb_museum:collection:export'))
@Log(title='藏品信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_collection(dto: Collection):
    """导出藏品信息表列表"""
    collection_entity = Collection()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(collection_entity, attr):
            setattr(collection_entity, attr, getattr(dto, attr))
    _clear_page_context()
    collection_entity.page_num = None
    collection_entity.page_size = None
    collections = collection_service.select_collection_list(collection_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Collection)
    return excel_util.export_response(collections, "藏品信息表数据")

@reg.api.route('/exb_museum/collection/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def collection_import_template():
    """下载藏品信息表导入模板"""
    excel_util = ExcelUtil(Collection)
    return excel_util.import_template_response(sheetname="藏品信息表数据")

@reg.api.route('/exb_museum/collection/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('exb_museum:collection:import'))
@Log(title='藏品信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def collection_import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入藏品信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(Collection)
    collection_list = excel_util.import_file(file, sheetname="藏品信息表数据")
    msg = collection_service.import_collection(collection_list, update_support)
    return AjaxResponse.from_success(msg=msg)