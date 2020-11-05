---
title: C 学习笔记
date: 2018-12-25 23:18:45
author: xujiaji
categories:
 - C
tags:
 - C
 - 笔记
 - 学习
---

重学一次C语言，记录一下学习《C Primer Plus》的笔记，方便回忆！

<!-- more -->

## 编译

```
gcc -o foo.exe foo.c -lregex
gcc foo.c -o foo.exe -lregex
```

## 字符串和格式化输入/输出
1. 字符串以`char`数组来存储
2. 常量用 `#define` 定义
``` c
#define DENSITY 62.4
```
3. `strlen()`获取字符串的长度，注意需要`#include <string.h>`
4. `char`类型数组和`null`字符
 1. C语言没有专门用于储存字符串的变量类型，字符串都被储存在`char`类型的数组中
 2. 字符串以`\0`（空字符）结束，它是不打印出来的字符
 3. 如果有40哥存储单单元的字符串，只能储存39哥字符，剩下一个字节留给空字符
5. 一下代码`%s`作为转化说明，`scanf()`只会读取字符串中的一个单词。并且没有加`&`取地址符，`name`就是地址
``` c
char name[40];
scanf("%s", name);
```
6. `"x"`不同于`'x'`,`"x"`是字符串由`x`和`\0`组成
7. `sizeof`运算符，它以字节为单位给出对象的大小。`strlen()`只给出字符串长度，到空字符（不包括空字符）
 1. C99和C11标准专门为`sizeof`运算符的返回类型添加了`%zd`转换说明，对于`strlen()`也适用
 2. `sizeof`使用时，对于类型必须加括号。对于特定量，可有可无。类型：`sizeof(char)`, `sizeof(float)`; 特定量：`sizeof 6.28`, `sizeof name`

## 常量和C预处理器
1. C预处理器定义常量：`#define NAME value`，其中“NAME”为命令的常量名，约定大写；“value”是对应的值
``` swift
#define BEEP '\a'
#define TEE 'T'
#define ESC '\033'
#define OOPS "Now you have done it!"
```
2. `const`限定符，C90标准新增该关键字，用于限定一个变量为只读
3. 明示常量：C头文件`limits.h`和`float.h`分别提供了与整数类型和浮点数类型大小限制相关的详细信息
``` Swift
#include <stdio.h>
#include <limits.h>
#include <float.h>

int main()
{
    printf("Some number limits for this system: \n");
    printf("Biggest int: %d\n", INT_MAX);
    printf("Smallest long long: %lld\n", LLONG_MIN);
    return 0;
}
```
