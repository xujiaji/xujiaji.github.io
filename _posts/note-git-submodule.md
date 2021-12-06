---
title: Git子模块笔记
date: 2021-12-04 22:23:23
categories:
  - 笔记
tags:
  - Git
---

1. 添加子模块

添加flutter_together_ad仓库到当前项目的plugins目录下

``` shell
$ git submodule add https://github.com/xujiaji/flutter_together_ad.git plugins/flutter_together_ad
```

2. 查看子模块

``` shell
$ git submodule
 
4ff91a366b4673d60a9f426f639e6e3e5e9fdd39 plugins/flutter_together_ad (heads/main)
```

3. 更新子模块为远程最新

``` shell
git submodule update --remote
```

4. `.gitmodules`文件，添加`branch`指定分支

```
[submodule "plugins/flutter_together_ad"]
	path = plugins/flutter_together_ad
	url = https://github.com/xujiaji/flutter_together_ad.git
	branch = main
```