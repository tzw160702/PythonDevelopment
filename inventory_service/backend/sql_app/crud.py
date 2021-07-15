#!/usr/bin/python3

import os
import math
import copy
import json
import shutil
import requests

from pathlib import Path
from core import schemas
from login import env
from sql_app.models import *
from typing import List, Any
from sqlalchemy.sql import and_
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile
from fastapi import File, HTTPException
from oslo_db.sqlalchemy import utils as sqlalchemyutils

# 文件保存的目录
save_dir = "resources/images"


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


def db_create_type(db: Session, comm_type: schemas.Type):
    """
    增加类型
    :param db:
    :param comm_type:
    :return:
    """
    add_type = Type(type=comm_type.type)
    db.add(add_type)
    db.commit()
    db.refresh(add_type)
    return add_type


def db_get_type(db: Session):
    """
    获取所有类型
    :param db:
    :return:
    """
    fetch_type: List[Any] = db.query(Type.type_id, Type.type).all()
    type_list = []

    for one in fetch_type:
        data_handler = dict()
        data_handler['type_id'] = one[0]
        data_handler['type'] = one[1]
        data_handler['type'] = one[1]
        type_list.append(data_handler)
    all_type = dict()
    all_type["type_list"] = type_list
    return all_type


def db_modify_type(modify_type: schemas.CommType, db: Session):
    """
    修改商品类型
    :param db:
    :param modify_type
    :return:
    """
    result = db.query(Type).filter(Type.type_id == modify_type.type_id).first()
    if result is None:
        return {"Message: Error!"}
    else:
        db.query(Type).filter(Type.type_id == modify_type.type_id).update(
            {Type.type: modify_type.type})
        db.commit()
        local_type = db.query(Type).filter(
            Type.type_id == modify_type.type_id).first()
        return local_type


def db_del_type(type_id: int, db: Session):
    """
    删除商品类型
    :param db:
    :param type_id:
    :return:
    """
    all_type: List[Any] = db.query(Type.type_id).all()
    all_type_id = [item[0] for item in all_type]
    if type_id in all_type_id:
        db.query(Type).filter(Type.type_id == type_id).delete()
        db.commit()
        return {"Message": "Success!"}
    else:
        raise HTTPException(status_code=404, detail="类型id错误或id不存在")


def db_get_datatype(db: Session):
    """
    查询所有规格值数据类型
    :param db:
    :return:
    """
    fetch_datatype: List[Any] = db.query(Datatype.data_type_id,
                                         Datatype.data_type).all()
    return fetch_datatype


def db_create_spec(spec, db: Session):
    """
    添加规格
    :param spec:
    :param db:
    :return:
    """
    # 存放新增数据返回的 主键id
    list_id_spec = list()

    # 需要返回新增的数据列表
    list_add_spec = list()
    for item in spec:
        add_spec = Spec(
            spec_name=item.spec_name,
            data_type_id=item.data_type_id,
            spec_remark=item.spec_remark
        )
        db.add(add_spec)
        db.commit()
        db.refresh(add_spec)

        # 拿到主键 id 存放到列表.
        if add_spec.spec_id not in list_id_spec:
            list_id_spec.append(add_spec.spec_id)
        else:
            pass

    # 对新增值所返回的 id 查询。
    for ID in list_id_spec:
        res = db.query(Spec.spec_id, Spec.spec_name,
                       Spec.spec_remark, Datatype.data_type).outerjoin(
            Datatype, Spec.data_type_id == Datatype.data_type_id
        ).filter(Spec.spec_id == ID).first()
        list_add_spec.append(res)

    return list_add_spec


def db_get_spec(db: Session):
    """
    查询所有规格
    :param db:
    :return:
    """
    fetch_spec: List[Any] = db.query(Spec.spec_id, Spec.spec_name,
                                     Spec.spec_remark,
                                     Datatype.data_type).outerjoin(
        Datatype, Spec.data_type_id == Datatype.data_type_id).all()

    return fetch_spec


def db_modify_spec(spec_datatype: schemas.SpecDatatype, db: Session):
    """
    修改商品规格
    :param spec_datatype:
    :param db:
    :return:
    """
    result = db.query(Spec). \
        filter(Spec.spec_id == spec_datatype.spec_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="规格id错误或id不存在")
    else:

        db.query(Spec).filter(Spec.spec_id == spec_datatype.spec_id). \
            update({
                Spec.spec_name: spec_datatype.spec_name,
                Spec.data_type_id: spec_datatype.data_type_id,
                Spec.spec_remark: spec_datatype.spec_remark})
        db.commit()
        local_modify_spec = db.query(
            Spec.spec_id, Spec.spec_name, Spec.spec_remark,
            Datatype.data_type). \
            outerjoin(Datatype, Spec.data_type_id == Datatype.data_type_id). \
            filter(Spec.spec_id == spec_datatype.spec_id).first()

        return local_modify_spec


def db_create_commodity(commodity: schemas.Commodity, db: Session):
    """
    新增商品
    :param commodity:
    :param db:
    :return:
    """
    # Commodity 表添加数据
    add_comm = Commodity(
        commodity_name=commodity.commodity_name,
        quantity_in_stock=commodity.quantity_in_stock,
        remark=commodity.remark)
    db.add(add_comm)
    db.commit()

    # Commodity 表与 CommodityType 表关联数据
    for typeid in commodity.type:
        add_comm_type = CommodityType(
            commodity_id=add_comm.commodity_id,
            type_id=typeid.type_id
        )
        db.add(add_comm_type)
        db.commit()

    spec_info_id = list()
    # SpecInfo 表添加数据
    for spec in commodity.spec:
        add_comm_spec_info = SpecInfo(
            spec_id=spec.spec_id,
            spec_info_val=spec.spec_info_val
        )
        db.add(add_comm_spec_info)
        db.commit()

        # 拿到新添加的数据返回的主键ID
        spec_info_id.append(add_comm_spec_info.spec_info_id)

    # Commodity 表与 SpecInfo 表关联数据
    for sii in spec_info_id:
        add_comm_spec = CommoditySpec(
            commodity_id=add_comm.commodity_id,
            spec_info_id=sii
        )
        db.add(add_comm_spec)
        db.commit()

    # 获取新增的这条数据的信息
    # 商品表
    local_add_comm = db.query(
        Commodity.commodity_id, Commodity.commodity_name,
        Commodity.quantity_in_stock, Commodity.remark,
    ).filter(Commodity.commodity_id == add_comm.commodity_id).first()

    # 类型表
    get_type = db.query(CommodityType.type_id, Type.type).outerjoin(
        Type, CommodityType.type_id == Type.type_id).filter(
        CommodityType.commodity_id == add_comm.commodity_id).all()

    # 规格表
    get_spec = db.query(
        Spec.spec_id, Spec.spec_name, SpecInfo.spec_info_val). \
        outerjoin(SpecInfo, and_(Spec.spec_id == SpecInfo.spec_id)). \
        outerjoin(CommoditySpec, and_(
            SpecInfo.spec_info_id == CommoditySpec.spec_info_id)).filter(
        CommoditySpec.commodity_id == add_comm.commodity_id).all()

    return {"commodity_id": local_add_comm.commodity_id,
            "commodity_name": local_add_comm.commodity_name,
            "quantity_in_stock": local_add_comm.quantity_in_stock,
            "type": get_type,
            "spec": get_spec,
            "remark": local_add_comm.remark}


def db_create_picture(commodity_id: int, files: File, db: Session):
    """
    新增商品图片
    :param commodity_id:
    :param files:
    :param db:
    :return:
    """
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

    picture_id = list()
    for one_name in tmp_filename:
        add_comm = Picture(path="backend/images/",
                           picture_name=one_name,
                           commodity_id=commodity_id)
        db.add(add_comm)
        db.commit()
        db.refresh(add_comm)
        picture_id.append(add_comm.picture_id)
    query_result = list()
    for Id in picture_id:
        query = db.query(
            Picture.path,
            Picture.picture_id,
            Picture.picture_name).filter(Picture.picture_id == Id). \
            filter(Picture.commodity_id == commodity_id).first()
        query_result.append(query)
    return query_result


def db_modify_commodity(modify_commodity: schemas.ModifyCommodity,
                        db: Session):
    """
    修改商品信息
    :param modify_commodity:
    :param db:
    :return:
    """
    result = db.query(Commodity). \
        filter(Commodity.commodity_id == modify_commodity.commodity_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="商品id错误或id不存在")
    else:
        # 有单个值或者多个值,直接对原有数据删除重新关联
        # 拿到 CommoditySpec 表和 SpecInfo 表关联的 spec_info_id 外键
        query_id = db.query(CommoditySpec.spec_info_id).filter(
            CommoditySpec.commodity_id == modify_commodity.commodity_id).all()
        spec_info_id = [Id for spec_info_id in query_id for Id in spec_info_id]

        # 删除 CommoditySpec 表
        db.query(CommoditySpec).filter(
            CommoditySpec.commodity_id == modify_commodity.commodity_id).delete()
        # 删除 SpecIfo 表
        for commodity_spec_info_id in spec_info_id:
            db.query(SpecInfo). \
                filter(
                SpecInfo.spec_info_id == commodity_spec_info_id).delete()
            db.commit()

        # 更新 Commodity 表
        db.query(Commodity). \
            filter(Commodity.commodity_id == modify_commodity.commodity_id). \
            update({
             Commodity.commodity_name: modify_commodity.commodity_name,
             Commodity.quantity_in_stock: modify_commodity.quantity_in_stock,
             Commodity.remark: modify_commodity.remark})

        # 更新 CommodityType 表
        for typeid in modify_commodity.type:
            add_comm_type = CommodityType(
                commodity_id=modify_commodity.commodity_id,
                type_id=typeid.type_id)
            db.add(add_comm_type)
            db.commit()

        # 更新 SpecInfo 表
        spec_info_id = list()
        for spec in modify_commodity.spec:
            add_comm_spec_info = SpecInfo(
                spec_id=spec.spec_id,
                spec_info_val=spec.spec_info_val
            )
            db.add(add_comm_spec_info)
            db.commit()

            # 拿到新添加的数据返回的主键ID
            spec_info_id.append(add_comm_spec_info.spec_info_id)

        # CommoditySpec 表与 SpecInfo 表关联数据
        for sii in spec_info_id:
            add_comm_spec = CommoditySpec(
                commodity_id=modify_commodity.commodity_id,
                spec_info_id=sii
            )
            db.add(add_comm_spec)
            db.commit()

        # -------------------获取修改信息------------------------
        # 商品表
        modify_comm = db.query(
            Commodity.commodity_id, Commodity.commodity_name,
            Commodity.quantity_in_stock, Commodity.remark,
        ).filter(
            Commodity.commodity_id == modify_commodity.commodity_id).first()

        # 类型表
        get_type = db.query(CommodityType.type_id, Type.type).outerjoin(
            Type, CommodityType.type_id == Type.type_id).filter(
            CommodityType.commodity_id == modify_commodity.commodity_id).all()

        # 规格表
        get_spec = db.query(
            Spec.spec_id, Spec.spec_name, SpecInfo.spec_info_val). \
            outerjoin(SpecInfo, and_(Spec.spec_id == SpecInfo.spec_id)). \
            outerjoin(CommoditySpec, and_(
            SpecInfo.spec_info_id == CommoditySpec.spec_info_id)).filter(
            CommoditySpec.commodity_id == modify_commodity.commodity_id).all()

        return {"commodity_id": modify_comm.commodity_id,
                "commodity_name": modify_comm.commodity_name,
                "quantity_in_stock": modify_comm.quantity_in_stock,
                "type": get_type,
                "spec": get_spec,
                "remark": modify_comm.remark}


def db_modify_images(commodity_id: int, files: File, db: Session):
    """
    修改商品图片
    :param commodity_id:
    :param files:
    :param db:
    :return:
    """
    query_picture = db.query(Picture.picture_name).filter(
        Picture.commodity_id == commodity_id).all()

    if query_picture is not None:
        for picture in query_picture:
            path = "resources/images/"
            if os.path.exists(path + picture.picture_name):
                os.remove(path + picture.picture_name)
            else:
                db.query(Picture).filter(
                    Picture.commodity_id == commodity_id).delete()

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

    picture_id = list()
    for one_name in tmp_filename:
        add_comm = Picture(path="backend/images/",
                           picture_name=one_name,
                           commodity_id=commodity_id)
        db.add(add_comm)
        db.commit()
        db.refresh(add_comm)
        picture_id.append(add_comm.picture_id)
    query_result = list()
    for Id in picture_id:
        query = db.query(
            Picture.path,
            Picture.picture_id,
            Picture.picture_name).filter(Picture.picture_id == Id). \
            filter(Picture.commodity_id == commodity_id).first()
        query_result.append(query)

    return query_result


def db_assign_commodity(commodity_id: int, db: Session):
    """
    查询指定商品
    :param commodity_id:
    :param db:
    :return:
    """
    all_type_comm = db.query(Commodity.commodity_id,
                             Commodity.commodity_name,
                             Commodity.quantity_in_stock,
                             Commodity.remark).filter(
        Commodity.commodity_id == commodity_id).filter(
        Commodity.status == 0).first()

    if all_type_comm is None:
        pass
    else:
        # 类型表
        get_type = db.query(CommodityType.type_id, Type.type).outerjoin(
            Type, CommodityType.type_id == Type.type_id).filter(
            CommodityType.commodity_id == commodity_id).all()
        types = list()
        for type in get_type:
            data_type = dict()
            data_type["type_id"] = type.type_id
            data_type["type"] = type.type
            types.append(data_type)

        get_spec = db.query(
            Spec.spec_id, Spec.spec_name, SpecInfo.spec_info_val). \
            outerjoin(SpecInfo, and_(Spec.spec_id == SpecInfo.spec_id)). \
            outerjoin(CommoditySpec, and_(
            SpecInfo.spec_info_id == CommoditySpec.spec_info_id)). \
            filter(CommoditySpec.commodity_id == commodity_id).all()
        specs = list()
        for spec in get_spec:
            data_spec = dict()
            data_spec["spec_id"] = spec.spec_id
            data_spec["spec_name"] = spec.spec_name
            data_spec["spec_info_val"] = spec.spec_info_val
            specs.append(data_spec)

        # 图片表
        get_picture = db.query(Picture.path, Picture.picture_name).filter(
            Picture.commodity_id == commodity_id).all()
        pictures = list()
        for picture in get_picture:
            data_picture = dict()
            data_picture["picture_name"] = picture.picture_name
            data_picture["path"] = picture.path
            pictures.append(data_picture)

        return {
            "commodity_id": all_type_comm.commodity_id,
            "commodity_name": all_type_comm.commodity_name,
            "quantity_in_stock": all_type_comm.quantity_in_stock,
            "type": types,
            "picture": pictures,
            "spec": specs,
            "remark": all_type_comm.remark
        }


def fetchall_commodity(page, limit, db: Session):
    """
    查询所有商品
    :param page
    :param limit
    :param db:
    :return:
    """
    temp_offset = None

    all_commodity = db.query(Commodity).filter(Commodity.status == 0)

    total_count = all_commodity.count()

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

    resource_list = paginate_query(all_commodity, Commodity, limit,
                                   temp_offset, sort_key="commodity_id")
    page_count = int(math.ceil(total_count / limit))

    data = list()
    add_data = dict()
    for resource in resource_list:
        data_handler = copy.deepcopy(add_data)
        data_handler['commodity_id'] = resource.commodity_id
        data_handler['commodity_name'] = resource.commodity_name
        data_handler['quantity_in_stock'] = resource.quantity_in_stock
        data_handler['remark'] = resource.remark
        data.append(data_handler)

    return {"data": data, "page_count": page_count}


def fetch_type_commodity(type_id, db: Session):
    """
    根据类型查询所有商品
    :param type_id:
    :param db:
    :return:
    """
    commodity_id = list()
    for Id in type_id:
        query = db.query(Commodity.commodity_id).outerjoin(CommodityType, and_(
            Commodity.commodity_id == CommodityType.commodity_id)).filter(
            CommodityType.type_id == Id).all()
        commodity_id.append(query)

    one_comm = list()
    for commodity_list in commodity_id:
        for commodity in commodity_list:
            for one in commodity:
                one_comm.append(one)
    transform = set(one_comm)

    # 拿到所有查询类型的 commodity_id 进行查询
    all_commodity_type = list()
    local_comm_type_id = list(transform)
    for commodity_id in local_comm_type_id:
        # 商品表
        all_type_comm = db.query(Commodity.commodity_id,
                                 Commodity.commodity_name,
                                 Commodity.quantity_in_stock,
                                 Commodity.remark).filter(
            Commodity.commodity_id == commodity_id).filter(
            Commodity.status == 0).first()

        if all_type_comm is None:
            pass
        else:
            # 类型表
            get_type = db.query(CommodityType.type_id, Type.type).outerjoin(
                Type, CommodityType.type_id == Type.type_id).filter(
                CommodityType.commodity_id == commodity_id).all()
            types = list()
            for type in get_type:
                data_type = dict()
                data_type["type_id"] = type.type_id
                data_type["type"] = type.type
                types.append(data_type)

            # 规格表
            get_spec = db.query(
                Spec.spec_id, Spec.spec_name, SpecInfo.spec_info_val). \
                outerjoin(SpecInfo, and_(Spec.spec_id == SpecInfo.spec_id)). \
                outerjoin(CommoditySpec, and_(
                    SpecInfo.spec_info_id == CommoditySpec.spec_info_id)). \
                filter(CommoditySpec.commodity_id == commodity_id).all()
            specs = list()
            for spec in get_spec:
                data_spec = dict()
                data_spec["spec_id"] = spec.spec_id
                data_spec["spec_name"] = spec.spec_name
                data_spec["spec_info_val"] = spec.spec_info_val
                specs.append(data_spec)

            # 图片表
            get_picture = db.query(Picture.path, Picture.picture_name).filter(
                Picture.commodity_id == commodity_id).all()
            pictures = list()
            for picture in get_picture:
                data_picture = dict()
                data_picture["picture_name"] = picture.picture_name
                data_picture["path"] = picture.path
                pictures.append(data_picture)

            query = {"commodity_id": all_type_comm.commodity_id,
                     "commodity_name": all_type_comm.commodity_name,
                     "quantity_in_stock": all_type_comm.quantity_in_stock,
                     "type": types,
                     "picture": pictures,
                     "spec": specs,
                     "remark": all_type_comm.remark}
            all_commodity_type.append(query)
    return all_commodity_type


def db_del_commodity(commodity_id: int, db: Session):
    """
    删除指定商品
    :param commodity_id:
    :param db:
    :return:
    """
    result = db.query(Commodity).filter(
        Commodity.commodity_id == commodity_id).first()

    if result is not None:
        db.query(Commodity).filter(
            Commodity.commodity_id == commodity_id).update(
            {Commodity.status: 1})
        db.commit()

        # 查询
        query = db.query(Commodity).filter(Commodity.status == 0). \
            filter(Commodity.commodity_id == commodity_id).first()
        if query is None:
            return {"Message": "Success!"}
    else:
        raise HTTPException(status_code=404, detail="商品id错误或id不存在")


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