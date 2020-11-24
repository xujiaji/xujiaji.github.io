---
title: Mac Use Node
date: 2019-05-06 11:11:53
updated: 2020-04-17 12:03:06
tags:
---

# Mac 使用笔记

## rsync备份文件到硬盘

> [参考文章](https://www.ruanyifeng.com/blog/2020/08/rsync.html)

``` sh
rsync -anv --exclude-from='exclude-file.txt' /Users/jiajixu/ /Volumes/cc/MacBak
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
