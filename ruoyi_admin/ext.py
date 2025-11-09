# -*- coding: utf-8 -*-
# @Author  : YY

from werkzeug.local import LocalProxy
from flask import current_app

from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_cors import CORS
from redis import Redis

from ruoyi_common.ruoyi.extension import FlaskRuoYi
from ruoyi_common.sqlalchemy.extension import SQLAlchemy
    

ruoyi = FlaskRuoYi()
cors = CORS()

fredis = FlaskRedis()
redis_cache:Redis = LocalProxy(
    lambda: current_app.extensions["redis"]._redis_client
) 
lm = LoginManager()
lm.login_view = 'api.login.index_login'
db = SQLAlchemy()
