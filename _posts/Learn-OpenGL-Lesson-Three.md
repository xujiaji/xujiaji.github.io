---
title: OpenGL Android课程三：使用每片段照明
date: 2019-01-26 17:55:49
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/Screenshot_2019-02-07-13-45-15-213_com.xujiaji.le.png
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---
> 翻译文

原文标题：Android Lesson Three: Moving to Per-Fragment Lighting
原文链接：http://www.learnopengles.com/android-lesson-three-moving-to-per-fragment-lighting/
<!-- more -->

---

|||
|-|-|
|欢迎来到第三课！这节课，我们将会在[第二课][2]的基础上，<br>学习如何使用每像素技术来达到相同的照明。<br>简单的正方体即使使用标准的漫射照明我们也能看到差异。|![][1]|



## 前提条件
本系列的每节课都以前面的课程为基础，本节课是[第二课][2]的补充，因此请务在阅读了之前的课程后再来回顾。

> 下面是本系列课程的前几课：

- [OpenGL Android课程一：入门][3]
- [OpenGL Android课程二：环境光和漫射光][2]

## 什么是每像素照明
随着着色器的使用，每像素照明在游戏中是一种相对较新的现象。许多有名的旧游戏，例如原版的[半条命][4]，都是在着色器之前开发出来的，主要使用静态照明，通过一些技巧模拟动态照明，使用每顶点（也称为[Gouraud阴影][5]）照明或其他技术，如动态[光照贴图][6]。

光照贴图可以提供非常好的效果，有时可以比单独的着色器提供更好的效果，因为可以预先计算昂贵的光线计算。但缺点是它们占用了大量内存并使用它们进行动态照明仅限于简单的计算。

使用着色器，现在很多这些计算转给GPU，这可以完成更多实时的效果。

## 从每顶点照明转移到每片段照明
这本课中，我们将针对每顶点解决方案和每片段解决方案查看相同的照明代码。尽管我将这种类型称为每像素，但在OpenGL ES中我们实际上使用片段，并且几个片段可以贡献一个像素的最终值。

手机的GPU变得越来越快，但是性能仍然是一个问题。对于“软”照明例如地形，每顶点照明可能足够好。确保您在质量和速度之间取得适当的平衡。

在某些情况下可以看到两种类型的照明之间的显著差异。看看下面的屏幕截图：

||||
|-|-|-|
|![][7]<br>每顶点照明；<br>在正方形四个顶点为中心|![][8]<br>每片段照明；<br>在正方形四个顶点为中心|在左图的每顶点照明中正方体的<br>正面看起来像是平面阴影，不能<br>表明附近有光源。这是因为正面<br>的四个顶点和光源距离差不多相<br>等，并且四个点的低光强度被简<br>单的插入两个三角形构成的正面。<hr>相对比，每片段照明很好的<br>显示了亮点特性|
|![][9]<br>每顶点照明；<br>在正方形角落|![][10]<br>每片段照明；<br>在正方形角落|左图显示了一个[Gouraud阴影][5]<br>立方体。当光源移动到立方体正<br>面角落时，可以看到类似三角形<br>的效果。这是因为正面实际上是<br>由两个三角形组成，并且在每个<br>三角形不同方向插值，我们能看<br>到构成立方体的基础几何图形。<hr>每片段的版本显示上没有此类插<br>值的问题并且它在边缘附近显示<br>了一个漂亮的圆形高光。|

### 每顶点照明概述
我们来看看[第二课][2]讲的着色器；在该课程中可以找到详细的着色器说明。

### 顶点着色器

``` glsl
uniform mat4 u_MVPMatrix;      // 一个表示组合model、view、projection矩阵的常量
uniform mat4 u_MVMatrix;       // 一个表示组合model、view矩阵的常量
uniform vec3 u_LightPos;       // 光源在眼睛空间的位置

attribute vec4 a_Position;     // 我们将要传入的每个顶点的位置信息
attribute vec4 a_Color;        // 我们将要传入的每个顶点的颜色信息
attribute vec3 a_Normal;       // 我们将要传入的每个顶点的法线信息

varying vec4 v_Color;          // 这将被传入片段着色器

void main()                    // 顶点着色器入口
{                              
// 将顶点转换成眼睛空间
   vec3 modelViewVertex = vec3(u_MVMatrix * a_Position);                
// 将法线的方向转换成眼睛空间
   vec3 modelViewNormal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));       
// 将用于哀减
   float distance = length(u_LightPos - modelViewVertex);               
// 获取从光源到顶点方向的光线向量
   vec3 lightVector = normalize(u_LightPos - modelViewVertex);          
// 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
   float diffuse = max(dot(modelViewNormal, lightVector), 0.1);         
// 根据距离哀减光线
   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));    
// 将颜色乘以亮度，它将被插入三角形中
   v_Color = a_Color * diffuse;                                         
// gl_Position是一个特殊的变量用来存储最终的位置
// 将顶点乘以矩阵得到标准化屏幕坐标的最终点
   gl_Position = u_MVPMatrix * a_Position;                              
}                                              
```

### 片段着色器
``` glsl
precision mediump float;     // 我们将默认精度设置为中等，我们不需要片段着色器中的高精度
varying vec4 v_Color;        // 这是从三角形每个片段内插的顶点着色器的颜色
void main()                  // 片段着色器入口
{                            
   gl_FragColor = v_Color;   // 直接将颜色传递
}                            
```

正如您所见，大部分工作都在我们的着色器中做的。转移到每片段着色照明意味着，我们的片段着色器还有更多的工作要做。

### 实现每片段照明
以下是移动到每片段照明后的代码的样子。

### 顶点着色器
``` glsl
uniform mat4 u_MVPMatrix;    // 一个表示组合model、view、projection矩阵的常量
uniform mat4 u_MVMatrix;     // 一个表示组合model、view矩阵的常量

attribute vec4 a_Position;   // 我们将要传入的每个顶点的位置信息
attribute vec4 a_Color;      // 我们将要传入的每个顶点的颜色信息
attribute vec3 a_Normal;     // 我们将要传入的每个顶点的法线信息

varying vec3 v_Position;     
varying vec4 v_Color;        
varying vec3 v_Normal;       

// 顶点着色器入口点
void main()
{
   // 将顶点位置转换成眼睛空间的位置
   v_Position = vec3(u_MVMatrix * a_Position);
   // 传入颜色
   v_Color = a_Color;
   // 将法线的方向转换在眼睛空间
   v_Normal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));
   // gl_Position是一个特殊的变量用来存储最终的位置
   // 将顶点乘以矩阵得到标准化屏幕坐标的最终点
   gl_Position = u_MVPMatrix * a_Position;
}
```
顶点着色器比之前更加的简单。我们添加了两个线性插值变量用来传入到片段着色器：顶点位置和顶点法线。它们将在片段着色器计算光亮的时候被使用。


### 片段着色器
``` glsl
precision mediump float; //我们将默认精度设置为中等，我们不需要片段着色器中的高精度
uniform vec3 u_LightPos; // 光源在眼睛空间的位置
varying vec3 v_Position; // 插入的位置
varying vec4 v_Color;    // 插入的位置颜色
varying vec3 v_Normal;   // 插入的位置法线
void main()              // 片段着色器入口
{
   // 将用于哀减
   float distance = length(u_LightPos - v_Position);
   // 获取从光源到顶点方向的光线向量
   vec3 lightVector = normalize(u_LightPos - v_Position);
   // 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
   float diffuse = max(dot(v_Normal, lightVector), 0.1);
   // 根据距离哀减光线
   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));
   // 颜色乘以亮度哀减得到最终的颜色
   gl_FragColor = v_Color * diffuse;
}
```
使用每片段照明，我们的片段着色器还有更多的工作要做。我们基本上将[朗伯计算][11]和哀减移到了每像素级别，这为我们提供了更逼真的照明，而无需添加更多顶点。

## 进一步练习
我们可以在顶点着色器中计算距离，然后赋值给变量通过线性插值传入片段着色器吗？

## 教程目录
- [OpenGL Android课程一：入门][3]
- [OpenGL Android课程二：环境光和漫射光][2]
- [OpenGL Android课程三：使用每片段照明][14]
- [OpenGL Android课程四：介绍纹理基础][15]

## 打包教材
可以在Github下载本课程源代码：[下载项目][12]
本课的编译版本也可以再Android市场下：[google play 下载apk][13]






[1]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190126183929.png
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[4]: https://en.wikipedia.org/wiki/Half-Life_(video_game)
[5]: http://en.wikipedia.org/wiki/Gouraud_shading
[6]: https://en.wikipedia.org/wiki/Lightmap
[7]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190127004415.png
[8]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190127004455.png
[9]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190127004542.png
[10]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190127004615.png
[11]: https://en.wikipedia.org/wiki/Lambert%27s_cosine_law
[12]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[13]: https://market.android.com/details?id=com.learnopengles.android
[14]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[15]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
