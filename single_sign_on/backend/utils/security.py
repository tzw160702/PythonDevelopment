#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-03-01 10:36:17
# @Author  : chen lei
# @Email   : senouit@163.com
# @Desc    :

"""
密码、安全系列
"""

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    获取 hash 后的密码
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 原密码
    :param hashed_password: hash后的密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

