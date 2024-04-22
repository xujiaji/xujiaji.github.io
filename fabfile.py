#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# fabfile.py
# 导入Fabric API:
from fabric.api import *

import os, re
import shutil

# 服务器登录用户名:
# env.user = 'ubuntu'
# sudo用户为root:
# env.sudo_user = 'ubuntu'
# 服务器地址，可以有多个，依次部署:
env.port = 1229
env.hosts = ['root@8.210.6.57']
env.key_filename = '~/.ssh/id_rsa.xu'
# env.ssh_config_path = '~/.ssh/config'
# env.use_ssh_config = True

_TAR_FILE = 'dist-awesome-blog.tar.gz'


def replaceText(path, old_text, new_text):
    with open(path) as fr:
        result = re.sub(re.compile(old_text), new_text, fr.read())
        with open(path, 'w') as fw:
            fw.write(result)


def deploy_ready():
    replaceText('_config.inside.yml', old_text='static_prefix:', new_text='static_prefix: //xujiaji.oss-accelerate.aliyuncs.com/blog/statics')
    replaceText('_config.inside.yml', old_text='data_prefix:', new_text='data_prefix: //xujiaji.oss-accelerate.aliyuncs.com/blog/api')

def deploy_over():
    replaceText('_config.inside.yml', old_text='static_prefix: //xujiaji.oss-accelerate.aliyuncs.com/blog/statics', new_text='static_prefix:')
    replaceText('_config.inside.yml', old_text='data_prefix: //xujiaji.oss-accelerate.aliyuncs.com/blog/api', new_text='data_prefix:')


def deploy():
    deploy_ready()
    local('tar -czvf %s public' % _TAR_FILE)
    with cd('/www/wwwroot/xujiaji/blog'):
        sudo('pwd')
        sudo('rm -rf *')
        put(_TAR_FILE, '.')
        local('rm -f %s' % _TAR_FILE)
        sudo('tar -xzvf %s' % _TAR_FILE)
        sudo('mv public/* .')
        sudo('rm -rf public')
        sudo('rm -f %s' % _TAR_FILE)
    deploy_over()
