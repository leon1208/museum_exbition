# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_controller.py
# @Time    : 2024-05-20 14:00:00

from flask import request, g
from flask_login import login_required
from typing import List
from werkzeug.datastructures import FileStorage
from datetime import datetime

from exb_museum.service.museum_media_service import MuseumMediaService
from exb_museum.service.collection_service import CollectionService
from exb_museum.service.exhibition_service import ExhibitionService
from exb_museum.service.exhibition_unit_service import ExhibitionUnitService  # 添加展览单元服务导入
from ruoyi_common.base.model import AjaxResponse, TableResponse, PageModel, CriterianMeta
from ruoyi_common.constant import HttpStatus, Constants
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, FileUploadValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize

from exb_museum.domain.entity import MuseumMedia, Museum, Collection, Exhibition, ExhibitionUnit, Activity, ActivityReservation  # 添加活动预约实体导入
from exb_museum.service.museum_media_service import MuseumMediaService
from exb_museum.service.museum_service import MuseumService
from exb_museum.service.activity_service import ActivityService  # 添加活动服务导入
from exb_museum.service.activity_reservation_service import ActivityReservationService  # 添加活动预约服务导入
from exb_museum.service.wx_auth_service import WxAuthService
from functools import wraps


from .. import reg

def require_wx_token(f, check_sign=False):
    """
    微信用户认证装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # 从请求头获取token
        auth_header = request.headers.get(Constants.TOKEN_HEADER)
        if auth_header and auth_header.startswith(Constants.TOKEN_PREFIX):
            token = auth_header[len(Constants.TOKEN_PREFIX):]
        elif auth_header:  # 如果没有Bearer前缀，直接使用
            token = auth_header
        
        if not token:
            return JsonSerializer().serialize(f, AjaxResponse.from_error(msg="缺少认证令牌"))
            
        # 验证token
        auth_service = WxAuthService()
        payload = auth_service.verify_access_token(token)
        if not payload:
            return JsonSerializer().serialize(f, AjaxResponse.from_error(msg="无效或过期的令牌"))
        
        # 获取签名的相关参数
        method = request.method
        path = request.path
        body = request.get_data(as_text=True) or ''
        timestamp = int(request.headers.get('X-Timestamp', 0))
        nonce = request.headers.get('X-Nonce', '')
        sign = request.headers.get('X-Sign', '')

        # 验证请求签名
        if check_sign and not auth_service.verify_request(method, path, body, timestamp, nonce, sign, token):
            return JsonSerializer().serialize(f, AjaxResponse.from_error(msg="无效的请求签名"))

        # 获取wx_user_id
        wx_user = auth_service.get_wx_user(payload.get('app_id'), payload.get('open_id'))
        if not wx_user:
            return JsonSerializer().serialize(f, AjaxResponse.from_error(msg="用户不存在"))

        # 将用户信息存储到全局对象中
        g.wx_user_payload = payload
        g.wx_open_id = payload.get('open_id')
        g.wx_app_id = payload.get('app_id')
        g.wx_user_id = wx_user.id
        return f(*args, **kwargs)
    return decorated_function


@reg.api.route('/wx/auth/login', methods=["POST"])
@JsonSerializer()
def wx_login():
    """
    微信登录接口
    小程序端调用wx.login()获取code后发送到此接口
    """
    data = request.get_json()
    if not data or 'code' not in data or 'app_id' not in data:
        return AjaxResponse.from_error(msg="缺少登录凭证code或者应用ID")
    
    code = data['code']
    app_id = data['app_id']
    
    # 使用code进行登录
    auth_service = WxAuthService()
    wx_user = auth_service.get_or_create_wx_user(app_id, code)
    if not wx_user:
        return AjaxResponse.from_error(msg="登录失败，请重试")
    access_token = auth_service.generate_access_token(wx_user.open_id, app_id)
    if not access_token:
        return AjaxResponse.from_error(msg="登录失败，请重试")
    
    user_info = {
        "nickname": wx_user.nickname,
        "avatarUrl": wx_user.avatar_url
    }
    return AjaxResponse.from_success(data={"access_token": access_token, "user_info": user_info}, msg="登录成功")


@reg.api.route('/wx/my/update', methods=["POST"])
@require_wx_token
@JsonSerializer()
def update_user_info():
    """更新用户信息"""
    data = request.get_json()
    nickname = data.get('nickname')
    avatar_url = data.get('avatarUrl')
    
    # 更新用户信息
    auth_service = WxAuthService()
    updated = auth_service.update_wx_user_nickname_or_avatar(g.wx_app_id, g.wx_open_id, nickname, avatar_url)
    if not updated:
        return AjaxResponse.from_error(msg="更新用户信息失败")
    
    return AjaxResponse.from_success(msg="用户信息更新成功")


@reg.api.route('/wx/museum/home/<string:app_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def museum_home(app_id: str):
    """获取博物馆首页数据"""

    # 从数据库获取真实数据
    museum_service = MuseumService()
    media_service = MuseumMediaService()
    collection_service = CollectionService()
    exhibition_service = ExhibitionService()

    g.criterian_meta = CriterianMeta()
    g.criterian_meta.page = PageModel(pageNum=1, pageSize=5) #大坑啊，这里要用驼峰命名，因为前端都是驼峰的
    g.criterian_meta.scope = None # 不限制范围，必须加

    # 获取博物馆信息
    museum = museum_service.select_museum_by_app_id(app_id)
    if not museum:
        return AjaxResponse.from_error(msg="博物馆不存在")
    
    # 获取博物馆的媒体
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

    # 获取该博物馆下的活动列表
    activity_service = ActivityService()
    activity = Activity()
    activity.museum_id = museum.museum_id
    activity.status = 0  # 只获取正常状态的活动
    activities = activity_service.select_activity_list(activity)

    # 构建返回数据
    # 转换藏品数据格式
    collectio_media_map = media_service.select_museum_media_list_batch(object_ids=[col.collection_id for col in collections], object_type='collection', media_type='1')
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
        medias = collectio_media_map.get(col.collection_id, [])
        media_field = media_service.extend_media_list_fields(medias)
        collection_item.update(media_field)

        collection_list.append(collection_item)

    # 转换展览数据格式
    exhibition_media_map = media_service.select_museum_media_list_batch(object_ids=[exh.exhibition_id for exh in exhibitions], object_type='exhibition', media_type='1')
    exhibition_list = []
    for exh in exhibitions:
        exhibition_item = {
            "id": exh.exhibition_id,
            "title": exh.exhibition_name or "",
            "description": exh.description or "",
            "date": exh.get_formated_date(),
            "place": exh.hall or "",
            "status": exh.get_status(),
            "statusText": exh.get_status_text(),
            "img": "",  # 后续可以从媒体表获取图片
            "organizer": exh.organizer or "",
            "startTime": exh.start_time.strftime('%Y-%m-%d') if exh.start_time else "",
            "endTime": exh.end_time.strftime('%Y-%m-%d') if exh.end_time else ""
        }
        # 从媒体表获取展览图片
        medias = exhibition_media_map.get(exh.exhibition_id, [])
        media_field = media_service.extend_media_list_fields(medias)
        exhibition_item.update(media_field)
        
        exhibition_list.append(exhibition_item)

    # 转换活动数据格式
    activity_media_map = media_service.select_museum_media_list_batch(object_ids=[act.activity_id for act in activities], object_type='activity', media_type='1')
    activity_list = []
    for act in activities:
        activity_item = {
            "id": act.activity_id,
            "title": act.activity_name or "",
            "description": act.introduction or "",
            "type": act.activity_type or "",
            "location": act.location or "",
            "maxRegistration": act.max_registration or 0,
            "registrationCount": act.registration_count or 0,
            "presenter": act.presenter or "",
            "targetAudience": act.target_audience or "",
            "startTime": act.activity_start_time.strftime('%Y-%m-%d') if act.activity_start_time else "",
            "endTime": act.activity_end_time.strftime('%Y-%m-%d') if act.activity_end_time else "",
            "time": act.get_formatted_time(),
        }

        # 从媒体表获取活动图片
        medias = activity_media_map.get(act.activity_id, [])
        media_field = media_service.extend_media_list_fields(medias)
        activity_item.update(media_field)

        activity_list.append(activity_item)
    
    # 构建首页数据
    home_data = {
        "museum": {
            "id": museum.museum_id,
            "name": museum.museum_name,
            "description": museum.description,
            "openStatus": "今日开放",
            "openTime": "10:00 - 18:00",
            "bgImageList": [media.media_url for media in media_list] if media_list else []
        },
        "collections": collection_list,
        "exhibitions": exhibition_list,
        "educations": activity_list,
    }
    return AjaxResponse.from_success(data=home_data)


@reg.api.route('/wx/museum/exhibition/<int:museum_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def exhibition_list_by_museum(museum_id: int):
    """根据博物馆ID获取展览列表"""
    # 从数据库获取真实数据
    media_service = MuseumMediaService()
    exhibition_service = ExhibitionService()

    # 获取该博物馆下的展览列表
    exhibition = Exhibition()
    exhibition.museum_id = museum_id
    exhibition.status = 0  # 只获取正常状态的展览
    exhibitions = exhibition_service.select_exhibition_list(exhibition)

    # 批量获取展览图片
    exhibition_media_map = media_service.select_museum_media_list_batch(
        object_ids=[exh.exhibition_id for exh in exhibitions],
        object_type='exhibition',
        media_type='1'
    )

    # 转换展览数据格式
    exhibition_list = []
    for exh in exhibitions:
        exhibition_item = {
            "id": exh.exhibition_id,
            "title": exh.exhibition_name or "",
            "description": exh.description or "",
            "date": exh.get_formated_date(),
            "place": exh.hall or "",
            "status": exh.get_status(),
            "statusText": exh.get_status_text(),
            "organizer": exh.organizer or "",
            "startTime": exh.start_time.strftime('%Y-%m-%d') if exh.start_time else "",
            "endTime": exh.end_time.strftime('%Y-%m-%d') if exh.end_time else "",
            "exhibitionType": exh.get_exhibtion_type_desc(),
            "contentTags": exh.content_tags or ""
        }
        # 从媒体表获取展览图片
        exhibition_medias = exhibition_media_map.get(exh.exhibition_id, [])
        medias_field = media_service.extend_media_list_fields(exhibition_medias)        
        exhibition_item.update(medias_field)

        exhibition_list.append(exhibition_item)

    return AjaxResponse.from_success(data=exhibition_list)


@reg.api.route('/wx/museum/exhibition/detail/<int:exhibition_id>', methods=["GET"])
@require_wx_token
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
        "date": exhibition.get_formated_date(),
        "startDate": exhibition.start_time.strftime('%Y-%m-%d') if exhibition.start_time else "",
        "endDate": exhibition.end_time.strftime('%Y-%m-%d') if exhibition.end_time else "",
        "organizer": exhibition.organizer or "",
        "hall": exhibition.hall or "",
        "exhibitionType": exhibition.get_exhibtion_type_desc(),
        "contentTags": exhibition.content_tags or "",
        "sections": exhibition.sections or "",
    }
    media_fields = media_service.extend_media_list_fields(exhibition_medias)
    exhibition_data.update(media_fields)

    # 获取展览单元的媒体
    unit_medias_map = media_service.select_museum_media_list_batch(
        object_ids=[unit.unit_id for unit in exhibition_units],
        object_type='exhibition_unit',
        media_type=[1,2,3]
    )

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
        }

        # 获取展览单元的媒体
        unit_medias = unit_medias_map.get(unit.unit_id, [])
        unit_medias_field = media_service.extend_media_list_fields(unit_medias)
        unit_data.update(unit_medias_field)
        
        units_data.append(unit_data)

    # 构建返回数据
    detail_data = {
        "exhibition": exhibition_data,
        "units": units_data
    }

    return AjaxResponse.from_success(data=detail_data)


@reg.api.route('/wx/museum/exhibition/unit/detail/<int:unit_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def unit_detail(unit_id: int):
    """获取展览单元详情，包括媒体列表"""
    # 获取服务实例
    exhibition_unit_service = ExhibitionUnitService()
    media_service = MuseumMediaService()
    collection_service = CollectionService()

    # 获取展览单元信息
    unit = exhibition_unit_service.select_exhibition_unit_by_id(unit_id)
    if not unit:
        return AjaxResponse.from_error(msg="展览单元不存在")

    # 获取关联的展览信息
    exhibition_service = ExhibitionService()
    exhibition = exhibition_service.select_exhibition_by_id(unit.exhibition_id)
    
    # 获取展览单元的媒体
    unit_medias = media_service.select_museum_media_list(
        object_id=unit_id, 
        object_type='exhibition_unit', 
        media_type=[1,2,3]  # 1为图片，2为视频，3为音频
    )
    
    # 构建单元详情数据
    unit_data = {
        "id": unit.unit_id,
        "name": unit.unit_name or "",
        "type": unit.unit_type,  # 0展品单元 1文字单元 2多媒体单元
        "section": unit.section or "",
        "sortOrder": unit.sort_order or 0,
        "exhibitLabel": unit.exhibit_label or "",
        "guideText": unit.guide_text or "",
        "collections": unit.collections or "",  # JSON字符串格式的藏品ID列表
        "exhibitionId": unit.exhibition_id,
        "exhibitionName": exhibition.exhibition_name if exhibition else "",
    }

    unit_medias_field = media_service.extend_media_list_fields(unit_medias)
    unit_data.update(unit_medias_field)

    # 如果是展品单元，获取关联的藏品信息和媒体
    collection_list = _get_unit_collections(unit)
    if collection_list and len(collection_list) > 0:
        unit_data["collectionsDetail"] = collection_list

    return AjaxResponse.from_success(data=unit_data)


def _get_unit_collections(unit: ExhibitionUnit) -> list:
    """获取展览单元关联的藏品列表"""

    # 获取服务实例
    media_service = MuseumMediaService()
    collection_service = CollectionService()

    if unit.unit_type == 0 and unit.collections:
        import json
        try:
            collection_ids = json.loads(unit.collections) if unit.collections else []
        except json.JSONDecodeError:
            collection_ids = []

        collections = collection_service.select_collection_by_ids(collection_ids)
        collection_medias_map = media_service.select_museum_media_list_batch(
            object_ids=collection_ids,
            object_type='collection',
            media_type='1'
        )

        collection_list = []
        for collection in collections:
            collection_data = {
                "id": collection.collection_id,
                "name": collection.collection_name or "",
                "age": collection.age or "",
                "description": collection.description or "",
                "material": collection.material or "",
                "sizeInfo": collection.size_info or "",
                "author": collection.author or "",
                "type": collection.collection_type or "",
            }
            # 添加藏品的媒体列表
            collection_medias = collection_medias_map.get(collection.collection_id, [])
            media_fields = media_service.extend_media_list_fields(collection_medias)
            collection_data.update(media_fields)

            collection_list.append(collection_data)
        
        return collection_list
    return None


@reg.api.route('/wx/museum/collection/<int:museum_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def collection_list_by_museum(museum_id: int):
    """获取藏品列表，供小程序端使用"""
    # 获取服务实例
    collection_service = CollectionService()
    media_service = MuseumMediaService()

    # 从查询参数获取过滤条件
    # page_num = request.args.get('pageNum', 1, type=int)
    # page_size = request.args.get('pageSize', 10, type=int)
    
    # 构建查询条件
    collection_query = Collection()
    if museum_id > 0:
        collection_query.museum_id = museum_id
    collection_query.status = 0  # 只获取正常状态的藏品

    # 获取藏品列表
    collections = collection_service.select_collection_list(collection_query)

    # 从媒体表获取藏品图片
    collection_medias_map = media_service.select_museum_media_list_batch(
        object_ids=[col.collection_id for col in collections],
        object_type='collection',
        media_type='1'
    )
    
    # 转换藏品数据格式，适配小程序前端需求
    collection_list = []
    for col in collections:
        collection_item = {
            "id": col.collection_id,
            "name": col.collection_name or "",
            "type": col.collection_type or "",
            "age": col.age or "",
            "material": col.material or "",
            "sizeInfo": col.size_info or "",
            "author": col.author or "",
            "description": col.description or "",
            "museumId": col.museum_id
        }
        
        # 从媒体表获取藏品图片
        collection_medias = collection_medias_map.get(col.collection_id, [])
        medias_field = media_service.extend_media_list_fields(collection_medias)
        collection_item.update(medias_field)

        collection_list.append(collection_item)

    return AjaxResponse.from_success(data=collection_list)


@reg.api.route('/wx/museum/collection/detail/<int:collection_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def collection_detail(collection_id: int):
    """获取藏品详情，供小程序端使用"""
    # 获取服务实例
    collection_service = CollectionService()
    media_service = MuseumMediaService()

    # 根据ID获取藏品信息
    collection = collection_service.select_collection_by_id(collection_id)
    if not collection:
        return AjaxResponse.from_error(msg="藏品不存在")
    
    # 获取藏品媒体（包括图片、视频、音频）
    medias = media_service.select_museum_media_list(
        object_id=collection_id, 
        object_type='collection', 
        media_type=[1, 2, 3]  # 1为图片，2为视频，3为音频
    )
    
    # 构建藏品详情数据
    collection_detail = {
        "id": collection.collection_id,
        "name": collection.collection_name or "",
        "type": collection.collection_type or "",
        "age": collection.age or "",
        "material": collection.material or "",
        "sizeInfo": collection.size_info or "",
        "author": collection.author or "",
        "description": collection.description or "",
        "museumId": collection.museum_id,
        "museumName": "",  # 后续可从博物馆表获取名称
    }

    medias_field = media_service.extend_media_list_fields(medias)
    collection_detail.update(medias_field)

    museum_service = MuseumService()
    museum = museum_service.select_museum_by_id(collection.museum_id)
    if museum:
        collection_detail["museumName"] = museum.museum_name or ""

    return AjaxResponse.from_success(data=collection_detail)

# 在现有代码基础上添加以下两个函数（插入在exhibition_list_by_museum之后）

@reg.api.route('/wx/museum/activity/<int:museum_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def activity_list_by_museum(museum_id: int):
    """根据博物馆ID获取教育活动列表"""
    # 从数据库获取真实数据
    media_service = MuseumMediaService()
    activity_service = ActivityService()

    # 获取该博物馆下的活动列表
    activity = Activity()
    activity.museum_id = museum_id
    activity.status = 0  # 只获取正常状态的活动
    activities = activity_service.select_activity_list(activity)

    # 从媒体表获取活动图片
    activity_medias_map = media_service.select_museum_media_list_batch(
        object_ids=[act.activity_id for act in activities],
        object_type='activity',
        media_type='1'
    )

    # 转换活动数据格式
    activity_list = []
    for act in activities:
        activity_item = {
            "id": act.activity_id,
            "title": act.activity_name or "",
            "description": act.introduction or "",
            "type": act.activity_type or "",
            "location": act.location or "",
            "maxRegistration": act.max_registration or 0,
            "registrationCount": act.registration_count or 0,
            "presenter": act.presenter or "",
            "targetAudience": act.target_audience or "",
            "startTime": act.activity_start_time.strftime('%Y-%m-%d') if act.activity_start_time else "",
            "endTime": act.activity_end_time.strftime('%Y-%m-%d') if act.activity_end_time else "",
            "contentTags": act.activity_type or "",  # 活动类型作为标签 
            "canRegister": act.can_register(),
            "status": act.get_status_display(),
            "time": act.get_formatted_time(),
        }

        # 从媒体表获取活动图片
        activity_medias = activity_medias_map.get(act.activity_id, [])
        medias_field = media_service.extend_media_list_fields(activity_medias)        
        activity_item.update(medias_field)

        activity_list.append(activity_item)

    return AjaxResponse.from_success(data=activity_list)


@reg.api.route('/wx/museum/activity/detail/<int:activity_id>', methods=["GET"])
@require_wx_token
@JsonSerializer()
def activity_detail(activity_id: int):
    """获取教育活动详情"""
    # 获取服务实例
    activity_service = ActivityService()
    media_service = MuseumMediaService()

    # 获取活动信息
    activity = activity_service.select_activity_by_id(activity_id)
    if not activity:
        return AjaxResponse.from_error(msg="活动不存在")

    # 获取活动媒体
    activity_medias = media_service.select_museum_media_list(
        object_id=activity_id, 
        object_type='activity', 
        media_type='1'
    )
    # 构建活动详情数据
    activity_detail = {
        "id": activity.activity_id,
        "title": activity.activity_name or "",
        "description": activity.introduction or "",
        "type": activity.activity_type or "",
        "location": activity.location or "",
        "maxRegistration": activity.max_registration or 0,
        "registrationCount": activity.registration_count or 0,
        "presenter": activity.presenter or "",
        "targetAudience": activity.target_audience or "",
        "startTime": activity.activity_start_time.strftime('%Y-%m-%d %H:%M') if activity.activity_start_time else "",
        "endTime": activity.activity_end_time.strftime('%Y-%m-%d %H:%M') if activity.activity_end_time else "",
        "status": activity.get_status_display(),
        "time": activity.get_formatted_time(),
        "canRegister": activity.can_register(),
    }

    medias_field = media_service.extend_media_list_fields(activity_medias)
    activity_detail.update(medias_field)

    # 检查用户是否已预约该活动
    activity_reservation_service = ActivityReservationService()
    existing_reservation = activity_reservation_service.select_activity_reservation_by_activity_and_user(
        activity_id, g.wx_user_id
    )

    activity_detail["isReserved"] = bool(existing_reservation)
    activity_detail["reservationId"] = existing_reservation.reservation_id if existing_reservation else None

    return AjaxResponse.from_success(data=activity_detail)


@reg.api.route('/wx/my/activity_reservation/', methods=["GET"])
@require_wx_token
@JsonSerializer()
def wx_my_activity_reservation_list():
    """
    获取当前微信用户的活动预约清单
    """    
    activity_reservation_entity = ActivityReservation()
    activity_reservation_entity.wx_user_id = g.wx_user_id
    
    activity_reservation_service = ActivityReservationService()
    media_service = MuseumMediaService()
    activity_service = ActivityService()
    
    reservations = activity_reservation_service.select_activity_reservation_list(activity_reservation_entity)
    activity_medias_map = media_service.select_museum_media_list_batch(
        object_ids=[reservation.activity_id for reservation in reservations],
        object_type='activity',
        media_type='1'
    )
    
    # 构造包含活动详细信息的预约清单
    reservation_list = []
    for reservation in reservations:
        activity = activity_service.select_activity_by_id(reservation.activity_id)
        if activity:
            reservation_info = {
                "reservationId": reservation.reservation_id,
                "activityId": reservation.activity_id,
                "title": activity.activity_name or "",
                "description": activity.introduction or "",
                "location": activity.location or "",
                "startTime": activity.activity_start_time.strftime('%Y-%m-%d %H:%M') if activity.activity_start_time else "",
                "endTime": activity.activity_end_time.strftime('%Y-%m-%d %H:%M') if activity.activity_end_time else "",
                "registrationTime": reservation.registration_time.strftime('%Y-%m-%d %H:%M') if reservation.registration_time else "",
                "phoneNumber": reservation.phone_number or "",
                "status": activity.get_status_display(),
                "time": activity.get_formatted_time(),
            }

            # 从媒体表获取活动图片
            activity_medias = activity_medias_map.get(reservation.activity_id, [])
            medias_field = media_service.extend_media_list_fields(activity_medias)
            reservation_info.update(medias_field)

            reservation_list.append(reservation_info)
    
    return AjaxResponse.from_success(data=reservation_list)


@reg.api.route('/wx/my/activity_reservation/<int:activity_id>', methods=['POST'])
@require_wx_token
@JsonSerializer()
def wx_add_activity_reservation(activity_id: int):
    """
    微信用户新增活动预约
    """
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not activity_id:
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='活动ID不能为空')
    
    activity_reservation_service = ActivityReservationService()
    result = activity_reservation_service.add_activity_reservation(activity_id, g.wx_user_id, phone_number)
    if result == '预约成功':
        return AjaxResponse.from_success(msg=result)
    else:
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg=result)


@reg.api.route('/wx/my/activity_reservation/<int:reservation_id>', methods=['DELETE'])
@require_wx_token
@JsonSerializer()
def wx_cancel_activity_reservation(reservation_id: int):
    """
    微信用户取消活动预约
    """
    activity_reservation_service = ActivityReservationService()
    result = activity_reservation_service.cancel_activity_reservation(reservation_id, g.wx_user_id)
    if result == '取消预约成功':
        return AjaxResponse.from_success(msg=result)
    else:
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg=result)