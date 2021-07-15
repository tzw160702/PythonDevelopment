#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-03-01 10:15:47
# @Author  : chen lei
# @Email   : senouit@163.com
# @Desc    :

"""
业务逻辑层
"""

import re
import random
import string
import json

import schemas
import crud

from fastapi import Request
from sqlalchemy.orm import Session

from utils import security, verify_code
from common import deps, logger

RE_EMAIL = r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$"  # 邮箱校验正则表达式
RE_PHONE = r"^1[3|4|5|6|7|8][0-9]{9}$"  # 手机号校验正则表达式


def get_verify_code(*, number: str):
    """
    获取 邮箱/短信 验证码
    :param db:
    :param number:  邮箱或手机号
    :return:
    """

    code = "".join(random.sample(string.digits, k=6))  # 自动生成 6位 随机数
    # 判断账号为邮箱还是手机号
    if re.match(RE_EMAIL, number):
        re_code = verify_code.get_email_code(email=number, email_code=code)
    elif re.match(RE_PHONE, number):
        re_code = verify_code.get_phone_code(phone=number, phone_code=code)
    else:
        message = "输入账号信息有误，请重新输入"
        logger.error(message)
        return None, message

    if not re_code:
        message = f"账号为 {number} 的验证码发送失败"
        logger.error(message)
    else:
        message = "验证码发送成功"
    return re_code, message


def get_client_code():
    """
    获取客户端验证码
    :return:
    """
    client_code = "".join(random.sample(string.hexdigits, k=6))  # 自动生成 6位 随机字符串
    return client_code


def get_userinfo_by_id(db: Session, id: int):
    """
    通过 用户id 查询用户信息
    :param db:
    :param id:  用户id
    :return:    用户信息
    """
    user = crud.get_user_by_id(db, id=id)
    if not user:
        message = "该用户不存在"
        logger.error(message)
    else:
        message = "用户信息查询成功"
    return user, message


def get_users(db: Session, paginate: str, filter: str, sort: str):
    """
    查询所有用户信息
    :param db:
    :param paginate:        当前第几页，每页显示的条数
    :param filter:          查询条件
    :param sort:            排序
    :return:                用户信息列表
    """
    js_paginate = json.loads(paginate)
    js_filter = json.loads(filter)
    js_sort = json.loads(sort)
    users = crud.get_all_user(db, paginate=js_paginate, filter=js_filter, sort=js_sort)
    if users:
        message = "查询成功"
    return users, message


def sign_in(db: Session, request: Request, *, obj_in: schemas.LogInByPwd, redis_client_code: str):
    """
    用户使用密码登陆
    :param db:
    :param number:              手机号或者邮箱
    :param pwd:                 密码
    :param client_code:         客户端登录验证码
    :param callback_url:        系统回调地址
    :param redis_client_code:   存储在 redis 中的页面打开验证码
    :return:                    userid, token, message
    """
    # 判断账号为邮箱还是手机号
    if re.match(RE_EMAIL, obj_in.number):
        user = crud.get_user_by_email(db, email=obj_in.number)
    elif re.match(RE_PHONE, obj_in.number):
        user = crud.get_user_by_phone(db, phone=obj_in.number)
    else:
        message = "输入账号信息有误"
        logger.error(message)
        return None, None, message

    # 判断账号是否注册过
    if not user:
        message = "账号未注册"
    elif user.status == 1:
        message = f"该用户 {obj_in.number} 账号已禁用"
    else:
        # 比较验证码是否匹配
        if obj_in.client_code != redis_client_code:
            message = "验证码不正确或已过期"
            logger.error(message)
            return None, None, message

        # 验证是否设置过初始密码
        if not user.hashed_password:
            message = f"账号还未设置初始密码"
            return None, None, message

        # 密码进行比对
        if not security.verify_password(obj_in.pwd, user.hashed_password):
            message = "用户密码不正确"
            logger.error(message)
        else:
            message = "用户登录成功"
            token = deps.create_access_token(user.id)  # 生成 token 只存放了 userid
            # 登录成功之后向数据库添加一条登录 token 日志信息
            ip = request.client.host
            token_logs = crud.add_token_logs(db, userid=user.id, token=token, callback_url=obj_in.callback_url, ip=ip)
            if not token_logs:
                message = "添加登录 token 日志信息失败"
                logger.error(message)
            userid = user.id
            return userid, token, message
    logger.error(message)
    return None, None, message


def sign_in_by_code(db: Session, request: Request, *, obj_in: schemas.LogInBycode, redis_verify_code: str):
    """
    使用 邮箱/手机号 验证码登录
    :param db:
    :param number:              手机号或者邮箱
    :param pwd:                 密码
    :param verify_code:         验证码
    :param callback_url:        系统回调地址
    :param redis_verify_code:   存储在 redis 中的验证码
    :return:                    userid(用户id), token(用户token), message(提示信息)
    """
    # 比较验证码是否匹配
    if obj_in.verify_code != redis_verify_code:
        message = "验证码不正确或已过期"
        logger.error(message)
        return None, None, message

    # 判断账号为邮箱还是手机号
    if re.match(RE_EMAIL, obj_in.number):
        user = crud.get_user_by_email(db, email=obj_in.number)
    elif re.match(RE_PHONE, obj_in.number):
        user = crud.get_user_by_phone(db, phone=obj_in.number)
    else:
        message = "输入账号信息有误，请重新输入"
        logger.error(message)
        return None, None, message

    userid = None
    if not user:
        # 判断账号为邮箱还是手机号
        if re.match(RE_EMAIL, obj_in.number):
            db_userid = crud.create_by_email(db, email=obj_in.number, pwd=None)  # 通过邮箱进行一次性登录注册
        elif re.match(RE_PHONE, obj_in.number):
            db_userid = crud.create_by_phone(db, phone=obj_in.number, pwd=None)  # 通过手机号进行一次性登录注册
        if not db_userid:
            message = "登录失败"
            logger.error(message)
            return None, None, message
        userid = db_userid  # 将新增之后的 用户id 赋值给变量
    elif user.status == 1:
        message = "该用户账号已禁用"
        logger.error(message)
        return None, None, message

    if user:
        userid = user.id
    token = deps.create_access_token(userid)  # 生成 token 只存放了 userid
    # 登录成功之后向数据库添加一条登录 token 日志信息
    ip = request.client.host
    token_logs = crud.add_token_logs(db, userid=userid, token=token, callback_url=obj_in.callback_url, ip=ip)
    if not token_logs:
        message = "用户添加登录 token 日志信息失败"
        logger.error(message)
    else:
        message = "用户登录成功"
    return userid, token, message


def get_userinfo_by_token(db: Session, token: str):
    """
    查询 token 对应的用户信息
    :param db:
    :param token:   用户 token
    :return:        用户信息
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(token)
    if not decode_token:
        logger.error(message)
        return None, message

    # 获取 token 对应的用户信息
    db_user = crud.get_user_by_token(db, token=token)
    if not db_user:
        message = '获取用户信息失败'
        logger.error(message)
    else:
        message = '获取用户信息成功'
    return db_user, message


def user_signup(db: Session, *, obj_in: schemas.SignUp, redis_verify_code: str):
    """
    用户注册接口
    :param db:
    :param number:              手机号或者邮箱
    :param pwd:                 密码
    :param verify_code:         验证码
    :param redis_verify_code:   存储在 redis 中的验证码
    :return:                    用户id，提示信息
    """
    # 比较验证码是否正确
    if obj_in.verify_code != redis_verify_code:
        message = "验证码不正确或已过期"
        logger.error(message)
        return None, message

    # 判断账号为邮箱还是手机号
    if re.match(RE_EMAIL, obj_in.number):
        user = crud.get_user_by_email(db, email=obj_in.number)
        if user:
            message = f'该账号 {obj_in.number} 已被注册'
            logger.error(message)
            return None, message
        hash_pwd = security.get_password_hash(obj_in.pwd)  # HASH 后的新密码
        db_userid = crud.create_by_email(db, email=obj_in.number, pwd=hash_pwd)  # 通过邮箱进行一次性登录注册
    elif re.match(RE_PHONE, obj_in.number):
        user = crud.get_user_by_phone(db, phone=obj_in.number)
        if user:
            message = f'该账号 {obj_in.number} 已被注册'
            logger.error(message)
            return None, message
        hash_pwd = security.get_password_hash(obj_in.pwd)  # HASH 后的新密码
        db_userid = crud.create_by_phone(db, phone=obj_in.number, pwd=hash_pwd)  # 通过手机号进行一次性登录注册
    else:
        message = "账号输入有误"
        logger.error(message)
        return None, message

    if not db_userid:
        message = "注册失败"
        logger.error(message)
    else:
        message = "注册成功"
    return db_userid, message


def user_signout(db: Session, *, token: str):
    """
    用户登出
    :param token:       用户token
    :return:            用户id, 提示信息
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(token)
    userid = decode_token.get("sub")
    if not decode_token:
        logger.error(message)
        return None, message

    # 查询账号状态是否正常
    db_user = crud.get_user_by_id(db, id=userid)
    if not db_user:
        message = "该账号状态异常"
        return None, message

    # 更新记录 token 退出时间
    result = crud.update_tokeninfo_by_token(db, token=token)
    if not result:
        message = '登出失败'
        logger.error(message)
        return None, message
    message = '登出成功'
    return userid, message


def user_log_off(db: Session, *, token: str):
    """
    用户注销账号
    :param token:   用户token
    :return:        用户id, 提示信息
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(token)
    if not decode_token:
        logger.error(message)
        return None, message
    userid = decode_token.get("sub")

    # 更新用户账户状态信息
    result = crud.update_user_status_by_id(db, userid=userid, status=1)
    if not result:
        message = '注销失败'
        logger.error(message)
    else:
        message = '注销成功'
    return userid, message


def update_userinfo_by_token(db: Session, *, token: str, obj_in: schemas.UserInfo):
    """
    通过 token 修改用户信息
    :param db:
    :param token:           用户 token
    :param username:        用户名
    :param phone:           手机号
    :param email:           邮箱
    :return:                修改后的用户信息
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(token)
    if not decode_token:
        logger.error(message)
        return None, message

    userid = decode_token.get('sub')
    # 查询一次用户是否存在
    db_user = crud.get_user_by_id(db, id=userid)
    if not db_user:
        message = '该用户不存在'
        logger.error(message)
        return None, message
    if db_user.status == 1:
        message = '该用户已禁用'
        logger.error(message)
        return None, message

    result = crud.update_user_info(db, userid=userid, obj_in=obj_in)
    if not result:
        message = '修改失败'
        logger.error(message)
    else:
        message = '修改成功'
    return result, message


def update_userinfo_by_id(db: Session, *, obj_in: schemas.UserInfo):
    """
    通过 用户id 修改用户信息
    :param db:
    :param username:        用户名
    :param phone:           手机号
    :param email:           邮箱
    :return:
    """
    # 查询一次用户是否存在
    db_user = crud.get_user_by_id(db, id=obj_in.userid)
    if not db_user:
        message = '该用户不存在'
        logger.error(message)
        return None, message
    if db_user.status == 1:
        message = '该用户已禁用'
        logger.error(message)
        return None, message

    result = crud.update_user_info(db, obj_in=obj_in)
    if not result:
        message = '修改失败'
        logger.error(message)
    else:
        message = '修改成功'
    return result, message


def update_user_status_by_id(db: Session, *, id: int, status: int):
    """
    更新用户账户状态信息
    :param db:
    :param id:              用户 id
    :param status:          用户状态（0：可用，1：禁用）
    :return:
    """
    # 查询一次用户是否存在
    db_user = crud.get_user_by_id(db, id=id)
    if not db_user:
        message = '该用户不存在'
        logger.error(message)
        return None, message

    result = crud.update_user_status_by_id(db, id=id, status=status)
    if not result:
        message = '修改失败'
        logger.error(message)
    else:
        message = '修改成功'
    return result, message


def change_password(db: Session, *, obj_in=schemas.ChangePwd):
    """
    修改密码
    :param db:
    :param token:       用户 token
    :param old_pwd:     旧密码
    :param new_pwd:     新密码
    :return:            用户id，提示信息
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(obj_in.token)
    if not decode_token:
        logger.error(message)
        return None, message

    userid = decode_token.get('sub')
    user = crud.get_user_by_id(db, id=userid)
    if not user:
        message = '该用户不存在'
        logger.error(message)
        return None, message

    # 判断原始密码是否匹配
    if not security.verify_password(obj_in.old_pwd, user.hashed_password):
        message = '用户旧密码不正确'
        logger.error(message)
        return None, message
    hash_pwd = security.get_password_hash(obj_in.new_pwd)  # HASH 后的新密码
    db_user = crud.update_password(db, userid=user.id, pwd=hash_pwd)
    if not db_user:
        message = '用户密码修改失败'
        logger.error(message)
        return None, message
    message = '用户密码修改成功'
    return user.id, message


def forgot_password(db: Session, *, obj_in: schemas.SignUp, redis_verify_code: str):
    """
    忘记密码
    :param db:
    :param number:          用户账号（邮箱 或 手机号）
    :param pwd:             密码
    :param verify_code:     验证码
    redis_verify_code:      存储在 redis 中的对应验证码
    :return:                用户id, 提示信息
    """
    # 比较验证码是否匹配
    if obj_in.verify_code != redis_verify_code:
        message = "验证码不正确或已过期"
        return None, message

    # 判断账号为邮箱还是手机号
    if re.match(RE_EMAIL, obj_in.number):
        user = crud.get_user_by_email(db, email=obj_in.number)
    elif re.match(RE_PHONE, obj_in.number):
        user = crud.get_user_by_phone(db, phone=obj_in.number)
    else:
        message = "输入账号信息有误，请重新输入"
        logger.error(message)
        return None, message

    if not user:
        message = f"用户 {obj_in.number} 未注册"
        logger.error(message)
        return None, message
    if user.status == 1:
        message = f"用户 {obj_in.number} 已被禁用"
        logger.error(message)
        return None, message

    hash_pwd = security.get_password_hash(obj_in.pwd)  # HASH 后的新密码
    result = crud.update_password(db, userid=user.id, pwd=hash_pwd)
    if not result:
        message = '密码重置失败'
        logger.error(message)
        return None, message
    message = '密码重置成功'
    return user.id, message


async def verify_token(request: Request, *, token: str):
    """
    校验 token
    :param token:   用户 token
    :return:        userid, message
    """
    # 校验 token
    decode_token, message = deps.check_jwt_token(token)
    if not decode_token:
        logger.error(message)
        return None, message
    userid = decode_token.get('sub')

    # ------- 在 redis 中查找 token 是否存在 --------- #
    redis_token = await request.app.state.redis.get(f"{userid}")
    if not redis_token:
        message = "token 校验失败"
        return None, message
    return userid, message


async def verify_token_add_info(db: Session, request: Request, *, obj_in: schemas.VerifyUserInfo):
    """
    添加用户在系统的登陆信息
    :param db:
    :param token:           用户 token
    :param callback_url:    系统回调地址
    :return:                登录日志id, 提示信息
    """
    # 校验 token
    userid, message = await verify_token(request, token=obj_in.token)
    if not userid:
        return None, message

    ip = request.client.host
    logid = crud.add_token_logs(db, userid=userid, token=obj_in.token, callback_url=obj_in.callback_url, ip=ip)
    if not logid:
        message = '添加失败'
        logger.error(message)
    else:
        message = '添加成功'
    return logid, message

