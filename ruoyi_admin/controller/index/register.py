# -*- coding: utf-8 -*-
# @Author  : YY

from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import BodyValidator
from ruoyi_common.domain.vo import RegisterBody
from ruoyi_system.service import SysConfigService
from ruoyi_framework.service.sys_register import RegisterService
from ... import reg


@reg.api.route("/register", methods=["POST"])
@BodyValidator()
@JsonSerializer()
def index_register(dto: RegisterBody):
    '''
    注册接口
    '''
    value = SysConfigService.select_config_by_key("sys.account.registerUser")
    if value != "true":
        return AjaxResponse.from_error("当前系统没有开启注册功能！")
    msg = RegisterService.register(dto)
    if msg:
        return AjaxResponse.from_error(msg=msg)
    else:
        return AjaxResponse.from_success()
