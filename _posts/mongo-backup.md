---
title: MongoDB数据备份
date: 2022-04-20 11:42:17
categories:
 - MongoDB
tags:
	- MongoDB
---

## 数据导出
``` shell
mongodump -h dbhost -d dbname -o dbdirectory
```
- `-h` MongoDB所在服务器地址
- `-d` 需要备份的数据库实例
- `-o` 备份打哪个目录

> `mongodump -d yapi -o /www/backup`

备份yapi数据库实例到`/www/backup`

## 数据导入
``` shell
mongorestore -h dbhost -d dbname --drop --dir backupdirectory
```
- `-h` MongoDB所在服务器地址
- `-d` 需要导入的数据库实例
- `--drop` 恢复的时候，先删除当前数据，然后恢复备份的数据
- `--dir` 指定备份的目录

> `mongorestore -d yapi --drop /www/backup/yapi`

导入备份目录`/www/backup/yapi`到yapi数据库实例，同时删除当前已有数据