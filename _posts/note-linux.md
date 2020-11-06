---
title: Linux 笔记
date: 2017-12-12 12:25:29
author: xujiaji
thumbnail: blog/linux-notes.jpg
categories:
 - Linux
tags:
 - Linux
 - 笔记
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
