---
title: Mac 使用笔记
date: 2019-05-06 11:11:53
updated: 2020-04-17 12:03:06
tags:
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

> 查看`8080`端口的进程占用

``` sh
lsof -i tcp:8080
```

> 杀死进程

``` sh
kill pid
```
