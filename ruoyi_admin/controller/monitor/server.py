# -*- coding: utf-8 -*-
# @Author  : YY

from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_framework.domain.entity import Server
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ... import reg


@reg.api.route('/monitor/server',methods=['GET'])
@PreAuthorize(HasPerm("monitor:server:list"))
@JsonSerializer()
def monitor_server_get():
    '''
        获取服务器信息
    '''
    server = Server.from_module()
    return AjaxResponse.from_success(data = server)
