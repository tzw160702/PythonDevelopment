<div align='center' ><font size='10'>Restframework</font></div>

* ***DjangoRestframework 主要使用  APIView 类，其 APIView 实质是对 View 进行继承加工了更多功能***
* ***请求进来 APIView() 首先执行 self.dispatch() 方法，此方法对 原有 request 进行了再次封装***

**一、 基于 FBV 视图函数**

```python
* 全站使用 csrf 认证
'django.middleware.csrf.CsrfViewMiddleware', # 全站使用csrf认证

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt # 该函数无需认证
def users(request):
    user_list = ['alex','oldboy']
    return HttpResponse(json.dumps((user_list)))

* 全站不使用 csrf 认证 
#'django.middleware.csrf.CsrfViewMiddleware', # 全站不使用csrf认证

from django.views.decorators.csrf import csrf_protect

@csrf_protect # 该函数需认证
def users(request):
    user_list = ['alex','oldboy']
    return HttpResponse(json.dumps((user_list)))
```

**二、基于 CBV 的视图函数**

> CBV csrf 时需要使用

* @method_decorator(csrf_exempt)
* 在dispatch()方法中（单独方法无效） 


```python
方式一：
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
class StudentsView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
    	return super(StudentsView,self).dispatch(request, *args, **kwargs)
方式二：
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch')
class StudentsView(View):
    
    def get(self,request,*args,**kwargs):
        print('get方法')
        return HttpResponse('GET')
```



## 一、认证(有些API需要用户登录成功之后才能访问；有些无需登录就能访问)

```python
* 内置认证类
   1. 认证类，必须继承：from rest_framework.authentication import BaseAuthentication
   2. 其他认证类：BasicAuthentication

* 使用：
继承 BaseAuthentication； 必须实现：authenticate()和 authenticate_header()方法
	- 创建类:继承 BaseAuthentication;
		from rest_framework.authentication import BaseAuthentication
		class Authtication(BaseAuthentication):
    		def authenticate(self,request):
        		token = request._request.GET.get('token')
        		token_obj = models.UserToken.objects.filter(token=token).first()
        		if not token_obj:
            		raise exceptions.AuthenticationFailed('用户认证失败')
        	return (token_obj.user, token_obj)

    		def authenticate_header(self, request):
        		return 'Basic realm="api"'
	- 返回值：
    - None,我不管了，下一认证来执行。
    - raise exceptions.AuthenticationFailed('用户认证失败') # from rest_framework import exceptions
    - (元素1，元素2)  # 元素1赋值给request.user; 元素2赋值给request.auth 
    - 局部使用
        class UserInfoView(APIView):
        	""" 订单相关业务 """
            authentication_classes = [自定义认证类1,自定义认证类2]
            def get(self,request,*args,**kwargs):
            	print(request.user)
            	return HttpResponse('用户信息')
	- 全局使用：
    	REST_FRAMEWORK = {
        	# 全局使用的认证类
            "DEFAULT_AUTHENTICATION_CLASSES":[
                'api.utils.auth.自定义认证类1', 'api.utils.auth.自定义认证类2',],
            # "UNAUTHENTICATED_USER":lambda :"匿名用户",
            "UNAUTHENTICATED_USER":None,  # 匿名，request.user = None
            "UNAUTHENTICATED_TOKEN":None, # 匿名，request.auth = None
        }
```

__案例：__

```python
auth.py
class Authtication(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在 rest framework 内部会将整个两个字段赋值给request，以供后续操作使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        return 'Basic realm="api"'

views.py
class OrderView(APIView):
	authentication_classes = []    # 该 post 请求不需要认证可以访问，如果 settings.py 中做了全局配置，优先使用局部
    # authentication_classes = [Authtication，]      # 如果全局中没有配置，局部使用需要这样写
    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None,'data':None}
        return JsonResponse(ret)

sittings.py
REST_FRAMEWORK = {
    # 全局使用的认证类
    "DEFAULT_AUTHENTICATION_CLASSES":['api.utils.auth.Authtication', ],  # 列表中是路径
	}
```



## 二、权限( 不同的视图不同权限可以访问 )

```python
*内置认证类 
	权限类，必须继承：from rest_framework.permissions import BasePermission

* 使用： 
继承 BasePermission，必须实现：has_permission 方法
	- 创建类继承：BasePermission，必须实现：has_permission方法
    	from rest_framework.permissions import BasePermission 
        class SVIPPermission(BasePermission):
            message = "必须是SVIP才能访问"
            def has_permission(self,request,view):
                if request.user.user_type != 3:
                    return False
                return True
            def has_object_permission(self, request, view, obj):
        		"""对某个对象的访问权限"""
        		pass
    - 返回值：	
    - retrun True, 有权访问
    - return False，无权访问
	- 局部使用
    	class UserInfoView(APIView):
            """
            订单相关业务（普通用户、VIP）
            """
            permission_classes = [自定权限类1, 自定义权限类2 ]

            def get(self,request,*args,**kwargs):
                return HttpResponse('用户信息')
	- 全局使用
    	REST_FRAMEWORK = {
            "DEFAULT_PERMISSION_CLASSES":[
                'api.utils.permission.自定义权限类1'，
                'api.utils.permission.自定义权限类1'，
            ]
        }		
```

**案列 **

```Python
permission.py
class SVIPPermission(BasePermission):
    message = "必须是SVIP才能访问"
    def has_permission(self,request,view):
        if request.user.user_type != 3:
            return False
        return True

views.py
class OrderView(APIView):
    """
    订单相关业务(只有SVIP用户有权限)
   	"""
    permission_classes = [SVIPPermission, ]     # 如果 sittings.py 中做了全局配置， 此步骤可以省略。 
    # permission_classes = []      # 任何用户都可以访问， 如果 settings.py 中做了配置，优先使用局部

    def get(self,request,*args,**kwargs):
        return HttpResponse('用户信息')
settings.py
REST_FRAMEWORK = {
		"DEFAULT_PERMISSION_CLASSES":['api.utils.permission.自定义权限类1'，],
    }
```



## 三、控制访问频率或限流(控制访问频率 )

```python
* 内置类
	节流类，必修继承：from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
    
* 使用
- 自定义频率控制类：继承：BaseThrottle，必须实现：allow_request()和wait() 方法
- 内置频率控制类：继承：SimpleRateThrottle，实现：get_cache_key()、scope = "Luffy" # setting 配置文件中的 key
- 返回值  return True  # 可以继续访问  
         return False  # 访问频率太高被限制
	- 自定义节流：
		import time
        VISIT_RECORD = {}

        class VisitThrottle(object):
            """60s内只能访问3次"""

            def __init__(self):
                self.history = None

            def allow_request(self,request,view):
                # 1. 获取用户IP
                remote_addr = request.META.get('REMOTE_ADDR')
                # remote_addr = request._request.META.get('REMOTE_ADDR') 
                ctime = time.time()
                if remote_addr not in VISIT_RECORD:
                    VISIT_RECORD[remote_addr] = [ctime,]
                    return True
                history = VISIT_RECORD.get(remote_addr)
                self.history = history

                while history and history[-1] < ctime - 60:
                    history.pop()
                    
                if len(history) < 3:
                    history.insert(0,ctime)
                    return True

                # return True    # 表示可以继续访问
                # return False   # 表示访问频率太高，被限制
                
             def wait(self):
                """
                还需要等多少秒才能访问
                :return:
                """
                ctime = time.time()
                return 60 - (ctime - self.history[-1])
	- 内置节流
    	from rest_framework.throttling import SimpleRateThrottle
    	class VisitThrottle1(SimpleRateThrottle):
        	scope = "Luffy"

            def get_cache_key(self, request, view):
                return self.get_ident(request)

        class UserThrottle2(SimpleRateThrottle):
            scope = "LuffyUser"
            
            def get_cache_key(self, request, view):
                return request.user.username		
- 局部使用 
	class AuthView(APIView):
        """
        用于用户登录认证
        """
        # 如果 sittings.py 中做了全局配置， 此步骤可以省略。
        throttle_classes = [VisitThrottle,]
        def post(self,request,*args,**kwargs):
           
			ret = {'code':1000,'msg':None}
            try:
                user = request._request.POST.get('username')
                pwd = request._request.POST.get('password')
                obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
                if not obj:
                    ret['code'] = 1001
                    ret['msg'] = "用户名或密码错误"
                    # 为登录用户创建token
            	token = md5(user)
            	# 存在就更新，不存在就创建
            	models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            	ret['token'] = token
            except Exception as e:
                ret['code'] = 1002
                ret['msg'] = '请求异常'

            return JsonResponse(ret)
 - 全局使用
	REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_CLASSES":["api.utils.throttle.UserThrottle"],  # 自定义 Throttle 类
        # 继承自带的 Throttle 类
        "DEFAULT_THROTTLE_RATES":{
            "Luffy":'3/m',
            "LuffyUser":'10/m',
        }
    }
```

__案列__

```Python
Throttle.py
from rest_framework.throttling import SimpleRateThrottle
class VisitThrottle(SimpleRateThrottle):
    scope = "Luffy"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = "LuffyUser"

    def get_cache_key(self, request, view):
        return request.user.username    # 对当前用户进行限制

views.py
class UserInfoView(APIView):
    throttle_classes = [VisitThrottle,]

    def get(self,request,*args,**kwargs):
        return HttpResponse('用户信息')

settings.py
REST_FRAMEWORK = {
	"DEFAULT_THROTTLE_RATES":{
        "Luffy":'3/m',
        "LuffyUser":'10/m',
    }
}
```



## 四、版本

```python
* 使用
	- URL中通过GET传参()
		http://127.0.0.1:8000/api/users/?version=v2
    	自定义：			
        class ParamVersion(object):
        	def determine_version(self, request, *args, **kwargs):
            	version = request.query_params.get('version')
                return version

		class UsersView(APIView):
			versioning_class = ParamVersion
            def get(self,request,*args,**kwargs):
            	# version = request._request.GET.get('version')     
            	# version = request.query_params.get('version')
            	return HttpResponse('用户列表')
        使用自带类:
        from rest_framework.versioning import QueryParameterVersioning
        
        class MyVersion(APIView):
		    versioning_class = QueryParameterVersioning

		    def get(self, request, *args, **kwargs):
        		print(request.version)
        		return HttpResponse('查看版本！')
         
         settings：
         REST_FRAMEWORK = { 
         	"DEFAULT_VERSION": "v1",            # 默认版本
		    "ALLOWED_VERSIONS": ["v1", "v2"],   # 允许的版本
    		"VERSION_PARAM": "version",         # url 中获取值得 key
		 	}
        		
	- 在URL中
    	views：
		class MyVersion(APIView):
            
		    def get(self, request, *args, **kwargs):    
        		# 通过 request.version 来获取版本
        		print(request.version)

                # 获取版本的对象
                print(request.versioning_scheme)

                # 反向生成 URL （Rest Framework）
                url = request.versioning_scheme.reverse(viewname='Versions', request=request)
                print(url)

                # django 的反向生产 URL
                from django.urls import reverse
                url1 = reverse(viewname='Versions', kwargs={'version': 'v2'})
                print(url1)

                return HttpResponse('查看版本！')
		
		settings 中：
		REST_FRAMEWORK = { 
			"DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
            "DEFAULT_VERSION": "v1",            # 默认版本
		    "ALLOWED_VERSIONS": ["v1", "v2"],   # 允许的版本
    		"VERSION_PARAM": "version",         # 参数 key
		}
		url 中：
		urlpatterns = [
			re_path(r'api/(?P<version>[v1|v2]+)/version/$', MyVersion.as_view(), name='Versions'),
		]        
```



## 五、解析器

```python
* 使用
	settings 中:
    REST_FRAMEWORK = {
        "DEFAULT_PARSER_CLASSES": [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.FormParser",
        ],
    }
    views:
    class MyParser(APIView):
        """
        JSONParser: 仅处理请求头: content-type:application/json 的请求体
        FormParser: 仅处理请求头: content-type:application/x-www-form-urlencoded 请求体
     	MultiPartParser: 仅处理请求头: content-type:multipart/form-data 的请求体
        FileUploadParser(仅上传文件): 仅处理请求头: content-type 为 multipart/form-data 的请求体
        """
        # parser_classes = [JSONParser,FormParser,]

        def post(self, request, *args, **kwargs):
            print(request.content_type)   # 获取请求头类型
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
            import json
            return HttpResponse(json.dumps(result))
	在URL中:
    urlpatterns = [
        re_path(r'api/(?P<version>[v1|v2]+)/parsers/$', MyParser.as_view()),
    ]
    
    
# >>>>>> application/x-www-form-urlencoded 或 multipart/form-data 时，request.POST 中才有值 <<<<<<
```



## 六、序列化

### 1. 序列化

```python
Django ORM对象 --> JSON格式的数据　　序列化
JSON格式的数据 --> Django ORM数据　　反序列化

# 序列化类
from rest_framework.serializers import Serializer
from rest_framework.serializers import MoselSerializer 

"""
字段参数：
	source, 指定要序列化表中的哪个字段
	many=True, 序列化多个对象
	read_only = True, 正向序列化用 
	write_ony = True, 反向序列化用 
"""
# serialize.py
# ----------------------------- 序列化 -----------------------------
class RoleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()


# 继承 serializers.Serializer
class UserInfoSerializer(serializers.Serializer):
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
#         # exclude = [] 可以明确排除掉哪些字段
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
#     # 参数 lookup_url_kwarg 指的是 url 中 pk 的值
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

        # 总结
# 当序列化时继承 ModelSerializer
"""
使用步骤：
	1、新建序列化类，继承ModelSerializer
	2、类中定义和模型表一一对应的字段，这里可以定义class Meta: 然后指定模型表 model 和映射字段 fields，比 Serializer更简洁
    	-其中类中的名字可以改变，需要在 serializers.CharField()的括号中指定 source=某个字段，建立映射关系
    	-外键关系的字段可以用 serializers.SerializerMethodField()，需要在下方固定写 get_字段名 的方法，
         这里可以写具体逻辑，最终返回结果就是该字段的结果。
	3、当新增数据的时候不需要重写父类的 create 方法，这里 ModelSerializer做了封装
	4、当修改数据的时候不需要重写父类的 update 方法，这里 ModelSerializer做了封装
	5、当完成这些配置后就可以在视图类中实例化调用了，序列化的时候序列化，反序列化的时候校验
	
	字段详解：
	# 使用 fields来明确字段，__all__表名包含所有字段，也可以写明具体哪些字段，如
	# 使用 exclude可以明确排除掉哪些字段
	# 使用 extra_kwargs参数为 ModelSerializer添加或修改原有的选项参数
"""

                
# views.py
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
        many=True, 如果序列化多条，一定要写many=True
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

```

### 2. 校验

*** 校验规则由序列化对象的 `is_valid` 触发**

```python
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
```



## 七、分页

### 1. 常规分页： `PageNumberPagination`

> **看第n页，每页显示n条数据；**  

```python
'''
PageNumberPagination类：支持用户按 ?page=2 这种方式查询，你可以通过 page_size 这个参数手动指定每页展示给用户数据的数量。它还支持用户按 ?page=3&size=10 这种更灵活的方式进行查询，这样用户不仅可以选择页码，还可以选择每页展示数据的数量。对于第二种情况，你通常还需要设置 max_page_size这个参数限制每页展示数据的最大数量，以防止用户进行恶意查询(比如size=10000), 这样一页展示1万条数据将使分页变得没有意义。
'''
# views.py
# 自定制分页继承 PageNumberPagination
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 3    # 每页显示的默认条数
    page_size_query_param = 'size'  # 查询参数的key, 更改每页条数(?size=3)
    max_page_size = 8  # 每页查询的最大条数

    page_query_param = 'page'  # 查询参数的key, 查询第几页(?page=2)
    """
    注意:
        也可以不用继承类 PageNumberPagination，
        直接在视图函数中实例化 pg = PageNumberPagination()，
        然后通过 对象.属性 去设置, 例如：pg.page_size = 3
    """


class Paging1View(APIView):
    """分页"""
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

# setting.py
REST_FRAMEWORK = {
    "PAGE_SIZE" = 3,  # 每页默认显示条数
}
```



### 2. 偏移分页：`LimitOffsetPagination`

> **在n个位置， 向后查看n条数据;**

```python
'''
LimitOffsetPagination类：偏移分页器。支持用户按?limit=20&offset=100这种方式进行查询。offset是查询数据的起始点，limit是每页展示数据的最大条数，类似于page_size。当你使用这个类时，你通常还需要设置max_limit这个参数来限制展示给用户数据的最大数量。
'''

# views.py
from rest_framework.pagination import LimitOffsetPagination
                                       

class Paging2View(APIView):
    """分页"""
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

        # 每页显示最大的条数
        pag.max_limit = 5

        # 在数据库中获取分页数据
        result = pag.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        roles_ser = serializer.PagerSerializer(instance=result, many=True)

        # 生成上一页或下一页链接(get_paginated_response)
        # return pag.get_paginated_response(roles_ser.data)
        return Response(roles_ser.data)
    
    
# setting.py
REST_FRAMEWORK = {
    "PAGE_SIZE" = 3,  # 每页默认显示条数
}
```



### 3. cursor游标方式分页：`CursorPagination`

> **上一页和下一页。**

```python
"""
CursorPagination类：加密分页器。这是DRF提供的加密分页查询，仅支持用户按响应提供的上一页和下一页链接进行分页查询，每页的页码都是加密的。使用这种方式进行分页需要你的模型有"created"这个字段，否则你要手动指定ordering排序才能进行使用。
"""

# views.py
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

    
# setting.py
REST_FRAMEWORK = {
    "PAGE_SIZE" = 3,  # 每页默认显示条数
}
```

*分页参考连接:* <https://www.cnblogs.com/qianzhengkai/p/11146539.html>



## 八、视图

### 1. 视图

```python
"""
一、AIPView - API 视图类
	APIView 是 Django REST Framework 提供的所有视图的基类，继承自 Django 的 View 父类。

与 Django View 的不同
	1.传入到视图方法中的是 REST framework 的 Request 对象，而不是 Django 的 HttpRequeset 对象
	2.视图方法可以返回 REST framework 的 Response 对象，视图会为响应数据设置（render）符合前端要求的格式
	3.任何 APIException 异常都会被捕获到，并且处理成合适的响应信息
	4.在进行 dispatch() 分发前，会对请求进行身份认证、权限检查、流量控制
 	
重要类属性
AIPView 有如下可设置的重要类属性：
	1.authentication_classes：列表或元祖，身份认证类
	2.permissoin_classes：列表或元祖，权限检查类
	3.throttle_classes：列表或元祖，流量控制类
"""


"""
二、GenericAPIView - 通用 API 视图类
	通用 API 视图类 GenericAPIView 继承自 APIView，完全兼容 APIView，主要增加了操作序列化器和数据库查询的方法，作用是为下面 Mixin 扩展类的执行提供基础类支持。通常在使用时，可以配合一个或多个 Mixin 扩展类。

GenericAPIView 比 APIView 多了什么
	1.get_queryset()：从类属性 queryset中获得 model 的 queryset 数据。群操作就走 get_queryset() 方法 (包括群查，群增等)。
	2.get_object()：从类属性 queryset 中获得 model 的 queryset 数据，再通过有名分组 pk 确定唯一操作对象。单操作就走 get_object() 方法（包括单查，单增等）。
	3.get_serializer()：从类属性 serializer_class 中获得 serializer 的序列化类。

重要类属性:
GenericAPIView 有如下可设置的重要类属性：
	列表视图与详情视图共用:
		queryset：指明视图需要的数据（model 查询数据）
		permissoin_classes：指明视图使用的序列化器
	列表视图使用:
		pagination_class：指定分页控制类
		filter_backends：指定过滤控制后端
	详情页视图使用:
		lookup_field：自定义主键，有名分组的查询，默认是 pk
		lookup_url_kwarg：查询单一数据时 url 中的参数关键字名称，默认与 look_field 相同
重要类方法:	
	get_queryset()：从类属性 queryset 中获得 model 的 queryset 数据　　
	get_object()：从类属性 queryset 中获得 model 的 queryset 数据，再通过有名分组 pk 来确定唯一操作对象
	get_serializer()：从类属性 serializer_class 中获得 serializer 的序列化类，主要用来提供给 Mixin 扩展类使用
"""
# 使用：
# views.py
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
    
    
"""
三、xxxAPIView - 功能性子视图类
	功能性子视图类继承了 GenericAPIView 和各种 Mixins 工具类
	功能性视图类都是 GenericAPIView 的子类，且不同的子类继承了不同的工具类
	工功能性视图类的功能可以满足需求，只需要继承工具视图，并且提供 queryset 与 serializer_class 即可.
	
	
功能性视图子类:
	1）CreateAPIView:
		提供 post 方法, 继承自： GenericAPIView、CreateModelMixin
	2）ListAPIView:
    	提供 get 方法, 继承自：GenericAPIView、ListModelMixin
    3）RetrieveAPIView:
    	提供 get 方法, 继承自: GenericAPIView、RetrieveModelMixin
    4）DestoryAPIView:
    	提供 delete 方法, 继承自：GenericAPIView、DestoryModelMixin
    5）UpdateAPIView:
    	提供 put 和 patch 方法, 继承自：GenericAPIView、UpdateModelMixin
    6）RetrieveUpdateAPIView:
    	提供 get、put、patch方法, 继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin
   	7）RetrieveUpdateDestoryAPIView
		提供 get、put、patch、delete方法,继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、				DestoryModelMixin
"""
# 使用：
# views.py
from rest_framework.generics import ListAPIView, CreateAPIView


class View1View(ListAPIView, CreateAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination
```

**各大功能子视图类表：**

|   视图类    |     作用     | 请求类型 |              父类              |
| :---------: | :----------: | :------: | :----------------------------: |
| ListAPIView | 查询多条数据 |   get    | GenericAPIView、ListModelMixin |
| CreateAPIView | 新增一条数据 | post | GenericAPIView、CreateModelMixin |
| RetrieveAPIView | 查询一条数据 | get | GenericAPIView、RetrieveModelMixin |
| UpdateAPIView | 修改一条数据 | put、patch | GenericAPIView、UpdateModelMixin |
| DestroyAPIView | 删除一条数据 | delete | GenericAPIView、DestroyModelMixin |
| RetrieveUpdateAPIView | 单查、更新一条数据 | get、put、patch | GenericAPIView、RetrieveModelMixin、UpdateModelMixin |
| RetrieveUpdateDestroyAPIView | 单查、更新、修改、删除一条数据 | get、put、patch、delete | GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestroyModelMixin |
| ListCreateAPIView | 群查、更新一条 | get、post | GenericAPIView、ListModelMixin、CreateModelMixin |



### 2. 视图集

```python
"""
一、常用视图集父类
1.ViewSetMixin
	ViewSetMixin 主要是自定义了 as_view 方法，使可以通过其参数指定 HTTP_METHOD 与函数的映射关系，如 view = 		MyViewSet.as_view({'get': 'list', 'post': 'create'})

2.ViewSet:
	继承自 APIView 和 ViewSetMixin，没有提供任何方法，需要自己写

3.GenericViewSet:
	继承 GenericAPIView 和 ViewSetMixin，其中 GenericAPIView 提供了基础方法，可以直接搭配 Mixin扩展类使用，因此比较常用

4.ModelViewSet　　
	继承 GenericViewset，但同时也包括 ListModelMixin、CreateModelMixin 等 mixin 扩展类
*注意*：
	1.视图集都是默认【优先继承 ViewSetMixin 类】，再继承一个视图类（GenericAPIView 或 APIView）
	2.ViewSetMixin 提供了重写的 as_view() 方法，继承视图集的视图类，配置路由时调用 as_view() 必须传入 请求名 - 函数名 映射关系字典


二、xxxModelMixin - 视图类的模型工具集
作用:
	1.提供了几种后端视图（对数据资源的增删改查）处理流程的实现，如果需要编写的视图属于这五种，则视图可以通过继承相应的扩展类来复用代码，减少自己编写的代码量。
	2.mixins 有五个工具类文件，一共提供了五个工具类，六个工具方法：单查、群查、单增、单删、单整体改、单局部改
使用:
	1.继承工具类可以简化请求函数的实现体，但是必须继承 GenericAPIView，需要 GenericAPIView 类提供序列化器与数据库查询的方法 (见上方 GenericAPIView 基类知识点)
	2.工具类的工具方法返回值都是 Response 类型对象，如果要格式化数据格式再返回给前台，可以通过 response.data 拿到工具方法返回的 Response 类型对象的响应数据

五大模型工具类：
1）ListModelMixin 群查:
	1.列表视图扩展类，提供 list(request, *args, **kwargs) 方法快速实现查询视图
	2.返回 200 状态码
	3.除了查询，该 list 方法会对数据进行过滤和分页
2）CreateModelMixin 单增:
	1.创建视图扩展类，提供 create(request, *args, **kwargs) 方法快速创建资源的视图，成功返回 201 的状态码
	如果序列化器对前端发送的数据验证失败，返回400错误。
	2.没有群增的方法，需要自己手动写
3）RetrieveModelMixin 单查:
	1.详情视图扩展类，提供 retrieve(request, *args, **kwargs) 方法，可以快速实现返回一个存在的数据对象
	2.如果存在，返回200， 否则返回404。
4）UpdateModelMixin 更新/修改:
	1.更新视图扩展类，提供 update(request, *args, **kwargs) 方法，可以快速实现更新一个存在的数据对象，同时也提供 partial_update 方法，可以实现局部更新
	2.只有单整体改和单局部改，没有群整体改和群局部改
	3.成功返回200，序列化器校验数据失败时，返回400错误。
5）DestoryModelMixin 删除:
	1.删除视图扩展类，提供 destory(request, *args, **kwargs) 方法，可以快速实现删除一个存在数据对象
	2.一般不怎么用到，因为实际开发中并不会真的删除数据，而是修改是否可用的标记
	3.成功返回204，不存在返回404。

三、使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
	list() 提供一组数据
	retrieve() 提供单个数据
	create() 创建数据
	update() 保存数据
	destory() 删除数据
ViewSet 视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。
视图集只在使用as_view()方法的时候，才会将action动作与具体请求方式对应上。
"""

# 使用：
# view.py
# 使用方法1
from rest_framework.viewsets import GenericViewSet


class View1View(GenericViewSet):
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
# urls.py
urlpatterns = [
	re_path(r'api/(?P<version>[v1|v2]+)/views/$', View1View.as_view({'get': 'list'})),
]


# 使用方法2
from rest_framework.viewsets import ModelViewSet


class View1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination
# urls.py
urlpatterns = [
	re_path(r'api/(?P<version>[v1|v2]+)/views/(?P<pk>\d+)/$',
    	View1View.as_view({
            'get': 'retrieve', 'delete': 'destroy',
            'put': 'update', 'patch': 'partial_update'
        })),
]


# 使用方法3
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin


class View1View(CreateModelMixin, GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializer.PagerSerializer
    pagination_class = PageNumberPagination   
# urls.py
urlpatterns = [
	re_path(r'api/(?P<version>[v1|v2]+)/views/$', View1View.as_view({'post': 'create'})),,
]
```

**常用视图集父类表：**

| 视图类  | 继承类 | 作用                                                         |
| ------- | ------ | ------------------------------------------------------------ |
| ViewSetMixin | None   | ViewSetMixin` 主要是自定义了 `as_view` 方法，使可以通过其参数指定 `HTTP_METHOD` 与函数的映射关系，如 `view = MyViewSet.as_view({'get': 'list', 'post': 'create'}) |
|ViewSet|APIView、ViewSetMixin|没有提供任何方法，需要自己写|
|GenericViewSet|GenericAPIView、ViewSetMixin|Mixin扩展类依赖于`GenericAPIView`，所以还需要继承`GenericAPIView`   `GenericAPIView` 提供了基础方法，可以直接搭配 `Mixin` 扩展类使用，因此比较常用|
|ModelViewSet|GenericViewset、|同时也包括 `ListModelMixin`、`CreateModelMixin` 等 `mixin` 扩展类|



视图继承图：

![继承图](/photo/1.png)

### 异同：

1. `GenericViewSet` 和 `ViewSet` 都继承了 `ViewSetMixin`，`as_view` 都可以配置 请求 - 函数 映射

2. <font color=red> `GenericViewSet` 继承的是 `GenericAPIView` 视图类，用来完成标准的 `model` 类操作接口</font>

3. `ViewSet` 继承的是 `APIView` 视图类，用来完成不需要 `model` 类参与，或是非标准的 `model` 类操作

   接口，如

   - `post` 请求在标准的 `model` 类操作下就是新增接口，登陆的 `post` 不满足。登陆的 post 请求，并不是完成数据的新增，只是用 post 提交数据，得到的结果也不是登陆的用户信息，而是登陆的认证信息
   - `post` 请求验证码的接口，不需要 `model` 类的参与



## 九、路由

```python
# 自动生成路由

from django.urls import re_path, include
from rest_framework import routers

# 路由注册
router = routers.DefaultRouter()
router.register(r'view6', View6View)

urlpatterns = [
    re_path(r'^api/(?P<version>[v1|v2]+)/', include(router.urls)),
]
# urlpatterns += router.urls

# 生成以下映射 URL.
# /api/(?P<version>[v1|v2]+)/ ^view6/$ [name='role-list']
# /api/(?P<version>[v1|v2]+)/ ^view6\.(?P<format>[a-z0-9]+)/?$ [name='role-list']
# /api/(?P<version>[v1|v2]+)/ ^$ [name='api-root']
# /api/(?P<version>[v1|v2]+)/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']

# 总结： 单个或者两个 URL，自定义， 实现增删改查就是用自动生成。
```



## 十、渲染器

**作用:  使返回的数据美观**

使用：

```python
全局配置中添加:
INSTALLED_APPS = [
    'rest_framework',
]

视图中:
from rest_framework.response import Response
class xxx(APIView):
    return Response(Serializer_Obj.data)
```



__rest_framework部分参考__：<https://www.cnblogs.com/wupeiqi/articles/7805382.html>

