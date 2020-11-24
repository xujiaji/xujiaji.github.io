---
title: Flutter笔记
date: 2019-03-29 09:59:55
updated: 2020-05-06 18:55:06
categories:
 - 笔记
tags:
 - Flutter
---

# Flutter笔记

## 运行桌面版本

<https://flutter.dev/desktop/>

## idea新建文件模板（下划线文件名，自动创建驼峰类名）

> 效果

1. 创建`ab_cd.dart`
2. 自动生成内容：

``` dart
class AbCd {

}
```

> 模板代码

``` velocity
#set ($s = $NAME.split("_"))
#set ($result="")
#foreach ($foo in $s)
    #set ($result = ${result} + $foo.substring(0,1).toUpperCase() + $foo.substring(1))
#end

class  $result {

}
```
