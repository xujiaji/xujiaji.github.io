---
title: Git笔记
date: 2017-12-12 11:02:34
author: xujiaji
thumbnail: image/git-notes.png
tags:
    - git
    - 笔记
---

## 分支
- 查看本地分支
``` sh
$ git branch
```
- 查看远程分支
``` sh
$ git branch -a
```
- 创建分支1.1.  `2并切换到1.1.2分支
``` sh
$ git checkout -b 1.1.2
```
- 拆分写法
``` sh
$ git branch 1.1.2
$ git checkout 1.1.2
```
- 删除本地分支
``` sh
$ git branch -d 1.1.2
```
- 推送本地分支到远程分支，远程分支不存在则创建
``` sh
$ git push origin 1.1.2:1.1.2
```
- 本地分支留空则是删除远程分支
``` sh
$ git push origin :1.1.2
```
- 本地分支推送到远程分支
``` sh
$ git push origin 1.1.2
```
- 合并work分支到当前分支
``` sh
$ git merge work
```
