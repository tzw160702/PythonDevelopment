#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-03-02 09:54:36
# @Author  :wei
# @Email   :
# @Desc    :

"""
操作数据库
"""

import models
import schemas

from fastapi import Request
from typing import Optional
from sqlalchemy.orm import Session

from database import engine
from models import User, SignInLog
from sqlalchemy.sql import func
import sqlalchemy_filters
import math
import json

models.Base.metadata.create_all(bind=engine)  # 生成数据库表


def save(db):
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_all_user(db: Session, paginate: json, filter: json, sort: json) -> Optional[User]:
    """
    查找所有可用状态的用户信息
    :param db:
    :param filter 过滤条件,数据模型为 [{"fieldname":"id","option":"is_not_null"}]', sort='[{"field":"id","direction":"desc"}]
    :param sort 排序条件，数据模型为  [{"field":"id","direction":"desc"}]
    :param paginate: 分页条件数据，数据模型为 {"page":1,"limit":10}
    :return:    用户信息
    """
    query = db.query(models.User)
    filters = []
    for f_data in filter:
        if "value" in f_data:
            j_data = {'model': 'User', 'field': f_data["fieldname"], 'op': f_data["option"], 'value': f_data["value"]}
        else:
            j_data = {'model': 'User', 'field': f_data["fieldname"], 'op': f_data["option"]}
        filters.append(j_data)

    filtered_query = sqlalchemy_filters.apply_filters(query, filters)

    count = len(filtered_query.all())
    sorts = []

    for s_data in sort:
        js_data = {"field": s_data['field'], "direction": s_data['direction']}
        sorts.append(js_data)
    data = sqlalchemy_filters.apply_sort(filtered_query, sorts)
    paginated_query, pagination = sqlalchemy_filters.apply_pagination(
        data, paginate['page'], paginate['limit']
    )
    result = paginated_query.all()
    page_count = int(math.ceil(count / paginate['limit']))
    return {"data": result, "data_count": count, "page": paginate['page'], "page_count": page_count,
            "page_size": paginate['limit']}


def get_user_by_id(db: Session, *, id: int) -> Optional[User]:
    """
    通过 用户id 查找用户信息
    :param db:
    :param id:  用户id
    :return:    用户对象信息
    """
    result = db.query(User).filter(User.id == id, User.status == 0).first()
    return result


def get_user_by_phone(db: Session, *, phone: str) -> Optional[User]:
    """
    通过手机号码查询用户信息
    :param db:
    :param phone:   手机号
    :return:        User 对象
    """
    db_user = db.query(User).filter(User.phone == phone, User.status == 0).first()
    return db_user


def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    """
    通过邮箱查询用户信息
    :param db:
    :param email:   邮箱
    :return:        User 对象
    """
    db_user = db.query(User).filter(User.email == email, User.status == 0).first()
    return db_user


def create_by_email(db: Session, *, email: str, pwd: str) -> Optional[int]:
    """
    通过邮箱注册账号
    :param db:
    :param email:   邮箱
    :param pwd:     HASH 后的新密码
    :return:        插入主键 id
    """
    user = User(email=email, hashed_password=pwd)
    db.add(user)
    save(db)
    db.refresh(user)
    return user.id


def create_by_phone(db: Session, *, phone: str, pwd: str) -> Optional[int]:
    """
    通过手机号码注册账号
    :param db:
    :param phone:   手机号码
    :param pwd:     HASH 后的新密码
    :return:        插入主键 id
    """
    user = User(phone=phone, hashed_password=pwd)
    db.add(user)
    save(db)
    db.refresh(user)
    return user.id


def update_user_info(db: Session, *, userid: str, obj_in: schemas.UserInfo) -> Optional[User]:
    """
    通过 用户id 更新用户信息
    :param db:
    :param userid           用户id
    :param obj_in           用户信息,包含了username：用户名,phone：手机号,email：邮箱
    :return:                修改后的用户对象信息
    """
    user = db.query(User).filter(User.id == userid).first()
    if obj_in.username:
        user.username = obj_in.username
    if obj_in.phone:
        user.phone = obj_in.phone
    if obj_in.email:
        user.email = obj_in.email
    save(db)
    db.refresh(user)
    return user


def update_user_status_by_id(db: Session, *, userid: int, status: int) -> Optional[User]:
    """
    更新用户账户状态信息
    :param db:
    :param userid:              用户 id
    :param status:          用户状态（0：可用，1：禁用）
    :return:
    """
    user = db.query(User).filter(User.id == userid).first()
    user.status = status
    save(db)
    db.refresh(user)
    return user


def update_password(db: Session, *, userid: int, pwd: str):
    """
    修改用户密码
    :param db:
    :param userid:      用户 id
    :param pwd:     HASH 后的新密码
    :return:
    """
    user = db.query(User).filter(User.id == userid).first()
    user.hashed_password = pwd
    save(db)
    db.refresh(user)
    return user


def add_token_logs(db: Session, ip: str, *, userid: int, token: str, callback_url: str) -> Optional[int]:
    """
    添加一条登录 token 日志信息
    :param db:
    :param ip:              ip地址
    :param userid:          用户 id
    :param token:           用户
    :param callback_url:    系统回调地址
    :return:                插入主键 id
    """
    db_token = SignInLog(userid=userid, token=token, callback_url=callback_url, ip=ip)
    db.add(db_token)
    save(db)
    db.refresh(db_token)
    return db_token.id


def get_user_by_token(db: Session, *, token: str) -> object:
    """
    token 对应的用户信息(关联 user 表)
    :param db:
    :param token:   用户 token
    :return:        用户信息和用户登录信息
    """
    info = db.query(SignInLog, User).join(User, SignInLog.userid == User.id).filter(
        SignInLog.token == token).first()
    return info


def update_tokeninfo_by_token(db: Session, *, token: str) -> Optional[SignInLog]:
    """
    更新 token 注销时间(登出)
    :param db:
    :param token:   用户 token
    :return:        SignInLog
    """
    sign_in_log = db.query(SignInLog).filter(SignInLog.token == token).first()
    sign_in_log.updated_at = func.now()
    save(db)
    db.refresh(sign_in_log)
    return sign_in_log
