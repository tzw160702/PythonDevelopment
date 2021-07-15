#!/usr/bin/python3

import sys

sys.path.append("../")

import pymysql
from fastapi import FastAPI
from sql_app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


database_app = FastAPI()

pymysql.install_as_MySQLdb()

user = "root"
password = "root"
host = "192.168.0.114"
SQLALCHEMY_DATABASE_URL =\
    f"mysql+pymysql://{user}:{password}@{host}:3306/inventory_service"


# 初始化数据库
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8')

# 创建 database session 类型
database_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 session 对象
session = database_session()

# 数据库中生成表 (如果表已经存在，则不会创建)
# Base.metadata.create_all(engine)

# 删除所有表 (数据库更改、调试)
# Base.metadata.drop_all(engine)
