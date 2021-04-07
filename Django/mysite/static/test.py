import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor, Cursor

# # Create your tests here.
# v = [
#     {'name': '日天', 'tid': 1, 'classname': '全栈58888期'},
#     {'name': '日天', 'tid': 1, 'classname': '全栈656期'},
#     {'name': '日地', 'tid': 2, 'classname': '黑客来了'},
#     {'name': '日地', 'tid': 2, 'classname': '全栈100期'},
#     {'name': '日方少伟', 'tid': 3, 'classname': '全栈58888期'},
#     {'name': '日方少伟', 'tid': 3, 'classname': '全栈656期'},
#     {'name': '日方少伟', 'tid': 3, 'classname': '黑客来了'}
# ]
# result = {
#     # 1:{'tid':1, 'name':'日天', 'classnames':['全栈58888期',]}
# }
# for row in v:
#     tid = row['tid']    # 1 1 2 2 3 3 3
#     if tid in result:
#         result[tid]['classnames'].append(row['classname'])
#     else:
#         result[tid] = {'tid': row['tid'], 'name': row['name'],
#                                           'classnames': [row['classname'], ]}
# print(result)
#
# # for item in result.values():
# #     print(item)


# def get_list(sql, args):
#     conn = pymysql.connect(host='tzw160702.work', port=3307, user='root',
#     passwd='password', db='stu_manage', charset='utf8')
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cursor.execute(sql, args)
#     result = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return result
#
#
# answer = get_list("select * from class", [])
# for row in answer:
#     print(row)


# class Foo(object):
#     staticField = "old boy"
#
#     def __init__(self):
#         self.name = 'wupeiqi'
#
#     def func(self):
#         return 'func'
#
#     @staticmethod
#     def bar():
#         return 'bar'
#
#
# print(getattr(Foo, 'staticField'))
# print(setattr(Foo, 'name', '大哥'))
# print(getattr(Foo, 'name'))

# data = {
#     "name": "kuls",
#     "age": 18,
#     "dict": {"city": "cs"},
#     "list": [0, 1, 2, 3],
#     "int": 1
# }
# print(*data)


