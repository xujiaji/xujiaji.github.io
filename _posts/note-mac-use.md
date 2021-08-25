---
title: Mac 使用笔记
date: 2019-05-06 11:11:53
updated: 2021-07-10 19:50:40
categories:
  - 笔记
tags:
  - MacOS
  - Linux
---

# Mac 使用笔记

## [mac中接入移动硬盘后自动备份数据](http://www.xiaocai.name/2017/07/07/mac%E4%B8%AD%E6%8E%A5%E5%85%A5%E7%A7%BB%E5%8A%A8%E7%A1%AC%E7%9B%98%E8%87%AA%E5%8A%A8%E5%A4%87%E4%BB%BD%E6%95%B0%E6%8D%AE(launchctl)/)

> 注意在隐私设置中添加`/bin/sh`文件夹访问权限，不然无法同步文件

## rsync备份文件到硬盘

> [参考文章](https://www.ruanyifeng.com/blog/2020/08/rsync.html)

``` sh
rsync -av --exclude-from='exclude-file.txt' /Users/jiajixu/ /Volumes/cc/MacBak
```

## 删除所有以`.iml`结尾的文件

``` sh
find ./ -name "*.iml" -exec rm -rf {} \;
```

## 创建替身（快捷方式）

按住`option`+`command`，鼠标拖出对应的目标就可以了

## ll、la、l等ls别名

``` shell
cd ~
touch .bash_profile
echo "alias l='ls -alhF'" >>.bash_profile
echo "alias la='ls -AFh'" >>.bash_profile
echo "alias ll='ls -lhAF'" >>.bash_profile
source ~/.bash_profile
```

## 启动一个网页服务

对应项目目录下执行：

``` shell
python3 -m http.server
```

## 查看端口占用和杀死进程

> 找到对应进程(这里找到gradle的进程)

``` sh
ps -A | grep gradle
```

> 查看`8080`端口的进程占用

``` sh
lsof -i tcp:8080
```

> 杀死进程

``` sh
kill pid
```

## mysql

> 启动mysql

``` sh
sudo mysql.server start
```

## mac下dos2unix文件转换

``` sh
find . -type f -exec fromdos {} \;
```

## 软件没有访问路径的权限导致报错 Operation not permitted

解决参考地址：<https://blog.csdn.net/WangJiankun_ls/article/details/103110241/>

``` sh
1.左上角点击选择‘System Preferences’

2.选择“Security & Privacy”

3.选择 “Privacy”-->“Full Disk Access”

4.点击左下角按钮获得管理员操作权限

5.把出问题的应用程序加到“Full Disk Access”列表中
```

## VirtualBox linux创建共享目录
<https://www.shuzhiduo.com/A/kjdw0RLrzN//>
> 准备环境

```
yum install -y gcc gcc-devel gcc-c++ gcc-c++-devel make kernel kernel-devel
```

> 安装增强工具（在菜单栏设备里面点击一下安装增强）

```
# 然后查看当前虚拟机中所有连接的虚拟设备
lsscsi

# [0:0:0:0]    disk    ATA      VBOX HARDDISK    1.0   /dev/sda 
# [1:0:0:0]    cd/dvd  VBOX     CD-ROM           1.0   /dev/sr0 

# 创建挂载目录:
mkdir /mnt/cdrom

# 挂载 VBOX 盘符　　
sudo mount /dev/sr0 /mnt/cdrom

# 安装增加工具
cd /mnt/cdrom
./VBoxLinuxAdditions.run
```

> 在VirtualBox中创建共享目录，这里目录取名为`gopath`

```
mkdir /mnt/gopath

# 运行挂载命令, 这里的 gopath 就是上面共享文件夹名称
mount -t vboxsf gopath /mnt/gopath
```