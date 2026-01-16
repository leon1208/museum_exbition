# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_controller.py
# @Time    : 2024-05-20 14:00:00

from flask import request
from flask_login import login_required
from typing import List
from werkzeug.datastructures import FileStorage

from exb_museum.service.museum_media_service import MuseumMediaService
from exb_museum.service.collection_service import CollectionService
from exb_museum.service.exhibition_service import ExhibitionService
from exb_museum.service.exhibition_unit_service import ExhibitionUnitService  # 添加展览单元服务导入
from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, FileUploadValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize

from exb_museum.domain.entity import MuseumMedia, Museum, Collection, Exhibition, ExhibitionUnit
from exb_museum.service.museum_media_service import MuseumMediaService
from exb_museum.service.museum_service import MuseumService

from .. import reg


@reg.api.route('/wx/museum/home/<string:app_id>', methods=["GET"])
@JsonSerializer()
def museum_home(app_id: str):
    """获取博物馆首页数据"""

    # 从数据库获取真实数据
    museum_service = MuseumService()
    media_service = MuseumMediaService()
    collection_service = CollectionService()
    exhibition_service = ExhibitionService()

    # 获取博物馆信息
    museum = museum_service.select_museum_by_app_id(app_id)
    if not museum:
        return AjaxResponse.from_error(msg="博物馆不存在")
    
    # 获取展览媒体
    media_list = media_service.select_museum_media_list(object_id=museum.museum_id, object_type='museum', media_type='1')

    # 获取该博物馆下的藏品列表
    collection = Collection()
    collection.museum_id = museum.museum_id
    collection.status = 0  # 只获取正常状态的藏品
    collections = collection_service.select_collection_list(collection)
    
    # 获取该博物馆下的展览列表
    exhibition = Exhibition()
    exhibition.museum_id = museum.museum_id
    exhibition.status = 0  # 只获取正常状态的展览
    exhibitions = exhibition_service.select_exhibition_list(exhibition)

    # 构建返回数据
    # 转换藏品数据格式
    collection_list = []
    for col in collections:
        collection_item = {
            "id": col.collection_id,
            "title": col.collection_name or "",
            "period": col.age or "",
            "img": "",  # 后续可以从媒体表获取图片
            "description": col.description or "",
            "material": col.material or "",
            "sizeInfo": col.size_info or "",
            "author": col.author or "",
            "type": col.collection_type or ""
        }
        # 从媒体表获取藏品图片
        medias = media_service.select_museum_media_list(object_id=col.collection_id, object_type='collection', media_type='1')
        if medias:
            collection_item["img"] = medias[0].media_url

        collection_list.append(collection_item)

    # 转换展览数据格式
    exhibition_list = []
    for exh in exhibitions:
        exhibition_item = {
            "id": exh.exhibition_id,
            "title": exh.exhibition_name or "",
            "desc": exh.description or "",
            "date": f"{exh.start_time.strftime('%m月%d日') if exh.start_time else ''} - {exh.end_time.strftime('%m月%d日') if exh.end_time else ''}",
            "place": exh.hall or "",
            "status": "",
            "statusText": "",
            "img": "",  # 后续可以从媒体表获取图片
            "organizer": exh.organizer or "",
            "startTime": exh.start_time.strftime('%Y-%m-%d') if exh.start_time else "",
            "endTime": exh.end_time.strftime('%Y-%m-%d') if exh.end_time else ""
        }
        # 从媒体表获取展览图片
        medias = media_service.select_museum_media_list(object_id=exh.exhibition_id, object_type='exhibition', media_type='1')
        if medias:
            exhibition_item["img"] = medias[0].media_url
        
        # 通过当前时间和展览时间判断展览状态
        from datetime import datetime
        now = datetime.now()
        if now < exh.start_time:
            exhibition_item["status"] = "upcoming"
            exhibition_item["statusText"] = "即将开始"
        elif now > exh.end_time:
            exhibition_item["status"] = "ended"
            exhibition_item["statusText"] = "已结束"
        else:
            exhibition_item["status"] = "ongoing"
            exhibition_item["statusText"] = "正在热展"

        exhibition_list.append(exhibition_item)

    # 构建首页数据
    home_data = {
        "museum": {
            "name": museum.museum_name,
            "description": museum.description,
            "openStatus": "今日开放",
            "openTime": "10:00 - 18:00",
            # "bgImage": media_list[0].media_url if media_list else "",
            "bgImageList": [media.media_url for media in media_list] if media_list else []
        },
        "collections": collection_list,
        "exhibitions": exhibition_list,
        "educations": [
            {
                "type": "工作坊",
                "title": "陶艺体验大师课",
                "time": "明日 10:00",
                "img": "/wx_static/tmp_images/act01.png"
            },
            {
                "type": "讲座",
                "title": "策展人视角导览",
                "time": "周日 14:00",
                "img": "/wx_static/tmp_images/act02.png"
            }
        ]
    }
    return AjaxResponse.from_success(data=home_data)


@reg.api.route('/wx/museum/exhibition/detail/<int:exhibition_id>', methods=["GET"])
@JsonSerializer()
def exhibition_detail(exhibition_id: int):
    """获取展览详情，包括展览信息和展览单元信息"""
    # 获取服务实例
    exhibition_service = ExhibitionService()
    exhibition_unit_service = ExhibitionUnitService()
    media_service = MuseumMediaService()
    collection_service = CollectionService()

    # 获取展览信息
    exhibition = exhibition_service.select_exhibition_by_id(exhibition_id)
    if not exhibition:
        return AjaxResponse.from_error(msg="展览不存在")

    # 获取展览媒体
    exhibition_medias = media_service.select_museum_media_list(
        object_id=exhibition_id, 
        object_type='exhibition', 
        media_type='1'
    )

    # 获取该展览的所有展览单元
    exhibition_units = exhibition_unit_service.select_exhibition_units_by_exhibition_id(exhibition_id)

    # 处理展览信息
    exhibition_data = {
        "id": exhibition.exhibition_id,
        "title": exhibition.exhibition_name or "",
        "description": exhibition.description or "",
        "startDate": exhibition.start_time.strftime('%Y-%m-%d') if exhibition.start_time else "",
        "endDate": exhibition.end_time.strftime('%Y-%m-%d') if exhibition.end_time else "",
        "organizer": exhibition.organizer or "",
        "hall": exhibition.hall or "",
        "exhibitionType": exhibition.exhibition_type or "",
        "contentTags": exhibition.content_tags or "",
        "sections": exhibition.sections or "",
        "coverImg": exhibition_medias[0].media_url if exhibition_medias else "",
        "galleryImages": [media.media_url for media in exhibition_medias] if exhibition_medias else []
    }

    # 处理展览单元信息
    units_data = []
    for unit in exhibition_units:
        unit_data = {
            "id": unit.unit_id,
            "name": unit.unit_name or "",
            "type": unit.unit_type,  # 0展品单元 1文字单元 2多媒体单元
            "section": unit.section or "",
            "sortOrder": unit.sort_order or 0,
            "exhibitLabel": unit.exhibit_label or "",
            "guideText": unit.guide_text or "",
            "collections": unit.collections or "",  # JSON字符串格式的藏品ID列表
            "mediaList": [],  # 初始化媒体列表,
            "hasAudio": False,
            "audioUrl": ""
        }

        # 如果是展品单元，获取关联的藏品信息和媒体
        if unit.unit_type == 0 and unit.collections:
            import json
            try:
                collection_ids = json.loads(unit.collections) if unit.collections else []
                if collection_ids:
                    # 获取藏品详细信息
                    collection_list = []
                    for col_id in collection_ids:
                        collection = collection_service.select_collection_by_id(col_id)
                        if collection:
                            # 获取藏品媒体
                            col_medias = media_service.select_museum_media_list(
                                object_id=col_id, 
                                object_type='collection', 
                                media_type='1'
                            )
                            
                            collection_data = {
                                "id": collection.collection_id,
                                "name": collection.collection_name or "",
                                "age": collection.age or "",
                                "description": collection.description or "",
                                "material": collection.material or "",
                                "sizeInfo": collection.size_info or "",
                                "author": collection.author or "",
                                "type": collection.collection_type or "",
                                "imageUrl": col_medias[0].media_url if col_medias else "",
                                "mediaList": [{"url": media.media_url, "type": media.media_type} for media in col_medias]
                            }
                            collection_list.append(collection_data)
                    
                    unit_data["collectionsDetail"] = collection_list
            except Exception as e:
                print(f"解析藏品ID列表时出错: {str(e)}")
                unit_data["collectionsDetail"] = []

        # 获取展览单元的媒体
        unit_medias = media_service.select_museum_media_list(
            object_id=unit.unit_id, 
            object_type='exhibition_unit', 
            media_type=[1, 3]
        )
        unit_data["mediaList"] = [{"url": media.media_url, "type": media.media_type} for media in unit_medias if media.media_type in [1]]

        # 检查是否有音频
        unit_data["hasAudio"] = any(media.media_type == 3 for media in unit_medias)
        if unit_data["hasAudio"]:
            unit_data["audioUrl"] = next((media.media_url for media in unit_medias if media.media_type == 3), "")
        
        units_data.append(unit_data)

    # 构建返回数据
    detail_data = {
        "exhibition": exhibition_data,
        "units": units_data
    }

    return AjaxResponse.from_success(data=detail_data)