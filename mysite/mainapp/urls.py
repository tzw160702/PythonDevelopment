"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from .views import *


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login),
    path('index/', index),

    # 班级
    path('classes/', classes),
    path('add_class/', add_class),
    path('del_class/', del_class),
    path('edit_class/', edit_class),

    path('modal_add_class/', modal_add_class),  # 拟态对话框 添加班级
    path('modal_edit_class/', modal_edit_class),

    # 学生
    path('students/', students),
    path('add_student/', add_student),
    path('del_student/', del_student),
    path('edit_student/', edit_student),

    path('modal_add_student/', modal_add_student),    # 模态对话框添加学生
    path('modal_edit_student/', modal_edit_student),

    # 教师
    path('teachers/', teachers),
    path('add_teacher/', add_teacher),
    path('del_teacher/', del_teacher),
    path('edit_teacher/', edit_teacher),

    path('get_all_class/', get_all_class),       # 模态对话框添加 (拿到所有老师)
    path('modal_add_teacher/', modal_add_teacher),
    path('btn_edit_teacher/', btn_edit_teacher),   # 功能未实现

    path('responsive_page/', responsive_page),  # 响应式布局

    path('layout/', layout),  # 后台管理页面布局
]
