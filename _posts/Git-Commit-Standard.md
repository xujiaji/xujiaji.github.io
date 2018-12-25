---
title: Git Commit Standard
date: 2018-09-05 10:21:44
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/git/git_commit.jpg
categories:
 - 工具
tags:
    - Git
    - 笔记
---

记录一下Git的提交规范，方便以后查阅

<!-- more -->

## 提交命令
1. `git commit -m "提交修改信息"`，这样这只能有一行信息
2. `git commit`，会进入`vi`文本编辑器，可写多行。

## 提交信息的格式
> 每次提交信息都包括三个部分：Header、Body和Footer。其中，Header 是必需的，Body 和 Footer 可以省略。

```
<type>(<scope>): <subject>
// 空一行
<body>
// 空一行
<footer>
```

> 文字描述

```
# 标题行：50个字符以内，描述主要变更内容
#
# 主体内容：更详细的说明文本，建议72个字符以内。 需要描述的信息包括:
#
# * 为什么这个变更是必须的? 它可能是用来修复一个bug，增加一个feature，提升性能、可靠性、稳定性等等
# * 他如何解决这个问题? 具体描述解决问题的步骤
# * 是否存在副作用、风险?
#
# 尾部：如果需要的化可以添加一个链接到issue地址或者其它文档，或者关闭某个issue。
```


## `<type>`
|Value|Description|
|:-|:-|
|feat|feature新功能|
|fix|修复bug|
|doc|仅仅修改了文档，比如README, CHANGELOG, CONTRIBUTE等等|
|style|代码格式改变，不改变代码逻辑|
|refactor|代码重构，没有加新功能或者修复bug|
|perf|优化相关，比如提升性能、体验|
|test|测试用例，包括单元测试、集成测试等|
|chore|改变构建流程、或者增加依赖库、工具等|
|revert|回滚到上一个版本|

## `<scope>`
|Value|Description|
|:-|:-|
|all|表示影响面大 ，如修改了网络框架  会对真个程序产生影响|
|loation|表示影响小，某个小小的功能|
|module|表示会影响某个模块 如登录模块、首页模块 、用户管理模块等等|

## `<subject>`
1. subject是 commit 目的的简短描述，不超过50个字符。
2. 以动词开头，第一个字母小写，使用第一人称现在时，比如change，而不是changed或changes
第一个字母小写
3. 结尾不加句号"."

## `<body>`
对本次 commit 的详细描述，可以分成多行。

## `<footer>`
1. 并联Issue，本次提交如果和摸个issue有关系则需要写上这个，格式如下：
```
Issue #1, #2, #3
```
2. 关闭 Issue，如果当前提交信息解决了某个issue，那么可以在 Footer 部分关闭这个 issue，关闭的格式如下：
```
Close #1, #2, #3
```

## 完整例子
```
feat(all): add login

add login in project

- qq login
- weixin login
- sina login

Issue #1, #2
Close #1, #2
```
