---
title: Springboot项目部署Linux笔记
date: 2021-12-09 10:03:07
categories:
  - 笔记
tags:
  - Linux
  - 笔记
  - CentOS
  - Java
---

自动化部署打包部署到线上仅需要一个命令即可！

通过Fabric自动打包springboot项目并上传jar包到linux服务器，然后自动重启服务。

项目在服务器的服务通过supervisor来管理。

下面记录一下搭建整个本地配置和线上配置的流程，和包括linux权限的分配。

<!-- more -->

## 所需工具和环境
1. Python3
2. Fabric3
3. Supervisor
4. CentOS
5. JDK8

这里打比方部署的项目是：<https://github.com/xujiaji/mk-example/>

## 服务器配置
### 下载JDK和配置
1. 下载JDK8（[JDK8下载地址](https://www.oracle.com/java/technologies/downloads/#java8)），这里下载的是`jdk-8u311-linux-x64.tar.gz`，然后把下载链接copy一下，在linux中下载。
2. CentOS中下载和配置

``` shell
# 下载JDK到当前文件
wget https://download.oracle.com/otn/java/jdk/8u311-b11/4d5417147a92418ea8b615e228bb6935/jdk-8u311-linux-x64.tar.gz?AuthParam=1638978229_f812016f834625d5a181096d5bd0484f -O jdk-8u311-linux-x64.tar.gz
# 查看文件
ls -lht
# 创建解压目录
mkdir /usr/local/java
# 解压缩
tar -zxvf jdk-8u311-linux-x64.tar.gz -C /usr/local/java/
```

> 配置jdk环境，添加到系统环境中，让重启后也有效

``` shell
vim /etc/profile.d/java.sh
```

然后添加下方配置到`java.sh`中，保存退出

``` shell
#!/bin/bash
JAVA_HOME=/usr/local/java/jdk1.8.0_311
PATH=$JAVA_HOME/bin:$PATH
export PATH JAVA_HOME
export CLASSPATH=.
```

执行配置

``` shell
# 添加运行权限
chmod +x /etc/profile.d/java.sh
# 加载jdk环境
source /etc/profile.d/java.sh
# 验证是否成功
java -version
```

### 添加用户和用户组

> 用来管理项目和supervisor的权限，也可以不做这步，直接用root账号。

``` shell
# 添加用户
useradd xujiaji
# 给该用户设置登录密码
passwd xujiaji
# 添加用户组supervisor
groupadd supervisor
# 将该用户添加到用户组
gpasswd -a xujiaji supervisor
# 添加用户组mk（一个项目对应一个用户组，这里的项目叫mk）
groupadd mk
# 将该用户添加到用户组
gpasswd -a xujiaji mk
# 查看用户组信息（直接查看/etc/group末尾10行）
tail /etc/group
# 创建项目目录
cd /home/
mkdir mk
chown root:mk mk
chmod g+w mk
```

### 安装配置Supervisor
1、安装
``` shell
yum install supervisor
```
1.1 或pip安装
``` shell
pip install supervisor
# 测试安装是否成功
echo_supervisord_conf
# 创建配置文件
mkdir -p /etc/supervisor
mkdir -m 755 -p /etc/supervisor/
# 生成默认配置文件
echo_supervisord_conf > /etc/supervisord.conf
sed -i "s/\;\[include\]/\[include\]/" /etc/supervisord.conf 
echo "files = /etc/supervisor/*.conf" >> /etc/supervisord.conf
```
2、指定用户组权限
``` shell
# 修改所有组
chown :supervisor /usr/bin/supervisorctl
chown :supervisor /usr/bin/supervisord
# 修改组权限
chmod g+x /usr/bin/supervisorctl
chmod g+x /usr/bin/supervisord
```
3、修改配置

修改`/etc/supervisord.conf`

``` shell
vim /etc/supervisord.conf
```

下面是要修改的文件内容，请参照注释

```
; 这个配置在开头，把chmod和chown放开，配置成如下的配置，分号是注释
[unix_http_server]
file=/run/supervisor/supervisor.sock   ; (the path to the socket file)
chmod=0770                 ; sockef file mode (default 0700)
chown=root:supervisor       ; socket file uid:gid owner
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))

; 这个配置在最后一行，将最后的ini改成conf
[include]
files = supervisord.d/*.conf
```

4、添加项目配置（这里管理的项目是[mk-example](https://github.com/xujiaji/mk-example/)）

创建编辑`/etc/supervisord.d/mk-admin.conf`，`mk-admin.conf`依据自己的项目来命名，这里是`mk`的管理服务所以名为为`mk-admin.conf`。

``` shell
vim /etc/supervisord.d/mk-admin.conf
```

添加下面的内容

```
[program:mk-admin]

command     = java -jar /home/mk/mk-admin.jar
directory   = /home/mk
user        = xujiaji
startsecs   = 3

redirect_stderr         = true
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups  = 10
stdout_logfile          = /home/mk/logs/supervisor/mkadmin_supervisor.log
```

5、添加为添加日志目录

``` shell
cd /home/mk
# 创建存放jar包的目录
mkdir package-mk
# 创建存放supervisor日志的目录
mkdir -p logs/supervisor
# 配置所有组和权限
cd ..
chown root:mk -R mk
chmod g+w -R mk
```

6、Supervisor命令相关

``` shell
# 启动服务
supervisord
# 加载配置（每当在/etc/supervisord.d中添加了新的配置后，通过这个命令可以加载到）
# 记得要把/home/mk/mk-admin.jar添加到对应目录后再执行才行，不然会加载失败
supervisorctl reload
# 查看当前所有服务的运行状态
supervisorctl status
# 启动mk服务（刚刚添加的服务）
supervisorctl start mk
# 关闭mk服务
supervisorctl stop mk
# 重启mk服务
supervisorctl restart mk
```

### 本地Fabric自动化部署

> 这里使用的是Fabric3

1、首先得有Python3.6及其以上版本（Python安装不做介绍）
2、安装Fabric3
``` shell
pip3 install fabric3
```
3、编写python部署脚本代码

> `local_property.py`配置linux登录账号和密码

{% codeblock local_property.py %}
server_user = "xujiaji"
server_password = "123456"
{% endcodeblock %}

> `fabfile.py`配置自动化打包部署，把该文件直接放到自己项目的根目录就行，比如说这里用的项目是`mk-example`，那就放在`mk-example/fabfile.py`。里面的内容需要根据自己的实际情况做修改和跳转

{% codeblock fabfile.py lang:Python %}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
# 导入Fabric API:
from fabric.api import *
from datetime import datetime
import local_property


# 服务器登录用户名:
env.user = local_property.server_user
# sudo用户为root:
# env.sudo_user = 'root'
# 服务器端口号
env.port = 22
# 服务器地址，可以有多个，依次部署:
#env.hosts = ['root@48.120.129.84']
env.hosts = ['%s@139.9.4.22' % local_property.server_user]
env.password = local_property.server_password
#env.key_filename = '~/.ssh/id_rsa_zs'
#env.key_filename = 'C:/Users/lgiht/.ssh/id_rsa'

def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

# 部署
def deploy():
    print('########开始部署########')
    local("mvn clean package -Dmaven.test.skip=true")
    print('打包结束....')
    with cd('/home/mk'):
        new_todo = 'package-mk/mk-admin-%s.jar' % _now()
        put('security-example/security-admin-example/target/security-admin-example-0.0.1-SNAPSHOT.jar', new_todo)
        run('rm -f mk-admin.jar')
        run('ln -s %s mk-admin.jar' % new_todo)
        run('supervisorctl restart mk-admin')
        run("echo 成功啦~~~")


def rollback():
    print('########版本回滚########')
    with cd('/home/mk'):
        ls = run('ls package-mk')
        packages = sorted(ls.split('  '))
        print('历史版本：')
        for index, package in enumerate(packages):
            print("| %s | %s |" % (index, package))
        no = int(input("\n请选择要回滚的编号："))
        run('rm -f mk-admin.jar')
        run('ln -s package-mk/%s mk-admin.jar' % packages[no])
        run('supervisorctl restart mk-admin')
        run("echo 回滚成功啦~~~")
        
def stop():
    run('supervisorctl stop mk-admin')
{% endcodeblock %}

3、运行自动化部署

> 在`fabric.py`同级目录执行，下面的`deploy`就是脚本里面的方法名

``` shell
fab deploy
```

> 关闭服务器服务

``` shell
fab stop
```

> 回滚

``` shell
fab rollback
```