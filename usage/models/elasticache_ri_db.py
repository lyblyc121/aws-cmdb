#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :2020/9/24
# @Author  : Fred liuchuanhao
# @File    : elasticache_ri_db.py
# @Role    : ORM


from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class RiElastiCache(Base):
    __tablename__ = 'ri_elasticache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ReservedCacheNodeId = Column('ReservedCacheNodeId', String(128))
    ReservedCacheNodesOfferingId = Column('ReservedCacheNodesOfferingId', String(255))
    CacheNodeType = Column('CacheNodeType', String(255))
    Duration = Column('Duration', String(255), )
    FixedPrice = Column('FixedPrice', String(128))
    UsagePrice = Column('UsagePrice', String(128))
    CacheNodeCount = Column('CacheNodeCount', String(128))
    ProductDescription = Column('ProductDescription', String(128))
    OfferingType = Column('OfferingType', String(128))
    State = Column('State', String(128))
    RecurringCharges = Column('RecurringCharges', String(128))
    create_time = Column('create_time', DateTime(), default=datetime.now)
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
