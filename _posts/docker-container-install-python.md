---
title: Docker容器内编译安装Python3
date: 2022-05-16 11:54:17
categorys: 
	- 笔记
tags:
	- Docker
	- Linux
---

## 下载
1. 下载Python3.9地址：https://www.python.org/downloads/release/python-3912/
2. 点击`Gzipped source tarball`下载
3. Docker 通过root进入容器
``` sh
# 查看容器id
docker ps
# 以root账户进入容器，这里的47500d3da07c是上一步查看的id
docker exec -it --user root 47500d3da07c /bin/bash
# 进入下载目录
cd /var/jenkins_home/pythons/
# 下载
curl -O https://www.python.org/ftp/python/3.9.12/Python-3.9.12.tgz
# 解压
tar zxvf Python-3.9.12.tgz
```

# Docker中容器中安装

``` shell
# 重名名进入解压目录
mv Python-3.9.12 Python-3.9.12-Inteller
cd Python-3.9.12-Inteller
# 安装编译需要的库
apt update
apt install -y gcc make zlib1g-dev libbz2-dev
# 配置，--prefix是安装的目录
./configure --with-zlib=/usr/include --prefix=/var/jenkins_home/pythons/Python-3.9.12
# 编译&安装
make && make install
```