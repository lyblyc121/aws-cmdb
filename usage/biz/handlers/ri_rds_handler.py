#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :


import json
from sqlalchemy import or_
from libs.base_handler import BaseHandler
from models.rds_ri_db import RiRds, model_to_dict
from models.elasticache_ri_db import RiElastiCache
from websdk.db_context import DBContext
from tornado.web import RequestHandler
from libs.aws.rds_ri import main as rds_main
from libs.aws.elasticache_ri import main as elasticache_main


class RIRdsHandler(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        pageNum = int(self.get_argument('page', default='1', strip=True))
        pageSize = int(self.get_argument('limit', default='10', strip=True))
        with DBContext('r') as session:
            if key:
                ri_rds_data = session.query(RiRds).filter(
                    or_(RiRds.ReservedDBInstanceId.like('%{}%'.format(key)),
                        RiRds.ReservedDBInstancesOfferingId.like('%{}%'.format(key)),
                        RiRds.DBInstanceClass.like('%{}%'.format(key)),
                        RiRds.Duration.like('%{}%'.format(key)),
                        RiRds.FixedPrice.like('%{}%'.format(key)),
                        RiRds.UsagePrice.like('%{}%'.format(key)),
                        RiRds.CurrencyCode.like('%{}%'.format(key)),
                        RiRds.DBInstanceCount.like('%{}%'.format(key)),
                        RiRds.ProductDescription.like('%{}%'.format(key)),
                        RiRds.OfferingType.like('%{}%'.format(key)),
                        RiRds.MultiAZ.like('%{}%'.format(key)),
                        RiRds.State.like('%{}%'.format(key)),
                        RiRds.RecurringCharges.like('%{}%'.format(key)),
                        RiRds.ReservedDBInstanceArn.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                ri_rds_data = session.query(RiRds).all()
            data_dict = list()
            for msg in ri_rds_data:
                msg = model_to_dict(msg)
                msg.pop("create_time")
                msg.pop("update_time")
                data_dict.append(msg)
            ri_rds_list_re = data_dict[(pageNum - 1) * pageSize:pageNum * pageSize]
        self.write(dict(code=0, msg='获取成功', count=len(data_dict), data=ri_rds_list_re))


class RiElastiCacheHandler(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        pageNum = int(self.get_argument('page', default='1', strip=True))
        pageSize = int(self.get_argument('limit', default='10', strip=True))
        with DBContext('r') as session:
            if key:
                ri_elasticache_data = session.query(RiElastiCache).filter(
                    or_(RiElastiCache.ReservedCacheNodeId.like('%{}%'.format(key)),
                        RiElastiCache.ReservedCacheNodesOfferingId.like('%{}%'.format(key)),
                        RiElastiCache.CacheNodeType.like('%{}%'.format(key)),
                        RiElastiCache.Duration.like('%{}%'.format(key)),
                        RiElastiCache.FixedPrice.like('%{}%'.format(key)),
                        RiElastiCache.UsagePrice.like('%{}%'.format(key)),
                        RiElastiCache.CacheNodeCount.like('%{}%'.format(key)),
                        RiElastiCache.ProductDescription.like('%{}%'.format(key)),
                        RiElastiCache.OfferingType.like('%{}%'.format(key)),
                        RiElastiCache.State.like('%{}%'.format(key)),
                        RiElastiCache.RecurringCharges.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                ri_elasticache_data = session.query(RiElastiCache).all()
            data_dict = list()
            for msg in ri_elasticache_data:
                msg = model_to_dict(msg)
                msg.pop("create_time")
                msg.pop("update_time")
                data_dict.append(msg)
            ri_elasticache_list_re = data_dict[(pageNum - 1) * pageSize:pageNum * pageSize]
        self.write(dict(code=0, msg='获取成功', count=len(data_dict), data=ri_elasticache_list_re))


class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        elasticache_main()
        rds_main()
        return self.write({"test":"sucess"})

rds_elasticache_urls = [
    (r"/v1/cmdb/ri_rds/", RIRdsHandler),
    (r"/v1/cmdb/ri_elasticache/", RiElastiCacheHandler),
    (r"/v1/cmdb/ri_rds/test/", ApiTest),
]

if __name__ == "__main__":
    pass
