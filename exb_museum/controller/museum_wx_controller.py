# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_controller.py
# @Time    : 2024-05-20 14:00:00

from flask import request
from flask_login import login_required
from typing import List
from werkzeug.datastructures import FileStorage

from exb_museum.service.museum_media_service import MuseumMediaService
from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, FileUploadValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize

from exb_museum.domain.entity import MuseumMedia, Museum
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

    # 获取博物馆信息
    museum = museum_service.select_museum_by_app_id(app_id)
    if not museum:
        return AjaxResponse.from_error(msg="博物馆不存在")
    
    # 获取展览媒体
    media_list = media_service.select_museum_media_list(museum_id=museum.museum_id, media_type='1')

    # 这里可以替换为从数据库获取真实数据
    home_data = {
        "museum": {
            "name": museum.museum_name,
            "description": museum.description,
            "openStatus": "今日开放",
            "openTime": "10:00 - 18:00",
            "bgImage": media_list[0].media_url
        },
        "collections": [
            {
                "title": "明代青花瓷",
                "period": "明朝",
                "img": "/wx_static/tmp_images/it01.png"
            },
            {
                "title": "皇家金冠",
                "period": "18世纪",
                "img": "/wx_static/tmp_images/it02.png"
            },
            {
                "title": "青铜短剑",
                "period": "青铜时代",
                "img": "/wx_static/tmp_images/it03.png"
            }
        ],
        "exhibitions": [
            {
                "title": "2024 现代艺术展",
                "desc": "一场当代表现主义的探索之旅。",
                "date": "10月12日 - 12月30日",
                "place": "二层 A厅",
                "status": "hot",
                "statusText": "正在热展",
                "img": "/wx_static/tmp_images/exb01.png"
            },
            {
                "title": "罗马帝国的荣耀",
                "desc": "探索塑造世界的伟大帝国。",
                "date": "1月10日 - 3月15日",
                "place": "中央大厅",
                "status": "upcoming",
                "statusText": "即将开展",
                "img": "/wx_static/tmp_images/exb02.png"
            }
        ],
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
