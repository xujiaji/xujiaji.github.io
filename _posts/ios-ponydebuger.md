---
title: 好用的iOS调试工具PonyDebugger
date: 2019-10-15 23:38:02
thumbnail: blog/ponydebugger.jpeg
categories:
 - iOS
tags:
 - Debug
---

# 好用的iOS调试工具PonyDebugger

PonyDebugger：<https://github.com/square/PonyDebugger/>

## 简介

PoneyDebugger是一个很给力的调试工具，它能通过浏览器调试App。

需要电脑上配置服务环境，在iOS项目添加sdk的配置。便可以对App进行网络请求监控、Core Data数据查看、查看当前界面UI层级等。

### 网络请求调试

我们的请求会通过PonyDebugger的代理服务[ponyd](https://github.com/square/PonyDebugger/tree/master/ponyd)，可以直观的像在浏览器上调试网页请求一样，调试App的请求。

> 我就直接把官方的图搬运过来用了`^_^`

![NetworkDebugging](https://xujiaji.oss-cn-beijing.aliyuncs.com/blog/poneydebugger/NetworkDebugging.png)

### Core Data 浏览

Core Data浏览，只需要通过在应用程序的代码中启用就可以了`ponyDebugger?.enableCoreDataDebugging()`

![CoreDataBrowser](https://xujiaji.oss-cn-beijing.aliyuncs.com/blog/poneydebugger/CoreDataBrowser.png)

### 视图层次调试

PonyDebugger会在浏览器中以XML的方式展示应用视图层次结构，并且可以在其中看到视图元素的属性。在面板中选中一个元素时，对应手机上也会被选中。当删除一个时也对应删除，可调整视图大小。

![ViewHierarchyDebugging](https://xujiaji.oss-cn-beijing.aliyuncs.com/blog/poneydebugger/ViewHierarchyDebugging.png)

## 远程日志

PonyDebuggert通过PDLog和PDLogObjects函数远程记录日志查看对象数据

![RemoteLogging](https://xujiaji.oss-cn-beijing.aliyuncs.com/blog/poneydebugger/RemoteLogging.png)



## 安装视频演示

<div style="width: 100%; display: inline-block; position: relative; padding-top: 70%; display: block; content: '';">
    <div style="position: absolute; top: 0; bottom: 0; right: 0; left: 0;">
    {%iframe //player.bilibili.com/player.html?aid=71370834&cid=123663162&page=1 100% 100% %}
    </div>
</div>

## 创建一个目录`ponyd`，并进去该目录

``` shell
mkdir ponyd
cd ponyd
```

## 将必要的依赖下载这个目录中`ponyd`

``` shell
curl -O -L https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz

curl -O -L https://pypi.python.org/packages/25/5d/cc55d39ac39383dd6e04ae80501b9af3cc455be64740ad68a4e12ec81b00/setuptools-0.6c11-py2.7.egg

curl -O -L https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pybonjour/pybonjour-1.1.1.tar.gz

tar xvf pybonjour-1.1.1.tar.gz
mv pybonjour-1.1.1 pybonjour
```

## 下载`bootstrap-ponyd.py`

``` shell
curl -O -L https://github.com/downloads/square/PonyDebugger/bootstrap-ponyd.py
```

## 在`bootstrap-ponyd.py`添加安装`pybonjour`的命令

``` shell
subprocess.check_call([join(home_dir, 'bin', 'python'),  join('pybonjour', 'setup.py'), 'install'])
```

> 添加在如下的位置上

``` shell
def after_install(options, home_dir):
    subprocess.check_call([join(home_dir, 'bin', 'python'),  join('pybonjour', 'setup.py'), 'install'])

    subprocess.check_call([join(home_dir, 'bin', 'pip'),
                     'install', '-U', '-e', 'git+https://github.com/square/PonyDebugger.git#egg=ponydebugger'])
```

## 通过运行bootstrap安装

``` shell
cat ./bootstrap-ponyd.py | python - --never-download --ponyd-symlink=/usr/local/bin/ponyd ~/Library/PonyDebugger
```

## 上面的安装会出错，因为一些包无法找到，我们通过下面的命令去修复

``` shell
~/Library/PonyDebugger/bin/easy_install --find-links https://pypi.python.org/simple/singledispatch/ -U singledispatch
~/Library/PonyDebugger/bin/easy_install --find-links https://pypi.python.org/simple/backports-abc/ -U backports_abc
~/Library/PonyDebugger/bin/easy_install --find-links https://pypi.python.org/simple/certifi -U certifi
~/Library/PonyDebugger/bin/easy_install --find-links https://pypi.python.org/simple/six/ -U six
~/Library/PonyDebugger/bin/easy_install --find-links https://pypi.python.org/simple/futures -U futures
sudo ~/Library/PonyDebugger/bin/easy_install -U pybonjour
```

## 安装devtools

``` shell
ponyd update-devtools
```

## 运行

``` shell
ponyd serve --listen-interface=127.0.0.1
```

## 配置iOS sdk

> 下面演示的是通过pod安装的

1. 在项目Podfile中引入`pod 'PonyDebugger'`
2. 打开一个在项目目录的命令窗口，运行`pod install`
3. swift项目，需要在连接桥文件中导入头文件，`#import <PonyDebugger/PonyDebugger.h>`
4. 添加sdk配置：
``` swift
let ponyDebugger = PDDebugger.defaultInstance()
ponyDebugger?.enableNetworkTrafficDebugging()
ponyDebugger?.enableViewHierarchyDebugging()
ponyDebugger?.setDisplayedViewAttributeKeyPaths(["frame", "hidden", "alpha"])
ponyDebugger?.forwardAllNetworkTraffic()
ponyDebugger?.enableCoreDataDebugging()
ponyDebugger?.enableRemoteLogging()
ponyDebugger?.connect(to: URL(string: "ws://localhost:9000/device"))
```

## 打开调试网页

<http://localhost:9000/>

## 结束

这里主要还是演示了一些怎么安装配置的PonyDebugger，因为在这里遇到些问题所以在此记录一波。谢谢观看！
