---
title: OpenGL Android课程五：介绍混合（Blending）
date: 2019-02-12 16:37:00
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190219114206.jpg
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---

> 翻译文

原文标题：Android Lesson Five: An Introduction to Blending
原文链接：<http://www.learnopengles.com/android-lesson-five-an-introduction-to-blending/>
<!-- more -->

---

# 介绍混合（Blending）

|||
|-|:-:|
|这节课，我们来学习混合(blending)在OpenGL中的<br>基本使用。我们来看看如何打开或关闭混合，怎样设置<br>不同的混合模式，以及不同的混合模式如何模仿显示生<br>活中的效果。在后面的课程中，我们还将介绍如何使用<br>alpha通道，如何使用深度缓冲区在同一个场景中渲染<br>半透明和不透明的物体，以及什么时候按深度排序对象，<br>以及为什么。<br><br>我们还将研究如何监听触摸事件，然后基于此更改渲染<br>状态。|![display][6]<br>*基本混合*|

## 前提条件

本系列每个课程构建都是以前一个课程为基础。然而，对于这节课，如果您理解了[OpenGL Android课程一：入门][1]就足够了。尽管代码基本上是前一课的，照明和纹理部分已在本课中移除，因此我们仅关注混合。

## 混合（Blending）

混合是将一种颜色与另一种颜色组合以获得第三种颜色的行为。我们在现实世界任何时候都能看到混合：当光穿过玻璃时，当它从表面反射时，当光源本身叠加在背景上时，例如我们在晚上看到一盏明亮的路灯周围的耀斑。

OpenGL有不同的混合模式，我们能使用它模拟这种效果。在OpenGL中，混合发生在渲染过程的后期：一旦片段着色器计算出片段的最终输出颜色并且它即将被写入帧缓冲区，就会发生这种情况。通常情况下，这片段会覆盖之前所有内容，但如果启用了混合，那么该片段将与之前的片段混合。

默认情况下，当`glBlendEquation()`设置为默认值`GL_FUNC_ADD`时OpenGL的默认混合方程式为：

``` c
// 输出 = （源因子 * 源片段） + （目标因子 * 目标片段）
output = (source factor * source fragment) + (destination factor * destination fragment)
```

OpenGL ES 2 中还有另外两种模式`GL_FUNC_SUBTRACT`和`GL_FUNC_REVERSE_SUBTRACT`。
这些可能在以后的教程中介绍，然而，当我尝试调用此函数时，我在Nexus S上遇到了
`UnsupportedOperationException`，因此Android实现可能实际上不支持此功能。
这不是世界末日，因为你可以用`GL_FUNC_ADD`做很多事情。

使用函数`glBlendFunc()`设置源因子和目标因子。下面将给出几个常见混合因子的概述；更多信息以及不同可能的因素的列举，请参阅[Khronos在线手册][7]：

- [glBlendFunc()][8]
- [glBlendEquation()][9]

### 截取（Clamping）

OpenGL预期的输入被限制在[0,1]的范围内，并且输入也被限制在[0,1]。这在实践中意味着当您进行混合时，颜色可以在色调中移动。
如果继续想帧缓冲区添加红色（RGB = 1，0，0），最终颜色会是红色。如果想添加一点儿绿色，您要添加（RGB = 1，0.1，0）到缓冲区，即使您开始带红色的色调，最后也会得到黄色！
打开混合时，您可以在本课程的Demo中看到此效果：不同颜色的重叠的颜色变得过饱和。

## 不同类型的混合以及它们有怎样不同的效果

### 相加混合（Additive blending）

|![rgb][10]|
|:-:|
|*RGB颜色相加模型； 来源：Wikipedia*|

相加混合是当我们添加不同颜色在一起的混合，这就是我们的视觉与光一起工作的模式，这就是我们如何在我们的显示器上感知数百万种不同的颜色——它们实际上只是将三种不同的原色混合在一起。

这种混合在3D混合中很有用，例如在粒子效果中，它们似乎发出光线和覆盖物，例如灯光周围的光晕，或光剑周围的发光效果。

相加混合能通过调用`glBlendFunc(GL_ONE, GL_ONE)`指定，
混合的结果等式`输出=（1 * 源片段） + （1 * 目标片段）`，运算后：`输出=源片段 + 目标片段`

### 相乘混合（Multiplicative blending）

|![rg][11]|
|:-:|
|*光照贴图的一个例子*|

相乘混合（也称为调制）是另一种有用的混合模式，它表示光在通过过滤器时的行为方式，或从被点燃的物体反射并进入我们的眼睛。一个红色的物体看上去是红色是因为白光照射到这个物体上，蓝光和绿光被吸收，只有红光反射回我们的眼睛。在上面的例子中，我们能看到一些红色和绿色，但是很少会有一点蓝色。

当多纹理不可用时，乘法混合用于在游戏中实现光照贴图。纹理与光照贴图相乘，以填充在明亮和阴影的区域。

相乘混合能通过调用`glBlendFunc(GL_DST_COLOR, GL_ZERO)`指定，
其混合的结果等式`输出=（目标片段 * 源片段）+ （0 * 目标片段）`，写作：`输出=目标片段 * 源片段`。

### 插值混合（Interpolative blending）

|![textures][12]|
|:-:|
|*一个两个纹理一起插值的案例*|

插值混合结合了乘法和加法，以提供插值效果。与添加和调制本身不同，此混合模式也可是依赖绘制顺序的。因此在某些情况下，如果您先画出最远的半透明物体，然后绘制更近的物体，结果才会是正确。即使排序也不是完美，因为三角形可能重叠并相交，但产生的伪像可能是可接受的。

插值通常是将相邻的表面混合在一起，以及做有色玻璃或淡入淡出的效果。上面这个图片显示了两个纹理（纹理来自[公共领域纹理][13]）使用插值混合在一起。

插值混合能通过调用`glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)`指定，
其混合结果等式`输出 = （源alpha * 源片段） + （（1 - 源alpha） * 目标片段）`。这是一个例子：

想象一下，我们正在绘制一个只有25%不透明的绿色（0，1，0），当前屏幕上的物体时红色（1，0，0）。

``` c
输出 = （源因子 * 源片段） + （目标因子 * 目标片段）
输出 = （源alpha * 源片段） + （（1 - 源alpha） * 目标片段）

输出 = (0.25 * (0, 1, 0)) + (0.72 * (1, 0, 0))
输出 = (0, 0.25, 0) + (0.75, 0, 0)
输出 = (0.75, 0.25, 0)
```

注意，我们不需要对目标alpha做任何涉及，因为这个帧缓冲区本身不需要alpha通道，这为我们提供了更多的颜色通道位。

## 使用混合

在我们的课程中，我们的Demo将使用相加混合将立方体显示为光的发射器。发光的东西不需要其他光源照亮，因此这个Demo中没有灯光。我也删除了纹理，虽然它可以很好地使用。本课程的着色器程序很简单；我们只需要一个可传递颜色的着色器。

### 顶点着色器

``` glsl
uniform mat4 u_MVPMatrix;
attribute vec4 a_Position;
attribute vec4 a_Color;

varying vec4 v_Color;

void main()
{
    v_Color = a_Color;
    gl_Position = u_MVPMatrix * a_Position;
}
```

### 片段着色器

``` glsl
precision mediump float;
varying vec4 v_Color;

void main()
{
    gl_FragColor = v_Color;
}
```

### 打开混合

打开混合就像是做一些方法调用那么简单：

``` java
// 关闭剔除去掉背面
GLES20.glDisable(GLES20.GL_CULL_FACE);
// 关闭深度测试
GLES20.glDisable(GLES20.GL_DEPTH_TEST);

// 启动混合
GLES20.glEnable(GLES20.GL_BLEND);
GLES20.glBlendFunc(GLES20.GL_ONE, GLES20.GL_ONE);
```

我们关闭背面剔除，是因为如果立方体是半透明的，那么现在我们能看到立方体的背面。我们需要绘制它们，否则可能看起来会很奇怪。出于同样的原因我们关闭了深度测试。

## 学习触摸事件并进行操作

你将注意到，当您运行Demo时，可以通过点击屏幕来打开和关闭混合。

现实触摸事件，您首先需要创建您的`GLSurfaceView`自定义view。在这个view中，创建一个默认构造用来调用父类，创建一个新的方法来接收特定的渲染器替换常用接口，并覆写`onTouchEvent()`。我们传入一个具体的渲染器类，因为我们将要在`onTouchEvent()`方法中调用这个类的特定方法。

在Android中，OpenGL渲染器在独立的线程中完成，因此我们还将看看如何安全的从正在监听触摸事件的主线程调度到单独的渲染器线程。

``` java
public class LessonFiveGLSurfaceView extends GLSurfaceView {

    private LessonFiveRenderer mRenderer;

    public LessonFiveGLSurfaceView(Context context) {
        super(context);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (
                event == null
                || event.getAction() != MotionEvent.ACTION_DOWN
                || mRenderer == null) {
            return super.onTouchEvent(event);
        }
        // 确保我们在OpenGL线程上调用switchMode()
        // queueEvent() 是GLSurfaceView的一个方法，它将为我们做到这点
        queueEvent(new Runnable() {
            @Override
            public void run() {
                mRenderer.switchMode();
            }
        });
        return true;
    }

    public void setRenderer(LessonFiveRenderer renderer) {
        mRenderer = renderer;
        super.setRenderer(renderer);
    }
}
```

在`LessonFiveRenderer`中实现`switchMode()`

``` java
public void switchMode() {
    mBlending = !mBlending;

    if (mBlending) {
        // 关闭剔除去掉背面
        GLES20.glDisable(GLES20.GL_CULL_FACE);
        // 关闭深度测试
        GLES20.glDisable(GLES20.GL_DEPTH_TEST);

        // 启动混合
        GLES20.glEnable(GLES20.GL_BLEND);
        GLES20.glBlendFunc(GLES20.GL_ONE, GLES20.GL_ONE);
    } else {
        GLES20.glEnable(GLES20.GL_CULL_FACE);
        GLES20.glEnable(GLES20.GL_DEPTH_TEST);
        GLES20.glDisable(GLES20.GL_BLEND);
    }
}
```

仔细看`LessonFiveGLSurfaceView::onTouchEvent()`，主要记住触摸事件都是在UI主线程中
，而`GLSurfaceView`在一个单独的线程中创建OpenGL ES上下文，这意味着我们的渲染器的回调也在一个单独的线程中运行。这是一个需要记住的重点，因为我们不能再其他线程调用OpenGL并希望其工作。

辛运的是，编写`GLSurfaceView`的人也想到了这点，并提供了一个`queueEvent()`方法，这使得你可以调用OpenGL线程上的东西。因此，当我们想通过点击屏幕打开和关闭混合时，我们确保通过在UI线程中使用`queueEvent()`来正确调用OpenGL线程中的内容。

### 进一步练习

这个Demo目前仅使用相加混合，尝试改变其为插值混合并重新添加灯光和纹理。如果您只在黑色背景上绘制两个半透明纹理，绘制顺序是否重要？什么时候重要？

## 教程目录

- [OpenGL Android课程一：入门][1]
- [OpenGL Android课程二：环境光和漫射光][2]
- [OpenGL Android课程三：使用每片段照明][3]
- [OpenGL Android课程四：介绍纹理基础][4]
- [OpenGL Android课程五：介绍混合（Blending）][5]

## 打包教材

可以在Github下载本课程源代码：[下载项目][15]  
本课的编译版本也可以再Android市场下：[google play 下载apk][16]  
“我”也编译了个apk，方便大家下载：[github download][14]

[1]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[4]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[5]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[6]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190212163914.png
[7]: http://www.khronos.org/opengles/sdk/docs/man/
[8]: https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glBlendFunc.xml
[9]: https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glBlendEquation.xml
[10]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190213200752.png
[11]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190213202603.png
[12]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190213205158.png
[13]: http://pdtextures.blogspot.com/
[14]: https://github.com/xujiaji/LearnOpenGL/releases
[15]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[16]: https://market.android.com/details?id=com.learnopengles.android
