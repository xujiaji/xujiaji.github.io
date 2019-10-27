---
title: 好用的iOS网络请求调试工具Bagel
date: 2019-10-24 23:24:42
thumbnail: blog/screenshot_bagel.png
tags:
  - iOS
  - 工具
---

# iOS网络请求调试神器使用

这是一个方便调试api的工具，只需要简单的配置即可方便的看到App中数据的请求

Bagel: <https://github.com/yagiz/Bagel/>

## 视频演示

<div style="width: 100%; display: inline-block; position: relative; padding-top: 70%; display: block; content: '';">
    <div style="position: absolute; top: 0; bottom: 0; right: 0; left: 0;">
    {%iframe //player.bilibili.com/player.html?aid=73544560&cid=125799021&page=1 100% 100% %}
    </div>
</div>

## 安装Mac应用

通过下载源码运行得到一个mac上面运行的程序

1. 下载源码
``` shell
git clone https://github.com/yagiz/Bagel.git
```
2. 安装对应的依赖库`pod install`
3. 编译运行项目


## 配置项目

1. 为项目添加依赖，这里展示的是podfile的配置方式。在Podfile中添加
``` shell
pod 'Bagel', '~>  1.3.2'
```
2. 下载Bagel库`pod install`

## 使用

1. 导入Bagel模块`import Bagel`
2. 开启Bagel`Bagel.start()`
``` swift
// 只在debug的模式下才开启网络监听
#if DEBUG
Bagel.start()
#endif
```
