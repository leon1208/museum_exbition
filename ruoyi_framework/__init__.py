# -*- coding: utf-8 -*-
# @Author  : YY

import sys
from types import ModuleType

from ruoyi_common.descriptor.listener import ModuleSignalListener
from ruoyi_common.base.signal import module_initailize
from ruoyi_common.ruoyi.registry import RuoYiModuleRegistry


@ModuleSignalListener(sys.modules[__name__],module_initailize)
def import_hook(module:ModuleType, registry:RuoYiModuleRegistry):
    """
    导入模块

    Args:
        module: 模块对象
        module_register: 模块注册器
    """
    pass
