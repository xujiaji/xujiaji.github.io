---
title: linux笔记
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
