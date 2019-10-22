---
title: Android开发中的bug清单
date: 2017-12-12 15:34:41
author: xujiaji
thumbnail: blog/android-bug-list.png
categories:
 - Android
tags:
    - Android
    - Bug
---
## Android Gradle plugin 3.0.0-alpha5 must not be applied to project
- 解决地址：https://stackoverflow.com/questions/44857191/failed-to-apply-plugin-android-gradle-plugin-3-0-0-alpha5-must-not-be-applied-to
- 原因：
- 解决办法：

> 在gradle.properties：

```
org.gradle.configureondemand=false
```
> 然后在终端窗口中停止守护进程

```
gradlew --stop
```

## java.lang.IllegalStateException: Fragment already added: DialogFragment
- 解决地址：http://blog.csdn.net/kifile/article/details/47442899
- 原因：点击过快DialogFragment消息队列还没有执行完
- 解决办法：

``` java
getFragmentManager().executePendingTransactions();
if (!mDialogFragment.isAdded())
{
    mDialogFragment.show(getFragmentManager(), "DialogFragment");
}
```

## java.lang.RuntimeException: Unable to get provider
- 解决地址：https://stackoverflow.com/questions/37312103/unable-to-get-provider-com-google-firebase-provider-firebaseinitprovider
- 原因：在SDK <22的设备中遇到同样的问题，原因是MultiDex，MultiDex.install必须在attachBaseContext方法中
- 解决方法
自定义Application中添加如下：
``` java
public class YourApplication extends Application {

    @Override
    protected void attachBaseContext(Context context) {
        super.attachBaseContext(context);
        MultiDex.install(this);
    }
}
```

build.gradle中添加如下：
```
compile 'com.android.support:multidex:1.0.1'
```

## 安装报错 INSTALL_FAILED_NO_MATCHING_ABIS

由于没有对应当前设备的ndk模块导致命令安装报错

遇到这个的原因是腾讯x5内核只有`armeabi`，于是在手机上命令安装会遇到这个问题（小米测试不能上架），于是我把`armeabi`里的x5内核动态库拷贝到`armeabi-v7a`

`build.gradle`添加下面配置（其实`armeabi-v7a`大多数设备就够了）

``` groovy
android {
    defaultConfig {
        ndk {
            abiFilters "armeabi", "x86", "armeabi-v7a"
        }
    }
}
```
