---
title: 好用的iOS调试工具PonyDebugger
date: 2019-10-15 23:38:02
categories:
 - iOS
tags:
 - Debug
---

# 好用的iOS调试工具PonyDebugger

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
  480  ponyd update-devtools
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
