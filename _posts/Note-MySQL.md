---
title: MySQL相关笔记
date: 2020-04-17 12:03:06
updated: 2020-04-17 12:03:06
thumbnail: blog/mysql/mysql-logo.jpg
tags:
 - MySQL
---

# MySQL笔记

## 解决在mysql表中删除自增id数据后，再添加数据时不会接着自增

在删除自增列表的数据后，执行下面的语句`table_name`替换成对应的表明

``` mysql
ALTER TABLE table_name AUTO_INCREMENT = 1;
```

## 集合差运算

查询表bz_connection的id，cidnumber
查询表bz_member的idnumber
bz_connection的cidnumber和bz_member的idnumber要一样
条件：合并后bz_member的idnumber不为空

``` mysql
select id, cidnumber FROM bz_connection LEFT JOIN
(select idnumber as i from bz_member) as t1
ON bz_connection.cidnumber=t1.i where t1.i IS NULL
```

## 查询某个字段的值在集合内所有数据

``` mysql
SELECT * FROM bz_connection WHERE id IN (102, 125, 139, 154)
```
