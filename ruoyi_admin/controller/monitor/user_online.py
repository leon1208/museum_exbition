# -*- coding: utf-8 -*-
# @Author  : YY

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, PathValidator
from ruoyi_system.service.sys_user_online import SysUserOnlineService
from ruoyi_system.domain.entity import SysUserOnline
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ... import reg


@reg.api.route('/monitor/online/list',methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm("monitor:online:list"))
@JsonSerializer()
def monitor_online_list(dto:SysUserOnline):
    '''
        获取在线用户列表
    '''
    rows = SysUserOnlineService.select_online_list(dto)
    return TableResponse(rows=rows)


@reg.api.route('/monitor/online/<string:id>',methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm("monitor:online:forceLogout"))
@Log(title = "在线用户", business_type = BusinessType.FORCE)
@JsonSerializer()
def monitor_online_logout(id:str):
    '''
        强制退出登录
    '''
    SysUserOnlineService.force_logout(id)
    return AjaxResponse.from_success()
    
