---
title: ffmpeg 使用小记
date: 2019-10-16 22:54:28
author: xujiaji
categories:
  - 笔记
tags:
  - 工具
  - FFMPEG
---

# ffmpeg 使用小记

## 合并两个视屏文件

合并`1.mp4`和`2.mp4`

> 将mp4转化为同样编码形式的ts溜，因为ts是可以concate的
> 然后concate ts流
> 最后再把ts流转为mp4

``` shell
ffmpeg -i 1.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb 1.ts
ffmpeg -i 2.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb 2.ts
ffmpeg -i "concat:1.ts|2.ts" -acodec copy -vcodec copy -absf aac_adtstoasc output.mp4
```
