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

## 编译windows exe文件，在非开发环境中安装后无法打开

原因是因为缺少环境库文件：`msvcp140.dll`、`vcruntime140.dll`、`vcruntime140_1.dll`

这几个文件可以在开发换成的VC的目录中找到（可能不同版本有区别），本电脑在目录：`C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Redist\MSVC\14.40.33807\x64\Microsoft.VC143.CRT`

在该目录中可以看到上面三个文件

1、临时解决问题：我们可以将上面三个文件拷贝到安装后的目录即可运行

2、一劳永逸处理：我们可以将这三个文件拷贝到项目中。这里我们可以拷贝到项目目录下的：`[FlutterProject]/windows/libs`(只是为了方便后面不用再去找)

修改`inno_setup.iss`中的`[Files]`配置，在打包exe安装包时，将这几个库放进去

```
[Files]
Source: "windows\libs\*.dll"; DestDir: "{app}"; Flags: ignoreversion
```