#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-03-01 16:10:15
# @Author  : chen lei
# @Email   : senouit@163.com
# @Desc    :

"""
获取验证码
"""

import smtplib
import json

import env

from email.mime.text import MIMEText
from email.header import Header

from aliyunsdkcore.client import AcsClient      # 安装阿里云 SDK 核心库: pip install aliyun-python-sdk-core-v3
from aliyunsdkcore.request import CommonRequest


def get_email_code(*, email: str, email_code: str) -> str:
    """
    获取邮箱验证码
    """
    smtp_server = env.EMAIL_SMTPSERVER       # 163 邮箱 SMTP 服务器地址
    port = env.EMAIL_PORT                    # 163 邮箱服务器 SSL 的端口号
    from_addr = env.EMAIL_FROM_ADDR          # 发送方邮件地址
    password = env.EMAIL_PASSWORD            # 发送方邮箱密码
    to_addrs = email                         # 收件人邮箱地址

    subject = "单点登录"
    msg = MIMEText(f'您的验证码为：{email_code}\n <10分钟之内有效>', 'plain', 'utf-8')
    msg['From'] = Header(from_addr)               # msg['From'] 与 msg['To'] 中 不能加 'utf-8' 否则会邮箱系统被视为垃圾短信，则发不出去
    msg['To'] = Header(to_addrs)
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP_SSL(smtp_server, port)            # 获取 SMTP 协议证书
        server.login(from_addr, password)                       # 通过授权码登录邮箱
        server.sendmail(from_addr, to_addrs, msg.as_string())   # 发送
        server.quit()                                           # 退出
    except smtplib.SMTPException:
        return None
    return email_code


def get_phone_code(*, phone: int, phone_code: str) -> str:
    """
    获取短信验证码
    phone: 手机号
    """
    AccessKey = env.PHONE_ACCESSKEY
    AccessSecret = env.PHONE_ACCESSSECRET
    code = 'cn-hangzhou'
    try:
        client = AcsClient(AccessKey, AccessSecret, code, phone)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', env.PHONE_SIGNNAME)
        request.add_query_param('TemplateCode', env.PHONE_TEMPLATECODE)

        json_data = json.dumps({'code': phone_code})
        request.add_query_param('TemplateParam', json_data)
        client.do_action(request)
    except:
        return None
    return phone_code


