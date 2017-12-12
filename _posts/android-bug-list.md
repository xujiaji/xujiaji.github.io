---
title: Android开发中的bug清单
date: 2017-12-12 15:34:41
author: xujiaji
thumbnail: image/android-bug-list.png
tags:
    - android
    - bug
---

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
