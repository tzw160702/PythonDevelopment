#!/usr/bin/python3
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


# 全部订单
class OrderPicture(BaseModel):
    path: str = Field(..., description="图片服务器路径")
    photo_name: str = Field(..., description="图片名称")


class Consignee(BaseModel):
    consignee_name: str = Field(..., description="收件人姓名")
    consignee_addr: str = Field(..., description="收件地址")
    consignee_phone: int = Field(..., description="电话")


class DetailsOrder(BaseModel):
    order_id: int = Field(..., description="订单id")
    order_name: str = Field(..., description="订单名称")
    picture: List[OrderPicture]
    order_amount: str = Field(..., description="订单数量")
    order_money: float = Field(..., description="订单金额")
    consignee: Consignee
    order_status: str = Field(..., description="订单状态")
    order_time: datetime = Field(..., description="订单时间")
    order_number: str = Field(..., description="订单号")

    class Config:
        orm_mode = True


class Order(BaseModel):
    order_id: int = Field(..., description="订单id")
    order_name: str = Field(..., description="订单名称")
    picture: OrderPicture
    order_amount: str = Field(..., description="订单数量")
    order_money: float = Field(..., description="订单金额")
    consignee: Consignee
    order_status: str = Field(..., description="订单状态")
    order_time: datetime = Field(..., description="订单时间")
    order_number: str = Field(..., description="订单号")

    class Config:
        orm_mode = True


class Data(BaseModel):
    data: List[Order]
    page_count: int = Field(..., description='总页数')


# 修改订单
class UpdateOrder(BaseModel):
    order_id: int = Field(..., description="订单id")
    order_name: str = Field(..., description="订单名称")
    order_amount: int = Field(..., description="订单数量")
    order_money: float = Field(..., description="订单金额")
    consignee: Consignee
    order_status: str = Field(..., description="订单状态")


# 购物车
class ShopCar(BaseModel):
    id: int = Field(..., description='商品id')
    commodity_name: str = Field(..., description='商品名称')
    commodity_spec: str = Field(..., description='商品规格')
    price: float = Field(..., description='商品价格')
    commodity_count: int = Field(..., description='商品数量')
    picture: OrderPicture

    class Config:
        orm_mode = True


# Login
class SignUp(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    pwd: str = Field(title='密码', description='密码')
    verify_code: str = Field(title='验证码', description='验证码')


class LogInByPwd(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    pwd: str = Field(title='密码', description='密码')
    client_code: str = Field(title='客户端验证码', description='客户端验证码')
    callback_url: str = Field(title='系统回调地址', description='系统回调地址')


class LogInByCode(BaseModel):
    number: str = Field(title='手机号或者邮箱', description='手机号或者邮箱')
    verify_code: str = Field(title='手机或邮箱验证码', description='手机或邮箱验证码')
    callback_url: str = Field(title='系统回调地址', description='系统回调地址')


class ChangePwd(BaseModel):
    token: str = Field(title='Token', description='Token')
    old_pwd: str = Field(title='旧密码', description='旧密码')
    new_pwd: str = Field(title='新密码', description='新密码')

