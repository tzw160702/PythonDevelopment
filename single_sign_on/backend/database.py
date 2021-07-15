# 导入SQLAlchemy部分
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import env
from pydantic import BaseSettings, AnyHttpUrl, IPvAnyAddress

link_mysql = env.MYSQL_USERNAME + ":" + env.MYSQL_PASSWORD + "@" + env.MYSQL_IP + ":" + env.MYSQL_PORT + "/" + env.MYSQL_DATABASE
engine = create_engine("mysql+pymysql://" + link_mysql)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 现在，我们将使用declarative_base()返回类的函数。
# 稍后，我们将从该类继承以创建每个数据库模型或类（ORM模型）：
Base = declarative_base()
