---
title: OpenGL Android课程八：介绍Index Buffer Objects（索引缓冲对象，简称：IBO）
date: 2019-03-28 13:53:50
author: xujiaji
thumbnail:
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---

> 翻译文

原文标题：Android Lesson Eight: An Introduction to Index Buffer Objects (IBOs)
原文链接：<http://www.learnopengles.com/android-lesson-eight-an-introduction-to-index-buffer-objects-ibos/>
<!-- more -->

---

# 介绍Index Buffer Objects（索引缓冲对象，简称：IBO）

|||
|-|-|
|在上节课，我们学习了[怎样在Android中使用顶点缓冲对象][7]<br>我们了解了客户端内存和GPU专用内存之间的区别，<br>以及将纹理、位置、法线数据分别存储在单独的缓冲区<br>和共用一个缓冲区的区别。<br><br>这节课我们来学习索引缓冲对象，并看看怎样在<br>实际案例中使用它们。以下是我们要介绍的内容：<br><br>⭕️仅使用顶点缓冲对象和顶点缓冲对象<br>索引缓冲对象一起使用的区别<br>⭕️如何使用退化三角形来加入共同的三角形条带，<br>并在单个渲染的调用渲染整个高度图|![screenshot][9]|

让我们开始讨论顶点缓冲对象和索引缓冲对象的不同点：

## 顶点缓冲对象和索引缓冲对象

在上节课中，我们知道了一个顶点缓冲对象仅是一个顶点数据数组，它直接被OpenGL渲染。我们可以为每个属性分配缓冲区，例如位置和颜色，我们也能使用一个缓冲区将所有数据交错在一起。[顶点数据最佳实践][10]建议交错数据并确保它与4字节边界对齐，以获得更好的性能。

当我们一遍又一遍地使用许多相同的顶点时，顶点缓冲区的缺点就出现了。例如，高度图可以分解为一系列三角形条带。因为每个邻近的条带共享一行顶点，使用顶点缓冲，我们最终会重复很多顶点。

![vbo][11]

您可以看到一个顶点缓冲对象包含了两行三角形条带。上面展示了当使用`glDrawArrays(GL_TRIANGLE_STRIP, …)`绘制时，展示了顶点的显示顺序，也显示出三角形通过这些顶点的定义。在这个例子中，我们假设每行三角形都单独对`glDrawArrays()`调用。每个顶点包含的数据如下所示：

``` java
vertexBuffer = {
    // 顶点1位置
    0, 0, 0,
    // 颜色
    1,1,1
    // 法线
    0,0,1,
    // 顶点2位置
    1, 0, 0,
    ...
}
```

正如您所见，顶点中间的行需要发送两次，并且发生在高度图的每一个额外行。随着我们高度图变大，我们的顶点缓冲最后会重复大量的位置、颜色和法线数据并且消耗许多额外内存。

我们怎样才能完善这种情形的事情？我们可以使用索引缓冲对象代替在顶点缓冲的重复顶点，我们将定义每个顶点一次，仅一次。我们将使用偏移引用这些顶点到顶点缓冲区，并且当我们需要重用一个顶点时，我们将重复偏移，而不是整个顶点。下面是新顶点缓冲区的一个可视化插图：

![new vertex buffer][12]

注意我们的顶点不再连接成三角形，我们不再直接传入顶点缓冲对象，我们将使用一个索引缓冲区将顶点捆在一起。这个索引缓冲区将仅包含顶点缓冲区对象的偏移量。如果我们想要使用上面的缓冲区绘制一个三角形，我们的索引缓冲区将包含如下数据：

``` java
indexBuffer = {
    1, 6, 2, 7, 3, 8, ...
}
```

这就是我们将所有东西联系在一起的方式，当我们重复顶点中间那行时，我们仅重复这些数字来代替整个数据块的重复。我们调动`glDrawElements(GL_TRIANGLE_STRIP,…)`来绘制索引缓冲。

## 三角形条带和退化三角形合并

[1]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[4]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[5]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[6]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
[7]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Seven
[8]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Eight
[9]: blog/learn-opengl/20190328142011.png
[10]: https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/TechniquesforWorkingwithVertexData/TechniquesforWorkingwithVertexData.html
[11]: blog/learn-opengl/vbo.png
[12]: blog/learn-opengl/20190422185642.png
