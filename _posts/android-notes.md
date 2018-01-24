---
title: Android开发笔记
date: 2018-1-24 17:03:41
author: xujiaji
thumbnail: image/android-notes/banner.png
tags:
    - android
    - 笔记
---

## adb之Wifi连接手机
> 查看当前设备`adb devices`

``` sh
$ adb devices
7d1cbcbb	device
192.168.56.101:5555	device
```
> 让adb重新启动，并监听端口5555`adb -s 设备名 tcpip 5555`

``` sh
$ adb -s 7d1cbcbb tcpip 5555
restarting in TCP mode port: 5555
```
> 连接`adb connect ip地址:端口`，在手机上查看连接的wifi地址，WiFi需要和电脑网络同网段

```
$ adb connect 192.168.2.207:5555
connected to 192.168.2.207:5555
```
