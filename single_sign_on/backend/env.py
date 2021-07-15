#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


# sql database configuration
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "single_sign_on"
MYSQL_PORT = "3306"
MYSQL_IP = "127.0.0.1"
# HOST_IP  represent self ip address
# HOST_IP = get_ipv4_addrs(True)[0]
HOST_IP = "192.168.0.104"

HOST_PORT = 8008


# ---------- 项目根路径 -----------
BASE_PATH: str = (os.path.dirname(os.path.abspath(__file__)))


# -------- token 配置 ------------
# TOKEN 的过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

# TOKEN 的过期时间（秒钟）
ACCESS_TOKEN_EXPIRE_SECONDS: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60

# 验证码过期时间（秒钟）
VERIFY_CODE_EXPIRE_SECONDS = 300

# SECRET_KET
SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'

# 生成 token 的加密算法用（HS256 对称算法加密）
ALGORITHM: str = "HS256"


# -------- redis 配置 ----------
REDIS_HOST: str = "127.0.0.1"
REDIS_PASSWORD: str = ""
REDIS_DB: int = 0
REDIS_PORT: int = 6379
REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"


# 邮箱配置
EMAIL_SMTPSERVER = "smtp.163.com"       # 163 邮箱 SMTP 服务器地址
EMAIL_PORT = "465"                      # 163 邮箱服务器 SSL 的端口号
EMAIL_FROM_ADDR = "nerve_net@163.com"   # 发送方邮件地址
EMAIL_PASSWORD = "JPRSQERFLQHSCDTO"     # 发送方邮箱密码

# 手机配置
PHONE_ACCESSKEY = 'LTAI89k0P2GMHp0o'
PHONE_ACCESSSECRET = 'B8l1BNYzVaRdLr7HNjEUxFLr7aLD2X'
PHONE_SIGNNAME = "速运快递"
PHONE_TEMPLATECODE = "SMS_144850440"

# 验证码有效时间配置(秒)
EFFECTIVE_TIME_CLIENT = 180
EFFECTIVE_TIME_SMS = 600
EFFECTIVE_TIME_EMAIL = 300
