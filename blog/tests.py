from django.test import TestCase

# Create your tests here.

# class User:
#     def login(self):
#         print('欢迎来到登录页面')
#
#     def register(self):
#         print('欢迎来到注册页面')
#
#     def save(self):
#         print('欢迎来到存储页面')
#
#
# user = User()
# while 1:
#     choose = input('>>>').strip()
#     if hasattr(user, choose):
#         func = getattr(user, choose)
#         func()
#
#     else:
#         print('输入错误。。。。')

# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class ApiView(View):
#     ...


# def fun():
#     a = 0
#     try:
#         yield
#     except Exception as e:
#         print(e)
#
# for i in fun():
#     print(i)

# import time
# time_recode = {}
#
# for i in range(10):
#     time.sleep(1)
#     ctime = time.time()
#     time_recode[i] = ctime
#
# print(time_recode)
# # {0: 1630589459.293494, 1: 1630589460.3083444, 2: 1630589461.313145,
# # 3: 1630589462.3153846, 4: 1630589463.316631, 5: 1630589464.328139,
# # 6: 1630589465.3307028, 7: 1630589466.335672, 8: 1630589467.341197,
# # 9: 1630589468.3556178}
#
# local_time = 1630589468.3556178 - 1
# previous_time = 1630589459.293494


# dic = {1: 'ni', 2: 'hao'}
# print(dic.pop(2,'ya'), dic.pop('3', 'ya'))


# class Foo(object):
#
#     def __init__(self, a1):
#         print(a1)
#         self.a = a1
#
#     def __new__(cls, *args, **kwargs):
#         """
#         1. 根据类创建对象，并返回
#         2. 执行返回值对象的 __init__ 方法
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         return "孙接龙"
#         # return object.__new__(cls)
#
#
# obj = Foo(123)
# print(obj)


class A:  # python3 写法
    def add(self, x):
        y = x + 1
        print(y)


class B(A):
    def add(self, x):
        super().add(x)  # !/usr/bin/python3
        super(B, self).add(x)  # !/uer/bin/python2


b = B()
b.add(2)
