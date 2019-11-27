---
title: Flutter资源自动生成配置脚本
date: 2019-11-27 17:36:09
author: xujiaji
thumbnail:
categories:
 - Flutter
tags:
 - Flutter
 - 工具
 - Python
---

# Flutter资源自动生成配置

项目地址：<https://github.com/xujiaji/FlutterAssetsSync/>

## 简介

各位小伙伴都知道flutter的资源配置需要在`pubspec.yaml`中配置资源路径。

我想吧！这么麻烦的事情因该有做贡献的同学提供插件吧！果不其然我找到一个叫[flutter-img-sync](https://github.com/Leo0618/flutter-img-sync)的插件，可以快速添加到配置中，并且生成一个类似android的R文件，方便快速准确的调用。

爽了几天，发现这个框架并不能满足了，首先每次生成资源会重新排序导致git版本合并代码都需要手动合并，其次生成的2.0x和3.0x是用的包含2.0x和3.0x的全路径名。

由于大佬插件代码不是开源的，于是想了想还是自己用python快速搞一个一样功能的出来吧，可以自己自定义，并且可以全方位满足自己需求！

## 视频介绍

## 环境

> 安装了Python3.0+就行了

## 配置

1. 在`pubspec.yaml`的`assets`处添加自动自动构建的位置区间
> 这个区间内不可添加其他资源，因为每次构建都会替换`# assets-generator-begin`和`# assets-generator-end`之间的内容

```yaml
  assets:
  # assets-generator-begin
  # assets-generator-end
```

2. 接下了就是配置资源的目录了
首先，在项目中假如说你的资源目录就如下所示是`assets`
![](blog/flutter_pubspec/55813610-18E1-478F-BBFD-C24D4307F949.png)
那么，你需要在`assets_generator.py`（顶部进入项目地址下载哦）中配置对应的位置，如下所示：
![](blog/flutter_pubspec/B8358DF2-32C5-4D24-B7DC-D6062B42AA31.png)

3. 把脚本`assets_generator.py`拷贝到您的项目根目录

## 使用

在项目目录下打开命令行，运行`./assets_generator.py`
![](blog/flutter_pubspec/1F3A4EDA-47F3-4236-9ED6-39076479FF7F.png)

此时会在`pubspec.yaml`配置的区域添加上路径
![](blog/flutter_pubspec/21218262-4206-424D-A578-DE1A968BAE4B.png)

同时会生成一个`r.dart`的文件，内容如下：（篇幅原因就粘贴部分了）
```dart
class R {
  /// ![](http://127.0.0.1:3333/assets/fonts/fzxz300.ttf)
  static final String assetsFontsFzxz300 = 'assets/fonts/fzxz300.ttf';
  /// ![](http://127.0.0.1:3333/assets/h5/index.html)
  static final String assetsH5Index = 'assets/h5/index.html';
  /// ![](http://127.0.0.1:3333/assets/h5/relationship.js)
  static final String assetsH5Relationship = 'assets/h5/relationship.js';
  /// ![](http://127.0.0.1:3333/assets/image/add_ico.png)
  static final String assetsImageAddIco = 'assets/image/add_ico.png';
}
```

在代码中使用非常方便只需要向下面这样，当然需要先导入`r.dart`

```dart
 Image.asset(R.assetsImageMan)
```

同时在选对应的图片时，也可以进行图片预览（如果你把那个python脚本终止了那就不能预览了）

![](blog/flutter_pubspec/241D6239-21E2-4651-9840-576E094997C8.png)

> 如果添加了新的图片，重新运行一下这个脚本就可以了

## 功能

1. 自动在yaml文件中生成资源路径配置
2. 自动在lib目录创建一个`r.dart`来管理资源调用
3. 生成名字有序
4. 通过`R.`对应资源可以进行预览
