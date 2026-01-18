# -*- coding: utf-8 -*-
# @Author  : LeeOn123

import requests
# import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
# from exb_museum.domain.entity.wx_user import WxUserPo
# from ruoyi_admin.ext import db
from ruoyi_framework.config import TokenConfig
import jwt
import logging
# from ruoyi_admin.config.wx_config import WxConfig

from exb_museum.service.museum_service import MuseumService

logger = logging.getLogger(__name__)

# 微信API基础URL
WX_API_BASE_URL = 'https://api.weixin.qq.com'
# 登录code换session的API
WX_LOGIN_URL = f'{WX_API_BASE_URL}/sns/jscode2session'

class WxAuthService:
    """
    微信小程序认证服务
    """
    
    def __init__(self):
        # 使用配置文件中的值
        # self.app_id = WxConfig.WX_APP_ID
        # self.app_secret = WxConfig.WX_APP_SECRET
        self.token_config = TokenConfig()
        
    def code_to_session(self, app_id: str, app_secret: str, code: str) -> Optional[Dict[str, Any]]:
        """
        使用code换取session_key等信息
        
        Args:
            code: 微信登录凭证
            
        Returns:
            包含openid、session_key等信息的字典，失败则返回None
        """
        url = WX_LOGIN_URL
        params = {
            'appid': app_id,
            'secret': app_secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.get(url, params=params)
            result = response.json()
            
            if 'errcode' in result:
                logger.error(f"获取session失败: {result}")
                return None
                
            return result
        except Exception as e:
            logger.error(f"请求微信API失败: {str(e)}")
            return None
    
    def generate_access_token(self, open_id: str) -> str:
        """
        生成JWT访问令牌
        
        Args:
            user_id: 用户ID
            
        Returns:
            JWT令牌字符串
        """
        payload = {
            'openid': open_id,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=self.token_config.expire_seconds()),
            'iat': datetime.now(timezone.utc)
        }
        
        token = jwt.encode(payload, self.token_config.secret, algorithm='HS256')
        return token
    
    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证访问令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            解码后的payload，验证失败则返回None
        """
        try:
            payload = jwt.decode(token, self.token_config.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("令牌已过期")
            return None
        except jwt.InvalidTokenError:
            logger.warning("无效令牌")
            return None
    
    def verify_request(self, method: str, path: str, body: str, timestamp: int, nonce: str, sign: str, token: str):
        # ts = int(req.headers['X-Timestamp'])
        # nonce = req.headers['X-Nonce']
        # sign = req.headers['X-Sign']

        # 1. 时间窗口（5 分钟）
        now = int(datetime.now(timezone.utc).timestamp())
        if abs(now - timestamp) > 300:
            return False
            # raise Exception("timestamp expired")

        # 2. nonce 是否已使用
        # if redis.exists(f"nonce:{payload['openid']}:{nonce}"):
        #     raise Exception("replay attack")

        # 3. 计算签名
        # body = req.get_data(as_text=True) or ''
        sign_str = "\n".join([
            method,
            path,
            body,
            str(timestamp),
            nonce,
            token
        ])
        from hashlib import sha256
        expected = sha256(sign_str.encode('utf-8')).hexdigest()

        if sign != expected:
            return False
            # raise Exception("invalid signature")
        # 4. 记录 nonce（TTL = 时间窗口）
        # redis.setex(
        #     f"nonce:{payload['openid']}:{nonce}",
        #     300,
        #     1
        # )

        return True

    def get_or_create_wx_user(self, app_id: str, code: str) -> str:
        """
        通过code获取或创建微信用户
        
        Args:
            code: 微信登录凭证
            
        Returns:
            包含openid的字符串，失败则返回空字符串
        """
        # 通过app_id从数据库查询出app_secret
        museum_service = MuseumService()
        museum = museum_service.select_museum_by_app_id(app_id)
        if not museum or not museum.app_secret:
            return None
        
        app_secret = museum.app_secret
        # 使用code换取session信息
        session_info = self.code_to_session(app_id, app_secret, code)
        if not session_info or 'openid' not in session_info:
            return None
            
        openid = session_info['openid']
        return openid
        
        # # 查找或创建用户
        # wx_user = db.session.query(WxUserPo).filter_by(openid=openid).first()
        
        # if not wx_user:
        #     # 创建新用户
        #     wx_user = WxUserPo(
        #         openid=openid,
        #         session_key=session_key,
        #         status=0,  # 默认启用
        #         del_flag=0  # 未删除
        #     )
        #     db.session.add(wx_user)
        # else:
        #     # 更新session_key
        #     wx_user.session_key = session_key
            
        # db.session.commit()
        
        # return wx_user
    
    # def login_with_code(self, code: str) -> Optional[Dict[str, Any]]:
    #     """
    #     使用code进行登录
        
    #     Args:
    #         code: 微信登录凭证
            
    #     Returns:
    #         包含用户信息和token的字典，失败则返回None
    #     """
    #     wx_user = self.get_or_create_wx_user(code)
    #     if not wx_user:
    #         return None
            
    #     # 生成访问令牌
    #     access_token = self.generate_access_token(wx_user.user_id)
        
    #     # 更新用户记录中的token
    #     wx_user.access_token = access_token
    #     wx_user.expires_in = datetime.utcnow() + timedelta(seconds=self.token_config.expire_seconds())
    #     db.session.commit()
        
    #     return {
    #         'user_id': wx_user.user_id,
    #         'openid': wx_user.openid,
    #         'access_token': access_token,
    #         'expires_in': self.token_config.expire_seconds(),
    #         'nickname': wx_user.nickname,
    #         'avatar': wx_user.avatar
    #     }
    
    # def refresh_user_info(self, openid: str, user_info: Dict[str, Any]) -> bool:
    #     """
    #     刷新用户信息
        
    #     Args:
    #         openid: 用户openid
    #         user_info: 用户信息字典
            
    #     Returns:
    #         更新成功返回True，否则返回False
    #     """
    #     try:
    #         wx_user = db.session.query(WxUserPo).filter_by(openid=openid).first()
    #         if not wx_user:
    #             return False
                
    #         # 更新用户信息
    #         wx_user.nickname = user_info.get('nickName')
    #         wx_user.avatar = user_info.get('avatarUrl')
    #         wx_user.gender = user_info.get('gender', 0)
    #         wx_user.country = user_info.get('country')
    #         wx_user.province = user_info.get('province')
    #         wx_user.city = user_info.get('city')
    #         wx_user.language = user_info.get('language')
            
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         logger.error(f"更新用户信息失败: {str(e)}")
    #         return False