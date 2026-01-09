# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_controller.py
# @Time    : 2024-05-20 14:00:00

from flask import request
from flask_login import login_required
from typing import List
from werkzeug.datastructures import FileStorage

from exb_museum.domain.entity import MuseumMedia
from exb_museum.service.museum_media_service import MuseumMediaService
from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, FileUploadValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize

from .. import reg


@reg.api.route('/exb_museum/museum/media/list', methods=['GET'])
@QueryValidator(is_page=False)
@login_required
@JsonSerializer()
def list_museum_media():
    """
    查询博物馆媒体列表
    """
    object_id = request.args.get('objectId', type=int)
    object_type = request.args.get('objectType')
    media_type = request.args.get('mediaType')
    
    media_service = MuseumMediaService()
    media_list = media_service.select_museum_media_list(object_id, object_type, media_type)
    
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=media_list)

@reg.api.route('/exb_museum/museum/media/<int:media_id>', methods=['GET'])
@login_required
@JsonSerializer()
def get_museum_media(media_id):
    """
    通过ID查询博物馆媒体
    """
    media_service = MuseumMediaService()
    media = media_service.select_museum_media_by_id(media_id)
    
    if media:
        return AjaxResponse.from_success(data=media)
    return AjaxResponse.from_error(msg='媒体不存在')

@reg.api.route('/exb_museum/museum/media/upload', methods=['POST'])
@login_required
@PreAuthorize(HasPerm('exb_museum:media:add'))
@FileUploadValidator()
@JsonSerializer()
def upload_museum_media(file: List[FileStorage]):
    """
    上传博物馆媒体
    """
    try:
        object_id = request.form.get('objectId', type=int)
        object_type = request.form.get('objectType')
        media_type = request.form.get('mediaType', '1')  # image/video/audio
        file = file[0]

        if not object_id:
            return AjaxResponse.error(msg='关联对象ID不能为空')
        if not object_type:
            return AjaxResponse.error(msg='关联对象类型不能为空')        
        
        if not file:
            return AjaxResponse.error(msg='文件不能为空')
        
        media_service = MuseumMediaService()
        media = media_service.upload_museum_media(object_id, object_type, file, media_type)
        
        return AjaxResponse.from_success(data=media, msg='上传成功')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'上传失败：{str(e)}')

@reg.api.route('/exb_museum/museum/media', methods=['PUT'])
@login_required
@PreAuthorize(HasPerm('exb_museum:media:edit'))
@JsonSerializer()
def update_museum_media():
    """
    更新博物馆媒体
    """
    try:
        media_data = request.get_json()
        media = MuseumMedia(**media_data)
        
        
        media_service = MuseumMediaService()
        result = media_service.update_museum_media(media)
        
        if result > 0:
            return AjaxResponse.from_success(msg='更新成功')
        return AjaxResponse.from_error(msg='更新失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'更新失败：{str(e)}')

@reg.api.route('/exb_museum/museum/media/<int:media_id>', methods=['DELETE'])
@login_required
@PreAuthorize(HasPerm('exb_museum:media:remove'))
@JsonSerializer()
def delete_museum_media(media_id):
    """
    通过ID删除博物馆媒体
    """
    try:
        media_service = MuseumMediaService()
        result = media_service.delete_museum_media_by_id(media_id)
        print(result)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(msg='删除失败')
    except Exception as e:
        print(e)
        return AjaxResponse.from_error(msg=f'删除失败：{str(e)}')
