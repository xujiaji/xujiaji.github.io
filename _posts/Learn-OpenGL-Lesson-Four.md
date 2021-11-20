---
title:  OpenGL Android课程四：介绍纹理基础
date: 2019-02-08 19:26:29
author: xujiaji
thumbnail: blog/learn-opengl/20190211205340.jpg
categories:
 - OpenGL
tags:
 - Android
 - OpenGL
 - 学习
 - 翻译
---
> 翻译文

原文标题：Android Lesson Four: Introducing Basic Texturing
原文链接：<http://www.learnopengles.com/android-lesson-four-introducing-basic-texturing/>
<!-- more -->

---

# 介绍纹理基础

&nbsp;|&nbsp;
-|-
这是我们Android系列的第四个课程。<br>在本课中，我们将添加我们在[第三课][4]<br>中学到的内容，并学习如何添加纹理。<br>我们来看看如何从应用资源中获取一张<br>图片加载到OpenGLES中，并展示到<br>屏幕上。<br><br>跟着我一起来，你将马上明白纹理的<br>基本使用方式。|![screenshot][1]

## 前提条件

本系列每个课程构建都是以前一个课程为基础，这节课是[第三课][4]的扩展，因此请务必在继续之前复习该课程。

> 已下是本系列课程的前几课：

- [OpenGL Android课程一：入门][2]
- [OpenGL Android课程二：环境光和漫射光][3]
- [OpenGL Android课程三：使用每片段照明][4]

## 纹理基础

纹理映射的艺术（以及照明）是构建逼真的3D世界最重要的部分。没有纹理映射，一切都是平滑的阴影，看起来很人工，就像是90年代的老式控制台游戏。

第一个开始大量使用纹理的游戏，如Doom和Duke Nukem 3D，通过增加视觉冲击力，大大提升了游戏的真实感——如果在晚上玩可能会真的吓唬到我们。

> 这里我们来看有纹理和没有纹理的场景

&nbsp;|&nbsp;|&nbsp;
:-:|:-:|-
![pre-fragment lighting][5]<br>*每片段照明；<br>正方形四个顶点中心位置*|![added texture][6]<br>*添加了纹理；<br>正方形四个顶点中心位置*|看左边的图片，这个场景通过每像<br>素照明和着色点亮。这个场景看起<br>来非常平滑，现实生活中我们走进<br>一个房间有充满了光滑阴影的东西<br>就像是这个立方体。<br><br>在看右边的图片，同样的场景现在<br>纹理化了。环境光也增加了，因为<br>纹理的使用使整个场景变暗，也可<br>以看到纹理对侧面立方体的影响。<br>立方体具有和以前相同数量的多边<br>形，但它们有新纹理看起来更加详<br>细。<br><br>满足于那些好奇的人，这个纹理的<br>资源来自于[公共领域的资源][7]

## 纹理坐标

在OpengGL中，纹理坐标时常使用坐标(s,t)代替(x,y)。(s,t)表示纹理上的一个纹理元素，然后映射到多边形。另外需要注意这些纹理坐标和其他OpengGL坐标相似：t(或y)轴指向上方，所以值越高您走的越远。

大多数计算机图形，y轴指向下方。这意味着左上角是图片的原点(0,0)，并且y值向下递增。换句话说，OpenGL的坐标系和大多数计算机图形相反，这是您需要考虑到的。

|*OpenGL的纹理坐标系*|
|:-:|
|![coordiante][8]|

## 纹理映射基础

在本课中，我们将来看看常规2D纹理（`GL_TEXTURE_2D`）和红，绿，蓝颜色信息（`GL_RGB`）。OpenGL ES 也提供其他纹理模式让你做更多不同的特殊效果。我们将使用`GL_NEAREST`查看点采样，`GL_LINEAR`和MIP-映射将在后面的课程中讲解。

让我们一起来到代码部分，看看怎样开始在Android中使用基本的纹理。

### 顶点着色器

我们将采用上节课中的每像素照明着色器，并添加纹理支持。

> 这儿是新的变化：

``` glsl
attribute vec2 a_TexCoordinate;// 我们将要传入的每个顶点的纹理坐标信息
...
varying vec2 v_TexCoordinate;  // 这将会传入到片段着色器

void main()
{
   // 传入纹理坐标
   v_TexCoordinate = a_TexCoordinate;
   ...
}
```

在顶点着色器中，我们添加一个新的属性类型`vec2`（一个包含两个元素的数组），将用来放入纹理坐标信息。这将是每个顶点都有，同位置，颜色，法线数据一样。我们也添加了一个新的变量，它将通过三角形表面上的线性插值将数据传入片段着色器。

### 片段着色器

``` glsl
uniform sampler2D u_Texture;" +  // 传入纹理
...
varying vec2 v_TexCoordinate;" + // 插入的纹理坐标
void main()
{
   ...
   // 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
   float diffuse = max(dot(v_Normal, lightVector), 0.1);" +
   // 根据距离哀减光线
   diffuse = diffuse * (1.0 / (1.0 + (0.10 * distance * distance)));" +
   // 添加环境照明
   diffuse = diffuse + 0.3;" +
   // 颜色乘以亮度哀减和纹理值得到最终的颜色
   gl_FragColor = v_Color * diffuse * texture2D(u_Texture, v_TexCoordinate);" +
}
```

我们添加了一个新的常量类型`sampler2D`来表示实际纹理数据（与纹理坐标对应），
由定点着色器插值传入纹理坐标，我们再调用`texture2D(texture, textureCoordinate)`
得到纹理在当前坐标的值，我们得到这个值后再乘以其他项得到最终输出的颜色。

这种方式添加纹理会使整个场景变暗，因此我们还会稍微增强环境光照并减少光照哀减。

### 将一个图片加载到纹理

``` java
public static int loadTexture(final Context context, final int resourceId) {
    final int[] textureHandle = new int[1];

    GLES20.glGenTextures(1, textureHandle, 0);

    if (textureHandle[0] != 0) {
        final BitmapFactory.Options options = new BitmapFactory.Options();
        options.inScaled = false; // 没有预先缩放

        // 得到图片资源
        final Bitmap bitmap = BitmapFactory.decodeResource(context.getResources(), resourceId, options);

        // 在OpenGL中绑定纹理
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureHandle[0]);

        // 设置过滤
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_NEAREST);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_NEAREST);

        // 将位图加载到已绑定的纹理中
        GLUtils.texImage2D(GLES20.GL_TEXTURE_2D, 0, bitmap, 0);

        // 回收位图，因为它的数据已加载到OpenGL中
        bitmap.recycle();
    }

    if (textureHandle[0] == 0) {
        throw new RuntimeException("Error loading texture.");
    }
    return textureHandle[0];
}
```

这段代码将Android`res`文件夹中的图形文件读取并加载到OpenGL中，我会解释每一部分的作用。

我们首先需要告诉OpenGL去为我们创建一个新的`handle`，这个`handle`作为一个唯一标识，我们想在OpenGL中引用纹理时就会使用它。

``` glsl
final int[] textureHandle = new int[1];
GLES20.glGenTextures(1, textureHandle, 0);
```

这个OpenGL方法可以用来同时生成多个`handle`，这里我们仅生成一个。

因为我们这里只需要一个handle去加载纹理。首先，我们需要得到OpenGL能理解的纹理格式。
我们不能只从PNG或JPG提供原始数据，因为它不会理解。我们需要做的第一步是将图像文件解码为Android Bitmap对象：

``` glsl
final BitmapFactory.Options options = new BitmapFactory.Options();
options.inScaled = false; // 没有预先缩放
// 得到图片资源
final Bitmap bitmap = BitmapFactory.decodeResource(context.getResources(), resourceId, options);
```

默认情况下，Android会根据设备的分辨率和你放置图片的资源文件目录而预先缩放位图。我们不希望Android根据我们的情况对位图进行缩放，因此我们将`inScaled`设置为`false`

``` glsl
// 在OpenGL中绑定纹理
GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureHandle[0]);

// 设置过滤
GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_NEAREST);
GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_NEAREST);
```

然后我们绑定纹理，并设置几个参数，绑定一个纹理，并告诉OpenGL后续OpenGL调用需要这样过滤这个纹理。我们将默认过滤器设置为`GL_NEAREST`，这是最快，也是最粗糙的过滤形式。它所做的就是在屏幕的每个点选择最近的纹素，这可能导致图像伪像和锯齿。

- `GL_TEXTURE_MIN_FILTER` 这是告诉OpenGL在绘制小于原始大小（以像素为单位）的纹理时要应用哪种类型的过滤。
- `GL_TEXTURE_MAG_FILTER` 这是告诉OpenGL在放大纹理到原始大小时要应用哪种类型的过滤。

``` glsl
// 将位图加载到已绑定的纹理中
GLUtils.texImage2D(GLES20.GL_TEXTURE_2D, 0, bitmap, 0);

// 回收位图，因为它的数据已加载到OpenGL中
bitmap.recycle();
```

安卓有一个非常实用的功能可以直接将位图加载到OpenGL中。一旦您将资源读入Bitmap对象`GLUtils.texImage2D()`将负责其他事情，这个方法的签名：

``` java
public static void texImage2D (int target, int level, Bitmap bitmap, int border)
```

我们想要一个常规的2D位图，因此我们传入`GL_TEXTURE_2D`作为第一个参数。第二个参数用于MIP-映射，并允许您指定要在哪个级别使用的图像。我们这里没有使用MIP-映射，因此我们将传入0设置为默认级别。我们传入位图，由于我们没有使用边框，所以我们传入0。

然后原始位图对象调用`recycle()`，这提醒Android可以回收这部分内存。由于纹理已被加载到OpenGL，我们不需要继续保留这个副本。
是的，Android应用程序在执行垃圾收集的Dalvik VM下运行，但Bitmap对象包含驻留在native内存中的数据，如果你不明确的回收它们，它们需要几个周期来进行垃圾收集。
这意味着如果您忘记执行此操作，实际上可能会因内存不足错误而崩溃，即使您不再持有对位图的任何引用。

### 将纹理应用到我们的场景

首先，我们需要添加各种成员变量来持有我们纹理所需要的东西：

``` java
// 存放我们的模型数据在浮点缓冲区
private final FloatBuffer mCubeTextureCoordinates;

// 用来传入纹理
private int mTextureUniformHandle;

// 用来传入模型纹理坐标
private int mTextureCoordinateHandle;

// 每个数据元素的纹理坐标大小
private final int mTextureCoordinateDataSize = 2;

// 纹理数据
private int mTextureDataHandle;
```

我们基本上是需要添加新成员变量来跟踪我们添加到着色器的内容，以及保持对纹理的引用。

### 定义纹理坐标

我们在构造方法中定义我们的纹理坐标

``` java
// S, T （或 X， Y）
// 纹理坐标数据
// 因为图像Y轴指向下方（向下移动图片时值会增加），OpenGL的Y轴指向上方
// 我们通过翻转Y轴来调整它
// 每个面的纹理坐标都是相同的
final float[] cubeTextureCoordinateData =
        {
                // 正面
                0.0F, 0.0F,
                0.0F, 1.0F,
                1.0F, 0.0F,
                0.0F, 1.0F,
                1.0F, 1.1F,
                1.0F, 0.0F,
        };
...
```

这坐标数据看起来可能有点混乱。如果您返回去看第三课中点的位置是如何定义的，您将会发现我们为正方体每个面都定义了两个三角形。点的定义方式像下面这样：

``` c
（三角形1）
左上，
左下，
右上
（三角形2）
左下，
右下，
右上
```

纹理坐标和正面的位置坐标对应，但是由于Y轴翻转，Y轴指向和OpenGL的Y轴相反的方向。

> 看下图，实线坐标表示在OpenGL中正方体正面X，Y坐标。虚线表示翻转后的坐标，可以看出和上面定义的纹理坐标是一一对应的

![纹理坐标对应][9]

### 设置纹理

我们在`onSurfaceCreated()`方法中加载纹理

``` java
@Override
public void onSurfaceCreated(GL10 gl, EGLConfig config) {
    ...
    mProgramHandle = ShaderHelper.createAndLinkProgram(vertexShaderHandle, fragmentShaderHandle, "a_Position", "a_Color", "a_Normal", "a_TexCoordinate");
    ...
    // 加载纹理
    mTextureDataHandle = TextureHelper.loadTexture(mActivityContext, R.drawable.bumpy_bricks_public_domain);
```

我们传入一个新的属性`a_TexCoordinate`绑定到我们的着色器中，并且我们通过之前创建的`loadTexture()`方法加载着色器。

### 使用纹理

我们也需要在`onDrawFrame(GL10 gl)`方法中添加一些代码。

``` java
@Override
public void onDrawFrame(GL10 gl) {
    ...
    mTextureUniformHandle = GLES20.glGetUniformLocation(mProgramHandle, "u_Texture");
    mTextureCoordinateHandle = GLES20.glGetAttribLocation(mProgramHandle, "a_TexCoordinate");

    // 将纹理单元设置为纹理单元0
    GLES20.glActiveTexture(GLES20.GL_TEXTURE0);

    // 将纹理绑定到这个单元
    GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, mTextureDataHandle);

    // 通过绑定到纹理单元0，告诉纹理标准采样器在着色器中使用此纹理
    GLES20.glUniform1i(mTextureUniformHandle, 0);
```

我们得到着色器中的纹理数据和纹理坐标句柄。在OpenGL中，纹理能在着色之前，需要绑定到纹理单元。纹理单元是读取纹理并实际将它传入着色器的中，因此可以再屏幕上显示。不同的图形芯片有不同数量的纹理单元，因此在使用它们之前，您需要检查是否存在其他纹理单元。

首先，我们告诉OpenGL我们想设置使用的纹理单元到第一个单元，纹理单元0。然后自动绑定纹理到第一个单元，通过调用`glBindTexture()`。最后，我们告诉OpenGL，我们想将`mTextureUniformHandle`绑定到第一个纹理单元，它引用了片段着色器中`u_Texture`属性。

简而言之：

1. 设置纹理单元
2. 绑定纹理到这个单元
3. 将此单元指定给片段着色器中的纹理标准

根据需要重复多个纹理。

### 进一步练习

一旦您做到这儿，您就完成的差不多了！当然这这并没有您预期的那么糟糕...或者确实糟糕？😉作为下一个练习，尝试通过加载另一个纹理，将其绑定到另一个单元，并在着色器中使用它。

## 回顾

现在我们回顾一下所有的着色器代码，以及我们添加了一个新的帮助功能用来从资源目录读取着色器代码，而不是存储在java字符串中：

### 顶点着色器 all

``` glsl
uniform mat4 u_MVPMatrix;                      // 一个表示组合model、view、projection矩阵的常量
uniform mat4 u_MVMatrix;                       // 一个表示组合model、view矩阵的常量

attribute vec4 a_Position;                     // 我们将要传入的每个顶点的位置信息
attribute vec4 a_Color;                        // 我们将要传入的每个顶点的颜色信息
attribute vec3 a_Normal;                       // 我们将要传入的每个顶点的法线信息
attribute vec2 a_TexCoordinate;                // 我们将要传入的每个顶点的纹理坐标信息

varying vec3 v_Position;
varying vec4 v_Color;
varying vec3 v_Normal;
varying vec2 v_TexCoordinate;                  // 这将会传入到片段着色器

// 顶点着色器入口点
void main()
{
   // 传入纹理坐标
   v_TexCoordinate = a_TexCoordinate;
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

### 片段着色器 all

``` glsl
precision mediump float; //我们将默认精度设置为中等，我们不需要片段着色器中的高精度
uniform sampler2D u_Texture;  // 传入纹理
uniform vec3 u_LightPos; // 光源在眼睛空间的位置
varying vec3 v_Position; // 插入的位置
varying vec4 v_Color; // 插入的位置颜色
varying vec3 v_Normal; // 插入的位置法线
varying vec2 v_TexCoordinate; // 插入的纹理坐标
void main()  // 片段着色器入口
{
   // 将用于哀减
   float distance = length(u_LightPos - v_Position);
   // 获取从光源到顶点方向的光线向量
   vec3 lightVector = normalize(u_LightPos - v_Position);
   // 计算光线矢量和顶点法线的点积，如果法线和光线矢量指向相同的方向，那么它将获得最大的照明
   float diffuse = max(dot(v_Normal, lightVector), 0.1);
   // 根据距离哀减光线
   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));
   // 添加环境照明
   diffuse = diffuse + 0.3;
   // 颜色乘以亮度哀减和纹理值得到最终的颜色
   gl_FragColor = v_Color * diffuse * texture2D(u_Texture, v_TexCoordinate);
}
```

### 怎样从raw资源目录中读取文本？

``` java
public class RawResourceReader {
    public static String readTextFileFromRawResource(final Context context, final int resurceId) {
        final InputStream inputStream = context.getResources().openRawResource(resurceId);
        final InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
        final BufferedReader bufferedReader = new BufferedReader(inputStreamReader);

        String nextLine;

        final StringBuilder body = new StringBuilder();

        try {
            while ((nextLine = bufferedReader.readLine()) != null) {
                body.append(nextLine).append('\n');
            }
        } catch (IOException e) {
            return null;
        } finally {
            try {
                bufferedReader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return body.toString();
    }
}
```

## 教程目录

- [OpenGL Android课程一：入门][2]
- [OpenGL Android课程二：环境光和漫射光][3]
- [OpenGL Android课程三：使用每片段照明][4]
- [OpenGL Android课程四：介绍纹理基础][10]
- [OpenGL Android课程五：介绍混合（Blending）][13]
- [OpenGL Android课程六：介绍纹理过滤][15]
- [OpenGL Android课程七：介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VOB）][16]

## 打包教材

可以在Github下载本课程源代码：[下载项目][11]  
本课的编译版本也可以再Android市场下：[google play 下载apk][12]  
“我”也编译了个apk，方便大家下载：[github download][14]

[1]: blog/learn-opengl/20190208193740.png
[2]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[3]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[4]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[5]: blog/learn-opengl/20190208215006.png
[6]: blog/learn-opengl/20190208215108.png
[7]: http://pdtextures.blogspot.com/2008/03/first-set.html
[8]: blog/learn-opengl/20190208225905.png
[9]: blog/learn-opengl/20190211153435.jpg
[10]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[11]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[12]: https://market.android.com/details?id=com.learnopengles.android
[13]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[14]: https://github.com/xujiaji/LearnOpenGL/releases
[15]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
[16]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Seven
