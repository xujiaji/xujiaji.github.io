---
title: Ubuntu安装Android studio
date: 2016-03-27 07:13
author: xujiaji
thumbnail: image/android-studio.jpg
tags:
    - Android
    - 工具
    - Linux
---

## 1.安装jdk
### ①由于linux自带openjdk因此我就将openjdk卸载了装jdk1.7
``` sh
 $ sudo apt-get remove openjdk-*
```
### ②下载jdk1.7
[jdk1.7下载链接](http://www.oracle.com/technetwork/cn/java/javase/downloads/jdk7-downloads-1880260.html)
我下载的文件为：jdk-7u79-linux-x64.tar.gz
### ③解压
- 创建/usr/java目录
 ``` sh
   $ sudo mkdir /usr/java
 ```
- 将当前目录下的jdk压缩包移/usr/java
 ``` sh
   ~/下载 $ sudo mv jdk-7u79-linux-x64.tar.gz /usr/java
 ```
- 解压到/usr/java，删除压缩包
 ``` sh
   $ cd /usr/java
   $ sudo tar -zxvf /usr/java/jdk-7u79-linux-x64.tar.gz
   $ sudo rm jdk-7u79-linux-x64.tar.gz 
 ```

### ④配置jdk环境变量
- 打开环境变量配置文件profile
``` sh
   $ sudo gedit /etc/profile
```
- 在文本最后添加如下信息，注意改成自己的jdk版本
``` sh
JAVA_HOME=/usr/java/jdk1.7.0_79
PATH=$JAVA_HOME/bin:$PATH
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME PATH CLASSPATH
```
- 保存、重启、java -version验证是否配置成功

## 2.安装android studio
### ①下载linux android studio
[官网下载](http://developer.android.com/intl/zh-cn/sdk/index.html)

### ②解压
将下载好的android studio压缩包移动到/usr/local目录，然后unzip命令解压
``` sh
unzip android-studio-ide-141.2456560-linux.zip
```
### ③运行
进入android-studio/bin,然后运行studio.sh
``` sh
 $ cd android-studio/bin
 $ sh studio.sh
```
### ④因为在linux mint第一天已经修改hosts翻墙，所以就自动下载sdk和更新，节省操作咯！
## 3.安装Genymotion
> Genymotion被称为是速度最快的Android模拟器可不是盖的，手机也没有两，就打算安装一个模拟器。

### [Genymotion官网](https://www.genymotion.com/)
注册一个号，登录了就能下载免费版本的虚拟机。[我下载版本的连接地址](http://files2.genymotion.com/genymotion/genymotion-2.6.0/genymotion-2.6.0-linux_x64.bin)
### 安装步骤
根据这篇教程[Ubuntu下安装Genymotion安卓模拟器 Linux教程](http://www.lihuan.com.cn/2015/02/15/521.html)
- 将genymotion-2.6.0-ubuntu15_x64.bin移动到用户目录`$ mv genymotion-2.6.0-ubuntu15_x64.bin /home/jiana`
- 需要安装一个软件virtualbox才能使用Gecymotion,命令:`sudo apt-get install virtualbox`
- 进入/home/jiana运行genymotion文件
``` sh
$ cd /home/jiana/
$ chmod +x genymotion-2.6.0-ubuntu15_x64.bin 
$ ./genymotion-2.6.0-ubuntu15_x64.bin 
```
- 完成后进入该用户目录下的genymotion目录，双击运行genymotion。好了，接下来就可以下载genymotion虚拟机来体验快感了。