---
title: Android开发笔记
date: 2018-1-24 17:03:41
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-notes/banner.png
categories:
 - Android
tags:
    - android
    - 笔记
---
## 垂直RecyclerView嵌套垂直RecyclerView滑动时出现的卡顿
原因：内部RecyclerView重复设置适配器导致的卡顿

解决：判断内部RecyclerView是否设置过适配器，如果没有才设置

``` java
//内部RecyclerView的获取和处理问题的代码
RecyclerView rvItem = helper.getView(R.id.rvItem);
rvItem.setNestedScrollingEnabled(false);
if(rvItem.getAdapter() == null)
{
    LinearLayoutManager layoutManager = new LinearLayoutManager(mContext);
    layoutManager.setAutoMeasureEnabled(true);
    rvItem.setLayoutManager(layoutManager);
    rvItem.setAdapter(new OrderItemAdapter(item.getList()));
}
```

##  ScrollView嵌套RecyclerView滑动滑动起来很吃力
``` java
recyclerView.setNestedScrollingEnabled(false);
```

## RecyclerView嵌套RecyclerView时，刷新内部RecyclerView会跳动
原因：内部RecyclerView抢占了焦点

解决：将内部RecyclerView的焦点设置为false
``` java
recyclerView.setFocusableInTouchMode(false);
```

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

## 空包签名
```
jarsigner -verbose -keystore [keystore签名秘钥路径] -signedjar [apk输出路径] [apk输入路径（需要签名的空包）] [签名秘钥别名]
```

## 获取签名sha1
```
keytool -list -v -keystore [签名路径]
```
