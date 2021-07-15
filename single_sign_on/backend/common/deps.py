#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-03-01 11:37:21
# @Author  : chen lei
# @Email   : senouit@163.com
# @Desc    :

"""
一些通用的依赖功能
"""

import env

from datetime import timedelta, datetime
from jose import jwt        # 安装依赖包：pip install python-jose 参照 https://pypi.org/project/python-jose/


def create_access_token(subject: str) -> str:
    """
    生成 token(常用参数含义)
        iss 【issuer】发布者的url地址
        sub 【subject】该JWT所面向的用户，用于处理特定应用，不是常用的字段
        aud 【audience】接受者的url地址
        exp 【expiration】 该jwt销毁的时间；unix时间戳
        nbf 【not before】 该jwt的使用时间不能早于该时间；unix时间戳
        iat 【issued at】 该jwt的发布时间；unix 时间戳
        jti 【JWT ID】 该jwt的唯一ID编号
    """
    expire = datetime.now() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(subject), "exp": expire}
    encode_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
    return encode_jwt


def check_jwt_token(token: str) -> str:
    """
    获取解析后的 token
    token: 用户的 token
    """
    try:
        decode_token = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])  # 解析 token

        current_time = datetime.now()           # 系统当前时间
        expiration_time = datetime.fromtimestamp(decode_token.get('exp')) - timedelta(hours=8)  # token 过期时间
        if current_time > expiration_time:      # 验证 token 是否过期
            message = "token 已过期"
            return None, message
    except jwt.JWTError:
        message = "用户身份验证失败"
        return None, message
    message = "token 认证成功"
    return decode_token, message




