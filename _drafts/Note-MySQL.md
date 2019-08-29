---
title: MySQL相关笔记
tags:
---

# MySQL笔记

## 解决在mysql表中删除自增id数据后，再添加数据时不会接着自增

在删除自增列表的数据后，执行下面的语句`table_name`替换成对应的表明

``` mysql
ALTER TABLE table_name AUTO_INCREMENT = 1;
```
