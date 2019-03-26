---
title: OpenGL Android课程六：介绍纹理过滤
date: 2019-02-19 16:24:18
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190224214007.jpg
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---

> 翻译文

原文标题：Android Lesson Six: An Introduction to Texture Filtering
原文链接：<http://www.learnopengles.com/android-lesson-six-an-introduction-to-texture-filtering/>
<!-- more -->

---

# 介绍纹理过滤

|||
|-|:-:|
|这节课，我们将介绍基本纹理过滤的不同类型和怎样使用它们，<br>包括最邻近（nearest-neighbour）过滤，[双线性(bilinear)过滤][7]，<br>和使用mipmap的[三线性(trilinear)过滤][8]。<br><br>你将学习如何使纹理看起来更平滑，以及平滑带来的缺点。<br>[这儿有旋转物体][]的不同方式，本课使用了其中一。|![screenshot][10]|

## 前提条件

强烈建议您先阅读[OpenGL Android课程四：介绍纹理基础][4]，理解纹理映射在OpenGL中的基本使用。

## 什么是纹理过滤？

OpenGLES中的纹理由元素数组组成，被称为纹素(texels)，其中包含颜色和alpha值。这与显示器相对应，显示器由一堆像素组成，并在每个点显示不同的颜色。在OpenGL中纹理被用在三角形上并绘制到屏幕，因此这些纹理能绘制出各种各样的尺寸和方向。OpenGL中的纹理过滤选项告诉它如何根据具体情况将纹理像素过滤到设备的像素上。

> 有三种情况：

- 每个纹素映射到多个像素，这被称为放大(magnification)
- 每个纹素精确的映射到一个像素，过滤不适合这种情况
- 每个纹素映射少于一个像素，这被称为缩小(minification)

OpenGL允许我们为放大和缩小分配过滤器，并允许我们使用最邻近、双线性和三线性过滤。我们将在下面解释这些意思。

## 放大和缩小

这里是放大和缩小的最邻近渲染的可视化，当您用USB连接你的Android设备时使用这个可爱的Android显示成功连接。

![cute android][11]

### 放大

![magnification android][12]

正如您所见，纹素现在很容易看到，因为当前一个纹素覆盖了很多像素展示出来。

### 缩小

![minification android][13]

随着缩小，许多纹素不能渲染到有限的像素上，许多细节将会丢失。

## 纹理过滤模式

### 双线性插值（Bilinear interpolation）

当纹素值之间没有插值时，在放大示例中，纹理的纹素清晰可见为大正方形。当使用最邻近方式时，像素将会分配到最邻近的像素。

通过切换到双线性插值，渲染质量显著提高。这些值将会在邻近的四个像素之间线性插值，而不是将一组像素分配给邻近相同的纹素值。每个像素被平滑化，使得最后的图片看起来也更平滑：

![smoother android][14]

一些块效果仍然很明显，但是这个图片看起来比之前更加平滑。那些在3D加速卡出现前玩过3D游戏的人将会记得软件渲染游戏和硬件加速游戏之间的特性：软件渲染游戏根本没有进行预计算处理，所以一切都显示得块状和锯齿状。一旦人们开始使用图形加速，这些东西都将变得平滑。

![smooth][15]

双线性插值大多使用在放大。它也能使用在缩小，但是超过某个度，我们将会遇到同样的问题，我们在尝试将太多的纹素放到相同的像素上。OpenGL仅使用最多4个纹素渲染一个像素，因此许多信息仍然会丢失。

如果我们看应用了双线性插值的纹理，当我们在远处看它移动时看起来会很嘈杂，因为每帧都会选择不同的纹素。

### 纹理映射（Mipmapping）

我们如何才能在缩小纹理时不引用嘈杂并使用上所有纹素呢？我们可以生成一组优化后的不同尺寸的纹理，然后在我们运行的时候使用它们。由于这些纹理已预先生成，它们能使用更多高昂的技术去过滤所有纹素，并且在运行时OpenGL会根据纹理在屏幕上的最终大小选择最合适的层。

![textures set][16]

生成的图片可以具有更多细节，更少噪点，并且整体上看起来更好。尽管需要更多的内存，但渲染速度也会更快，因为较小的层级能更容易保存在GPU的纹理缓存中。让我们来仔细研究一下原尺寸的1/8倍的图片，在使用了双线性过滤使用纹理映射和双线性过滤没有使用映射。为了清楚图片已被扩大：

#### 双线性过滤没有mipmap

![without mipmaps][17]

#### 双线性过滤+mipmap

![with mipmaps][18]

使用mipmap的版本拥有更多细节，由于图像预处理到单独的层级，所有纹素最终都会在最终的图像中使用。

### 三线性过滤（Trilinear filtering）

当使用双线性过滤的mipmap时，有时在渲染场景中可以看到明显的跳跃或线，由于OpenGL在纹理的不同mipmap层级之间切换。比较不同的OpenGL纹理的过滤模式将在下面进一步指出。

三线性插值通过在不同mipmap层级之间插值来解决这个问题，这样总共8个纹素将用于插值得到最终的像素值，使得图像更平滑。

## OpenGL 纹理过滤模式

OpenGL有两个可被设置的参数：

- `GL_TEXTURE_MIN_FILTER` 纹理缩小时的过滤模式
- `GL_TEXTURE_MAG_FILTER` 纹理放大时的过滤模式

这些相对应于上面的缩小和放大描述。  

- `GL_TEXTURE_MIN_FILTER`接受以下选项：
  - `GL_NEAREST`
  - `GL_LINEAR`
  - `GL_NEAREST_MIPMAP_NEAREST`
  - `GL_NEAREST_MIPMAP_LINEAR`
  - `GL_LINEAR_MIPMAP_NEAREST`
  - `GL_LINEAR_MIPMAP_LINEAR`
- `GL_TEXTURE_MAG_FILTER`接受以下选项：
  - `GL_NEAREST`
  - `GL_LINEAR`

`GL_NEAREST` 对应最邻近渲染；  
`GL_LINEAR` 对应双线性过滤；  
`GL_LINEAR_MIPMAP_NEAREST` 对应双线性过滤+mipmap；  
`GL_LINEAR_MIPMAP_LINEAR` 对应三线性过滤；  
本课中将进一步介绍图形示例和最常见选项的进一步说明。

### 怎样设置纹理过滤模式

我们首先需要绑定纹理，然后我们在这个纹理上设置合适的过滤参数：

``` java
GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, mTextureHandle);
GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, filter);
```

### 怎样生成mipmap

这真的很容易！在加载纹理到OpenGL中后，纹理仍然是绑定的，我们可以简单的调用：

``` java
GLES20.glGenerateMipmap(GLES20.GL_TEXTURE_2D);
```

它将为我们生成所有的mipmap层级，并且这些层级会根据纹理过滤自动使用。

## 它看起来怎么样？

以下是可用的最常见的组合的屏幕截图，当你看到它运动中时，效果更加引人注目，因此我建议下载[这个App][19]并试一试。

### 最邻近渲染

这个模式让人想起旧版3D游戏软件的渲染。

``` java
GL_TEXTURE_MIN_FILTER = GL_NEAREST
GL_TEXTURE_MAG_FILTER = GL_NEAREST
```

![nearest nearest][22]

### 双线性过滤，mipmap

许多支持3D加速的首批游戏都使用此模式，这是今天在Android手机上平滑纹理的有效方式。

``` java
GL_TEXTURE_MIN_FILTER = GL_LINEAR_MIPMAP_NEAREST
GL_TEXTURE_MAG_FILTER = GL_LINEAR
```

![linear mipmap][23]

静态图上很难看图问题，但是当物体运动时，您可能会注意到渲染的像素在mipmap层级之间切换的水平条带。

### 三线性过滤

此模式通过在mipmap层级之间进行插值，改进了使用mipmap的双线性过滤的渲染质量。

``` java
GL_TEXTURE_MIN_FILTER = GL_LINEAR_MIPMAP_LINEAR
GL_TEXTURE_MAG_FILTER = GL_LINEAR
```

![trilinear][24]

像素在近距离和远距离之间完全平滑；事实上，纹理现在可能在倾斜角度下显示的过于平滑。
[各向异性过滤（Anisotropic filtering）][25]是一种更先进的技术，受到某些移动GPU的支持，可用于改善最终结果，超出三线性过滤所能提供的效果。

### 进一步练习

使用其他模式可以达到什么样的效果？例如，您何时会使用像`GL_NEAREST_MIPMAP_LINEAR`这样的东西？

## 教程目录

- [OpenGL Android课程一：入门][1]
- [OpenGL Android课程二：环境光和漫射光][2]
- [OpenGL Android课程三：使用每片段照明][3]
- [OpenGL Android课程四：介绍纹理基础][4]
- [OpenGL Android课程五：介绍混合（Blending）][5]
- [OpenGL Android课程六：介绍纹理过滤][6]
- [OpenGL Android课程七：介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VOB）][26]

## 打包教材

可以在Github下载本课程源代码：[下载项目][20]  
本课的编译版本也可以再Android市场下：[google play 下载apk][21]  
“我”也编译了个apk，方便大家下载：[github download][19]

[1]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[4]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[5]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[6]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
[7]: https://en.wikipedia.org/wiki/Bilinear_filtering
[8]: https://en.wikipedia.org/wiki/Trilinear_filtering
[9]: http://www.learnopengles.com/rotating-an-object-with-touch-events/
[10]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190219164050.png
[11]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221100843.png
[12]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221100936.png
[13]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221101211.png
[14]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221103115.png
[15]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221104453.png
[16]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221143838.png
[17]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221145134.png
[18]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221145249.png
[19]: https://github.com/xujiaji/LearnOpenGL/releases
[20]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[21]: https://market.android.com/details?id=com.learnopengles.android
[22]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221163746.png
[23]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221164349.png
[24]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190221165703.png
[25]: https://en.wikipedia.org/wiki/Anisotropic_filtering
[26]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Seven
