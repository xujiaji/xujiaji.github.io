---
title: Flutter SDK放在exFAT文件系统无法执行
date: 2021-12-16 22:46:58
categories:
  - Flutter
tags:
  - Issues
  - Flutter
---

shlock .upgrade_lock fails on exFAT file system: shlock not supported 

原因：由于电脑硬盘空间不足，于是把Flutter SDK放到了移动硬盘，移动硬盘是exFAT的文件系统，于是就出现了这个错误

<!-- more -->

解决参考链接：https://github.com/flutter/flutter/issues/53016

1、在flutterSDK的目录全局搜索字符串：`FLUTTER_UPGRADE_LOCK`

我的搜索在`<flutter root>/bin/internal/shared.sh`中

2、
将
``` shell
FLUTTER_UPGRADE_LOCK="$FLUTTER_ROOT/bin/cache/.upgrade_lock"
```

修改成
``` shell
FLUTTER_UPGRADE_LOCK="$TMPDIR/.upgrade_lock"
```
