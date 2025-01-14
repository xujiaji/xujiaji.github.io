---
title: Linux 笔记
date: 2017-12-12 12:25:29
author: xujiaji
thumbnail: blog/linux-notes.jpg
categories:
 - 笔记
tags:
 - Linux
---

# Linux 笔记 - 一些命令和使用的记录

## 查看正在运行的进程

> 如：查看正在运行的python进程

``` sh
ps -ef |grep python
```

## 权限

> 创建用户组

``` sh
groupadd [groupname]
```

> 添加用户到用户组

``` sh
gpasswd -a [username] [groupname]
```

> 查看用户组信息

``` sh
vim /etc/group
```

> 修改文件所有着和所有组

``` sh
chown [username]:[groupname] [filename]
```

> 递归添加组权限rwx

``` sh
setfacl -R -m g:[groupname]:rwx [floder]
```

## 文件查询

``` sh
sudo find / | grep "fab"
```

> 查找并删除当前目录及子目录所有apk文件
> type： f文件；d目录

``` sh
find . -type f -name "*.apk" | xargs rm -rf
```

## 递归删除xxx

``` sh
find . -name "xxx" -type f | xargs rm -rf
```

## tar 打包压缩解压

> .tar打包解包

``` sh
解包：tar xvf FileName.tar
打包：tar cvf FileName.tar DirName
```

> .gz

``` sh
解压1：gunzip FileName.gz
解压2：gzip -d FileName.gz
压缩：gzip FileName
```

> .tar.gz 和 .tgz

``` sh
解压：tar zxvf FileName.tar.gz
压缩：tar zcvf FileName.tar.gz DirName
```

## zip分卷压缩和解压

``` sh
# ----- 分卷压缩 -----
# 将文件或者文件件打包为zip压缩包，book.zip大小为38.8M
zip -r book.zip ./input.pdf
# 将book.zip分割，每个压缩包不超过20M，生成两个压缩包subbook.zip（17.8M）和subbook.z01（21M）
zip -s 20m book.zip --out subbook.zip
# ----- 合并解压 -----
# 将上述两个压缩包合并为一个压缩文件single.zip
zip subbook.zip -s=0 --out single.zip
# 解压single.zip
unzip -d ./ single.zip
```

## supervisor权限管理

``` sh
groupadd supervisor
usermod -a -G supervisor

After logging-out/logging-in (so that the new group membership takes effect), edit the supervisord configuration file (/etc/supervisor/supervisor.conf) to make the unix_http_server section look as follows

[unix_http_server]
file=/var/run/supervisor.sock ; (the path to the socket file)
chmod=0770 ; socket file mode (default 0700)
chown=root:supervisor

Notice that we have chmod’ded the file to 0770 (writeable by owner and group), and chowned the file to root:supervisor, which will allow members of the supervisor group to make calls to supervisorctl. We must restart supervisord one last time

supervisorctl reload
```

## 读取文件里的键值对信息

> `local.properties`

```
sdk.dir=/Users/xxx/Library/Android/sdk
```

> 读取`sdk.dir`

```
grep "sdk.dir" local.properties | cut -d'=' -f2 | sed 's/\r//'
```

## 通过cpu或内存占用排序查进程

> 查使用内存最多的10个进程

```
ps -aux | sort -k4nr | head -10
```

> 查询系统内存占用并排序打印出所有的进程

```
ps aux --sort -rss
```

> 查使用CPU最多的3个进程

```
ps -aux | sort -k3nr | head -3
```

## SSH远程的时候，没有使用到这个远程用户的环境变量

> 创建`~/.ssh/environment`

> 在里面添加环境配置如：

```
PATH=/usr/local/opt/openjdk@11/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/Apple/usr/bin
```

> 编辑sshd配置`sudo vim /private/etc/ssh/sshd_config`

```
PermitUserEnvironment=yes
```

## 配置apt仓库源
编辑 `/etc/apt/sources.list`
将其中的地址替换成新的源地址

## ssh客户端，连接linux后，显示的中文名都是16进制的形式
> 如：

```
$ ls
''$'\344\270\213\350\275\275'  ''$'\345\205\254\345\205\261'  ''$'\345\233\276\347\211\207'  ''$'\346\226\207\346\241\243'  ''$'\346\241\214\351\235\242'  ''$'\346\250\241\346\235\277'  ''$'\350\247\206\351\242\221'  ''$'\351\237\263\344\271\220'
```
> 处理：

在`~/.bashrc`文件中添加以下内容
```
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
export LANGUAGE=zh_CN:en_US
```