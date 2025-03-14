---
title: WireGuard安装和配置记录
date: 2025-03-14 19:46:43
categories:
 - 笔记
tags:
  - Linux
---

## 安装和配置用于转发的Linux中间节点Peer（有公网ip，Debian）
1. 安装wiregaurd
``` sh
$ apt install wireguard
```
2. 进入配置目录
``` sh
$ cd /etc/wireguard/ 
```
3. 生成公钥和私钥文件
``` sh
$ wg genkey | tee privatekey | wg pubkey > publickey
```
4. 查看秘钥
``` sh
# 查看私钥
$ cat privatekey
# 查看公钥
$ cat publickey
```
5. 配置wireguard配置文件
``` sh
$ vim wg0.conf
# 写入内容：
[Interface]
# 定义一个网段，所有节点统一使用网段 10.55.99.0/24
Address = 10.55.99.1/24
# 监听的端口，注意是UDP端口（防火墙需要开放对应的UDP端口）
ListenPort = 20015
# 上面查看的私钥填入
PrivateKey = xxx
# 自定义dns
DNS = 1.1.1.1, 8.8.8.8
MTU = 1200

# 节点1
[Peer]
PublicKey = xxx
# 允许转发的ip或路由
AllowedIPs = 10.55.99.3/32,192.168.11.0/24

# 节点二
[Peer]
PublicKey = xxx
AllowedIPs = 10.55.99.30/32

# 节点三
[Peer]
PublicKey = xxx
AllowedIPs = 10.55.99.5/32
```

## 系统需要开启转发，才能使节点之间为相互配置也能相互访问
``` sh
$ vim /etc/sysctl.conf
# 添加内容：
net.ipv4.ip_forward = 1
# 添加保存后查看
$ sysctl -p
# 配置 iptables
$ iptables -A FORWARD -i wg0 -o wg0 -j ACCEPT
```
