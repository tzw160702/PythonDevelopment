#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-02-25 16:32:12
# @Author  : wei
# @Email   :
# @Desc    :

"""
表模型
"""

from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

from database import Base


class AuditTime():
    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
    )

    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())


class User(Base, AuditTime):
    """
    用户表
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    email = Column(String(128), nullable=True, comment="邮箱")
    phone = Column(String(18), nullable=True, comment="手机号")
    username = Column(String(30), comment="用户名")
    hashed_password = Column(String(128), comment="hash加密后的密码")
    status = Column(Boolean, server_default="0", comment="用户状态(0：可用，1：禁用)")


class SignInLog(Base, AuditTime):
    """
    登录 token 日志表
    """
    __tablename__ = 'signin_log'

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    userid = Column(Integer, ForeignKey("user.id"), comment="用户表")
    token = Column(String(128), comment="用户 token")
    callback_url = Column(String(256), comment="回调地址")
    ip = Column(String(128), comment="登录 ip")
