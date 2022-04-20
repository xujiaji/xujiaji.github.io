---
title: SSH笔记
date: 2022-04-20 11:01:44
categories:
 - 笔记
tags:
	- SSH
---

## 创建秘钥对文件

- `-t` 指定秘钥类型，默认`rsa`，可省略
- `-C` 设置注释文字，比如邮箱，可以省略

``` shell
ssh-keygen -t rsa -C  'your email@domain.com'
```

## 本地多秘钥配置

1. 在`~/.ssh/config`创建配置文件，添加ssh服务器信息（可配置多个）
```
Host            alias            # 自定义别名
HostName        hostname         # 替换为你的ssh服务器ip或domain
Port            port             # ssh服务器端口，默认为22
User            user             # ssh服务器用户名
IdentityFile    ~/.ssh/id_rsa    # 公钥对应的私钥文件本地路径
```
2. 可以用别名登录linux服务器
``` shell
$ ssh alias
```

## 问题处理
### linux Permission 0644 for are too open

原因本地私钥权限问题，需要设置为不能被其他人访问，通过`ls -l ~/.ssh`看到对应私钥权限

> 处理：

```
chmod 600 ~/.ssh/你的私钥
```