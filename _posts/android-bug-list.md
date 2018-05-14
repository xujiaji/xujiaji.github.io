---
title: Android开发中的bug清单
date: 2017-12-12 15:34:41
author: xujiaji
thumbnail: image/android-bug-list.png
categories:
 - 笔记
tags:
    - android
    - bug
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
