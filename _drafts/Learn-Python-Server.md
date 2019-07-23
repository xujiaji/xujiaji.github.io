---
title: Learn-Python-Server
categories:
 - Python
tags:
---

# 相关知识点

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
