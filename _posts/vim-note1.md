---
title: VIM爬坡到半山腰的总结
date: 2016-11-30 09:43
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/home.png
categories:
 - 笔记
tags:
    - linux
    - vim
    - 笔记
---
![banner](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/banner.png)

## 简介
将Linux Mint做为我的主系统后，来来回回到处撞墙。慢慢的到现在不仅习惯了Linux下的娱乐和开发，居然还渐渐的顺手顺眼起来，对于Linux生存有了保障的我现在对Linux下的`VIM`开始好奇了。

虽听说VIM乃是上古神器，但一直以来对于VIM映像只有黑不溜秋的界面、白晃晃的文字，只知道从命令界面进去后可以点击`i`进入文本编辑模式、上下左右箭头移动光标、修改完成后`Ese`然后`:wq`保存退出、走人。总的来说不想撩你，怕惹祸上身，最终精尽人亡（精神的精）。

这到现在都没面试，哎！手里闲不住，前几天开始对VIM开始下手了，胆颤心惊的先去网上秋秋别人的VIM长啥样啊！谷歌直接搜图片吧！（我已做好随时逝去）。这一看，瓦特？vim可以分屏？这个人的vim界面还有目录？这GIT分支结构侧边栏怎么都来了？为什么左侧还有代码行号？这些人的代码高亮的这么好看？最下面的那行漂亮的状态栏我咋过没有？我瞬间就被这些人的界面给吸引住了，我感觉我从农村第一次来到城市。

就这样我走上了撩VIM之路（我有Java精神我不怕，万物皆对象），到现在我已经将上面看到的目录结构弄出来、代码行号、代码高亮主题更换、状态栏显示、VIM中使用GIT等加入到我的VIM之中。从中我了解到了VIM的插件放哪、怎么配置插件，学习了一波基本命令助我前行。我认为写代码最主要的就是要先有个安心、悦目的环境，然后是快捷的操作，这样写代码会感觉很舒服。当然，还有就是提升了一个格调，集齐技术、快捷、装逼、高效与一身。

下图是我当前的VIM界面截图，是不是有鼻子有眼了。
![This is my vim.](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/my-vim.png)

## 有想要到达的方向，一切的困难不过是个过程

### 我从这里开始入门
先为您献上链接：
[世界上最牛的编辑器： Vim 1 (原创动图演示所有例子!)](http://www.imooc.com/article/13269)
[世界上最牛的编辑器： Vim 2 (原创动图演示所有例子!)](http://www.imooc.com/article/13272)
[世界上最牛的编辑器： Vim 3 (原创动图演示所有例子!)](http://www.imooc.com/article/13275)

当这三篇看完后，可以了解到VIM的基本操作，可以安装一些插件（其实我也只是用到了里面的几个插件，其他没用的先不管吧！）。虽然现在你是不明不白的安装了一些插件，但重在先体验体验VIM的感觉。

这里我想要补充一下(因为我是用的Linux，其他系统原谅我没了解)：
`.vimrc`就是vim的配置文件
`.vim/bundle`目录下放的都是插件，可以直接将Github插件`git clone`（下载到）这个目录。

`.vim/bundle/vundle`
1. 如果您下载了上面教程的`.vim`里面会有这个目录，这个插件可以在Github搜索然后更新一下。
2. 如果是Github上可下载的插件就不用亲自去克隆下来了，直接在`.vimrc`添加如：`Plugin 'majutsushi/tagbar'`（Github地址是：`htttps://github.com/majutsushi/tagbar`），直接取后面一部分就行了。
3. 最后打开终端输入`vim`回车，进入Vim。然后，输入命令`:PluginInstall`就会将所有的第二步这种形式的插件自动下载下来。

### 从这里开始明白了Vim插件管理，如何配置
还是先敬上链接：
[不要在害怕Vim](http://bhilburn.org/stop-being-scared-of-vim/)

当然我的英语水平是个渣渣，越来越不得不多学学English了。看了了大概，总体上面是介绍，下面是实际的一些例子。有预览图，理解起来还是比较轻松。里面介绍了一个Vim游戏http://vim-adventures.com/ ，挺有意思了玩到三关之后要money，20多美元解锁，屌丝的我只能干望着了。

这里简单说一下我装了的里面提及的几个：
[fugitive](https://github.com/tpope/vim-fugitive)：可以在Vim中对项目进行Git命令操作。
[gundo](https://github.com/sjl/gundo.vim)：查看提交以树行结构展示（请看下图）
![gundo](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/gundo.jpg)
[nerdtree](https://github.com/scrooloose/nerdtree)：展示目录结构，看起比使用`:Ve`展示的目录爽多了。（请看下图）
![nerdtree](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/nerdtree.png)
[powerline](https://github.com/Lokaltog/powerline)：底部状态栏，这个可是把我给折腾够了，不过弄完之后，瞬间展示效果杠杠的。
![powerline](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/powerline.png)

>还是简单记录一下我的历程吧！

一开始我以为和其他插件一样，直接在`.vimrc`中添加`Plugin 'Lokaltog/powerline'`然后在Vim中`:PluginInstall`，Very Good搞定。其实不然，根本就可以不需要往`.vim/bundle`中添加，需要配置python，需要在`.vimrc`中配置。

通过这篇文章：[为Bash和VIM配置一个美观奢华的状态提示栏](http://www.hi-linux.com/2016/04/22/%E4%B8%BABash%E5%92%8CVIM%E9%85%8D%E7%BD%AE%E4%B8%80%E4%B8%AA%E7%BE%8E%E8%A7%82%E5%A5%A2%E5%8D%8E%E7%9A%84%E7%8A%B6%E6%80%81%E6%8F%90%E7%A4%BA%E6%A0%8F/)
我不仅仅将Vim给加上了状态栏，命令界面的用户状态也变了，我把默认的字体改成powerline的字体，更加美观。先欣赏一下：

![My termina](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/termina.png)

我的步骤：
1. 安装python-pip 与 git 套件
```
sudo apt-get install python-pip git
```
2. 使用pip安装Powerline
```
pip install --user powerline-status
```
3. 字体配置（如果没有这字体，那么Powerline的那些符号我的会显示乱码）
```
$ git clone https://github.com/powerline/fonts.git
$ cd fonts
$ ./install.sh
```
4. 配置环境，打开`.bashrc`，添加如下信息。
```
export TERM="screen-256color"
export PATH="$HOME/.local/bin:$PATH"
export POWERLINE_COMMAND=powerline
export POWERLINE_CONFIG_COMMAND=powerline-config
powerline-daemon -q
POWERLINE_BASH_CONTINUATION=1
POWERLINE_BASH_SELECT=1
. ~/.local/lib/python2.7/site-packages/powerline/bindings/bash/powerline.sh
```
第二行是加入powerline的命令位置，下图是查看位置。
![查看powerline命令位置](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/powerline-position.png)
最下面的一行是安装powerline后的路径`. ~/.local/lib/python2.7/site-packages/powerline`可能大家会有所不同。（再执行第二步你会看到安装位置哦，如下图）
![查看powerline的安装位置](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/powerline-position2.png)
5. 选择字体，此时您应该已经可以在命令中中显示如上图的状态了，只是默字体可能无法显示其真正效果。`Edit > Preferences`看下图：我直接搜索选择了`powerline semi`
![选择字体操作](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/vim-1/choose-font.png)
6. 最终目的不要忘了，是配置Vim啊！
此时只需要在`.vimrc`中添加如下信息即可：（第一行为powerline目录）
```
set rtp+=~/.local/lib/python2.7/site-packages/powerline/bindings/vim/
set guifont=Sauce\ Code\ Powerline:h14.5
set laststatus=2
set encoding=utf-8
set t_Co=256
set number
set fillchars+=stl:\ ,stlnc:\
set term=xterm-256color
set termencoding=utf-8
set background=dark
```
7. 重启Vim看看，是不是搞定了！

> 最后献上一个我现在用的主题

[gruvbox](https://github.com/morhetz/gruvbox)

配置.vimrc
```
Plugin 'morhetz/gruvbox'
colorscheme gruvbox
set background=light
set background=dark
```
在Vim中下载
```
:PluginInstall
```


> 好了就到这里，其他插件看个人需求添加，都是大同小异的了。

## 总结结束
在放几个网址在这里：
[Vim Cheat Sheet](http://vim.rtorr.com/) : 多种语音查看Vim命令
[vimcolors](http://vimcolors.com/) : 很多的Vim配色
[[AndroidStudio-------IdeaVim插件](http://blog.csdn.net/ly0303521/article/details/50761365)](http://blog.csdn.net/ly0303521/article/details/50761365)

> 从现在开启Vim神器功能，进入无尽的砍怪之旅吧！

---

Github：[@xujiaji](https://github.com/xujiaji)
> 本文是我开始VIM爬到半山坡后的总结！什么半山坡啊！装B，其实就是刚刚个入了门，哈哈。
> 如有欠妥之处还望给予指正，如有什么Vim淫巧还望推荐，谢谢！
