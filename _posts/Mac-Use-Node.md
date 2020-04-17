---
title: Mac Use Node
date: 2019-05-06 11:11:53
updated: 2020-04-17 12:03:06
tags:
---

# Mac 使用笔记

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
