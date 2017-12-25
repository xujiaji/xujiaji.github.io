---
title: linux(Ubuntu)笔记
date: 2017-12-12 12:25:29
author: xujiaji
thumbnail: image/linux-notes.jpg
tags:
    - linux
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
The configuration area at '/./configuration' could not be created.  Please choose a writable location using the '-configuration' command line option.
```

> 解决：写一个命令脚步，先跳转到`~/xmind/XMind_amd64/`目录再执行`XMind`运行软件，脚步如下：

`start.sh`

``` sh
#!/bin/bash
cd ~/xmind/XMind_amd64
./XMind
```
> 下面时启动器`xmind.desktop`

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
