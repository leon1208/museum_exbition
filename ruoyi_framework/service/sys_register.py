# -*- coding: utf-8 -*-

from flask import flash

from ruoyi_common.domain.vo import RegisterBody
from ruoyi_common.utils import security_util as SecurityUtil
from ruoyi_common.constant import Constants, UserConstants
from ruoyi_common.exception import CaptchaException, CaptchaExpireException, NotContentException
from ruoyi_common.domain.entity import SysUser
from ruoyi_system.service import SysUserService, SysConfigService
from ruoyi_system.mapper import SysUserMapper
from ruoyi_admin.ext import redis_cache


class RegisterService:

    @classmethod
    def register(cls, body: RegisterBody) -> str:
        """
        注册用户

        Args:
            body (RegisterBody): 注册信息

        Returns:
            str: 注册结果信息
        """
        msg = ""
        username = body.username
        password = body.password

        captcha_on_off = SysConfigService.select_captcha_on_off()
        # Captcha switch
        if captcha_on_off:
            cls.validate_captcha(username, body.code, body.uuid)

        if not username:
            msg = "Username cannot be empty"
        elif not password:
            msg = "User password cannot be empty"
        elif len(username) < UserConstants.USERNAME_MIN_LENGTH or len(username) > UserConstants.USERNAME_MAX_LENGTH:
            msg = "Account length must be between 2 and 20 characters"
        elif len(password) < UserConstants.PASSWORD_MIN_LENGTH or len(password) > UserConstants.PASSWORD_MAX_LENGTH:
            msg = "Password length must be between 5 and 20 characters"
        elif SysUserMapper.check_user_name_unique(username) > 0:
            msg = f"Failed to save user '{username}', registration account already exists"
        else:
            sys_user = SysUser(
                user_name=username,
                nick_name=username,
                password=SecurityUtil.encrypt_password(body.password.get_secret_value())
            )
            reg_flag = SysUserService.register_user(sys_user)
            if not reg_flag:
                msg = "Registration failed, please contact system administrator"
            else:
                flash("user.register.success")
        return msg

    @classmethod
    def validate_captcha(cls, username: str, code: str, uuid: str):
        """
        验证码校验

        Args:
            username (str): 用户名
            code (str): 验证码
            uuid (str): 验证码唯一标识

        Raises:
            CaptchaException: 验证码错误
            CaptchaExpireException: 验证码过期
        """
        if not code:
            raise NotContentException()
        verify_key = Constants.CAPTCHA_CODE_KEY + (uuid if uuid is not None else "")
        captcha: bytes = redis_cache.get(verify_key)
        if not captcha:
            raise CaptchaExpireException()
        redis_cache.delete(verify_key)
        if code.lower() != captcha.decode("utf-8").lower():
            raise CaptchaException()
