# -*- coding: utf-8 -*-
# @Author  : YY

from .registry import RuoYiModuleRegistry
from .config import RuoYiConfigLoader
from .log import RuoYiLog


'''
    FlaskRuoYi 是用来模块化基于flask应用的目录结构
'''

class FlaskRuoYi(object):
    
    def __init__(self,app=None,proot=None):
        if app is not None:
            if proot is None:
                proot = app.root_path
            self.init_app(app,proot)
        
    def init_app(self,app,proot=None):
        """
        初始化插件
        
        Args:
            app: Flask应用实例
            proot: 项目根目录
        """
        if proot is None:
            proot = app.root_path
        self.proot = proot
        app.extensions['flaskruoyi'] = self
        
        config_loader = RuoYiConfigLoader(app.root_path)
        config_loader.set_app(app)
        
        module_reg = RuoYiModuleRegistry(app,proot)
        module_reg.register_modules()
        
        log_handler = RuoYiLog.generate_handler_from_config(config_loader.cache)
        if log_handler:
            app.logger.addHandler(log_handler)
                

__all__ = ["FlaskRuoYi"]
