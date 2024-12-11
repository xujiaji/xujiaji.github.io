---
title: GPG使用笔记
date: 2024-12-11 15:22:16
categories:
 - 笔记
tags:
 - gpg
---

> 生成

``` sh
gpg --gen-key
```

> 列出所有gpg

``` sh
gpg --list-keys
```

> 上传公钥到公共服务器,后面为公钥的摘要信息，创建后和`--list-keys`都可以看到

``` sh
gpg --keyserver keyserver.ubuntu.com --send-keys XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

中央服务器当前支持的 GPG 密钥服务器有：

```
keyserver.ubuntu.com
keys.openpgp.org
pgp.mit.edu
```

发送完需要验证是否成功（如果失败等待片刻再试，或重新上传）

``` sh
gpg --keyserver keyserver.ubuntu.com --recv-keys XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> 导出公钥证书

``` sh
gpg --armor --export XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> 导出私钥证书

``` sh
gpg -a --export-secret-keys XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```