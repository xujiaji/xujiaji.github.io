---
title: OpenGL Android课程七：介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VBOs）
date: 2019-03-09 16:49:10
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190324170029.png
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---

> 翻译文

原文标题：Android Lesson Seven: An Introduction to Vertex Buffer Objects (VBOs)
原文链接：<http://www.learnopengles.com/android-lesson-seven-an-introduction-to-vertex-buffer-objects-vbos/>
<!-- more -->

---

# 介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VBOs）

|||
|-|:-:|
|在这节课中，我们将介绍如何定义和如何去使用<br>顶点缓冲对象（VBOs）。下面是我们要讲到的几点：<br><br>1.怎样用顶点缓冲对象定义和渲染<br>2.单个缓冲区、所有数据打包进去、多个缓冲区之间的区别<br>3.问题和陷阱我们如何取处理它们|![screenshot][8]|

## 什么是顶点缓冲区对象？为什么使用它们？

到目前为止，我们所有的课程都是将对象数据存储在客户端内存中，只有在渲染时将其传输到GPU中。没有大量数据传输时，这很好，但随着我们的场景越来越复杂，有更多的物体和三角形，这会给GPU和内存增加额外的成本。

我们能做些什么呢？我们可以使用顶点缓冲对象，而不是每帧从客户端内存传输顶点信息，信息将被传输一次，然后渲染器将从该图形存储器缓存中得到数据。

## 前提条件

请阅读[OpenGL Android课程一：入门][1]介绍如何从客户端的内存上传顶点数据。了解OpenGL ES如何与顶点数组一起工作对于理解本课至关重要。

## 更详细的了解客户端缓冲区

一但了解了如何使用客户端内存进行渲染，切换到使用VBOs实际上并不太难。其主要的不同在于添加了一个上传数据到图形内存的额外步骤，以及渲染时添加了绑定这个缓冲区的额外调用。

本节课将使用四种不同的模式：

1. 客户端，单独的缓冲区
2. 客户端，打包的缓冲
3. 顶点缓冲对象，单独的缓冲区
4. 顶点缓冲对象，打包的缓冲

无论我们是否使用顶点缓冲对象，我们都需要先将我们的数据存储在客户端本地缓冲区。会想到[第一课][1]中OpenGL ES 是一个本地系统库，而java是运行在Android上的一个虚拟机中。如何去桥接这个距离？我们需要使用一组特殊的缓冲区类来在本地堆上分配内存，并使使其供OpenGL访问：

``` java
// Java 数组
float[] cubePositions;
...
// 浮点缓冲区
final FloatBuffer cubePositionsBuffer;
...
// 在本地堆上直接分配一块内存
// 字节大小为cubePositions的长度乘以每个浮点数的字节大小
// 每个float的字节大小为4，因为float是32位或4字节
cubePositionsBuffer = ByteBuffer.allocateDirect(cubePositions.length * BYTES_PRE_FLOAT)
// 浮点会以大端（big-endian）或小段（little-endian）的顺序排列
// 我想让其同本地平台相同的排列
.order(ByteOrder.nativeOrder())
// 在这个字节缓冲区上给我们一个浮点视角
.asFloatBuffer();
```

将Java堆上数据转换到本地堆上，就是两方法调用的事情：

``` java
// 将java堆上的数据拷贝到本地堆
cubePositionsBuffer.put(cubePositions)

// 重置这个缓冲区开始的缓冲位置
.position(0);
```

缓冲位置的目的是什么？通常，Java没有为我们提供一种在内存中使用[指针][13]，任意指定位置的方法。然而，设置缓冲区的位置在功能上等同于更改指向内存块指针的值。通过改变指针的位置，我们可以将缓冲区中任意的内存位置传递给OpenGL调用。当我们使用打包的缓冲作业时，这将派上用场。

一但数据存放到本地堆上，我们就不需要长时间持有float[]数组了，我们可以让垃圾回收器清理它。

使用客户端缓冲区进行渲染非常简单，我们仅需要启动对应属性的顶点素组，并将指针传递给我们的数据：

``` java
// 传入位置信息
GLES20.glEnableVertexAttribArray(mPositionHandle);
GLES20.glVertexAttriPointer(mPositionHandle, POSITION_DATA_SIZE,
    GLES20.GL_FLOAT, false, 0, mCubePositions)
```

[glVertexAttriPointer][14]参数说明：

- *mPositionHandle：* 我们着色器程序的位置属性索引
- *POSITION_DATA_SIZE：* 定义这个属性需要多少个float元素
- *GL_FLOAT：* 每个元素的类型
- *false：* 定点数据因该标准化吗？由于我们使用的是浮点数据，因此不适用。
- *0：* 跨度，设置0，以为着应安顺序读取。第一课中设置为7，表示每次读取跨度7个位置
- *mCubePositions：* 指向缓冲区的的指针，包含所有位置数据

## 使用打包缓冲区

使用打包缓冲区是非常相似的，替换了每个位置、法线等的缓冲区，现在一个缓冲区将包含所有这些数据。不同点看下面：

> 使用单缓冲区

``` c
positions = X,Y,Z,X,Y,Z,X,Y,Z,...
colors = R,G,B,A,R,G,B,A,...
textureCoordinates = S,T,S,T,S,T...
```

> 使用打包缓冲区

``` c
buffer = X,Y,Z,R,G,B,A,S,T...
```

使用打包缓冲区的好处是它将会使GPU更高效的渲染，因为渲染三角形所需的所有信息都位于内存同一块地方。缺点是，如果我们使用动态数据，更新可能会更困难，更慢。

当我们使用打包缓冲区时，我们需要以下几种方式更改渲染调用。首先，我们需要告诉OpenGL`跨度（stride）` ，定义一个顶点的字节数。

``` java
final int stride = (POSITION_DATA_SIZE + NORMAL_DATA_SIZE + TEXTURE_COORDINATE_DATA_SIZE)
    * BYTES_PER_FLOAT;

// 传入位置信息
mCubeBuffer.position(0);
GLES20.glEnableVertexAttribArray(mPositionHandle);
GLES20.glVertexAttribPointer(mPositionHandle, POSITION_DATA_SIZE,
    GLES20.GL_FLOAT, false, stride, mCubeBuffer);

// 传入法线信息
mCubeBuffer.position(POSITION_DATA_SIZE);
GLES20.glEnableVertexAttribArray(mNormalHandle);
GLES20.glVertexAttribPointer(mNormalHandle, NORMAL_DATA_SIZE,
    GLES20.GL_FLOAT, false, stride, mCubeBuffer);
...
```

这个跨度告诉OpenGL ES下一个顶点的同样的属性要再跨多远才能找到。例如：如果元素0是第一个顶点的开始位置，并且这里每个顶点有8个元素，然后这个跨度将是8个元素，也就是32个字节。下一个顶点的位置将找到第8个元素，下下个顶点的位置将找到第16个元素，以此类推。

请记住，传递给`glVertexAttriPointer`的跨度单位是字节，而不是元素，因此请记住进行该转换。

注意，当我们从指定位置切换到指定法线时，我们要更改缓冲区的其实位置。这是我们之前提到的指针算法，这是我们在使用OpengGL ES时用Java做的方式。我们仍然使用同一个缓冲区`mCubeBuffer`，但是我们告诉OpenGL从位置数据后的第一个元素开始读取法线信息。我们也告诉OpenGL下一个法线要跨越8个元素（也可以说是32个字节）开始。

## Dalvik和本地堆上的内存

如果你在本地堆上分配大量内存把并将其释放，您迟早会遇到心爱的`OutOfMemoryError` ，背后有几个原因：

1. 您可能认为通过让引用超出范围而自动释放了内存，但是本地内存似乎需要一些额外的GC周期才能完全清理，如果没有足够可用的内存并且尚未释放本地内存，Dalvik将抛出异常。
2. 本地堆可能会[碎片化][15]，调用`allocateDirect()`将会莫名其妙失败，尽管似乎有足够的内存可用。有时它有助于进行较小的分配，释放它，然后再次尝试更大的分配。

如何能避免这些问题？除了希望Google在未来的版本中改进Dalvik的行为之外，并不多。或者通过本地代码进行分配或预先分配一大块内存来自行管理堆，并根据此分离缓冲区。

> 注意：这些信息最初写于2012年初，现在Android使用了一个名为ART的不同运行时，它可能在相同程度上不会遇到这些问题。

## 移动到顶点缓冲区对象

现在我们已经回顾了使用客户端缓冲区，让我们继续讨论顶点缓冲区对象！首先，我们需要回顾几个非常重要的问题：

### 1. 缓冲区必须创建在一个有效的OpenGL上下文中

这似乎是一个明显的观点，但是它仅仅提醒你必须等到`onSurfaceCreated()`执行，并且你必须注意OpenGL ES调用是在GL线程上完成的。
看这个文档：[iOS OpenGL ES编程指南][16]，它可能是为iOS写的，但是OpenGL ES在Android的行为和这相同。

### 2. 顶点缓冲区对象使用不当会导致图形驱动程序崩溃

当你使用顶点缓冲对象时，需要注意传递的数据。不当的值将会导致OpenGL ES系统库或图形驱动库本地崩溃。在我的Nexus S上，一些游戏完全卡在我的手机上或导致手机重启，因为图形驱动因为他们的指令崩溃。并非所有的崩溃都会锁定您的设备，但至少您不会看到“此应用已停止工作”的对话框。您的活动将在没有警告的情况下重新启动，您将获得唯一的信息可能是日志中的本地调试跟踪。

## 上传顶点数据到GPU

要上传数据到GPU，我们需要像以前一样创建客户端缓冲区的相同步骤：

``` java
...
cubePositionsBuffer = ByteBuffer.allocateDirect(cubePositions.length * BYTES_PER_FLOAT)
.order(ByteOrder.nativeOrder()).asFloatBuffer();
cubePositionsBuffer.put(cubePositions).position(0);
...
```

一旦我们有了客户端缓冲区，我们就可以创建一个顶点缓冲区对象，并使用一下指令将数据从客户端内存上传到GPU：

``` java
// 首先，我们要尽可能的申请更多的缓冲区
// 这将为我们提供这些缓冲区的handle
final int buffers[] = new int[3];
GLES20.glGenBuffers(3, buffers, 0);

// 绑定这个缓冲区，将来的指令将单独影响此缓冲区
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, buffers[0]);

// 客户端内存中的数据转移到缓冲区
// 我们能在此次调动后释放客户端内存
GLES20.glBufferData(GLES20.GL_ARRAY_BUFFER, cubePositionsBuffer.capacity() * BYTES_PER_FLOAT,
    cubePositionsBuffer, GLES20.GL_STATIC_DRAW);

// 重要提醒：完成缓冲后，从缓冲区取消绑定
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);
```

一旦数据上传到了OpenGL ES，我们就可以释放这个客户端内存，因为我们不需要再继续保留它。这是[glBufferData][17]的解释：

- *GL_ARRAY_BUFFER：* 这个缓冲区包含顶点数据数组
- *cubePositionsBuffer.capacity() * BYTES_PER_FLOAT：* 这个缓冲区因该包含的字节数
- *cubePositionsBuffer：* 将要拷贝到这个顶点缓冲区对象的源
- *GL_STATIC_DRAW：* 这个缓冲区不会动态更新

我们对`glVertexAttribPointer`的调用看起来有点儿不同，因为最后一个参数现在是偏移量而不是指向客户端内存的指针：

``` java
// 传入位置信息
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, mCubePositionsBufferIdx);
GLES20.glEnableVertexAttribArray(mPositionHandle);
mGlEs20.glVertexAttribPointer(mPositionHandle, POSITION_DATA_SIZE, GLES20.GL_FLOAT, false, 0, 0);
...
```

像以前一样，我们绑定到缓冲区，然后启用顶点数组。由于缓冲区早已绑定，当从缓冲区读取数据时，我们仅需要告诉OpenGL开始的偏移。因为我们使用的特定的缓冲区，我们传入偏移量0。另请注意，我们使用自定义绑定来调用`glVertexAttribPointer`，因为官方SKD缺少此特定函数调用。

一旦我们用缓冲区绘制完成，我们应该解除它：

``` java
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);
```

当我们不想在保留缓冲区时，我们可以释放内存：

``` java
final int[] buffersToDelete = new int[] { mCubePositionsBufferIdx, mCubeNormalsBufferIdx,
    mCubeTexCoordsBufferIdx };
GLES20.glDeleteBuffers(buffersToDelete.length, buffersToDelete, 0);
```

## 打包顶点缓冲区对象

我们还可以使用单个缓冲区打包顶点缓冲区对象的所有顶点数据。打包顶点缓冲区的创建和上面相同，唯一的区别是我们从打包客户端缓冲区开始。打包缓冲区渲染也是一样的，除了我们需要传偏移量，就像在客户端内存中使用打包缓冲区一样：

``` java
final int stride = (POSITION_DATA_SIZE + NORMAL_DATA_SIZE + TEXTURE_COORDINATE_DATA_SIZE)
    * BYTES_PER_FLOAT;

// 传入位置信息
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, mCubeBufferIdx);
GLES20.glEnableVertexAttribArray(mPositionHandle);
mGlEs20.glVertexAttribPointer(mPositionHandle, POSITION_DATA_SIZE,
    GLES20.GL_FLOAT, false, stride, 0);

// 传入法线信息
GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, mCubeBufferIdx);
GLES20.glEnableVertexAttribArray(mNormalHandle);
mGlEs20.glVertexAttribPointer(mNormalHandle, NORMAL_DATA_SIZE,
    GLES20.GL_FLOAT, false, stride, POSITION_DATA_SIZE * BYTES_PER_FLOAT);
...
```

注意：偏移量需要以字节为单位指定。与之前一样解除绑定和删除缓冲区的相同注意事项也适用。

## 将顶点数据放到一起

这节课已构建了多立方体组成的立方体，每个面的立方体数量体相同。它将在1x1x1立方体和16x16x16立方体之间构建立方体。由于每个立方体共享相同的法线和纹理数据，因此在初始化客户端缓冲区时将重复复制此数据。所有立方体都将在同一个缓冲区对象中结束。

您可以查看课程中的代码并查看使用和不使用VBO，以及使用和不使用打包缓冲区进行渲染的示例。检查代码以查看如何处理一下某些操作：

- 通过`runOnUiThread()`将事件从OpenGL线程发布回UI主线程
- 异步生成顶点数据
- 处理内存溢出异常
- 我们移除了`glEnable(GL_TEXTURE_2D)`的调用，因为它实际在OpenGL ES 2是一个无效枚举。这是以前的固定写法延续下来的，在OpenGLES2中，这些东西由着色器处理，因此不需要使用`glEnable`或`glDisable`。
- 怎样使用不同的方式进行渲染，而不添加太多的if语句和条件。

## 进一步练习

您何时使用顶点缓冲区？什么时候从客户端内存传输数据更好？使用顶点缓冲区对象有哪些缺点？您将如何改进异步加载代码？

## 教程目录

- [OpenGL Android课程一：入门][1]
- [OpenGL Android课程二：环境光和漫射光][2]
- [OpenGL Android课程三：使用每片段照明][3]
- [OpenGL Android课程四：介绍纹理基础][4]
- [OpenGL Android课程五：介绍混合（Blending）][5]
- [OpenGL Android课程六：介绍纹理过滤][6]
- [OpenGL Android课程七：介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VBOs）][7]

## 打包教材

可以在Github下载本课程源代码：[下载项目][10]  
本课的编译版本也可以再Android市场下：[google play 下载apk][11]  
为了方便大家下载，“我”也编译了个apk，：[github download][9]

[1]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[4]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[5]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[6]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
[7]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Seven
[8]: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-opengl/20190309170313.png
[9]: https://github.com/xujiaji/LearnOpenGL/releases
[10]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[11]: https://market.android.com/details?id=com.learnopengles.android
[12]: https://en.wikipedia.org/wiki/Vertex_buffer_object
[13]: https://en.wikipedia.org/wiki/Pointer_(computer_programming)
[14]: https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glVertexAttribPointer.xml
[15]: https://stackoverflow.com/questions/6892676/android-bitmap-limit-preventing-java-lang-outofmemory
[16]: https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/Introduction/Introduction.html
[17]: http://www.learnopengles.com/android-lesson-seven-an-introduction-to-vertex-buffer-objects-vbos/GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER,%200);
