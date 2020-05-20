---
title: Docker笔记
date: 2020-05-20 10:59:12
categories:
 - 工具
tags:
 - 笔记
 - Docker
---

# Docker

## Docker 常用命令

1. 镜像相关
    * `docker pull <image>`
    * `docker search <image>`
2. 容器相关
    * `docker run`
    * `docker start/stop <容器名>`
    * `docker ps <容器名>`
    * `docker logs <容器名>`

## docker run的常用选项

``` shell
docker run [OPTIONS] IMAGE [COMMAND][ARG...]
```

1. 选项说明【OPTIONS】
    * `-d` 后台运行容器
    * `-e` 设置环境变量
    * `--expose / -p` 宿主端口：容器端口
    * `--name` 指定容器名称
    * `--link` 链接不同容器
    * `-v` 宿主目录：容器目录，挂载磁盘卷

## mongo笔记

> 安装

``` sh
$ docker pull mongo
Using default tag: latest
latest: Pulling from library/mongo
...
Digest: sha256:c880f6b56f443bb4d01baa759883228cd84fa8d78fa1a36001d1c0a0712b5a07
Status: Downloaded newer image for mongo:latest
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mongo               latest              3f3daf863757        3 weeks ago         388MB
$ docker run --name mongo -p 27017:27017 -v ~/docker-data/mongo:/data/db -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin -d mongo
9e69527dd1b69cb4cc4eec1ec0ec2a1767b56257d6513e417004f093f5aaf3e8
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
9e69527dd1b6        mongo               "docker-entrypoint.s…"   6 seconds ago       Up 5 seconds        0.0.0.0:27017->27017/tcp   mongo
```

> 登录到MongoDB容器中

$ docker exec -it mongo bash

> 通过shell连接MongoDB

$ mongo -u admin -p admin

> 创建库

$ use springbucks;

> 创建用户

``` sh
$ db.createUser(
    {
      user: "springbucks",
      pwd: "springbucks",
      roles: [
        { role: "readWrite", db: "springbucks" }
      ]
    }
  );
```

> 显示表

``` sh
$ show collections;
coffee
```

> 查看数据

``` sh
$ db.coffee.find();
{ "_id" : ObjectId("5ec4d3a3660d054f0edc5d2f"), "name" : "espresso", "price" : { "money" : { "currency" : { "code" : "CNY", "numericCode" : 156, "decimalPlaces" : 2 }, "amount" : "20.00" } }, "createTime" : ISODate("2020-05-20T06:52:19.557Z"), "updateTime" : ISODate("2020-05-20T06:52:19.557Z"), "_class" : "geektime.spring.data.mongodemo.model.Coffee" }
```

> 通过名字删除数据

``` sh
> db.coffee.remove({"name":"espresso"});
WriteResult({ "nRemoved" : 1 })
```

## Redis笔记

> 获取镜像

$ docker pull redis

> 启动Redis

$ docker run --name redis -d -p 6379:6379 redis
