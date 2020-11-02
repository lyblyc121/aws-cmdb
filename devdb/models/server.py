#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:52
# @Author  : Fred Yangxiaofei
# @File    : server.py
# @Role    : Server Models

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class Tag(Base):
    __tablename__ = 'asset_tag'

    ### 标签  通过标签来定义主机组 和DB集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column('tag_name', Text)
    tag_value = Column('tag_value', String(256))  
    tag_description = Column('tag_description', String(256))
    tag_aws_service = Column('tag_aws_service', String(256))
    #__table_args__ = (UniqueConstraint ('tag_name', 'tag_value', 'tag_aws_service'),)



class TagRule(Base):
    __tablename__ = 'asset_tag_rule'

    ### 定义标签规则、最近很多同学反应加标签太过复杂, 根据Hostname模糊查询+自定义的精确查询去自动匹配主机
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255))  ### 规则名字
    tag_name = Column('tag_name', String(255))  ### 关联的Tagname名称
    idc_rule = Column('idc_rule', String(255))  ### idc匹配条件/idc=AWS
    hostname_rule = Column('hostname_rule', String(255))  ### Hostname条件 匹配 OPS-SH-%


class ServerTag(Base):
    __tablename__ = 'asset_server_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column('server_id', Integer)
    tag_id = Column('tag_id', Integer)


class Server(Base):
    __tablename__ = 'asset_server'

    ### 服务器主要信息
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID自增长
    hostname = Column('hostname', String(1000), nullable=False)  # 主机名称
    ip = Column('ip', String(32), index=True, nullable=False)
    public_ip = Column('public_ip', String(32))  # 公网IP
    private_ip = Column('private_ip', String(32))  # 公网IP
    port = Column('port', Integer, nullable=False)  # 端口
    idc = Column('idc', String(128))  # IDC
    admin_user = Column('admin_user', String(128))  # 管理用户
    region = Column('region', String(128))  # 区域
    state = Column('state', String(128))  # 状态
    detail = Column('detail', String(128))  # 备注
    instance_id = Column('instance_id', String(128))
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间
    project = Column('project', String(128),nullable=True)
    tags = Column('tags', String(512),nullable=True)
    volumes_total = Column('volumes_total', Integer,nullable=True)

class ServerDetail(Base):
    __tablename__ = 'asset_server_detail'

    ### 服务器详细信息。均为自动获取到的信息，后续可方便扩展CMDB
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID自增长
    ip = Column('ip', String(32), nullable=False)  # IP,根据上面的IP进行关联
    sn = Column('sn', String(128))  # SN
    cpu = Column('cpu', String(128))  # CPU型号
    cpu_cores = Column('cpu_cores', String(128))  # CPU核心
    memory = Column('memory', String(128))  # 内存
    disk = Column('disk', String(128))  # 磁盘
    os_type = Column('os_type', String(128))  # 系统类型+版本
    os_kernel = Column('os_kernel', String(128))  # 系统内核
    instance_id = Column('instance_id', String(128))  # 实例ID
    instance_type = Column('instance_type', String(128))  # 实例类型
    instance_state = Column('instance_state', String(128))  # 实例状态
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间


class AdminUser(Base):
    __tablename__ = 'admin_users'

    ### 管理用户， 一般用来第一次登陆你主机用的
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    admin_user = Column('admin_user', String(80), unique=True, nullable=False)  # 管理用户名称 关联主机表
    system_user = Column('system_user', String(50), default='root')  # 系统用户
    # ssh_port = Column('ssh_port', Integer, default=22)  # 端口
    password = Column('password', String(100))  # 密码
    user_key = Column('user_key', Text())  # 密钥
    remarks = Column('remarks', String(150))  # 备注信息
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 更新时间


class SystemUser(Base):
    __tablename__ = 'system_users'

    ### 系统用户，一般来说是用后续的跳板+审计用的
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(80), unique=True, nullable=False)  # 名称
    system_user = Column('system_user', String(50), nullable=False)  # 系统用户，是会在系统上useradd xxx的用户
    priority = Column('priority', Integer, nullable=False)  # 优先级
    id_rsa = Column('id_rsa', Text())  # 私钥，生成密钥对，推送到系统用户中
    id_rsa_pub = Column('id_rsa_pub', Text())  # 公钥，生成密钥对，推送到系统用户中
    sudo_list = Column('sudo_list', Text())  # sudo权限，如:/bin/su
    bash_shell = Column('bash_shell', Text())  # sudo权限，如:/bin/su
    platform_users = Column('platform_users', Text())  ### 关联用户， 创建的系统用户和平台用户进行关联起来，做权限要用到
    remarks = Column('remarks', String(150))  # 备注信息
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间


class SSHConfigs(Base):
    __tablename__ = 'ssh_configs'

    ### 密钥对，推送公钥到HOST，CMDB免密登陆主机获取资产
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(80), unique=True, nullable=False)  # 名称
    id_rsa = Column('id_rsa', Text())  # 私钥
    id_rsa_pub = Column('id_rsa_pub', Text())  # 公钥


class AssetConfigs(Base):
    __tablename__ = 'asset_configs'
    # 资产配置，主要配置AWS/Aliyun/Qcloud的Key，用于自动获取资产信息
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(80), unique=True, nullable=False)  # 名称
    account = Column('account', String(50), nullable=False)  # 账号：AWS/aliyun/qcloud
    region = Column('region', String(50), nullable=False)  # 区域：如AWS：us-east-1 阿里云：cn-hangzhou等
    access_id = Column('access_id', String(120), nullable=False)  # IAM角色访问密钥
    access_key = Column('access_key', String(120), nullable=False)  # IAM角色访问密钥
    huawei_instance_id = Column('huawei_instance_id', String(120), nullable=False)  # Huawei云实例ID
    huawei_cloud = Column('huawei_cloud', String(120), nullable=False)  # Huawei云地址
    project_id = Column('project_id', String(120), nullable=False)  # huawei云区域对应的项目ID
    default_admin_user = Column('default_admin_user', String(120))  # 默认管理用户，会默认关联上一个管理用户，用来登陆机器
    state = Column('state', String(50), nullable=False)  # 状态，Ture：开启，Flase:关闭
    remarks = Column('remarks', String(150))  # 备注信息
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间


class AssetErrorLog(Base):
    __tablename__ = 'asset_error_log'
    ### 自动推送资产。错误日志信息
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    ip = Column('ip', String(32), nullable=False)  # IP
    error_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录时间
    error_log = Column('error_log', Text())  # 私钥


# class AssetOperateLog(Base):
#     '''资产操作日志,这是二期设计用的'''
#     __tablename__ = 'asset_operate_log'
#     id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
#     user = Column('user', String(20))
#     host = Column('host', String(200))
#     remote_ip = Column('remote_ip', String(50))
#     login_type = Column('login_type', String(20))
#     login_path = Column('login_path', String(20))
#     start_time =  Column('start_time', DateTime())
#     pid = Column('pid', String(20))
#     end_time = Column('end_time', DateTime())
#     filename = Column('filename', String(200))


class AwsEvents(Base):
    __tablename__ = 'aws_events'
    # 记录AWS Events事件
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(255))  # 名称
    region = Column('region', String(255))  # 区域
    instance_id = Column('instance_id', String(255))  # 实例ID
    event_id = Column('event_id', String(255))  # 事件ID
    event_status = Column('event_status', String(255))  # 事件状态
    event_desc = Column('event_desc', Text())  # 事件描述
    event_start_time = Column(DateTime)  # 到期时间
    record_state = Column('record_state', String(255))  # 记录状态
    record_create_time = Column('record_create_time', DateTime(), default=datetime.now)  # 记录创建创建时间


class AssetIDC(Base):
    __tablename__ = 'asset_idc'
    # IDC管理
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(255), unique=True, nullable=False)  # 名称
    contact = Column('contact', String(255))  # 机房联系人姓名
    email = Column('email', String(255))  # 机房联系人邮箱
    phone = Column('phone', String(255))  # 机房电话
    address = Column('address', String(255))  # 机房地址
    network = Column('network', String(255))  # 机房网络
    bandwidth = Column('bandwidth', String(255))  # 机房带宽大小
    ip_range = Column('ip_range', Text())  # IP地址段
    remarks = Column('remarks', String(150))  # 备注信息


class AssetOperationalAudit(Base):
    __tablename__ = 'asset_operational_audit'
    # 操作审计、操作记录
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    username = Column('username', String(255), nullable=False)  # 用户名
    request_object = Column('request_object', String(255))  # 请求对象
    request_host = Column('request_host', String(255))  # 请求Host
    request_method = Column('request_method', String(255))  # 请求方法
    original_data = Column('original_data', JSON)  # 原数据
    modify_data = Column('modify_data', JSON)  # 修改后的数据
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)
