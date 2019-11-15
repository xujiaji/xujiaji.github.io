---
title: linux(Ubuntu)笔记
date: 2017-12-12 12:25:29
author: xujiaji
thumbnail: blog/linux-notes.jpg
categories:
 - Linux
tags:
    - Linux
    - 笔记
---

## 每次开机弹出软件崩溃反馈
> 解决：删除崩溃日志

``` sh
$ sudo rm /var/crash/*
```

## 更新软件源的索引
``` sh
$ sudo apt-get update
```

## 升级软件
``` sh
$ sudo apt-get upgrade
```

## 修复依赖关系
> 假如用户的系统上有某个package不满足依赖条件，这个命令就会自动修复，安装程序包所依赖的包

``` sh
$ sudo apt-get -f install
```

## 创建启动器
> 安装软件

``` sh
$ sudo apt install gnome-panel
```

> 打开创建图标的界面，下边的`~/桌面/`为启动器创建的位置

``` sh
gnome-desktop-item-edit ~/桌面/ --create-new
```

> 最后根据提示创建图标

## 安装xmind-linux
> 下载地址：https://www.xmind.cn/download/

下载下来是一个压缩包，将其放到`~/`目录并解压。由于我是64位系统，所以进入`~/xmind/XMind_amd64/`目录双击XMind运行软件。

> 由于我创建启动器遇到下面的错误，必须在当前目录才能运行XMind，否则就有下面的错误提示对话框出现。

``` sh
The configuration area at '/./configuration'
could not be created.
Please choose a writable location
using the '-configuration' command line option.
```

> 解决：写一个命令脚步，先跳转到`~/xmind/XMind_amd64/`目录再执行`XMind`运行软件，脚步如下：

`start.sh`

``` sh
#!/bin/bash
cd ~/xmind/XMind_amd64
./XMind
```
> 下面是启动器`xmind.desktop`

``` sh
#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon[zh_CN]=/home/soul/xmind/icon.png
Name[zh_CN]=xmind
Exec=/home/soul/xmind/XMind_amd64/start.sh
Name=xmind
Icon=/home/soul/xmind/icon.png
```

## 更新hosts文件后让文件生效
```
sudo apt-get install nscd
sudo /etc/init.d/nscd restart
```

## 使用Samba让Linux与Windows共享文件夹
> 安装samba

``` sh
$ sudo apt-get install samba
```
> 创建共享目录

``` sh
$ mkdir /home/soul/文档/ShareFiles
$ sudo chmod /home/soul/文档/ShareFiles
```
> 修改samba配置文件

打开文件
``` sh
$ sudo vim /etc/samba/smb.conf
```
末尾添加如下内容
``` sh
[share]  
   comment = my share directory  
   path = /home/soul/文档/ShareFiles
   browseable = yes  
   writable = yes
   public = yes
   valid users = xujiaji
```
xujiaji是我当前linux的用户名，相应换成你的

> 设置登录密码

```
sudo touch /etc/samba/smbpasswd
sudo smbpasswd -a xujiaji
```
xujiaji换成上一步你设置的用户名

> 启动samba服务器

``` sh
$ sudo /etc/init.d/samba restart
```
> windows中打开

- 打开windows文件管理器，顶部输入`\\linux ip\share`
- 账号密码为linux账户的账户密码

## 清理系统
### 删除一些不必要的资源
``` sh
$ sudo apt-get autoclean
$ sudo apt-get autoremove
```

### 删除旧内核
> 查看当前使用的内核信息：`uname -a`

```
$ uname -a
Linux boomake-pc 4.10.0-42-generic #46~16.04.1-Ubuntu SMP Mon Dec 4 15:57:59 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```
> 查看已存在的内核：`dpkg --get-selections| grep linux`

``` sh
$ dpkg --get-selections| grep linux
console-setup-linux				install
libselinux1:amd64				install
libselinux1:i386				install
linux-base					install
linux-firmware					install
linux-generic-hwe-16.04				install
linux-headers-4.10.0-40				install
linux-headers-4.10.0-40-generic			install
linux-headers-4.10.0-42				install
linux-headers-4.10.0-42-generic			install
linux-headers-generic-hwe-16.04			install
linux-image-4.10.0-40-generic			install
linux-image-4.10.0-42-generic			install
linux-image-extra-4.10.0-40-generic		install
linux-image-extra-4.10.0-42-generic		install
linux-image-generic-hwe-16.04			install
linux-libc-dev:amd64				install
linux-libc-dev:i386				install
linux-sound-base				install
linuxbrew-wrapper				install
pptp-linux					install
syslinux					install
syslinux-common					install
syslinux-legacy					install
util-linux					install
```
> 删除：`sudo apt-get purge`

> 更新一下启动引导：`sudo update-grub`或者`sudo update-grub2`

## appstreamcli错误
> `sudo-apt get update`时出现下面错误

``` sh
The AppStream system cache was updated, but some errors were detected, which might lead to missing metadata. Refer to the verbose log for more information.
Reading package lists... Done
E: Problem executing scripts APT::Update::Post-Invoke-Success 'if /usr/bin/test -w /var/cache/app-info -a -e /usr/bin/appstreamcli; then appstreamcli refresh-cache > /dev/null; fi'
E: Sub-process returned an error code
```
> 解决

``` sh
$ sudo rm /usr/bin/appstreamcli
cd /tmp && mkdir asfix
cd asfix
wget https://launchpad.net/ubuntu/+archive/primary/+files/appstream_0.9.4-1ubuntu1_amd64.deb
wget https://launchpad.net/ubuntu/+archive/primary/+files/libappstream3_0.9.4-1ubuntu1_amd64.deb
sudo dpkg -i *.deb
```

## 安装截屏软件Shutter
> 添加软件源

``` sh
$ sudo add-apt-repository ppa:shutter/ppa
```
> 更新源并安装

``` sh
$ sudo apt-get update
$ sudo apt-get install shutter
```
> 设置快捷键

系统设置 > 键盘 > 快捷键 > 自定义快捷键 > +

|自定义快捷键||
|-|-|
|名称：|Shutter Select|
|命令：|shutter -s|

点击新添加条目的右侧新建快捷键，然后同时按住Ctrl+Alt+A，结束。

## 文件查询

``` sh
sudo find / | grep "fab"
```
