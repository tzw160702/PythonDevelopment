import time
import json
import hashlib
from blog import models
from .utils import serializer
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from blog.utils.throttles import VisitThrottle, IPThrottle
from rest_framework.versioning import QueryParameterVersioning
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination,
                                       CursorPagination)


def md5(user):
    ctime = str(time.time())
    secret = hashlib.md5(bytes(user, encoding='utf-8'))
    secret.update(bytes(ctime, encoding='utf-8'))
    return secret.hexdigest()


class AuthenticationView(APIView):
    """ 用户登录认证 """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 204
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建 token
            token = md5(user)
            models.UserToken.objects.update_or_create(
                user=obj, defaults={'token': token})
            ret['token'] = token

        except Exception as e:
            ret['code'] = 404
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


class ArticlesView(APIView):
    """ 查询 """
    throttle_classes = [VisitThrottle]

    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': None}
        article_dict = {
            1: {
                'name': '小周',
                'age': 19,
                'gender': "woman"
            },
            2: {
                'name': '王八',
                'age': 23,
                'gender': "man"
            }
        }

        try:
            ret['data'] = article_dict
        except Exception as e:
            pass
        return JsonResponse(ret)


class AllUserView(APIView):
    throttle_classes = [IPThrottle]

    def get(self, request, *args, **kwargs):
        user_list = list()
        users = models.UserInfo.objects.all()
        for user in users:
            if not hasattr(user_list, user.username):
                user_list.append(user.username)

        return HttpResponse(user_list)


# class MyVersion(APIView):
#     authentication_classes = []
#     permission_classes = []
#     versioning_class = QueryParameterVersioning
#
#     def get(self, request, *args, **kwargs):
#         # self.dispatch()
#         print(request.version)
#         return HttpResponse('查看版本！')


class MyVersionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):

        # 获取版本
        print(request.version)

        # 获取版本的对象
        print(request.versioning_scheme)

        # 反向生成 URL （Rest Framework）
        url = request.versioning_scheme.reverse(viewname='Versions', request=request)
        print(url)

        # django 的反向生产 URL
        # from django.urls import reverse
        # url1 = reverse(viewname='Versions', kwargs={'version': 'v2'})
        # print(url1)

        return HttpResponse('查看版本！')


class MyParserView(APIView):
    authentication_classes = []
    permission_classes = []
    """
    JSONParser:表示只能解析 content-type:application/json 请求头
    FormParser:表示只能解析 content-type:application/x-www-form-urlencoded 请求头
    """
    # parser_classes = [JSONParser,FormParser,]

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON格式数据
            a. content-type: application/json
            b. {"name": "alex", "age": 18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # 1. 获取用户请求
        # 2. 获取用户请求体
        # 3. 根据用户请求头 和 parser_classes = [JSONParser,FormParser,] 中支持的请求头进行比较
        # 4. JSONParser 对象去处理请求体
        # 5. request.data  获取结果
        print(request.data)
        result = request.data

        return HttpResponse(json.dumps(result))


class RoleView(APIView):
    def get(self, request, *args, **kwargs):
        # # 方式一
        # roles = models.UserInfo.objects.all().values('id', 'title')
        # roles = list(roles)

        # ensure_ascii=False 中文显示, 默认为 True
        # ret = json.dumps(roles, ensure_ascii=False)
        # print(ret)

        # 方式二 ***
        roles = models.Role.objects.all()
        # 参数 many=True 取多条数据, 前提是 Queryset 对象必须 iterable .
        roles = serializer.RoleSerializer(instance=roles, many=True)
        # 或者
        # roles = models.Role.objects.first()
        # roles = serializer.RoleSerializer(instance=roles, many=False)
        """
          instance=None, 要序列化的数据
          data=empty, 要反序列化的数据
          many=True 如果序列化多条，一定要写 many=True
        """

        # users.data 已经是转换完成的结果
        ret = json.dumps(roles.data, ensure_ascii=False)  # 方便页面渲染
        return HttpResponse(ret)


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()

        # 实例化一般将数据封装到对象
        users = serializer.UserInfoSerializer(instance=users,
                                          many=True,
                                          context={'request': request})
        print(users.data)
        return HttpResponse(json.dumps(users.data, ensure_ascii=False))


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = serializer.GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class UserGroupView(APIView):

    def post(self,request,*args,**kwargs):
        # print(request.data)  # 获取 post 请求的字典

        param = serializer.UserGroupSerializer(data=request.data)
        if param.is_valid():
            # assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。
            # assert的异常参数，其实就是在断言表达式后添加字符串信息，用来解释断言并更好的知道是哪里出了问题。
            print(param.validated_data['name'])
        else:
            print(param.errors)

        return HttpResponse('提交数据')


# 自定制分页继承 PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3    # 每页显示的默认条数
    page_size_query_param = 'size'  # 查询参数的key, 指定每页显示条数(?size=3)
    max_page_size = 8  # 每页查询的最大条数

    page_query_param = 'page'  # 查询参数的key, 查询第几页(?page=2)
    """
    注意:
        也可以不用继承类 PageNumberPagination，
        直接在视图函数中实例化 pg = PageNumberPagination()，
        然后通过 对象.属性 去设置, 例如：pg.page_size = 3
    """


class Paging1View(APIView):
    """常规分页"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        # pg = PageNumberPagination()
        pag = MyPageNumberPagination()

        # 在数据库中获取分页数据
        result = pag.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        roles_ser = serializer.PagerSerializer(instance=result, many=True)

        # 生成上一页或下一页链接(get_paginated_response)
        # return pag.get_paginated_response(roles_ser.data)
        return Response(roles_ser.data)


class Paging2View(APIView):
    """偏移分页"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        # pg = LimitOffsetPagination()
        pag = LimitOffsetPagination()

        # 每页显示的条数
        # 从标杆位置往后取几个，默认取3个，也可以指定
        pag.default_limit = 3

        # 往后偏移多少的key值，如 limit=4
        # 每次取的条数，可以自定义key值
        pag.limit_query_param = 'limit'

        # 从哪一页开始的标杆的key，如 offset=3
        # 标杆值，offset=6 就是在第六个位置往后拿三条
        pag.offset_query_param = 'offset'

        # 每页取的最大的条数
        pag.max_limit = 5

        # 在数据库中获取分页数据
        result = pag.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        roles_ser = serializer.PagerSerializer(instance=result, many=True)

        return Response(roles_ser.data)


class Paging3View(APIView):
    """游标分页"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        # pg = CursorPagination()
        pag = CursorPagination()

        # 查询的 Key 值.  注：key对应的值加密
        pag.cursor_query_param = 'cursor'

        pag.page_size = 3    # 每页默认显示多少条

        # 按什么排序
        # 字段前加一个 - 表示倒序
        pag.ordering = 'id'

        # # 查询参数的key, 指定每页显示条数(?size=3)
        pag.page_size_query_param = 'size'

        # 每页最多显示条数
        pag.max_page_size = 8

        # 在数据库中获取分页数据
        result = pag.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        roles_ser = serializer.PagerSerializer(instance=result, many=True)

        # 生成上一页或下一页链接(get_paginated_response)
        return pag.get_paginated_response(roles_ser.data)


# ------------------------------ 视图 -----------------------------------
from rest_framework.generics import GenericAPIView


class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()

        # 分页
        pager_roles = self.paginate_queryset(roles)

        # 序列化
        ser = self.get_serializer(instance=pager_roles, many=True)

        return Response(ser.data)


from rest_framework.generics import ListAPIView, CreateAPIView


class View2View(ListAPIView, CreateAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination

# -------------------------- 视图集 -----------------------------------------


from rest_framework.viewsets import GenericViewSet


class View3View(GenericViewSet):

    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()

        # 分页
        pager_roles = self.paginate_queryset(roles)

        # 序列化
        ser = self.get_serializer(instance=pager_roles, many=True)

        return Response(ser.data)


from rest_framework.viewsets import ModelViewSet


class View4View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin


class View5View(CreateModelMixin, GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination


class View6View(CreateModelMixin, GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination
