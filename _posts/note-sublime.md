---
title: Sublime笔记
date: 2022-04-26 13:58:35
categories: 
 - 笔记
tags:
 - Sublime
---

## 显示出Tab键和空格在文本中的区别

由于代码对格式要求严格，不显示出来又看不出区别

> 设置中（Preferences/Settings）添加`"draw_white_space":"all"`

修改后配置

``` json
{
	"font_size": 13,
	// "ignored_packages":
	// [
	// 	"Markdown",
	// 	"Vintage",
	// ],
	"ignored_packages":[
		"Markdown",
	],
	"theme": "Adaptive.sublime-theme",
	"color_scheme": "Mariana.sublime-color-scheme",
	"draw_white_space":"all"
}
```

## 把tab后四个空格改为tab`\r`

> View -> Indentation -> Indent Use Spaces