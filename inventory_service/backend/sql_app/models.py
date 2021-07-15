#!/usr/bin/python3

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

# declarative_base类维持了一个从类到表的关系，
# 通常一个应用使用一个Base实例，所有实体类都应该继承此类对象
Base = declarative_base()


class Commodity(Base):
    # 商品表
    __tablename__ = "commodity"

    commodity_id = Column(Integer, primary_key=True, autoincrement=True,
                          comment='商品ID')
    commodity_name = Column(String(30), nullable=False, comment='商品名称')
    quantity_in_stock = Column(Integer, default=0, comment='库存剩余数量')
    remark = Column(String(50), nullable=False, comment='备注')
    status = Column(Integer, server_default='0', comment='状态:{0：可用，1：已删除}')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class Datatype(Base):
    # 数据类型表
    __tablename__ = "data_type"

    data_type_id = Column(Integer, primary_key=True, autoincrement=True,
                          comment='类型id')
    data_type = Column(String(30), comment='数据类型')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class Spec(Base):
    # 规格表
    __tablename__ = "spec"

    spec_id = Column(Integer, primary_key=True, autoincrement=True,
                     comment='规格ID')
    spec_name = Column(String(30), nullable=False, comment='规格名称')
    data_type_id = Column(Integer, ForeignKey('data_type.data_type_id'),
                          comment='规格值数据类型,关联数据类型表主键id')
    data_type = relationship('Datatype', backref="spec_of_data_type")
    spec_remark = Column(String(120), nullable=False, comment='规格描述')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class SpecInfo(Base):
    # 规格值表
    __tablename__ = "spec_info"

    spec_info_id = Column(Integer, primary_key=True, autoincrement=True,
                          comment="规格值ID")
    spec_id = Column(Integer, ForeignKey('spec.spec_id'),
                     comment='规格id，关联规格表 spec')
    spec = relationship('Spec', backref='spec_info_of_spec')
    spec_info_val = Column(String(120), comment='规格值')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class CommoditySpec(Base):
    # 商品规格表
    __tablename__ = "commodity_spec"
    commodity_spec_id = Column(Integer, primary_key=True, autoincrement=True,
                               comment='商品规格id')
    commodity_id = Column(Integer, ForeignKey('commodity.commodity_id'),
                          comment='商品ID,关联商品表')
    commodity = relationship('Commodity',
                             backref='commodity_spec_of_commodity')
    spec_info_id = Column(Integer, ForeignKey('spec_info.spec_info_id'),
                          comment='商品规格值id,关联规格值表 spec_info')
    spec_info = relationship('SpecInfo', backref='commodity_spec_of_spec_info')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class Type(Base):
    # 类型表
    __tablename__ = "type"

    type_id = Column(Integer, primary_key=True, autoincrement=True,
                     comment='类型主键ID')
    type = Column(String(30), nullable=False, unique=True, comment='商品类型')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class CommodityType(Base):
    # 商品类型表
    __tablename__ = "commodity_type"
    commodity_type_id = Column(Integer, primary_key=True, autoincrement=True,
                               comment='商品类型主键ID')
    commodity_id = Column(Integer, ForeignKey('commodity.commodity_id'),
                          comment='关联商品表 commodity')
    commodity = relationship('Commodity',
                             backref='commodity_type_of_commodity')
    type_id = Column(Integer, ForeignKey('type.type_id'), comment='关联类型表 type')
    type = relationship('Type', backref='commodity_type_of_type')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')


class Picture(Base):
    # 图片表
    __tablename__ = "picture"

    picture_id = Column(Integer, primary_key=True, autoincrement=True,
                        comment='图片ID')
    picture_name = Column(String(30), nullable=False, unique=True,
                          comment='图片名称')
    path = Column(String(50), nullable=False, comment='图片路径')
    commodity_id = Column(Integer, ForeignKey('commodity.commodity_id'),
                          comment='关联商品表 commodity')
    commodity = relationship('Commodity', backref='picture_of_commodity')
    created_time = Column(DateTime(timezone=True), server_default=func.now(),
                          comment='创建时间')
    updated_time = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now(), comment='更新时间')
