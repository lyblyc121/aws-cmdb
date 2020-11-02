#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:52

# @File    : settings.py
# @Role    : 配置文件

import os
from websdk.consts import const

ROOT_DIR = os.path.dirname(__file__)
debug = True
xsrf_cookies = False
expire_seconds = 365 * 24 * 60 * 60

ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY', '')
ADMIN_TOKEN_SECRET = os.getenv('ADMIN_TOKEN_SECRET', '')


# 这是写库，
DEFAULT_DB_DBHOST = os.getenv('DEFAULT_DB_DBHOST', '127.0.0.1')
DEFAULT_DB_DBPORT = os.getenv('DEFAULT_DB_DBPORT', '3306')
DEFAULT_DB_DBUSER = os.getenv('DEFAULT_DB_DBUSER', 'root')
DEFAULT_DB_DBPWD = os.getenv('DEFAULT_DB_DBPWD', 'pwd')
DEFAULT_DB_DBNAME = os.getenv('DEFAULT_DB_DBNAME', 'cmdb_cmdb')

# 这是从库，读， 一般情况下是一个数据库即可，需要主从读写分离的，请自行建立好服务
READONLY_DB_DBHOST = os.getenv('READONLY_DB_DBHOST', '127.0.0.1')
READONLY_DB_DBPORT = os.getenv('READONLY_DB_DBPORT', '3306')
READONLY_DB_DBUSER = os.getenv('READONLY_DB_DBUSER', 'root')
READONLY_DB_DBPWD = os.getenv('READONLY_DB_DBPWD', 'pwd')
READONLY_DB_DBNAME = os.getenv('READONLY_DB_DBNAME', 'cmdb_cmdb')

# 这是Redis配置信息，默认情况下和cmdb-admin里面的配置一致
DEFAULT_REDIS_HOST = os.getenv('DEFAULT_REDIS_HOST', '127.0.0.1')
DEFAULT_REDIS_PORT = os.getenv('DEFAULT_REDIS_PORT', '6379')
DEFAULT_REDIS_DB = 8  # 默认和cmdb-admin保持一致
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'
DEFAULT_REDIS_PASSWORD = os.getenv('DEFAULT_REDIS_PASSWORD', '')

# Zabbix配置
DEFAULT_ZABBIX_HOST = os.getenv('DEFAULT_ZABBIX_HOST', '')
DEFAULT_ZABBIX_USER = os.getenv('DEFAULT_ZABBIX_USER', '')
DEFAULT_ZABBIX_PASSWORD = os.getenv('DEFAULT_ZABBIX_PASSWORD', '')

# aws key配置

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', '')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

try:
    from local_settings import *
except:
    pass



settings = dict(
    debug=debug,
    xsrf_cookies=xsrf_cookies,
    cookie_secret=ADMIN_SECRET_KEY,
    expire_seconds=expire_seconds,
    app_name='cmdb_cmdb',
    databases={
        const.DEFAULT_DB_KEY: {
            const.DBHOST_KEY: DEFAULT_DB_DBHOST,
            const.DBPORT_KEY: DEFAULT_DB_DBPORT,
            const.DBUSER_KEY: DEFAULT_DB_DBUSER,
            const.DBPWD_KEY: DEFAULT_DB_DBPWD,
            const.DBNAME_KEY: DEFAULT_DB_DBNAME,
        },
        const.READONLY_DB_KEY: {
            const.DBHOST_KEY: READONLY_DB_DBHOST,
            const.DBPORT_KEY: READONLY_DB_DBPORT,
            const.DBUSER_KEY: READONLY_DB_DBUSER,
            const.DBPWD_KEY: READONLY_DB_DBPWD,
            const.DBNAME_KEY: READONLY_DB_DBNAME,
        }
    },
    redises={
        const.DEFAULT_RD_KEY: {
            const.RD_HOST_KEY: DEFAULT_REDIS_HOST,
            const.RD_PORT_KEY: DEFAULT_REDIS_PORT,
            const.RD_DB_KEY: DEFAULT_REDIS_DB,
            const.RD_AUTH_KEY: DEFAULT_REDIS_AUTH,
            const.RD_CHARSET_KEY: DEFAULT_REDIS_CHARSET,
            const.RD_PASSWORD_KEY: DEFAULT_REDIS_PASSWORD
        }
    },
    zabbix={
        "host": DEFAULT_ZABBIX_HOST,
        "user": DEFAULT_ZABBIX_USER,
        "pwd": DEFAULT_ZABBIX_PASSWORD
    },
    aws_key={
        "region_name": AWS_DEFAULT_REGION,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
)
