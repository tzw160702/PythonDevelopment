#!/usr/bin/python3

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        Integer, Boolean,
                        String, DateTime,
                        ForeignKey, Float)

# declarative_base类维持了一个从类到表的关系，
# 通常一个应用使用一个Base实例，所有实体类都应该继承此类对象
Base = declarative_base()


class Time:
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='订单生成时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class OrderInfo(Base, Time):
    # 订单表
    __tablename__ = "order_info"

    order_id = Column(Integer, primary_key=True, autoincrement=True,
                      comment='订单ID')
    order_name = Column(String(30), nullable=True, comment='订单名称')
    order_amount = Column(Integer, nullable=True, comment='订单数量')
    order_money = Column(Float, nullable=True, comment='金额')
    order_status = Column(String(100), nullable=True, comment='状态， 完成，支付')
    order_number = Column(String(16), unique=True,
                          nullable=True, comment="订单号")
    is_delete = Column(Boolean, server_default="0", comment="删除, 0 存在, 1 删除")


class Photo(Base, Time):
    # 订单图片表
    __tablename__ = "order_photo"

    photo_id = Column(Integer, primary_key=True, autoincrement=True,
                      comment='图片ID')
    photo_name = Column(String(50), nullable=True, unique=True,
                        comment='图片名称')
    path = Column(String(50), nullable=False, comment='图片路径')

    # Photo of OrderInfo
    order_id = Column(Integer, ForeignKey('order_info.order_id'),
                      comment='关联订单表 order_info')

    order = relationship("OrderInfo",
                         backref=backref('photo', uselist=True))


class Consignee(Base, Time):
    # 收件信息
    __tablename__ = "consignee"

    consignee_id = Column(Integer, primary_key=True, autoincrement=True,
                          comment='收件信息ID')
    consignee_name = Column(String(30), nullable=True, comment='收件人姓名')
    consignee_addr = Column(String(200), autoincrement=True, comment='收件地址')
    consignee_phone = Column(String(11), nullable=True, comment="收件人电话")

    # Consignee of OrderInfo
    order_id = Column(Integer, ForeignKey('order_info.order_id'),
                      comment='关联订单表 order_info')
    order = relationship("OrderInfo",
                         backref=backref('consignee', uselist=False))


class ShopCar(Base, Time):
    # 购物车
    __tablename__ = "shop_car"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='购物车ID')
    commodity_name = Column(String(50), comment='商品名称')
    commodity_spec = Column(String(200), comment='商品规格')
    price = Column(Float, comment='商品单价')
    commodity_count = Column(Integer, comment="商品数量")
    is_delete = Column(Boolean, server_default="0", comment="删除, 0 存在, 1 删除")


class CommodityPicture(Base, Time):
    # 购物车商品图片
    __tablename__ = "comm_picture"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='购物车ID')
    path = Column(String(50), nullable=False, comment='图片路径')
    photo_name = Column(String(50), nullable=True, unique=True,
                        comment='图片名称')

    # Photo of shopCar
    shop_id = Column(Integer, ForeignKey('shop_car.id'),
                     comment='关联购物车表 shop_car')
    shop = relationship("ShopCar", backref=backref('shop_car', uselist=False))

