---
title: python web 从Win部署到ubuntu小记
date: 2018-5-28 15:54:30
author: xujiaji
thumbnail:
categories:
 - Python
tags:
    - linux
    - python
    - 笔记
dropcap: true
---

本篇文章主要是用来记录我将python后台部署到amazon ec2服务器的全过程，以及一些坑坑洼洼。希望对有需要的朋友提供帮助，并且往后也好快速回忆。我的学习地址:[廖雪峰 实战 Day15-部署Web App](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014323392805925d5b69ddad514511bf0391fe2a0df2b0000)
<!-- more -->


## 注册并创建Amazon EC2实例
1. 首先需要创建一个账号，有12 个月的免费套餐访问权限。注册流程有点麻烦，需要添加信用卡，支付1美元来认证账号(•́へ•́╬)。然后验证码居然是打电话认证，电脑上会显示验证码，随后电话来了等她说完，手机输入验证码“#”结束。到此因该都注册成功了！
2. 找到EC2启动实例，创建一个ubuntu的实例，默认创建就OK了。
3. 创建结束会让你输入一个ssh密钥的名称，你输入一个邮箱之类的就行了，随后会帮你生成一个`.pem`的私密，下载下来放好咯！这玩意儿就相当于登录密码了。
4. 编辑安全组，添加22端口和80端口的访问权限
    - 在EC2管理界面将你创建的实例拉拉到最右边有个叫安全组的栏目，点进去![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//an_quan_zu1.png)
    - 进去后点击入站-编辑<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//an_quan_zu2.png)
    - 创建SSH入站规则，绑定自己的IP地址，第3步选了后会自动获取你的ip地址。如下图![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//an_quan_zu3.png)
    - 您还需要添加http 80端口，并且设置为任何位置都可访问，如下：![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//20180530103931.png)

## 连接到服务器
### 使用 PuTTY 连接到服务器
1. [下载并安装PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
2. 找到PuTTY安装目录，双击打开`puttygen.exe`
3. 加载之前您下载的`.pem`文件，需要转换一下私密格式![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//load_pem.png)
4. 点击save进行保存<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//save_key.png)![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//server_key2.png)
5. 打开PuTTY进行配置
    1. 配置SSH![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//load_ppk.png)
    2. 配置主机地址(ubuntu服务器地址前需要加上`ubuntu@`)，并保存配置。主机地址![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//server_address.png)
    3. 最后输入配置名称点击保存，下次就可以直接双击已配置好的选项直接进入。![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//server_config_save.png)
    4. 打开后也许也许你会发现进不去！这时你需要检查服务器`安全组`里是否添加SSH（如果最后也无法连接可把ssh来源改为任何位置试试），还有检查window防火墙是否开放22端口（可关闭防火墙试试，或在防火墙高级规则里面添加22端口访问）<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//cannot_in_server.png)

### WinSCP 管理服务器文件资源
1. [下载地址](https://winscp.net/eng/download.php)
2. 安装时会自动检测到PuTTY的配置，选择导入<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//install_winSCP.png)![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//install_winSCP2.png)
3. 直接选中你的站点登录就OK了。
4. 也许你会遇到没有权限无法创建文件的情况[winscp普通用户上传文件没有权限解决](https://blog.csdn.net/xuejinliang/article/details/52301349)

## 配置python web环境
> 接下来可以直接到这里去看部署过程了 [廖雪峰 Python Day 15 - 部署Web App](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014323392805925d5b69ddad514511bf0391fe2a0df2b0000)

1. 此时我们通过PuTTY登录服务器，我们输入python，会发现进入的是python2的版本![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//python_version1.png)
2. 我们需要安装python 3.6的版本，注意我们不要直接`apt-get install python3`，这样会直接安装成3.5的版本，然而aiomysql这个库不支持，折腾了许久。pip3也需要自己手动去安装的。
3. [Ubuntu16.04安装Python3.6 和pip](https://www.cnblogs.com/weiyiming007/p/9075986.html)
4. 安装`Nginx`丶`Supervisor`丶`MySQL`命令：`$ sudo apt-get install nginx supervisor mysql-server`
    - mysql安装的时候需要配置密码，密码得记好了
    - 编辑mysql配置文件设置utf8编码，输入命令：`vim /etc/mysql/my.cnf`
    - `i`进入输入模式，添加下面配置, `Esc`进入命令模式 `:wq`进行保存退出
    - 重启MySQL
```
[client]
default-character-set = utf8

[mysqld]
default-storage-engine = INNODB
character-set-server = utf8
collation-server = utf8_general_ci
```
5.将sql建数据库和表的配置文件传到服务器运行：`$ mysql -u root -p < schema.sql`<br>
6.通过Navicat连接服务器数据库，这里的配置就跟本地的配置一样的，密码就是数据库的密码。然后我们去配置SSH<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//navicat_config1.png)<br>ip地址就是之前我们在网页后台看到的地址，端口号默认的22，选择公钥验证，私密选择我们之前用`puttygen.exe`导出的`.ppk`文件，密码短语就是创建服务器后创建的密钥名称（可以在EC2网页后台看到密钥名称这一栏）<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//navicat_config2.png)<br>这下就爽了<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//navicat_config3.png)<br>
7.安装Web App用到的python库，命令：`$ sudo pip3 install jinja2 aiomysql aiohttp`

## 部署
1. 安装自动化部署工具Fabric，命令：`pip3 install fabric3`
2. 此处都可以去看[廖老师所讲的部署](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014323392805925d5b69ddad514511bf0391fe2a0df2b0000)，因为教程是安装的python2环境下的fabric所以在这里绕了很久。
3. 配置的时候我们配置验证的时候我们可以直接用ssh来进行验证，`env.hosts`就是之前我们配置PuTTY是的主机地址，`env.key_filename `就是我们下载的ssh私密`.pem`<br>![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy//fabric_config.png)
4. 我的`fabric`配置：`fabfile.py`
``` py
# fabfile.py
import os, re
from datetime import datetime

# 导入Fabric API:
from fabric.api import *


# 服务器登录用户名:
# env.user = 'ubuntu'
# sudo用户为root:
# env.sudo_user = 'ubuntu'
# 服务器地址，可以有多个，依次部署:
env.hosts = ['ubuntu@ec2-18-220-216-89.us-east-2.compute.amazonaws.com']
env.key_filename = '~/.ssh/jiajixuqqcom.pem'
# env.ssh_config_path = '~/.ssh/config'
# env.use_ssh_config = True

# 服务器MySQL用户名和口令:
db_user = 'root'
db_password = '6Sb8qzM38'

_TAR_FILE = 'dist-awesome.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'


def touchfile():                         # 随便创建一个任务，用来测试
    run('touch /tmp/www.txt')


def deploy():
    newdir = 'www-%s' % _now()
    # 删除已有的tar文件:
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件:
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # 解压到新目录:
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
        # 需要添加权限浏览器才能访问
        sudo('chmod -R 775 static/')
        sudo('chmod 775 favicon.ico')
        # 由于app.py的文件格式有问题，转换一下
        run('dos2unix app.py')
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown ubuntu:ubuntu www')
        sudo('chown -R ubuntu:ubuntu %s' % newdir)
    # 重启Python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx reload')


def build():
    includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))
```

## 添加https
添加这个的原因嘛！就不加多少的啦！来看如何如何做吧！
1. 我是在阿里云上面找的一个免费版，可以在这里找到，进去后点击立即购买![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy/aliyun_ac1.png)
2. 选择免费类型，如下操作![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy/aliyun_ac2.png)
3. 然后就是需要填写一些您的个人信息和需要绑定的域名，比如我绑定：`www.xujiaji.com`，提交审核。（此时可能需要等个半个来小时审核）
4. 点击下载![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy/aliyun_ac_3.png)
5. 点击下载证书for Nginx，然后将压缩包解压得到两个文件。我们将这两个文件放到如下位置，`/ect/nginx/`是服务器nginx的安装目录，`cert`是新建的目录，就放这里面![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy/config_https1.png)
6. 然后我们编辑`/etc/nginx/sites-available/awesome`，我们将这些东西直接拷贝过来![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/python-web-deploy/config_https2.png)
7. 重启nginx：`sudo /etc/init.d/nginx reload`
8. 配置完成后您可能还是无法访问https（我就在这纠结了半天），注意需要在服务器安全组添加所有用户对`443`端口的访问权限。
9. 下面是我的nginx整体配置代码，含义请看注释
```
server {
    # 监听80端口，作用是将用户http的请求转发到https
    listen      80;
    # 绑定的域名
    server_name www.xujiaji.com;
    rewrite ^(.*)$  https://www.xujiaji.com permanent;
}


server {
    #listen      80;
    # 下面这部分就是从阿里云下载AC认证那里直接拷贝过来的配置
    listen 443;
    ssl on;
    ssl_certificate   cert/214731123750166.pem;
    ssl_certificate_key  cert/214731123750166.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;    

    # 代理的服务器根目录 日志
    root       /srv/awesome/www;
    access_log /srv/awesome/log/access_log;
    error_log  /srv/awesome/log/error_log;

    server_name www.xujiaji.com;

    client_max_body_size 1m;

    gzip            on;
    gzip_min_length 1024;
    gzip_buffers    4 8k;
    gzip_types      text/css application/x-javascript application/json;

    sendfile on;

    location /favicon.ico {
        root /srv/awesome/www;
    }

    location ~ ^\/static\/.*$ {
        root /srv/awesome/www;
    }

    location / {
        proxy_pass       http://127.0.0.1:9000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
```
