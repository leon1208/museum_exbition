# -*- coding: utf-8 -*-

import asyncio
from flask import request, jsonify

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.descriptor.serializer import JsonSerializer

from .. import reg
from ruoyi_exb.service.web_scraper import take_website_screenshot, scrape_url_to_markdown


@reg.api.route("/aicrawl/hello", methods=["GET"])
@JsonSerializer()
def hello():
    return AjaxResponse.from_success(msg="新增成功")
    # return AjaxResponse.from_error(msg="请提供有效的URL")
    # return [{
    #     'status': 'success',
    #     'message': 'Hello, World!'
    # }]

@reg.api.route("/aicrawl/convert-url", methods=["POST"])
@JsonSerializer()
def convert_url():
    """将网页URL转换为Markdown格式"""
    # 获取请求数据
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return AjaxResponse.from_error(msg="请提供有效的URL")
    
    try:
        # 运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scrape_url_to_markdown(url))
        loop.close()
        return AjaxResponse.from_success(msg="提取成功", data=result)
    except Exception as e:
        return AjaxResponse.from_error(msg=f"处理过程中发生错误: {str(e)}")

@reg.api.route("/aicrawl/take-screenshot", methods=["POST"])
@JsonSerializer()
def take_screenshot():
    """对指定URL的网页进行截图"""    
    # 获取请求数据
    data = request.get_json()
    url = data.get('url')
    full_page = data.get('fullPage', False)
    
    if not url:
        return AjaxResponse.from_error(msg="请提供有效的URL")
    
    try:
        # 运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
        result = loop.run_until_complete(take_website_screenshot(url, full_page))
        loop.close()
        return AjaxResponse.from_success(msg="截屏成功", data=result)
    except Exception as e:
        return AjaxResponse.from_error(msg=f"处理过程中发生错误: {str(e)}")