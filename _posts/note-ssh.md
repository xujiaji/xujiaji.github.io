---
title: SSH笔记
date: 2022-04-20 11:01:44
categories:
 - 笔记
tags:
	- ssh
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