from django.shortcuts import render, redirect, HttpResponse

from pymysql.connections import Connection
from pymysql.cursors import Cursor

from modular import sql_connect

import pymysql
import json

import time


# Create your views here.


def login(request):  # 所有跟请求相关的数据都封装到request对象里面

    # return HttpResponse("ok")
    # print(request.method)
    if request.method == "GET":
        return render(request, "login.html")
    else:
        print(request.POST)  # 拿到用户信息
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        if user == "root" and pwd == "123123":
            print("登录成功")
            # return redirect("http://www.tzw160702.work")
            return redirect('/index/')
        else:
            return render(request, "login.html", {"msg": "用户或者密码输入错误"})


def index(request):
    return render(
        request,
        "index.html",
        {
            'name': 'tzw',
            'sex': {'zhangsan': '1', 'lisi': '2'},
            'zhouyuan': [1, 2, 3, 4, 5],
            'user_list_dict': [
                {'id': 1, 'name': 'tzw', 'email': 'tzw160702@163.com'},
                {'id': 2, 'name': 'zhouyuan', 'email': '17765032911@163.com'},
                {'id': 3, 'name': 'alex', 'email': '123456@163.com'},
            ]
        }
    )


# 一对一
def classes(request):
    """
        查看班级
        :param request: 封装请求相关的所有信息
        :return:
    """
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
    # print("--OK--")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，将游标设置为字典类型
    cursor.execute('select id,classname from class')  # 执行sql语句
    class_list = cursor.fetchall()  # 获取所有数据
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    # print(class_list)
    return render(request, 'classes.html', {'class_list': class_list})


def add_class(request):
    """
        添加班级
        :param request: 封装请求相关的所有信息
        :return:
    """
    if request.method == "GET":
        return render(request, "add_class.html")
    else:
        print(request.POST)  # 查看所有提交的数据
        v = request.POST.get("classname")
        if len(v) > 0:
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
            cursor.execute('insert into class(classname) values(%s)', [v, ])  # 执行添加sql语句
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return redirect("/classes/")
        else:
            return render(request, "add_class.html", {'msg': '班级名称不能为空'})


def del_class(request):
    """
        删除班级
        :param request: 封装请求相关的所有信息
        :return:
    """
    nid = request.GET.get('nid')
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
    cursor.execute('delete from class where id=%s', [nid, ])  # 执行删除 sql语句
    conn.commit()  # 提交
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接

    return redirect("/classes/")


def edit_class(request):
    """
        编辑班级
        :param request: 封装请求相关的所有信息
        :return:
    """
    if request.method == "GET":
        nid = request.GET.get('nid')
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
        cursor.execute('select id,classname from class where id=%s', [nid, ])  # 执行删除 sql语句
        result = cursor.fetchone()
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        # print(result)
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        classname = request.POST.get('classname')
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
        cursor.execute('update class set classname=%s where id=%s', [classname, nid])  # 执行删除 sql语句
        conn.commit()  # 提交
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接

        return redirect("/classes")


# 一对多
def students(request):
    """
        学生列表
        :param request: 封装请求相关的所有信息
        :return:
    """
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
    cursor.execute('select student.id, student.name,student.class_id,class.classname \
                    from student left join \
                    class on student.class_id = class .id ')  # 执行sql语句
    students_list = cursor.fetchall()  # 获取所有数据
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接

    # 对话框调用数据库
    class_list = sql_connect.get_sql_list('select id,classname from class', [])

    return render(request, 'students.html', {'students_list': students_list, 'class_list': class_list})


def add_student(request):
    """
       添加学生
       :param request: 封装请求相关的所有信息
       :return:
    """
    if request.method == 'GET':
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
        cursor.execute('select * from class')  # 执行sql语句
        class_list = cursor.fetchall()  # 获取所有数据
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
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
        cursor.execute('insert into student(name,class_id) values(%s,%s)', [name, class_id])  # 执行sql语句
        conn.commit()  # 提交
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        return redirect('/students/')


def del_student(request):
    """
       删除学生
       :param request: 封装请求相关的所有信息
       :return:
    """
    nid = request.GET.get('nid')
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
    cursor.execute('delete from student where id=%s', [nid, ])  # 执行sql语句
    conn.commit()  # 提交
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return redirect('/students/')


def edit_student(request):
    """
       编辑学生
       :param request: 封装请求相关的所有信息
       :return:
    """
    if request.method == "GET":
        nid = request.GET.get('nid')
        class_list = sql_connect.get_sql_list("select id,classname from class", [])
        current_student_info = sql_connect.get_one('select id,name,class_id from student where id=%s', [nid, ])
        return render(request, 'edit_student.html',
                      {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_connect.modify_sql('update student set name=%s,class_id=%s where id=%s', [name, class_id, nid, ])
        return redirect('/students/')


#  多对多
def teachers(request):
    """
       老师
       :param request: 封装请求相关的所有信息
       :return:
    """
    # teacher_list = sql_connect.get_sql_list('select * from teacher', [])
    teacher_list = sql_connect.get_sql_list("""
        select teacher.id as tid, teacher.name,class.classname from teacher
        left join teacher_to_class on teacher.id = teacher_to_class.teacher_id
        left join class on class.id = teacher_to_class.class_id;""", [])
    # print(teacher_list)
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['classnames'].append(row['classname'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'classnames': [row['classname'], ]}
    # print(result.values())
    return render(request, "teachers.html", {'teacher_list': result.values()})


def add_teacher(request):
    """
       添加老师
       :param request: 封装请求相关的所有信息
       :return:
    """
    if request.method == "GET":
        class_list = sql_connect.get_sql_list('select id,classname from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')

        # 老师表中添加一条数据
        teacher_id = sql_connect.create('insert into teacher(name) values(%s)', [name, ])
        # print(teacher_id)
        # 老师和班级关系表中插入数据
        # 获取当前添加的老师id
        class_ids = request.POST.getlist('class_ids')
        # print(name, class_ids)

        # 多次连接多次提交
        # for cls_id in class_ids:
        #     sql_connect.modify_sql('insert into teacher_to_class(teacher_id, class_id) values (%s,%s)',
        #                               [teacher_id, cls_id])

        # 一次连接多次提交
        # obj = sql_connect.SqlHelper()
        # for cls_id in class_ids:
        #     obj.modify('insert into teacher_to_class(teacher_id, class_id) values (%s,%s)',
        #                            [teacher_id, cls_id])
        # obj.close()

        # 提高性能
        # 一次连接一次提交
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id, cls_id,)
            # print(temp)
            data_list.append(temp)
        obj = sql_connect.SqlHelper()
        obj.multiple_modify('insert into teacher_to_class(teacher_id, class_id) values (%s,%s)', data_list)
        obj.close()
        return redirect('/teachers/')


def edit_teacher(request):
    """
       编辑老师
       :param request: 封装请求相关的所有信息
       :return:
    """
    if request.method == "GET":
        nid = request.GET.get('nid')
        obj = sql_connect.SqlHelper()
        teacher_info = obj.get_one(
            'select id,name from teacher where id =%s', [nid, ])
        class_list = obj.get_list('select id,classname from class', [])
        class_id_list = obj.get_list(
            'select class_id from teacher_to_class where teacher_id=%s', [nid, ])
        obj.close()

        # print('当前老师信息', teacher_info)
        # print('班级列表', class_list)
        # print('当前老师任教的班级id', class_id_list)
        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])
        # print('所有班级', class_list)
        # return HttpResponse('...')
        return render(request, 'edit_teacher.html', {
            'teacher_info': teacher_info,
            'class_id_list': temp,
            'class_list': class_list,
        })
    else:
        nid = request.GET.get('nid')  # 提交是 url 传参，url 传参放到GET请求里面
        name = request.POST.get('name')
        # print(name)
        class_ids = request.POST.getlist('class_ids')  # 传的是多值 使用getlist
        obj = sql_connect.SqlHelper()
        # 更新老师表
        obj.modify('update teacher set name=%s where id=%s', [name, nid, ])
        # 更新老师和班级表
        # 先把当前老师和班级的对应关系删除，然后再添加
        obj.modify('delete from teacher_to_class where teacher_id=%s', [nid, ])
        # print('class_ids',class_ids)
        data_list = []
        for cls_id in class_ids:
            temp = (nid, cls_id,)
            data_list.append(temp)
        obj.multiple_modify(
            'insert into teacher_to_class(teacher_id, class_id) values (%s,%s)'
            , data_list)
        obj.close()
        return redirect('/teachers/')


# 删除老师
def del_teacher(request):
    nid = request.GET.get('nid')
    obj = sql_connect.SqlHelper()
    obj.modify('delete from teacher_to_class where teacher_id=%s', [nid, ])
    obj.modify('delete from teacher where id=%s', [nid, ])
    obj.close()
    return redirect('/teachers/')


# ===================================对话框添加==================================
# form 表单提交会刷新页面  对话框不能用form表单提交

# 添加班级
def modal_add_class(request):
    classname = request.POST.get('classname')
    if len(classname) > 0:
        sql_connect.modify_sql('insert into class(classname) values(%s)', [classname, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级标题不能为空')


# 编辑班级
def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sql_connect.modify_sql('update class set classname=%s where id=%s', [content, nid, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))


# 添加学生
def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_connect.modify_sql('insert into student(name,class_id) values(%s,%s)', [name, class_id])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


# 编辑学生
def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_connect.modify_sql(
                        'update student set name=%s,class_id=%s where id=%s',
                         [name, class_id, nid, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


# 模态对话框获取所有班级
def get_all_class(request):  # 拿到班级
    """
    模态对话框拿到所有班级
    :param request:
    :return:
    """
    time.sleep(0.5)   # 延迟获取数据
    obj = sql_connect.SqlHelper()
    class_list = obj.get_list('select id,classname from class', [])
    # print(class_list)
    obj.close()
    return HttpResponse(json.dumps(class_list))   # json.dumps() 将python对象编码成 json字符串


# 模态对话框添加老师
def modal_add_teacher(request):
    """
    :param request:
    :return: json对象
    """
    ret = {"status": True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        teacher_id = sql_connect.create('insert into teacher(name) values(%s)',
                                        [name, ])
        print(f'提交名称: {name} 提交班级: {class_id_list}')  # 列表
        # print(teacher_id)
        class_list = []
        for class_id in class_id_list:
            print('每个班级：', class_id)
            tmp = (teacher_id, class_id)
            class_list.append(tmp)
        print('处理过的数据：', class_list)
        obj = sql_connect.SqlHelper()
        obj.multiple_modify(
            'insert into teacher_to_class(teacher_id,class_id) values (%s, %s)'
            , class_list)
        obj.close()
        print(class_list)
    except Exception as e:
        ret['status'] = False
        ret['message'] = "错误!"
    return HttpResponse(json.dumps(ret))


# 模态对话框添加老师
def btn_edit_teacher(request):
    pass


# =========================================================
# 测试响应式布局
def responsive_page(request):
    return render(request, 'responsive_page.html')


# 后台管理布局
def layout(request):
    return render(request, 'layout.html')