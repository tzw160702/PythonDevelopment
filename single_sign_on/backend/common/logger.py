#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021-02-25 16:44:08
# @Author  : senou
# @Email   : senouit@163.com
# @Desc    :

"""
日志文件配置
"""

import os
import time

import env

from loguru import logger


# 定位到 log 日志文件
log_path = os.path.join(env.BASE_PATH, "logs")

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f"{time.strftime('%Y-%m-%d')}_error.log")

# 日志简单配置
logger.add(
    log_path_info,
    rotation="12:00",       # 每天中午 12:00 都会创建新文件
    retention="7 days",     # 7 天后清理
    enqueue=True
    )

__all__ = ["logger"]