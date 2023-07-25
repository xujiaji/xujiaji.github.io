---
title: Android开发-零碎笔记
date: 2018-1-24 17:03:41
author: xujiaji
thumbnail: blog/android-notes/banner.png
categories:
 - 笔记
tags:
    - Android
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

## ScrollView嵌套RecyclerView滑动滑动起来很吃力
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

## jadx反编译

``` shell
jadx -d out -j 1 classes.dex
```

## 本地创建maven

> 在模块`build.gralde`中添加以下代码

``` grovvy
apply plugin: 'maven'

uploadArchives {
    repositories.mavenDeployer {
        def mavenDirPath = file('../xujiajilocalmaven') // 打包在哪个目录，这里是项目根目录下的xujiajilocalmaven
        repository(url: "file://${mavenDirPath.absolutePath}")
        pom.project {
            groupId "com.github.xujiaji" // gradle依赖的goupid
            artifactId "xiangmu" // gradle依赖的artifactId，模块名
            version "1.0.0" // 模块版本号
        }
    }
}
```

> 打包：通过点击Android studio的Gradle命令中对应模块的

`clean`、`assemble`、`uploadArchives`

> 启动文件浏览服务，这里通过python在xujiajilocalmaven启动一个服务

``` shell
python3 -m http.server 5555
```

通过以上命令，启动服务后，可通过访问`http://localhost:5555/`来访问`xujiajilocalmaven`目录中的内容

> 依赖：

``` grovvy
repositories {
    maven { url "http://localhost:5555/" }
}

dependencies {
    implementation 'com.github.xujiaji:xiangmu:1.0.0' // 这里是根据上面的groupId、artifactId、version的配置来的
}
```

## linux安装Android SDK
```
# mkdir /usr/android/android_sdk      // 创建sdk 
# cd /usr/android/android_sdk   
# wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip    //下载android sdk
# unzip sdk-tools-linux-4333796.zip   //解压
# vim /etc/profile      // 配置环境变量
// 增加内容
export ANDROID_HOME=/usr/android/android_sdk
export PATH=$PATH:${ANDROID_HOME}/tools/bin
# source /etc/profile   // 使配置生效
# sdkmanager --list // 查看已安装信息
# sdkmanager "build-tools;29.0.3"
# sdkmanager "platform-tools"
# sdkmanager "platform-tools"   // sdk里面的工具
# sdkmanager "build-tools;29.0.3" // 这个上面已经安装了，编译工具
# sdkmanager "platforms;android-28"    // android版本对应的sdk版本
# sdkmanager "platforms;android-29"   // android版本对应的sdk版本
接下来把android 的sdk的环境变量去完善
# vim /etc/profile      // 配置环境变量，在前面android配置的基础上修改，结果如下
export ANDROID_HOME=/usr/android/android_sdk
export PATH=$PATH:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools
# source /etc/profile    // 环境变量生效
# adb version
```

sdk下载地址
https://developer.android.com/studio#cmdline-tools

--sdk_root 指定sdk路径
同意隐私协议
yes | cmdline-tools/bin/sdkmanager --licenses --sdk_root=/var/jenkins_home/AndroidSdk

## Plugin 断点
https://juejin.cn/post/6948626628637360135