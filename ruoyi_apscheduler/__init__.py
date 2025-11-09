# -*- coding: utf-8 -*-
# @Author  : YY

import sys
from types import ModuleType
from apscheduler.schedulers.background import BackgroundScheduler

from ruoyi_common.descriptor.listener import ModuleSignalListener
from ruoyi_common.base.signal import module_initailize
from ruoyi_common.ruoyi.registry import RuoYiModuleRegistry
from ruoyi_apscheduler.config import EXECUTORS, JOB_DEFAULTS, TIMEZONE


reg: RuoYiModuleRegistry
scheduler: BackgroundScheduler


@ModuleSignalListener(sys.modules[__name__],module_initailize)
def import_hook(module:ModuleType, registry:RuoYiModuleRegistry):
    """
    导入模块

    Args:
        module: 模块对象
        module_register: 模块注册器
    """
    global scheduler
    scheduler = BackgroundScheduler(
        executors=EXECUTORS,
        timezone=TIMEZONE,
        job_defaults=JOB_DEFAULTS
    )
    
    global reg
    reg = registry
