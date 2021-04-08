#!/usr/bin/python3
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor, Cursor


def get_sql_list(sql, args):
    db_params = {
        "host": "59.110.235.115",
        "port": 3307,
        "user": "root",
        "passwd": "password",
        "charset": "utf8",
        "db": "stu_manage",
        "autocommit": True,  # 自动提交事务
        "cursorclass": Cursor
    }
    conn = Connection(**db_params)  # 创建连接
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，将游标设置为字典类型
    cursor.execute(sql, args)  # 执行sql语句
    result = cursor.fetchall()
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return result


def get_one(sql, args):
    db_params = {
        "host": "59.110.235.115",
        "port": 3307,
        "user": "root",
        "passwd": "password",
        "charset": "utf8",
        "db": "stu_manage",
        "autocommit": True,  # 自动提交事务
        "cursorclass": Cursor
    }
    conn = Connection(**db_params)  # 创建连接
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，将游标设置为字典类型
    cursor.execute(sql, args)  # 执行sql语句
    result = cursor.fetchone()
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return result


def modify_sql(sql, args):
    db_params = {
        "host": "59.110.235.115",
        "port": 3307,
        "user": "root",
        "passwd": "password",
        "charset": "utf8",
        "db": "stu_manage",
        "autocommit": True,  # 自动提交事务
        "cursorclass": Cursor
    }
    conn = Connection(**db_params)  # 创建连接
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，将游标设置为字典类型
    cursor.execute(sql, args)  # 执行sql语句
    conn.commit()  # 提交
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接


def create(sql, args):
    db_params = {
        "host": "59.110.235.115",
        "port": 3307,
        "user": "root",
        "passwd": "password",
        "charset": "utf8",
        "db": "stu_manage",
        "autocommit": True,  # 自动提交事务
        "cursorclass": Cursor
    }
    conn = Connection(**db_params)  # 创建连接
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，将游标设置为字典类型
    cursor.execute(sql, args)  # 执行sql语句
    conn.commit()  # 提交
    last_row_id = cursor.lastrowid   # 获取最后插入行的主键ID
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return last_row_id


# 创建一个数据库助手类
class SqlHelper(object):
    def __init__(self):
        # 读取配置文件
        self.connect()

    # 创建数据库连接
    def connect(self):
        self.conn = pymysql.connect(host='tzw160702.work',
                                    port=3307, user='root',
                                    passwd='password',
                                    db='stu_manage',
                                    charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取所有行数据
    def get_list(self, sql, args):
        self.cursor.execute(sql, args)  # 执行sql语句
        result = self.cursor.fetchall()
        return result

    # 获取第一行数据
    def get_one(self, sql, args):
        self.cursor.execute(sql, args)  # 执行sql语句
        result = self.cursor.fetchone()
        return result

    # 修改
    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 批量修改
    def multiple_modify(self, sql, args):
        # self.cursor.executemany('insert into class(id, classname) values(%s,%s)', [(1,'xiaotang'),(2,'zhouyuan')])
        self.cursor.executemany(sql, args)    # executemany 对数据进行批量插入  注: 元组
        self.conn.commit()

    # 获取最后插入行的主键ID
    def create(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid()      # lastrowid 获取最新自增 ID

    # 关闭
    def close(self):
        self.cursor.close()
        self.conn.close()
