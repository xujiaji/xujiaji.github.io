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
```
$ git branch
```
- 查看远程分支
```
$ git branch -a
```
- 创建分支1.1.2并切换到1.1.2分支
```
$ git checkout -b 1.1.2
```
- 拆分写法
```
$ git branch 1.1.2
$ git checkout 1.1.2
```
- 删除本地分支
```
$ git branch -d 1.1.2
```
- 推送本地分支到远程分支，远程分支不存在则创建
```
$ git push origin 1.1.2:1.1.2
```
- 本地分支留空则是删除远程分支
```
$ git push origin :1.1.2
```
- 本地分支推送到远程分支
```
$ git push origin 1.1.2
```
- 合并work分支到当前分支
```
$ git merge work
```

## git pull和本地冲突
> 冲突log

``` sh
$ git pull
remote: Counting objects: 24, done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 24 (delta 7), reused 23 (delta 6), pack-reused 0
Unpacking objects: 100% (24/24), done.
From https://github.com/elmorec/hexo-theme-inside
   a98e719..3b64c8a  master     -> origin/master
error: Your local changes to the following files would be overwritten by merge:
        _config.yml
Please commit your changes or stash them before you merge.
Aborting
Updating a98e719..3b64c8a
```

> 1、用 `git stash`本地暂时保存起来

``` sh
$ git stash
Saved working directory and index state WIP on master: a98e719 update scripts
```

> 2、pull

> 3、还原`git stash pop stash@{0}`

``` sh
$ git stash pop stash@{0}
Auto-merging _config.yml
On branch master
Your branch is up-to-date with 'origin/master'.
```
