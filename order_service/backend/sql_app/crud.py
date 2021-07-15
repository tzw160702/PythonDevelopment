#!/usr/bin/python3

import math
import copy
import json
import requests

from login import env
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sql_app.models import OrderInfo, ShopCar
from oslo_db.sqlalchemy import utils as sqlalchemyutils


def save(db):
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def paginate_query(query, model, limit, temp_offset, sort_key, sort_dir="asc"):
    """
    分页查询
    :param model:
    :param query
    :param limit:
    :param temp_offset:
    :param sort_key:
    :param sort_dir:
    :param query:
    :return:
    """
    if not sort_key:
        sort_keys = []
    elif not isinstance(sort_key, list):
        sort_keys = [sort_key]
    else:
        sort_keys = sort_key

    query = sqlalchemyutils.paginate_query(query,
                                           model,
                                           limit,
                                           sort_keys,
                                           sort_dir=sort_dir)
    query = query.offset(temp_offset)
    return query.all()


def query_order(query):
    """
    数据处理
    :param query:
    :return:
    """
    one_order = {
        "picture": {"path": None, "photo_name": None},
        "consignee": {
            "consignee_name": None,
            "consignee_addr": None,
            "consignee_phone": None
        }
    }

    done_order = list()
    for item in query:
        order = copy.deepcopy(one_order)
        order["order_id"] = item.order_id
        order["order_name"] = item.order_name
        order["picture"]["path"] = item.photo[0].path
        order["picture"]["photo_name"] = item.photo[0].photo_name
        order["order_amount"] = item.order_amount
        order["order_money"] = item.order_money
        order["consignee"]["consignee_name"] = item.consignee.consignee_name
        order["consignee"]["consignee_addr"] = item.consignee.consignee_addr
        order["consignee"]["consignee_phone"] = item.consignee.consignee_phone
        order["order_status"] = item.order_status
        order["order_time"] = item.created_time
        order["order_number"] = item.order_number
        done_order.append(order)
    return done_order


def fetch_all_order(page, limit, db: Session):
    """
    获取全部订单
    :param page
    :param limit:
    :param db:
    :return:
    """
    temp_offset = None

    non_payment = db.query(OrderInfo).filter_by(is_delete=0)

    total_count = non_payment.count()

    page = page
    limit = limit
    if total_count >= 1:
        if total_count % limit == 0:
            page_count = total_count / limit
        else:
            page_count = (total_count / limit) + 1

        if page > page_count:
            page = page_count
        temp_offset = (page - 1) * limit

    resource_list = paginate_query(non_payment, OrderInfo, limit,
                                   temp_offset, sort_key="order_id")

    resources = query_order(resource_list)
    page_count = int(math.ceil(total_count / limit))

    return {"data": resources, "page_count": page_count}


def fetch_done_order(page, limit, db: Session):
    """
    已完成订单
    :param page
    :param limit
    :param db:
    :return:
    """
    temp_offset = None

    non_payment = db.query(OrderInfo).filter_by(order_status="已支付",
                                                is_delete=0)

    total_count = non_payment.count()
    limit = limit
    page = page
    if total_count >= 1:
        if total_count % limit == 0:
            page_count = total_count / limit
        else:
            page_count = (total_count / limit) + 1

        if page > page_count:
            page = page_count
        temp_offset = (page - 1) * limit

    resource_list = paginate_query(non_payment, OrderInfo, limit,
                                   temp_offset, sort_key="order_id")

    resources = query_order(resource_list)
    page_count = int(math.ceil(total_count / limit))

    return {"data": resources, "page_count": page_count}


def fetch_undone_order(page, limit, db: Session):
    """
    未完成订单
    :param page
    :param limit
    :param db:
    :return:
    """
    temp_offset = None

    non_payment = db.query(OrderInfo).filter_by(order_status="未支付",
                                                is_delete=0)

    total_count = non_payment.count()
    limit = limit
    page = page
    if total_count >= 1:
        if total_count % limit == 0:
            page_count = total_count / limit
        else:
            page_count = (total_count / limit) + 1

        if page > page_count:
            page = page_count
        temp_offset = (page - 1) * limit

    resource_list = paginate_query(non_payment, OrderInfo, limit,
                                   temp_offset, sort_key="order_id")

    resources = query_order(resource_list)
    page_count = int(math.ceil(total_count / limit))

    return {"data": resources, "page_count": page_count}


def order_details(order_id: int, db: Session):
    """
    订单详情
    :param order_id:
    :param db:
    :return:
    """
    query = db.query(OrderInfo).filter_by(order_id=order_id, is_delete=0).one()
    if query is None:
        return None

    picture = list()
    for photo in query.photo:
        dic_info = dict()
        dic_info["path"] = photo.photo_name
        dic_info["photo_name"] = photo.path
        picture.append(dic_info)

    return {
        "order_id": query.order_id,
        "order_name": query.order_name,
        "picture": picture,
        "order_amount": query.order_amount,
        "order_money": query.order_money,
        "consignee": {
            "consignee_name": query.consignee.consignee_name,
            "consignee_addr": query.consignee.consignee_addr,
            "consignee_phone":query.consignee.consignee_phone
        },
        "order_status": query.order_status,
        "order_time": query.created_time,
        "order_number": query.order_number
    }


def db_update_order(update_order, db: Session):
    """
    修改订单
    :param update_order:
    :param db:
    :return:
    """
    query = db.query(OrderInfo).filter_by(
        order_id=update_order.order_id, is_delete=0).one()
    if query is None:
        return None
    if update_order.order_name is not None:
        query.order_name = update_order.order_name
    if update_order.order_amount is not None:
        query.order_amount = update_order.order_amount
    if update_order.order_money is not None:
        query.order_money = update_order.order_money
    if update_order.consignee.consignee_name is not None:
        query.consignee.consignee_name = update_order.consignee.consignee_name
    if update_order.consignee.consignee_phone is not None:
        query.consignee.consignee_phone = update_order.consignee.consignee_phone
    if update_order.consignee.consignee_addr is not None:
        query.consignee.consignee_addr = update_order.consignee.consignee_addr
    if update_order.order_status is not None:
        query.order_status = update_order.order_status

    db.add(query)
    save(db)
    db.refresh(query)

    pictures = list()
    for photo in query.photo:
        dic_info = dict()
        dic_info["path"] = photo.photo_name
        dic_info["photo_name"] = photo.path
        pictures.append(dic_info)
    return {
        "order_id": query.order_id,
        "order_name": query.order_name,
        "picture": pictures,
        "order_amount": query.order_amount,
        "order_money": query.order_money,
        "consignee": {
            "consignee_name": query.consignee.consignee_name,
            "consignee_addr": query.consignee.consignee_addr,
            "consignee_phone": query.consignee.consignee_phone
        },
        "order_status": query.order_status,
        "order_time": query.created_time,
        "order_number": query.order_number
    }


def db_del_order(order_id: int, db: Session):
    """
    删除订单
    :param order_id:
    :param db:
    :return:
    """
    del_order = db.query(OrderInfo).filter_by(
        order_id=order_id, is_delete=0).one()
    if del_order is None:
        raise HTTPException(status_code=404, detail="类型id错误或id不存在")
    else:
        del_order.is_delete = 1
        db.add(del_order)
        save(db)
        db.refresh(del_order)
        return {"status": 200, "message": "Success!"}


def all_comm(db: Session):
    """
    购物车列表
    :param db:
    :return:
    """
    commodity_list = db.query(ShopCar).filter_by(is_delete=0).all()
    resolute_list = list()
    data_format = {
        "picture": {"path": None, "photo_name": None}
    }
    for commodity in commodity_list:
        data = copy.deepcopy(data_format)
        data["id"] = commodity.id
        data["commodity_name"] = commodity.commodity_name
        data["commodity_spec"] = commodity.commodity_spec
        data["price"] = commodity.price
        data["commodity_count"] = commodity.commodity_count
        data["picture"]["path"] = commodity.shop_car.path
        data["picture"]["photo_name"] = commodity.shop_car.photo_name
        resolute_list.append(data)

    return resolute_list


def del_comm(commodity_id, db: Session):
    """
    购物车删除删除商品
    :param commodity_id:
    :param db:
    :return:
    """
    del_commodity = db.query(ShopCar).filter_by(
        id=commodity_id, is_delete=0).one()
    if del_commodity is None:
        raise HTTPException(status_code=404, detail="类型id错误或id不存在")
    else:
        del_commodity.is_delete = 1
        db.add(del_commodity)
        save(db)
        db.refresh(del_commodity)
        return {"status": 200, "message": "Success!"}


# ------------------------------- 登录 ---------------------------------
# Admin
def load_user(data):
    url = env.SINGLE_SIGN_ON_USER + "/singin"
    headers = {'Content-Type': 'application/json'}
    dataload = {"number": data.number, "pwd": data.pwd,
                "client_code": data.client_code,
                "callback_url": data.callback_url}
    datas = json.dumps(dataload)
    # send data
    response = requests.post(url=url, data=datas, headers=headers)

    return json.loads(response.text)


def send_code(number):
    urlbase = env.SINGLE_SIGN_ON_CODE + "/verify_code"
    headers = {'Content-Type': 'application/json'}
    url = urlbase + f"?number={number}"
    # send data
    response = requests.post(url=url, headers=headers)

    return json.loads(response.text)


def verify_code_login(data):
    url = env.SINGLE_SIGN_ON_USER + "/signin/verifycode"
    headers = {'Content-Type': 'application/json'}
    dataload = {"number": data.number, "verify_code": data.verify_code,
                "callback_url": data.callback_url}
    datas = json.dumps(dataload)
    # send data
    response = requests.post(url=url, data=datas, headers=headers)

    return json.loads(response.text)


def create_user(data):
    url = env.SINGLE_SIGN_ON_USER + "/signup"
    headers = {'Content-Type': 'application/json'}
    dataload = {"number": data.number, "pwd": data.pwd,
                "verify_code": data.verify_code}
    datas = json.dumps(dataload)
    # send data
    response = requests.post(url=url, data=datas, headers=headers)

    return json.loads(response.text)


def client_code():
    url = env.SINGLE_SIGN_ON_CODE + "/client_code"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url=url, headers=headers)
    return json.loads(response.text)


def change_pwd(data):
    url = env.SINGLE_SIGN_ON_USER + "/password"
    headers = {'Content-Type': 'application/json'}
    dataload = {"token": data.token, "old_pwd": data.old_pwd,
                "new_pwd": data.new_pwd}
    datas = json.dumps(dataload)
    # send data
    response = requests.patch(url=url, data=datas, headers=headers)

    return json.loads(response.text)


def verify_code_password(data):
    url = env.SINGLE_SIGN_ON_USER + "/verify_code_password"
    headers = {'Content-Type': 'application/json'}
    dataload = {"number": data.number, "pwd": data.pwd,
                "verify_code": data.verify_code}
    datas = json.dumps(dataload)
    # send data
    response = requests.patch(url=url, data=datas, headers=headers)

    return json.loads(response.text)


# ----------------------- 用于上传文件 ---------------------------
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
save_dir = "resources/images"

# 文件上传
def upload(files):
# 判断目录是否存在
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    tmp_filename = list()
    for file in files:
        try:
            suffix = Path(file.filename).suffix
            with NamedTemporaryFile(
                    delete=False, suffix=suffix, dir=save_dir) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_filename.append(Path(tmp.name).name)
        except:
            raise
    return tmp_filename

