---
title: 安装Gitlab小记
date: 2019-09-24 20:49:42
author: xujiaji
thumbnail: blog/gitlab/gitlab-logo-gray-rgb.jpg
tags:
 - Linux
 - CentOS
 - Git
---

# 安装Gitlab小记

> 环境：CentOS7.6、外部Nginx

## 做了些什么？

1. 安装gitlab
2. 配置发送邮箱（用来验证账号修改密码）
3. 外置nginx配置（https）
4. 汉化
5. CI Pipelines安装

## 安装Gitlab

安装配合依赖（其实这里都是官网的安装说文档，我就直接搬运过来了）

``` shell
sudo yum install -y curl policycoreutils-python openssh-server
sudo systemctl enable sshd
sudo systemctl start sshd

sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo systemctl reload firewalld
```

添加Gitlab仓库

``` shell
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash
```

安装Gitlab，这里的`EXTERNAL_URL`换成自己的域名

``` shell
sudo EXTERNAL_URL="https://gitlab.example.com" yum install -y gitlab-ee
```

## 配置邮箱（不配置可以跳过这个步骤）

打开配置文件，添加邮箱配置。

这里以qq邮箱来举栗子（因为我配置的qq邮箱😆），其他都差不多类似。

注意需要在邮箱设置中开启smtp服务

``` shell
vim /etc/gitlab/gitlab.rb
```

> 直接在文件中添加下方配置

``` shell
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.qq.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "邮箱名@qq.com"
gitlab_rails['smtp_password'] = "dtjhinszpsasdhi"
gitlab_rails['smtp_domain'] = "smtp.qq.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = true
```

|字段|说明|
|-|-|
|`smtp_enable`|启用smtp|
|`smtp_address`|smtp.qq.com是qq的smtp服务器，根据自己的情况更换|
|`smtp_user_name`|是你要用来让gitlab发送的邮箱|
|`smtp_password`|是邮箱的登录密码（QQ的是在设置中生成的第三方登录密码）|
|`smtp_tls`|开启tls加密|

配置邮箱来源，与展示的名称

``` shell
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = '邮箱名@qq.com'
gitlab_rails['gitlab_email_display_name'] = '发送邮件的默认标题'
```

## 外置nginx配置

### 关闭Gilab内部nginx和一些其他配置

打开配置文件

``` shell
vim /etc/gitlab/gitlab.rb
```

添加如下配置

``` shell
external_url 'https://git.longpuji.com'

gitlab_workhorse['enable'] = true
gitlab_workhorse['listen_network'] = "tcp"
gitlab_workhorse['listen_addr'] = "127.0.0.1:8181"

# This example renews every 7th day at 12:30
letsencrypt['auto_renew_hour'] = "12"
letsencrypt['auto_renew_minute'] = "30"
letsencrypt['auto_renew_day_of_month'] = "*/7"

nginx['enable'] = false
```

|字段|说明|
|-|-|
|`external_url`|外部的url使用的url，如果不配置会导致有些链接不正常|
|`gitlab_workhorse['enable']`|开启gitlab工作空间配置|
|`gitlab_workhorse['listen_network']`|tcp网络协议|
|`gitlab_workhorse['listen_addr']`|`127.0.0.1:8181`（一会儿nginx反向代理的时候就用这个端口号）|
|`nginx['enable']`|关闭Gitlab内部nginx|

### 为外部nginx反向代理配置

配置如下

``` shell
location /
{
    expires 12h;
    if ($request_uri ~* "(php|jsp|cgi|asp|aspx)")
    {
         expires 0;
    }
    # 这个就是上面设置的gitlab_workhorse['listen_addr']
    proxy_pass http://127.0.0.1:8181;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header REMOTE-HOST $remote_addr;
    # 注意如果是域名配置了ssl，那么则必须加上这个配置，不然gitlab会在重置密码的时候报错422
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Ssl on;

    proxy_read_timeout                  900;
    proxy_cache off;
    proxy_buffering off;
    proxy_request_buffering off;
    proxy_http_version 1.1;

    add_header X-Cache $upstream_cache_status;
    add_header Cache-Control no-cache;
}
```

## 启动

> 上面的那些基本上Gitlab就已经配置好啦，现在需要对Gitlab重新加载配置和重启

重载配置

``` shell
gitlab-ctl reconfigure
```

重启服务

``` shell
gitlab-ctl start
```

到这里可以打开域名链接去看看，没有啥问题就可以正常使用，第一次进入的时候需要设置初始密码。
初始的账号是`root`
去登陆试试吧

## 汉化

查看当前版本

``` shell
cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
```

输出

``` shell
12.3.0-ee
```

> 由于汉化现在还没有支持到这么高的版本，于是这里以v12.2.4的版本汉化的。（大部分都没有被汉化😅，之后如果该仓库更新的对应版本可以再次尝试）

clone汉化项目

``` shell
git clone https://gitlab.com/xhang/gitlab.git
```

进入仓库

``` shell
cd gitlab
```

备份`gitlab-rails`到当前目录（如果之后出现问题，方便恢复）

``` shell
cp -rf /opt/gitlab/embedded/service/gitlab-rails/ .
```

生成12.2.4版本的汉化补丁

``` shell
git diff v12.2.4 v12.2.4-zh > ./12.2.4-zh.diff
```

关闭gitlab服务

``` shell
gitlab-ctl stop
```

打汉化补丁

``` shell
patch -d /opt/gitlab/embedded/service/gitlab-rails/ -p1 < ./12.2.4-zh.diff
```

> 这里有些汉化文件没有对应到的文件，直接回车，yes跳过就可以了

启动服务

``` shell
gitlab-ctl start
```

## CI Pipelines安装

这篇文件不错，我就不啰嗦了哈哈

<https://scarletsky.github.io/2016/07/29/use-gitlab-ci-for-continuous-integration/>

## 命令文件整理

> 命令整理

|命令|说明|
|-|-|
|`gitlab-ctl reconfigure`|重载gitlab配置|
|`gitlab-ctl restart`|重启gitlab|
|`gitlab-ctl stop`|停止gitlab服务|
|`gitlab-ctl start`|启动gitlab服务|

> 文件说明

|文件|说明|
|-|-|
|`/etc/gitlab/gitlab.rb`|gitlab配置文件|
|`/var/log/gitlab/gitlab-rails/production.log`|gitlab-rails日志文件|

## 备份

备份命令

``` shell
gitlab-rake gitlab:backup:create
```

安装同版本gitlab

从其他服务器拷贝到当前服务器

``` shell
scp root@172.28.17.155:/var/opt/gitlab/backups/1502357536_2017_08_10_9.4.3_gitlab_backup.tar /var/opt/gitlab/backups/
```

余下步骤参阅：https://blog.csdn.net/ouyang_peng/article/details/77070977

### 恢复备份后ci 500错误问题

Rails console

``` shell
gitlab-rails console
```

重置token

``` shell
Project.find_by_full_path('root/my-project').update(runners_token: nil, runners_token_encrypted:nil)
```

> 如果上面步骤不行，查看下面问题

DB Console

``` shell
gitlab-psql -d gitlabhq_production
```

查看数据库信息

``` sql
select id,runners_token,runners_token_encrypted from projects;
```

重置数据token

``` sql
UPDATE projects SET runners_token = null, runners_token_encrypted = null WHERE id = 28;
```
