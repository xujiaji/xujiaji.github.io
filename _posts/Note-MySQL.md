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

## mac上的mysql连接错误

> 2059 - Authentication plugin 'caching_sha2_password' cannot be loaded:
> dlopen(../Frameworks/caching_sha2_password.so, 2): image not found

解决：

> 方法一

``` sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'yourpassword';
```

> 方法二

<https://www.jianshu.com/p/0be40c133926/>

## 设置表中值唯一

``` sql
ALTER TABLE `sec_user` ADD unique(`user_id`);
```

## mysql8添加账户

> 1.创建新用户

``` sql
create user 'username'@'host' identified by 'password';
```

其中username为自定义的用户名；host为登录域名，host为’%'时表示为 任意IP，为localhost时表示本机，或者填写指定的IP地址；paasword为密码

> 2.为用户授权

``` sql
grant all privileges on *.* to 'username'@'%' with grant option;
```

其中*.第一个表示所有数据库，第二个表示所有数据表，如果不想授权全部那就把对应的写成相应数据库或者数据表；username为指定的用户；%为该用户登录的域名

> 3.授权之后刷新权限

``` sql
flush privileges;
```
