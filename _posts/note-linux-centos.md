---
title: Linux CentOS 笔记
date: 2020-04-17 12:03:06
updated: 2020-04-17 12:03:06
thumbnail: blog/linux/banner.png
tags:
 - Linux
---

# 服务器学习笔记

## 系统更新

``` shell
yum -y update
```

## 打包

``` shell
mvn clean package -Dmaven.test.skip
```

## java 环境

``` shell
https://www.jianshu.com/p/848b06dd19aa
```

## 安装maven

``` shell
wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
yum -y install apache-maven
```

## 没有.iml文件

在对应项目里运行

``` shell
mvn idea:module
```

## 挂载数据盘

<https://www.cnblogs.com/tv151579/p/6218901.html/>

## docker安装

<https://www.cnblogs.com/yu-hailong/p/7629120.html/>

## 安装python3.7

``` url
https://www.cnblogs.com/anxminise/p/9650206.html
```

## ssh添加私匙

``` shell
ssh-add -k key.pem  
```

## sshfs挂载

``` shell
sshfs root@149.129.84.13:/data/awsl/ /Users/jiajixu/Desktop/awsl/
```

> 自动重连，缓冲目录

``` shell
sshfs -o cache=yes,reconnect root@149.129.84.13:/data/awsl/ /Users/jiajixu/Desktop/awsl/
```

## sshfs卸载

``` shell
umount -f ~/Desktop/awsl/
```

## sshfs异常

``` shell
mount_osxfuse: the OSXFUSE file system is not available (255)
```

解决：

``` url
https://github.com/osxfuse/osxfuse/issues/315#issuecomment-271548072
```

## 安装nginx

``` shell
yum install nginx
```

> 随系统自动启动

``` shell
chkconfig --levels 235 nginx on
service nginx start
```

> 重启nginx

``` shell
systemctl restart nginx.service
```

> 查看状态

``` shell
systemctl status nginx.service
```

> 处理nginx启动错误Failed to read PID from file /run/nginx.pid

``` shell
https://my.oschina.net/u/2357619/blog/1609622
```

## Supervisor

Supervisor是一个管理进程的工具，可以随系统启动而启动服务，它还时刻监控服务进程，如果服务进程意外退出，Supervisor可以自动重启服务。

> 安装

``` shell
yum install supervisor
```

### `supervisorctl reload`报错

> 错误日志

``` shell
error: <class 'socket.error'>, [Errno 2] No such file or directory: file: /usr/lib64/python2.7/socket.py line: 224
```

> 解决，执行：

``` shell
supervisord
```

> 其他方法

``` shell
supervisorctl -c /etc/supervisord.conf
```

> 非root用户启动时的权限问题

``` shell
https://github.com/Supervisor/supervisor/issues/173
```

## 通过PID关闭进程

> 查询这里查询supervisord pid

``` shell
ps ax | grep supervisord
```

> 结束进程

``` shell
kill -9 [PID号]
```

## Python问题

> OSError: [Errno 98] Address already in use

``` shell
# netstat -tlnp|grep 8000
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      5538/python3

# kill -9 5538
```

## 重启ssh服务

``` shell
service sshd restart
```

## 创建软连接

> 如

``` shell
ln -s jiapuji_server/jiapuji_gateway/target/gateway-1.0.1.jar gateway.jar
```

## 配置ssh

路径

``` shell
vim /etc/ssh/sshd_config
```

重启ssh

``` shell
systemctl restart sshd
```

## Docker

### 基本命令

``` shell
docker ps
docker rm 8fa2f9c16a3b
docker stop 8fa2f9c16a3b
docker restart 8fa2f9c16a3b
```

### 安装gitlab

``` shell
docker images
docker search gitlab-ce
docker pull twang2218/gitlab-ce-zh
docker run -d --hostname gitlab.xxx.com:3000 -p 10443:10443 -p 3000:3000 -p 10222:10222 --name gitlab --restart always -v /home/gitlab/config:/etc/gitlab -v /home/gitlab/logs:/var/log/gitlab -v /home/gitlab/data:/var/opt/gitlab twang2218/gitlab-ce-zh
```

## Redis

### 安装

官网

<https://redis.io/download/>

安装

<https://segmentfault.com/a/1190000016012597/>

### 命令

启动Redis

``` shell
redis-server
```

设置后台运行

``` shell
# 编辑配置文件，修改 daemonize no 为 daemonize yes，这样就可以默认启动就后台运行
vim /etc/redis/redis.conf

# 启动redis
redis-server /etc/redis/redis.conf
```

终端连接Redis

``` shell
redis-cli
```

关闭服务

``` shell
redis-cli shutdown
```

测试启动(返回PONG则启动成功)

``` shell
redis-cli ping
```

## Gitlab CI

https://scarletsky.github.io/2016/07/29/use-gitlab-ci-for-continuous-integration/
https://www.jianshu.com/p/3c0cbb6c2936
