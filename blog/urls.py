"""
restframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import *
from django.urls import re_path, include
from rest_framework import routers

# 路由注册
router = routers.DefaultRouter()
router.register(r'view6', View6View)


urlpatterns = [
    re_path(r'^api/(?P<version>[v1|v2]+)/authentication/$',
            AuthenticationView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/articles/$', ArticlesView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/users/all/$', AllUserView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/version/$', MyVersionView.as_view(),
            name='Versions'),
    re_path(r'^api/(?P<version>[v1|v2]+)/parsers/$', MyParserView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/roles/$', RoleView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/users/$', UserInfoView.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$',
            GroupView.as_view(), name='gp'),
    re_path(r'^api/(?P<version>[v1|v2]+)/usergroup/$',
            UserGroupView.as_view(), name='gp'),

    re_path(r'^api/(?P<version>[v1|v2]+)/role1/$', Paging1View.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/role2/$', Paging2View.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/role3/$', Paging3View.as_view()),

    re_path(r'^api/(?P<version>[v1|v2]+)/views1/$', View1View.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/views2/$', View2View.as_view()),
    re_path(r'^api/(?P<version>[v1|v2]+)/views3/$', View3View.as_view({'get': 'list'})),
    re_path(r'^api/(?P<version>[v1|v2]+)/views4/(?P<pk>\d+)/$',
            View4View.as_view({
                'get': 'retrieve', 'delete': 'destroy',
                'post': 'create', 'patch': 'partial_update'
               })),
    re_path(r'^api/(?P<version>[v1|v2]+)/views5/$',
            View5View.as_view({'post': 'create'})),

    re_path(r'^api/(?P<version>[v1|v2]+)/', include(router.urls)),
]


# urlpatterns += router.urls