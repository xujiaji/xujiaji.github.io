---
title: OpenGL Android课程二：环境光和漫射光
date: 2019-01-23 15:50:51
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/5C1BB79E-9092-4559-B6A6-D3288D0FA000.png
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---
> 翻译文

原文标题：OpenGL Android Lesson One: Getting Started
原文链接：<http://www.learnopengles.com/android-lesson-two-ambient-and-diffuse-lighting/>
<!-- more -->

---

# 环境光和漫射光

|||
|-|-|
|欢迎来到第二课，我们将学习如何使用<br>着色器实现[朗伯反射（ Lambertian reflectance ）][2]，也称为标准漫射照明。<br><br>在OpengGLES2，我们需要实现我们自己的照明算法，<br>因此我们要学会数学如何工作以及如何应用到我们的场景中。|![screenshot][1]|

## 阅读本文前提条件

本系列的每节课都以前面的课程为基础。在开始前，[请看第一课][3]，因为本课程将以此为基础概念介绍。

## 什么是光

没错！一个没有光的世界是昏暗的。没有[光]，我们甚至不能感知世界或我们周围的物体，除了声音和触摸等其他感官。
光向我们展示了物体是明亮还是昏暗，是远还是近，它的角度是什么。

在现实世界，我们所感知的光实际是数万亿微小粒子的聚集，称为光子。它从光源飞出，反弹数千或数百万次，最终到达我们的眼镜我们称之为光。

我们如何通过计算机图形模拟光的影响？
有两种流行的方法：[光线追踪][5]和[光栅化][6]
光线跟踪的工作原理是通过数学计算跟踪实际光线并查看它们的最终位置。该技术可以得到非常精准和逼真的结果，但缺点是模拟所有这些光线的计算成本非常高，并且通常对于实时渲染来说太慢了。
由于这个限制，大多数实时图形计算使用光栅化，它通过近似值模拟光照。鉴于当前游戏的真实性，光栅化看起来非常好，即使在手机上也可以快速实现实时图形。OpengGL ES主要是一个光栅化库，因此我们主要关注这个。

### 不同种类的光

事实证明，我们可以抽象出光的工作方式，并提出三种基本的光照方式

|||
|-|-|
|![Ambient][7]<br>环境光|**环境光**<br>这是基本的照明水平，似乎遍布整个场景。它似乎不是来自任何<br>光源的光，因为它在到达你之前已经反弹了很多次。这种类型的光<br>在户外的阴天可以体验，或者在户内作为许多不同光源的积累影响。<br>我们可以为物体或场景设置一个基本的亮度，而不是为所有的<br>光单独计算。|
|![diffuse][8]<br>环境照明和漫射照明<br>的例子|**漫射照明**<br>这是直接从一个物体上跳弹后到达您眼睛中的光，物体的亮度<br>随着它与照明的角度而变化，面向灯光的方向比其他角度更加明亮<br>此外，无论我们相对于物体的角度怎样，我们都觉得物体是相同的<br>亮度，这也被称为[Lambert的余弦定律][9]。漫射照明或朗伯反射率在<br>日常生活中很常见，您可以在室内灯光照明的白墙上轻松看到。|
|![specular][10]<br>镜面高光的一个例子|**镜面照明**<br>与漫射照明不同，当我们相对于物体移动时，镜面光照也会<br>发生改变。这给物体带来“光泽”，并且可以在“更光滑”的表面<br>上看到，例如玻璃和其他有光泽的物体。|

### 模拟光

正如3D场景中的3中主要类型的光照一样，还有三种主要类型的光源：定向光源，点光源，聚光灯，这些也可以在日常生活中轻松看到。

|||
|-|-|
|![Directional lighting][11]<br>一个明亮的风景|**定向光源**<br>定向光照通常来自于一个很远的光源，它可以均匀的照亮整个<br>场景达到相同的亮度。这种光源是最简单的类型，无论您处在<br>场景哪里，光照都具有相同的强度和方向。|
|![Point lighting][12]<br>一个点光源的例子|**点光源**<br>点光源可以添加到场景中，以提供更多样化和逼真的照明。<br>点光的照射[随着距离而下降][13]，并且它的光线在所有方向上<br>向外传播，光源位于中心。|
|![Spot lighting][14]<br>聚光灯|**聚光灯**<br>除了具有点光源的特性外，聚光灯也有光哀减的方向，<br>通常呈锥形。|

### 数学

本节课，我们来看看来自一个点光源的环境照明和漫射照明。

### 环境照明

环境照明其实是[间接漫射照明][15]，但它也可以被认为是遍布整个场景的低级光。如果我们这么想，那么它将非常好计算：

``` c
// 最终颜色 = 材质颜色 * 环境光颜色
final color = material color * ambient light color
```

例如，我们有个红色的物体和一个暗白色的环境照明。我们假设三个颜色（红，绿，蓝）的数组存储颜色，使用[RGB颜色模型][16]：

``` c
// 最终颜色 = 红色 * 暗白色 = 暗红色
final color = {1, 0, 0} * {0.1, 0.1, 0.1} = {0.1, 0.0, 0.0}
```

物体的最终颜色将是暗红色，如果您有一个被昏暗的白光照明的红色物体，那么这就是您的预期。基本的环境光真的没有比这更多的了，除非您想加入更先进的照明技术，如光能传递。

### 漫射照明-点光源

对于漫射照明，我们需要添加哀减和光源位置。光源位置将用来计算光线和表面的角度，它将影响表面的整体光照水平。它还将用于计算光源到表面的距离，这决定了光在这个点上的强度。

#### 第一步：计算朗伯因子（lambert factor）

我们最重要的是需要弄清楚表面和光线之间的角度。面向光直射的表面因该全强度照射，而倾斜的表面因该得到较少的照射，比较合适的计算方式是使用[Lambert的余弦定律][9]。
果我们有两个向量，一个是从光到表面上的一个点，第二个是[表面的法线][17]（如果表面是平面，则表面法线是指向上或垂直于该表面的矢量），然后我们可以通过对每个向量进行归一化来计算余弦，使其长度为1，然后通过计算两个向量的[点积（数量积）][18]。
这个操作可以由OpenGL ES 2轻松完成。

我们称这位朗伯因子，它的取值范围在0~1之间

``` c
// 光线向量 = 光源位置 - 物体位置
light vector = light position - object position
// 余弦 = 物体法线和归一化后的光线向量的点积
cosine = dot product(object normal, normalize(light vector))
// 朗伯因子 = 取余弦和0中最大的
lambert factor = max(cosine, 0)
```

首先我们通过光源位置减去物体位置得到光线向量，然后我们通过物体法线和光向量的点积得到余弦。我们标准化光向量，这意味着改变它的长度，长度为1，这个物体的法线长度也是1，两个归一化向量的点积得到他们之间的余弦。因为点积的取值范围是-1~1，所以我们将其限制到0~1。

这儿有个处在原点的平面，其表面法线指向天空的例子。
> 光的位置在{0, 10, -10}，我们想要计算在原点的光。

``` c
// 光线向量
light vector = {0, 10, -10} - {0, 0, 0} = {0, 10, -10}
// 物体法线
object normal = {0, 1, 0}
```

> 简洁的说，如果们沿着光线矢量走，我们到达光源的位置。为了归一化矢量，我们将每个分量除以矢量长度：

``` c
// 光线向量长度 = 平方根(0*0 + 10*10 + (-10 * -10)) = 平方根(200) = 14.14
light vector length = square root(0*0 + 10*10 + (-10 * -10)) = square root(200) = 14.14
// 归一化光线向量
normalize light vector = {0, 10/14.14, -10/14.14} = {0, 0.707, -0.707}
```

> 然后我们计算点积：

``` c
// 点积
dot product({0, 1, 0}, {0, 0.707, -0.707}) = (0 * 0) + (1 * 0.707) + (0 * -0.707) = 0.707
```

[这里有个一对点积计算很好的解释][19]
> 最后我们限制范围：

``` c
// 朗伯因子
lambert factor = max(0.707, 0) = 0.707
```

OpenGL ES 2的着色器语言内置了对其中一些函数的支持，因此我们不需要手动完成所有数学运算，但它仍然有助于理解正在发生的事情。

#### 第二步：计算哀减系数

接下来，我们需要计算哀减。来自光源的实际光哀减遵循[反平方定律][13]
> 也可以这样表示：

``` c
// 亮度 = 1 / 距离的平方
luminosity = 1 / (distance * distance)
```

> 回到我们的列子，因为我们有光线长度为14.14，这儿我们最终的亮度：

``` c
luminosity = 1 / (14.14 * 14.14) = 1 / 200 = 0.005
```

正如您所见，反平方定律会导致距离的强烈哀减。这就是点光源的光在现实世界中的作用，但是由于我们图形展示范围有限，控制这个哀减系数是非常有用的，因此我们仍然能获得逼真的照明而不会让其看起来很昏暗。

#### 第三步：计算最终颜色

> 现在我们知道了余弦和哀减度，我们可以计算我们最终的亮度：

``` c
// 最终颜色 = 材质颜色 * （光的颜色 * 朗伯因子 * 亮度）
final color = material color * (light color * lambert factor * luminosity)
```

> 继续我们之前的红色物体和白光源的例子，这儿计算最终颜色：

``` c
final color = {1, 0, 0} * ({1, 1, 1} * 0.707 * 0.005) = {1, 0, 0} * {0.0035, 0.0035, 0.0035} = {0.0035, 0, 0}
```

回顾一下，对于漫射照明，我们需要使用表面和光线之间的角度以及距离，用来计算最终的整体漫射亮度。
> 以下是步骤：

``` c
// 第一步
light vector = light position - object position
cosine = dot product(object normal, normalize(light vector))
lambert factor = mac(cosine, 0)

// 第二步
luminosity = 1 / (distance * distance)

// 第三步
final color = material color * (light color * lambert factor * luminosity)

```

### 将这一切放到OpenGL ES 2着色器中

#### 顶点着色器

``` java
final String vertexShader =
        "uniform mat4 u_MVPMatrix;      \n" + // 一个表示组合model、view、projection矩阵的常量
        "uniform mat4 u_MVMatrix;       \n" + // 一个表示组合model、view矩阵的常量
        "uniform vec3 u_LightPos;       \n" + // 光源在眼睛空间（相对于相机视角）的位置

        "attribute vec4 a_Position;     \n" + // 我们将要传入的每个顶点的位置信息
        "attribute vec4 a_Color;        \n" + // 我们将要传入的每个顶点的颜色信息
        "attribute vec3 a_Normal;       \n" + // 我们将要传入的每个顶点的法线信息

        "varying vec4 v_Color;          \n" + // 这将被传入片段着色器

        "void main()                    \n" + // 顶点着色器入口
        "{                              \n" +
        // 将顶点转换成眼睛空间（相对于相机视角）
        "   vec3 modelViewVertex = vec3(u_MVMatrix * a_Position);                \n" +
        // 将法线的方向转换成眼睛空间（相对于相机视角）
        "   vec3 modelViewNormal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));       \n" +
        // 将用于哀减
        "   float distance = length(u_LightPos - modelViewVertex);               \n" +
        // 获取从光源到顶点方向的光线向量
        "   vec3 lightVector = normalize(u_LightPos - modelViewVertex);          \n" +
        // 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
        "   float diffuse = max(dot(modelViewNormal, lightVector), 0.1);         \n" +
        // 根据距离哀减光线
        "   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));    \n" +
        // 将颜色乘以亮度，它将被插入三角形中
        "   v_Color = a_Color * diffuse;                                         \n" +
        // gl_Position是一个特殊的变量用来存储最终的位置
        // 将顶点乘以矩阵得到标准化屏幕坐标的最终点
        "   gl_Position = u_MVPMatrix * a_Position;                              \n" +
        "}                                                                       \n";
```

这里有相当多的事情要做。我们在[第一课][20]讲到过我们要有一个model/view/projection的组合矩阵，但是我们还要添加了一个model/view矩阵。为什么？因为我们将需要这个矩阵去计算光源位置到当前顶点位置之间的距离。对于漫射照明，无论您使用世界空间（model矩阵）或眼睛空间（model/view矩阵）只要你能计算出合适的距离和角度实际上都没有问题。

我们传入顶点的颜色和位置信息，以及它的[法线][17]。我们会将最终的颜色传入片段着色器，它将在顶点之间插值，这也被称为[Gouraud着色法][21]。

让我们来看看着色器每一部分的意义：

``` java
// 将顶点转换成眼睛空间（相对于相机视角）
"   vec3 modelViewVertex = vec3(u_MVMatrix * a_Position);                \n"
```

因为我们是在眼睛空间观察光源位置，我们转换当前的顶点位置到眼睛空间的坐标系中，因此我们能计算出对应的距离和角度。

---

``` java
// 将法线的方向转换成眼睛空间（相对于相机视角）
"   vec3 modelViewNormal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));       \n" +
```

我们也需要转换法线的方向。这里我们只是想上面位置一样做了个常规乘法，但是如果model或view矩阵做过旋转或倾斜，那么将不能工作：我们实际上需要通过将法线乘以原始矩阵的反转来消除倾斜或缩放的影响。[这个网站很好的解释了为什么我们必须这么做][22]

---

``` java
// 将用于哀减
"   float distance = length(u_LightPos - modelViewVertex);               \n"
```

如前面数学部分所示，我们需要这个距离去计算哀减系数

---

``` java
// 获取从光源到顶点方向的光线向量
"   vec3 lightVector = normalize(u_LightPos - modelViewVertex);          \n"
```

我们也需要光线向量去计算朗伯反射因子

---

``` java
// 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
"   float diffuse = max(dot(modelViewNormal, lightVector), 0.1);         \n"
```

这与上面的数学部分相同，只是在OpenGL ES 2着色器中完成。后面的0.1是一种非常便宜的环境照明方式（最小值将被限制在0.1）。

---

``` java
// 根据距离哀减光线
"   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));    \n"
```

这里和上面的数学部分略有不同。我们将距离的平方缩放0.25以抑制衰减的效应，并且我们还将修改的距离加1，这样当光源非常接近物体时我们就不会过饱和（否则，当距离小于1时，该等式实际上回照亮光源而不是哀减它）。

---

``` java
// 将颜色乘以亮度，它将被插入三角形中
"   v_Color = a_Color * diffuse;                                         \n" +
// gl_Position是一个特殊的变量用来存储最终的位置
// 将顶点乘以矩阵得到标准化屏幕坐标的最终点
"   gl_Position = u_MVPMatrix * a_Position;                              \n"
```

当我们有了最终的光色，我们将它乘以顶点的颜色得到最终输出的颜色，然后我们将这个顶点的位置投影到屏幕上。

#### 像素着色器

``` java
final String fragmentShader =
        "precision mediump float;       \n" + // 我们将默认精度设置为中等，我们不需要片段着色器中的高精度
                "varying vec4 v_Color;          \n" + // 这是从三角形每个片段内插的顶点着色器的颜色
                "void main()                    \n" + // 片段着色器入口
                "{                              \n" +
                "   gl_FragColor = v_Color;     \n" + // 直接将颜色传递
                "}                              \n";
```

因为我们是在每个顶点的基础上计算光，我们的片段着色器和[上节课][20]一样，我们所做的是将颜色直接传过去。在下节课中，我们将学习每像素照明。

## 每顶点照明和每像素照明

这节课我们的关注点在实现每顶点照明。对于具有光滑表面的物体（如地形），或具有许多三角形的物体的漫反射，这通常是足够了。然而，当您的物体没有包含许多顶点时（例如我们的在这个案例中的正方体），或者有尖角，顶点光照可能会导致伪影，因为亮度在多边形上线性插值；当镜面高光添加到图像时，这些伪影也会变得更加明显。更多关于[Gouraud着色法][21]的Wiki文章

## 正方体的构造

在第一课中，我们将位置和颜色属性打包到一个数组中，但是OpengGL ES 2也允许让我们将属性单独存放：

``` java
//X, Y, Z
final float[] cubePositionData = {
        // 在OpenGL，逆时针绕组（下面的点事逆时针顺序）是默认的。
        // 这意味着当我们在观察一个三角形时，如果这些电视逆时针的，那么我们正在看"前面"，如果不是我们则正在看背面
        // OpenGL有一个优化，所有背面的三角形都会被剔除，因为它们通常代表一个物体的背面，无论如何都不可见
        // 正面
        -1.0F, 1.0F, 1.0F,
        -1.0F, -1.0F, 1.0F,
        1.0F, 1.0F, 1.0F,
        -1.0F, -1.0F, 1.0F,
        1.0F, -1.0F, 1.0F,
        1.0F, 1.0F, 1.0F,
        ...
};

// R，G，B，A
final float[] cubeColorData = {
        // 正面红色
        1.0F, 0.0F, 0.0F, 1.0F,
        1.0F, 0.0F, 0.0F, 1.0F,
        1.0F, 0.0F, 0.0F, 1.0F,
        1.0F, 0.0F, 0.0F, 1.0F,
        1.0F, 0.0F, 0.0F, 1.0F,
        1.0F, 0.0F, 0.0F, 1.0F,
        ...
};
```

## 新的OpenGL flag

我们还使用了`glEnable()`调用启用了剔除和深度缓冲：

``` java
// 使用剔除去掉背面
GLES20.glEnable(GLES20.GL_CULL_FACE);
// 启用深度测试
GLES20.glEnable(GLES20.GL_DEPTH_TEST);
```

作为优化，您可以告诉OpenGL剔除物体背面的三角形。当我们定义正方体时，我们还定义了每个三角形的三个点，以便当我们在查看正面的时候是逆时针的。当我们翻转三角形以便我们到背面时，这些点将会顺时针展示。
您只能同时看到一个正方体的三个面，所以这个优化告诉OpenGL不要浪费时间去绘制背面的三角形。

之后当我们绘制透明的物体时，我们希望关闭剔除，然后物体背面将会变得可见。

我们还开启了[深度测试][23]。如果你总是从后面向前面绘制物体，那么深度测试绝非必要，但是通过启用它您不仅不需要担心绘制顺序（尽管如果你先画最近的物体渲染会更快），一些显卡也将进行优化，通过花费更少的时间绘制像素来加速渲染。

## 加载着色器程序的修改

因为在OpenGL中加载着色器程序的步骤大致相同，这些步骤可以很容易的重构为一个单独的方法。我们还添加了以下调用来检索调试信息，以防编译/链接失败：

``` java
GLES20.glGetProgramInfoLog(programHandle);
GLES20.glGetShaderInfoLog(shaderHandle);
```

## 光点的顶点和着色程序

这个新的顶点和着色器程序绘制在屏幕上代表当前光源的位置：

``` java
// 定义一个简单的着色程序
final String pointVertexShader =
        "uniform mat4 u_MVPMatrix;                  \n" +
        "attribute vec4 a_Position;                 \n" +
        "void main()                                \n" +
        "{                                          \n" +
        "   gl_Position = u_MVPMatrix * a_Position; \n" +
        "   gl_PointSize = 5.0;                     \n" +
        "}                                          \n";
final String pointFragmentShader =
        "precision mediump float;                   \n" +
        "void main()                                \n" +
        "{                                          \n" +
        "   gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0) \n" +
        "}                                          \n";
```

这个着色器类似于第一课的简单着色器，这里有个新的成员`gl_PointSize`，直接固定它的值为5.0，这是点的像素尺寸。当我们使用`GLES20.GL_POINTS`模式绘制这个点的时候它会被使用。我们也直接设置了它的显示颜色为白色。

## 进一步练习

- 尝试删除“过渡饱和”看会发生什么
- 这里的照明方式存在缺陷，你能发现是什么吗？提示：我们做环境照明的方式的缺点是什么，以及alpha会放生什么？
- 如果将`gl_PointSize`添加到正方体着色器并使用`GL_POINTS`绘制它会发生什么？

## 进一步阅读

- [Clockworkcoders教程：每片段照明][24]
- [Lighthouse3d.com：法线矩阵][25]
- [arcsynthesis.org: OpenGL教程：法线转换][22]
- [OpenGL编程指南：5章 照明][26]

在编写本教程时，上面的进一步阅读部分对我来说是非常宝贵的资源，因此我强烈建议您阅读它们以获得更多的信息和解释。

## 教程目录

- [OpenGL Android课程一：入门][20]
- [OpenGL Android课程二：环境光和漫射光][29]
- [OpenGL Android课程三：使用每片段照明][30]
- [OpenGL Android课程四：介绍纹理基础][31]
- [OpenGL Android课程五：介绍混合（Blending）][32]
- [OpenGL Android课程六：介绍纹理过滤][34]

## 打包教材

可以在Github下载本课程源代码：[下载项目][27]  
本课的编译版本也可以再Android市场下：[google play 下载apk][28]  
“我”也编译了个apk，方便大家下载：[github download][33]

[1]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190123163828.png
[2]: https://en.wikipedia.org/wiki/Lambertian_reflectance
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[4]: https://en.wikipedia.org/wiki/Light
[5]: http://en.wikipedia.org/wiki/Ray_tracing_(graphics)
[6]: http://en.wikipedia.org/wiki/Rasterisation
[7]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190123234400.png
[8]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190124093759.png
[9]: https://en.wikipedia.org/wiki/Lambert%27s_cosine_law
[10]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190124105013.png
[11]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190124112017.png
[12]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190124112915.png
[13]: https://en.wikipedia.org/wiki/Inverse-square_law
[14]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190124113930.png
[15]: https://en.wikipedia.org/wiki/Radiosity_(computer_graphics)
[16]: https://en.wikipedia.org/wiki/RGB_color_model
[17]: https://en.wikipedia.org/wiki/Normal_(geometry)
[18]: https://en.wikipedia.org/wiki/Dot_product
[19]: http://programmedlessons.org/VectorLessons/vch07/vch07_5.html
[20]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[21]: https://en.wikipedia.org/wiki/Gouraud_shading
[22]: https://web.archive.org/web/20150101061328/http://www.arcsynthesis.org/gltut/Illumination/Tut09%20Normal%20Transformation.html
[23]: https://en.wikipedia.org/wiki/Z-buffering
[24]: https://www.opengl.org/sdk/docs/tutorials/ClockworkCoders/lighting.php
[25]: http://www.lighthouse3d.com/tutorials/glsl-12-tutorial/the-normal-matrix/
[26]: http://glprogramming.com/red/chapter05.html
[27]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[28]: https://market.android.com/details?id=com.learnopengles.android
[29]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[30]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[31]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[32]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[33]: https://github.com/xujiaji/LearnOpenGL/releases
[34]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
