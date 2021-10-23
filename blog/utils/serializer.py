# !/usr/bin/env python3
from .. import models
from rest_framework import serializers


# ----------------------------- 序列化 -----------------------------
class RoleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()


# 继承 serializers.Serializer
class UserInfoSerializer(serializers.Serializer):
    """
    字段参数：
    	source, 指定要序列化表中的哪个字段
    	many=True, 序列化多个对象
    	read_only = True, 正向序列化用
    	write_ony = True, 反向序列化用
    """
    # 如果生成 CharField(), 不带 source ,
    # 所序列化的字段赋给的名称必须是数据库对应的字段.
    # 带上 source 时，所赋给的名称 *需要* 自定义,
    # 否则会报错: because it is the same as the field name.
    # 同时参数 source="与数据库字段名称一一对应".
    id = serializers.CharField()
    username = serializers.CharField()

    # [{"id": "1", "username": "小梁", "user_type": "1"}, xxx] 【user_type 是对应的id】
    type_user = serializers.CharField(source='user_type')

    # [{"id": "1", "username": "小梁", "user_type": "普通用户"}, xxx] 【user_type 是对应的中文】
    # user_type = models.IntegerField(choices=user_grade)
    from_user = serializers.CharField(source='get_user_type_display')

    # 获取外键关联的字段的值
    gp = serializers.CharField(source='group.name')

    # 如果表中字段属性 CharField 中有 choices参数 , 或者有 ForeignKey 时，
    # 可以通过 source 拿到对应字段的值,
    # 如果 source 取不到值可以通过自定义方法去取值。

    # 如果该字段是 ManyToManyField, 可以通过自定义显示取值
    # rls = serializers.CharField(source='roles.title')  # 会报错拿不到数据
    rls = serializers.SerializerMethodField()   # 自定义显示方法

    def get_rls(self, obj):    # get_ + "field_name", obj 表示当前行的对象 rls.
        role_obj_list = obj.roles.all()
        role_list = list()
        for role in role_obj_list:
            role_list.append({'id': role.id, 'title': role.title})
        return role_list


# ModelSerializer 和 需要序列化的 model 一对一绑定的序列化类
# 继承 serializers.SerializerMethodField, 在类 Serializer 上进行封装
# class UserSerializer(serializers.ModelSerializer):
#     from_user = serializers.CharField(source='get_user_type_display')
#     rls = serializers.SerializerMethodField()  # 自定义显示
#
#     # class Meta: 做为嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准.
#     class Meta:
#         model = models.UserInfo
#         # fields = "__all__"          # 返回所有字段
#
#         # 返回指定字段
#         fields = ['id', 'username', 'password', 'from_user', 'group', 'rls']
#
#         # exclude = [] 排除某个字段
#         # extra_kwargs = {每个字段的一些额外参数}
#     def get_rls(self, obj):    # obj 表示当前行的对象 rls.
#         role_obj_list = obj.roles.all()
#         role_list = list()
#         for role in role_obj_list:
#             role_list.append({'id': role.id, 'title': role.title})
#         return role_list


# ----------------------------------------------------------------------------
# 自定义类(了解), 自定义方法可以实现。
"""
class MyField(serializers.CharField):
    def to_representation(self, value):
        print(value)      # value 是数据库对应字段的值
        return 'xxxx'     # 返回的值给了 name


class UserSerializer(serializers.ModelSerializer):
    name = MyField(source='username')

    # class Meta: 做为嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准.
    class Meta:
        from .. import models
        model = models.UserInfo

        # 返回指定字段
        fields = ['name']
"""
# ----------------------------------------------------------------------------


# class UserInfoSerializer(serializers.ModelSerializer):
#     """ 自动化序列连表 """
#     # HyperlinkedIdentityField 自动生成链接(了解)
#     # re_path(r'api/(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$',
#     #             GroupView.as_view(), name='gp'),
#     # lookup_field: 模型的字段应该用于执行对象查找个别的模型实例
#     # 参数 lookup_url_kwarg 指的是 url 中 pk 的值, 用于对象查找关键字参数
#     group = serializers.HyperlinkedIdentityField(
#         view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')
#
#     class Meta:
#         model = models.UserInfo
#         fields = "__all__"
#
#         # depth 对查询表所关联的表取值,
#         # 1 表示拿到当前所查询表的外键关联的表或者一对多，多对多表关系表中的字段,
#         # 数字越大拿到不同深度的表对应关系中的字段,
#         # 层数越多速度响应率越慢, 建议0~4之间.
#         depth = 1


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserGroup
        fields = "__all__"


# ------------------------------- 校验 --------------------------------
class ParamValidator(object):
    # 自定义校验
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须以（%s）为开头。' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class UserGroupSerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={'required': '标题不能为空'},
                                 validators=[ParamValidator('这个人'), ])

    # 局部钩子校验
    def validate_name(self, value):
        """类似于Form组件的局部钩子"""
        # from rest_framework import exceptions
        # raise exceptions.ValidationError('不能以 *这个人* 开头')
        return value

    # 全局钩子校验
    # 在序列化器中需要同时对多个字段进行比较验证时，可以定义validate方法来验证
    # def validate(self, attrs):
    #     print(attrs, type(attrs), attrs['name'])
    #     return attrs


# ------------------------------- 分页 --------------------------------
class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"