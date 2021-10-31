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

## 升级flutter后的项目
1. 查看项目中所有的有修复
``` shell
dart fix --dry-run
```
2. 批量应用上面查出修改
``` shell
dart fix --apply
```

## 在当前项目重新创建ios、android等模块

> -i iOS 用swift或objc
> -a android 用kotlin或java
> 下方创建iOS为swift语言，android为kotlin语言

```
flutter create -i swift -a kotlin .
```

## iOS虚拟机运行报错：Could not build the application for the simulator.
> 清理 `~/Library/Developer/Xcode/DerivedData`

```
flutter clean
flutter run
```

## 空安全迁移
> 查看依赖包的迁移空安全状态

```
flutter pub outdated --mode=null-safety
```

> 通过迁移工具命令（迁移前迁移后`dart sdk: ">=2.10.0 <3.0.0"`，迁移后`dart sdk: ">=2.12.0 <3.0.0"`）

```
dart migrate
```