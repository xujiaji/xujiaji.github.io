---
title: Git笔记
date: 2017-12-12 11:02:34
author: xujiaji
thumbnail: blog/git-notes.png
categories:
 - 工具
tags:
    - Git
    - 笔记
---

## 初始化git仓库
- 移动到需要初始化的目录
``` sh
$ git init
```
- 添加修改后的文件，或用“.”表示添加当前目录所有修改内容
``` sh
$ git add <文件>
```
- 提交修改了什么内容
``` sh
$ git commit -m "<内容>"
```

### 查看状态
- 查看当前版本库的状态，如：修改了什么文件，是否有需要添加或者提交的文件
``` sh
$ git status
```
- 查看修改前后的不同之处（difference）
``` sh
$ git diff
```
- 查看工作区和版本库里HEAD指向的版本（最新版本）有什么区别
```
$ git diff HEAD -- <文件>
```

## 版本回退
- 查看commit提交的日志，每个commit都有一串哈希值表示id
``` sh
$ git log
```
- 用一行信息来展示一次提交的信息（简化上面的展示）
``` sh
$ git log --pretty=oneline
```
- Git中，用`HEAD`表示当前版本，上个版本表示为`HEAD^`，上上版本就是`HEAD^^`...。也可直接指定，如往上100个版本：`HEAD~100`
``` sh
$ git reset --hard HEAD^
HEAD is now at ebeb505 add distributed
```
- 如果窗口还没关闭，还可以后悔。`7a19`是commit id的SHA1值开头，他会自动根据开头这几个字符去找
``` sh
$ git reset --hard 7a19
```
- 如果窗口关闭，那么也能后悔。查看你的历史命令的记录
``` sh
$ git reflog
```

## 撤销修改
- 如果还没有`git add`时想要撤销修改
``` sh
$ git checkout -- <文件>
```
- 如果`git add`了，想要撤销。先进行进行下面将文件从暂存区退回到工作区，然后在进行上面步骤。
``` sh
$ git reset HEAD <file>
```

## 删除文件
- 当删除文件后，需要更新版本库时。最后还需要commit提交
``` sh
$ git add/rm <file>
```

## 远程仓库
- 添加为本地仓库并联远程仓库
``` sh
$ git remote add origin xxx.git
```
- 删除已并联的远程库
``` sh
$ git remote rm origin
```
- 本地仓库并联多个远程仓库
``` sh
$ git remote rm origin
$ git remote add github git@github.com:xxx/xxx.git
$ git remote add gitee git@gitee.com:xxx/xxx.git
$ git remote -v
gitee    git@gitee.com:xxx/xxx.git (fetch)
gitee    git@gitee.com:xxx/xxx.git (push)
github    git@github.com:xxx/xxx.git (fetch)
github    git@github.com:xxx/xxx.git (push)

$ git push github master
$ git push gitee master
```
- 推送到远程仓库，第一次推送加上`-u`会把本地master分支和远程master分支并联起来，以后推送或拉取可简化命令
``` sh
$ git push -u origin master
```
- 查看远程仓库的名称，一般是origin，如果没有远程仓库则没有结果。
``` sh
$ git remote
```
- 查看更详细信息，如果没有推送权限则没有(push)标记的地址。
``` sh
$ git remote -v
```

## 设置用户信息
``` sh
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```
> 如果使用了 --global ，那么该命令只需要运行一次，因为之后无论你在该系统上做任何事情， Git 都会使用那些信息。
> 当你想针对特定项目使用不同的用户名称与邮件地址时，可以在那个项目目录下运行没有 --global 选项的命令来配置。

## 分支
- 查看本地分支
```
$ git branch
```
- 查看远程分支
```
$ git branch -a
```
- 创建分支1.1.2并切换到1.1.2分支
```
$ git checkout -b 1.1.2
```
- 拆分写法
```
$ git branch 1.1.2
$ git checkout 1.1.2
```
- 删除本地分支
```
$ git branch -d 1.1.2
```
- 把该分支上的所有本地提交推送到远程库（推送时，后面指定本地分支，这样git就会把该分支推送到远程库对应的远程分支上。）
``` sh
$ git push origin master
```
- 创建远程origin的dev分支到本地
``` sh
$ git checkout -b dev origin/dev
```
- 指定本地分支dev和远程origin/dev的链接
``` sh
$ git branch --set-upstream-to=origin/dev dev
```
- 推送本地分支到远程分支，远程分支不存在则创建
```
$ git push origin 1.1.2:1.1.2
```
- 本地分支留空则是删除远程分支
```
$ git push origin :1.1.2
```
- 合并work分支到当前分支
```
$ git merge work
```
- 合并分支时，git可能会用Fast forward模式。但这个模式下删除分支后会丢失分支信息。如要禁用Fast forward模式可在merge时`--no-ff`生成一个新的commit
``` sh
git merge --no-ff -m "<commit内容>" <分支>
```
- 强制删除分支
``` sh
$ git branch -D <分支名>
```
## 标签
- 创建标签，默认为`HEAD`，也可以指定一个commit id
``` sh
$ git tag <tagname>
$ git tag <tagname> <commit id>
```
- 创建带有说明的标签
``` sh
$ git tag -a <tagname> -m "<说明>" <commit id>
```
- 查看所有标签
``` sh
$ git tag
```
- 查看标签信息
``` sh
$ git show <tagname>
```
- 删除标签
``` sh
$ git tag -d <tagname>
```
- 推送某个标签到远程
``` sh
$ git push origin <tagname>
```
- 一次性推送全部尚未推送到远程的本地分支
``` sh
$ git push origin --tags
```
- 删除远程标签时，先删除本地，然后push，格式如下：
``` sh
$ git tag -d <tagname>
$ git push origin :refs/tags/<tagname>
```


## 解决冲突
- 当`git merge`发生冲突的时候
- 可先通过`git status`查看冲突的文件
- Git用`<<<<<<<`，`=======`，`>>>>>>>`标记出不同分支的内容我们修改后保存。
- 然后`git add`、`git commit -m`提交。
- 查看分支合并图
``` sh
$ git log --graph
$ git log --graph --pretty=oneline --abbrev-commit
```

## stash
- 临时需要处理其他分支任务的时候，可以将当前分支没完成的工作储藏起来。
``` sh
$ git stash
```
- 查看当前分支储藏
```
$ git stash list
stash@{0}: WIP on dev: 5e7a253 merge dev2 test
```
- 恢复储藏
    + 1.用`git stash apply`恢复，恢复后，stash内容并不删除，需要用`git stash drop`删除。
``` sh
$ git stash list
stash@{0}: WIP on dev: 5e7a253 merge dev2 test
$ git stash apply stash@{0}
$ git stash list
stash@{0}: WIP on dev: 5e7a253 merge dev2 test
$ git stash drop stash@{0}
Dropped stash@{0} (78fffa0577da9beb962a341cf13d74d9cfa148c6)
```
    + 2.用`git stash pop`恢复的同时删去stash
``` sh
$ git stash pop
```
## git pull和本地冲突
> 冲突log

``` sh
$ git pull
remote: Counting objects: 24, done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 24 (delta 7), reused 23 (delta 6), pack-reused 0
Unpacking objects: 100% (24/24), done.
From https://github.com/elmorec/hexo-theme-inside
   a98e719..3b64c8a  master     -> origin/master
error: Your local changes to the following files would be overwritten by merge:
        _config.yml
Please commit your changes or stash them before you merge.
Aborting
Updating a98e719..3b64c8a
```

> 1、用 `git stash`本地暂时保存起来

``` sh
$ git stash
Saved working directory and index state WIP on master: a98e719 update scripts
```

> 2、pull

> 3、还原`git stash pop stash@{0}`

``` sh
$ git stash pop stash@{0}
Auto-merging _config.yml
On branch master
Your branch is up-to-date with 'origin/master'.
```

## 克隆其他分支
> 如下所示，只克隆source分支

```
$ git clone -b source git@github.com:xujiaji/xujiaji.github.io.git
```

## 强制覆盖远程
```
git push -f
```

## 忽略特殊文件.gitignore
- 忽略python编译产生的`.pyc`、`.pyo`、dist等文件或目录
```
# Python:
*.py[cod]
*.so
*.egg
*.egg-info
dist
build
```

## 配置别名
> --global是针对当前用户起作用，如果不加只对当前仓库起作用

```
$ git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

$ git lg
```

- 配置文件位置：当前项目`.git/config`

- 当前用户的Git配置文件，在用户主目录的`.gitconfig`，配置别名可修改这个文件，也可删除用命令重新配置。
