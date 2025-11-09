# -*- coding: utf-8 -*-
# @Author  : YY

from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_framework.domain.entity import RedisCache
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_admin.ext import redis_cache
from ... import reg


@reg.api.route('/monitor/cache',methods=['GET'])
@PreAuthorize(HasPerm("monitor:cache:list"))
@JsonSerializer()
def monitor_cache():
    '''
        获取缓存信息
    '''
    cache = RedisCache.from_connection(redis_cache)
    return AjaxResponse.from_success(data = cache)
