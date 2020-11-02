#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/1 13:28
# @Author  : Fred Yangxiaofei
# @File    : sync_public_key.py
# @Role    : 推送公钥到主机，实现免密钥登陆

import os
import paramiko
from settings import PUBLIC_KEY
from models.server import SSHConfigs
from libs.db_context import DBContext
from libs.web_logs import ins_log
from libs.common import remote_upload_file, get_key_file, exec_shell
import fire

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RsyncPublicKey():
    def __init__(self):
        self.msg = ''

    def check_public_path(self):
        """
        检查是否有这个目录，没有目录就新建
        :return:
        """
        PUBLIC_KEY_PATH = os.path.dirname(PUBLIC_KEY)
        cmd = '[ ! -d {} ] && mkdir {} && chmod 700 {} ; '.format(PUBLIC_KEY_PATH, PUBLIC_KEY_PATH, PUBLIC_KEY_PATH)
        code, ret = exec_shell(cmd)
        if code == 0:
            return True
        else:
            return False

    def init_rsa(self):
        '''Server端生成秘钥对'''
        cmd = 'ssh-keygen -t rsa -P "" -f {}/id_rsa'.format(os.path.dirname((PUBLIC_KEY)))

        code, ret = exec_shell(cmd)
        if code == 0:
            return True
        else:
            return False

    def save_of(self):
        '''把读取或者生成的秘钥信息保存到SQL'''
        with open('%s/id_rsa' % os.path.dirname(PUBLIC_KEY), 'r') as id_rsa, open(
                '%s/id_rsa.pub' % os.path.dirname(PUBLIC_KEY), 'r') as id_rsa_pub:
            with DBContext('w') as session:
                new_config = SSHConfigs(name='cmdb', id_rsa=id_rsa.read(), id_rsa_pub=id_rsa_pub.read())
                session.add(new_config)
                session.commit()

    def check_rsa(self):
        """
        检查CMDB 密钥配置,没有则创建新的写入数据库
        :return:
        """
        # 检查路径
        self.check_public_path()
        with DBContext('r') as session:
            # 这张表里面直有一条信息，名字：cmdb， 一对密钥
            exist_rsa = session.query(SSHConfigs.id, SSHConfigs.id_rsa_pub, SSHConfigs.id_rsa).filter(
                SSHConfigs.name == 'cmdb').first()
            if not exist_rsa:
                # 检查本地是否存在
                local_id_rsa_exist = os.path.exists('{}/id_rsa'.format(os.path.dirname(PUBLIC_KEY)))
                if not local_id_rsa_exist:
                    check_rsa = self.init_rsa()
                    if not check_rsa:
                        return False
                self.save_of()

            elif exist_rsa:
                PUBLIC_KEY_PATH = os.path.dirname(PUBLIC_KEY)
                id_rsa_pub = exist_rsa[1]
                id_rsa = exist_rsa[2]
                cmd1 = 'echo "{}" > {}/id_rsa.pub'.format(id_rsa_pub, PUBLIC_KEY_PATH)
                cmd2 = 'echo "{}" > {}/id_rsa && chmod 600 {}/id_rsa'.format(id_rsa, PUBLIC_KEY_PATH, PUBLIC_KEY_PATH)
                exec_shell(cmd1)
                exec_shell(cmd2)
                return True
            else:
                return True

    def sync_key(self, server_list):
        """
        批量下发server端公钥到client端
        :param server_list: 主机信息，IP端口用户密码
        :return:
        """
        if not isinstance(server_list, list):
            raise ValueError()

        ip = server_list[0][0]
        port = server_list[0][1]
        user = server_list[0][2]
        user_key = server_list[0][3]
        cmd = '[ ! -d ~/.ssh ] && mkdir ~/.ssh && chmod 700 ~/.ssh ; ' \
              '[ ! -f ~/.ssh/authorized_keys ] && touch ~/.ssh/authorized_keys;  ' \
              'grep -c "`cat /tmp/id_rsa.pub`" ~/.ssh/authorized_keys >> /dev/null;' \
              '[ $? == 0 ] || cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo ok'
        # 将key写到本地
        ssh_key_file = get_key_file(user_key)
        if ssh_key_file:
            try:
                res = remote_upload_file(ip, user, ssh_key_file, cmd, PUBLIC_KEY, '/tmp/id_rsa.pub', port)
                if res[0] == 'ok':
                    self.msg = {
                        'status': True,
                        'ip': ip,
                        'port': port,
                        'user': user,
                        'msg': '推送成功'
                    }
                else:
                    # 状态改为False
                    self.msg = {
                        'status': False,
                        'ip': ip,
                        'msg': '推送失败'
                    }
            except paramiko.ssh_exception.AuthenticationException:
                self.msg = {
                    'status': False,
                    'ip': ip,
                    'msg': '认证失败，请检查管理用户Key是否正确'
                }

            except Exception as e:
                print(e)
                self.msg = {
                    'status': False,
                    'ip': ip,
                    'msg': '{}'.format(e)
                }

        ins_log.read_log('info', self.msg)
        return self.msg


def start_rsync(server_list):
    """
    推送CMDB公钥
    :param server_list: CMDB主机列表
    :return:
    """
    obj = RsyncPublicKey()
    return obj.sync_key(server_list)


if __name__ == '__main__':
    fire.Fire(start_rsync)
