---
title: OpenGL Android课程一：入门
date: 2019-01-21 16:10:46
author: xujiaji
thumbnail: blog/learn-opengl/6093CCF8-F7C1-4F4E-A668-C9E76783063F.png
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
原文链接：<http://www.learnopengles.com/android-lesson-one-getting-started/>
<!-- more -->

---

这是在Android中使用OpenGL ES2的第一个教程。这一课中，我们将一步一步跟随代码，学习如何创建一个OpenGL ES 2并绘制到屏幕上。
我们还将了解什么是着色器，它们如何工作，以及怎样使用矩阵将场景转换为您在屏幕上看到的图像。最后，您需要在清单文件中添加您正在使用OpenGL ES 2的说明，以告知Android应用市场支持的设备可见。

# 入门

我们将过一道下面所有的代码并且解释每一部分的作用。您可以跟着拷贝每一处的代码片段来创建您自己的项目，您也可以在文章末尾下载这个已完成的项目。
在开发工具（如：Android Studio）中创建您的Android项目，名字不重要，这里由于这个课程我将`MainActivity`更名为`LessonOneActivity`。

> 我们来看这段代码：

``` java
/** 保留对GLSurfaceView的引用*/
private GLSurfaceView mGLSurfaceView;
```

这个[GLSurfaceView][1]是一个特别的View，它为我们管理OpenGL界面并且将它绘制在Android View系统。它还添加了许多功能，使其更易于使用OpenGL，包括下面等等：

- 它为OpenGL提供一个专用的着色线程，因此主线程不会停懈
- 它支持连续或按需渲染
- 它使用[EGL][2] (OpenGL和底层系统窗口之间的接口)来处理屏幕设置

> `GLSurfaceView`使得在Android中设置和使用OpenGL相对轻松

``` java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    mGLSurfaceView = new GLSurfaceView(this);
    //检测系统是否支持OpenGL ES 2.0
    final ActivityManager activityManager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
    final ConfigurationInfo configurationInfo = activityManager.getDeviceConfigurationInfo();
    final boolean supportsEs2 = configurationInfo.reqGlEsVersion >= 0x20000;

    if (supportsEs2) {
        // 请求一个OpenGL ES 2.0兼容的上下文
        mGLSurfaceView.setEGLContextClientVersion(2);
        // 设置我们的Demo渲染器，定义在后面讲
        mGLSurfaceView.setRenderer(new LessonOneRenderer());
    } else {
        // 如果您想同时支持ES 1.0和2.0的话，这里您可以创建兼容OpenGL ES 1.0的渲染器
        return;
    }
    setContentView(mGLSurfaceView);
}
```

在`onCreate()`方法中是我们创建OpenGL上下文以及一切开始发生的重要部分。
在我们的`onCreate()`方法中,在调用`super.onCreate()`后我们首先创建了`GLSurfaceView`实例。
然后我们需要弄清楚系统是否支持OpenGL ES 2.为此，我们获得一个`ActivityManager`实例，它允许我们与全局系统状态进行交互。
然后我们使用它获取设备配置信息，它将告诉我们设备是否支持OpenGL ES 2。
我们也可以通过传入不同的渲染器来支持OpenGL ES 1.x，尽管因为API不同，我们需要编写不同的代码。对于本课我们仅仅关注支持OpenGL ES 2。

一旦我们知道设备是否支持OpenGL ES 2，我们告诉`GLSurfaceView`兼容OpenGL ES 2，然后传入我们的自定义渲染器。无论何时调整界面或绘制新帧，系统都会调用此渲染器。

最后，我们调用`setContentView()`设置GLSurfaceView为显示内容，它告诉Android这个活动内容因该被我们的OpenGL界面填充。要入门OpenGL，就是这么简单。

``` java
@Override
protected void onResume() {
    super.onResume();
    //Activity 必须在onResume中调用GLSurfaceView的onResume方法
    mGLSurfaceView.onResume();
}

@Override
protected void onPause() {
    super.onPause();
    //Activity 必须在onPause中调用GLSurfaceView的onPause方法
    mGLSurfaceView.onPause();
}
```

`GLSurfaceView`要求我们在Activity`onResume()`和`onPause()`的父方法被调用后分别调用它的`onResume()`和`onPause()`方法。我们在此添加调用以完善我们的Activity。

## 可视化3D世界

在这部分，我们来看怎样让OpenGL ES 2工作，以及我们如何在屏幕上绘制东西。
在Activity中我们传入自定义的[GLSurfaceView.Renderer][3]到`GLSurfaceView`，它将在这里定义。
这个渲染器有三个重要的方法，每当系统事件发生时，它们将会自动被调用：

> *public void onSurfaceCreated(GL10 gl, EGLConfig config)*

当界面第一次被创建时调用，如果我们失去界面上下文并且之后由系统重建，也会被调用。

> *public void onSurfaceChanged(GL10 gl, int width, int height)*

每当界面改变时被调用；例如，从纵屏切换到横屏，在创建界面后也会被调用。

> *public void onDrawFrame(GL10 gl)*

每当绘制新帧时被调用。

您可能注意到`GL10`的实例被传入名字是`gl`。当使用OpengGL ES 2绘制时，我们不能使用它；
我们使用`GLES20`类的静态方法来代替。这个`GL10`参数仅仅是在这里，因为相同的接口被使用在OpenGL ES 1.x。

> 在我们的渲染器可以显示任何内容之前，我们需要有些东西去显示。在OpenGL ES 2，我们通过制定数字数组传递内容。这些数字可以表示位置、颜色或任何我们需要的。在这个Demo中，我们将显示三个三角形。

``` java
// 新类成员
private final FloatBuffer mTriangle1Verticels;
private final FloatBuffer mTriangle2Verticels;
private final FloatBuffer mTriangle3Verticels;

/** 每个Float多少字节*/
private final int mBytePerFloat = 4;

/**
 * 初始Model数据
 */
public LessonOneRenderer() {
    // 这个三角形是红色，蓝色和绿色组成
    final float[] triangle1VerticesData = {
        // X, Y, Z,
        // R, G, B, A
        -0.5F, -0.25F, 0.0F,
        1.0F, 0.0F, 0.0F, 1.0F,

        0.5F, -0.25F, 0.0F,
        0.0F, 0.0F, 1.0F, 1.0F,

        0.0F, 0.559016994F, 0.0F,
        0.0F, 1.0F, 0.0F, 1.0F
    };
    ...
    // 初始化缓冲区
    mTriangle1Verticels = ByteBuffer.allocateDirect(triangle1VerticesData.length * mBytePerFloat).order(ByteOrder.nativeOrder()).asFloatBuffer();
    ...
    mTriangle1Verticels.put(triangle1VerticesData).position(0);
    ...
}
```

那么，这些是什么意思？如果您曾经使用过OpenGL 1， 您可能会习惯这样做：

``` java
glBegin(GL_TRIANGLES);
glVertex3f(-0.5f, -0.25f, 0.0f);
glColor3f(1.0f, 0.0f, 0.0f);
...
glEnd();
```

这种方法在OpenGL ES 2中不起作用。我们不是通过一堆方法调用来定义点，而是定义一个数组。让我们再来看看我们这个数组：

``` java
final float[] triangle1VerticesData = {
                // X, Y, Z,
                // R, G, B, A
                -0.5f, -0.25f, 0.0f,
                1.0f, 0.0f, 0.0f, 1.0f,
                ...
};
```

上面展示的代表三角形的一个点。我们已设置好前三个数字代表位置（X,Y,Z），随后的四个数字代表颜色（红，绿，蓝，透明度）。
您不必太担心如何定义这个数组；只要记住当我们想绘制东西在OpenGL ES 2时，我们需要以块的形式传递数据，而不是一次传递一个。

### 了解缓冲区

``` java
// 初始化缓冲区
mTriangle1Verticels = ByteBuffer.allocateDirect(triangle1VerticesData.length * mBytePerFloat).order(ByteOrder.nativeOrder()).asFloatBuffer();
...
```

我们在Android上使用Java进行编码，但OpengGL ES 2底层实现其实使用C语言编写的。
在我们将数据传递给OpenGL之前，我们需要将其转换成它能理解的形式。
Java和native系统可能不会以相同的顺序存储它们的字节，因此我们使用一个特殊的缓冲类并创建一个足够大的`ByteBuffer`来保存我们的数据，并告诉它使用native字节顺序存储数据。
然后我们将它转换成`FloatBuffer`，以便我们可以使用它来保存浮点数据。
最后，我们将数组复制到缓冲区。

这个缓冲区的东西看起来可能很混乱，单请记住，在将数据传递给OpenGL之前，我们需要做一个额外的步骤。我们现在的缓冲区已准备好可以用于将数据传入OpenGL。

**另外，[float缓冲区在Froyo上很慢][4],在Gingerbread上缓慢，因此您可能不希望经常更换它们。**

### 理解矩阵

``` java
// new class 定义

/**
 * 存储view矩阵。可以认为这是一个相机，我们通过相机将世界空间转换为眼睛空间
 * 它定位相对于我们眼睛的东西
 */
private float[] mViewMatrix = new float[16];

@Override
public void onSurfaceCreated(GL10 gl, EGLConfig config) {
    // 设置背景清理颜色为灰色
    GLES20.glClearColor(0.5F, 0.5F, 0.5F, 0.5F);

    // 将眼睛放到原点之后
    final float eyeX = 0.0F;
    final float eyeY = 0.0F;
    final float eyeZ = 1.5F;

    // 我们的眼睛望向哪
    final float lookX = 0.0F;
    final float lookY = 0.0F;
    final float lookZ = -5.0F;

    // 设置我们的向量，这是我们拿着相机时头指向的方向
    final float upX = 0.0F;
    final float upY = 1.0F;
    final float upZ = 0.0F;

    // 具体场景：把手机放桌子上，然后我们去看屏幕里面的东西

    // 设置view矩阵，可以说这个矩阵代表相机的位置
    // 注意：在OpenGL 1中使用ModelView matrix，这是一个model和view矩阵的组合。
    //在OpenGL2中，我们选择分别跟踪这些矩阵
    Matrix.setLookAtM(mViewMatrix, 0, eyeX, eyeY, eyeZ, lookX, lookY, lookZ, upX, upY, upZ);
    ...
}
```

另一个有趣的话题是矩阵！无论您何时进行3D编程，这些都将成为您最好的朋友。因此，您需要很好的了解他们。

当我们的界面被创建，我们第一件事情是设置清理颜色为灰色。alpha部分也设置为灰色，但在我们本课程中没有进行alpha混合，因此该值未使用。我们只需要设置一次清理颜色，之后我们不会更改它。

我们第二件事情是设置view矩阵。我们使用了几个不同种类的矩阵，它们都做了些重要的事情：

1. model（模型）矩阵，该矩阵用于在“世界”中的某处放置模型。例如，您有一个模型车，你想将它放置在东边一千米处，您将使用矩阵模型来做这件事。
2. view （视图)矩阵，该矩阵代表相机。如果我们想查看位于东边一千米处的车，我们也需要向东移动一千米（另一种思考方式是我们保持静止，世界向西移动一千米）。我们使用视图矩阵来做到这点。
3. projection（投影)矩阵。由于我们的屏幕是平面的，我们需要进行最后的转换，将我们的视图“投影”到我们的屏幕上并获得漂亮的3D视角。这就是投影矩阵的用途

可以在[SongHo的OpenGL教程][5]中找到很好的解释。我建议您阅读几次直到您把握好这个想法为止；别担心，我也阅读了它好几次！

在OpenGL 1中，模型和视图矩阵被组合并且假设了摄像机处于(0,0,0)坐标并面向Z轴方向。

我们不需要手动构建这些矩阵，Android有一个Matrix帮助类，它能为我们做繁重的工作。这里，我为摄像机创建了一个视图矩阵，它位于原点后，朝向远处。

### 定义vertex（顶点）和fragment（片段）着色器

``` java
final String vertexShader =
        "uniform mat4 u_MVPMatrix;    \n" + // 一个表示组合model、view、projection矩阵的常量
        "attribute vec4 a_Position;   \n" + // 我们将要传入的每个顶点的位置信息
        "attribute vec4 a_Color;      \n" + // 我们将要传入的每个顶点的颜色信息

        "varying vec4 v_Color;        \n" + // 他将被传入片段着色器

        "void main()                  \n" + // 顶点着色器入口
        "{                            \n" +
        "   v_Color = a_Color;        \n" + // 将颜色传递给片段着色器
                                            // 它将在三角形内插值
        "   gl_Position = u_MVPMatrix \n" + // gl_Position是一个特殊的变量用来存储最终的位置
        "               * a_Position  \n" + // 将顶点乘以矩阵得到标准化屏幕坐标的最终点
        "}                            \n";
```

在OpenGL ES 2中任何我们想展示在屏幕中的东西都必须先经过顶点和片段着色器，还好这些着色器并不像他们看起来的那么复杂。顶点着色器在每个顶点执行操作，并把这些操作的结果使用在片段着色器做额外的每像素计算。

每个着色器基本由输入（input）、输出（output）和一个程序（program）组成。
首先我们定义一个统一（uniform），它是一个包含所有变换的组合矩阵。它是所有顶点的常量，用于将它们投影到屏幕上。
然后我们定义了位置和颜色属性（attribute），这些属性将从我们之前定义的缓存区中读入，并指定每个顶点的位置和颜色。
接着我们定义了一个变量（varying），它负责在三角形中插值并传递到片段着色器。当它运行到片段着色器，它将为每个像素持有一个插值。

假设我们定义了一个三角形每个点都是红色、绿色和蓝色，我们调整它的大小让它占用10像素屏幕。当片段着色器运行时，它将为每像素包含一个不同的变量（varying）颜色。在某一点上，变量（varying）将是红色，但是在红色和蓝色之间它可能是更紫的颜色。

除了设置颜色，我们还告诉OpenGL顶点在屏幕上的最终位置。然后我们定义片段着色器：

``` java
final String fragmentShader =
        "precision mediump float;       \n" + // 我们将默认精度设置为中等，我们不需要片段着色器中的高精度
        "varying vec4 v_Color;          \n" + // 这是从三角形每个片段内插的顶点着色器的颜色
        "void main()                    \n" + // 片段着色器入口
        "{                              \n" +
        "   gl_FragColor = v_Color;     \n" + // 直接将颜色传递
        "}                              \n";
```

这是个片段着色器，它会将东西放到屏幕上。在这个着色器中，我们得到的变量（varying）颜色来自顶点着色器，然后将它直接传递给OpenGL。该点已按像素插值，因为片段着色器将针对每个将要绘制的像素点运行。

更多信息：[OpenGL ES 2 API快速参考卡][6]

### 将着色器加载到OpenGL

``` java
// 加载顶点着色器
int vertexShaderHandle = GLES20.glCreateShader(GLES20.GL_VERTEX_SHADER);
if (vertexShaderHandle != 0) {
    // 传入顶点着色器源代码
    GLES20.glShaderSource(vertexShaderHandle, vertexShader);
    // 编译顶点着色器
    GLES20.glCompileShader(vertexShaderHandle);

    // 获取编译状态
    final int[] compileStatus = new int[1];
    GLES20.glGetShaderiv(vertexShaderHandle, GLES20.GL_COMPILE_STATUS, compileStatus, 0);

    // 如果编译失败则删除着色器
    if (compileStatus[0] == 0) {
        GLES20.glDeleteShader(vertexShaderHandle);
        vertexShaderHandle = 0;
    }
}

if (vertexShaderHandle == 0) {
    throw new RuntimeException("Error creating vertex shader.");
}
```

首先，我们创建一个着色器对象。如果成功，我们将得到这个对象的引用。
然后，我们使用这个引用传入着色器源码然后编译它。
我们可以从OpenGL获取编译是否成功的状态，如果失败我们可以使用`GLES20.glGetShaderInfoLog(shader)`找到原因。我们按照相同的步骤加载片段着色器。

### 将顶点和片段着色器链接到一个程序中

``` java
// 创建一个程序对象并将引用放进去
int programHandle = GLES20.glCreateProgram();
if (programHandle != 0) {
    // 绑定顶点着色器到程序对象中
    GLES20.glAttachShader(programHandle, vertexShaderHandle);
    // 绑定片段着色器到程序对象中
    GLES20.glAttachShader(programHandle, fragmentShaderHandle);
    // 绑定属性
    GLES20.glBindAttribLocation(programHandle, 0, "a_Position");
    GLES20.glBindAttribLocation(programHandle, 1, "a_Color");
    // 将两个着色器连接到程序
    GLES20.glLinkProgram(programHandle);
    // 获取连接状态
    final int[] linkStatus = new int[1];
    GLES20.glGetProgramiv(programHandle, GLES20.GL_LINK_STATUS, linkStatus, 0);
    // 如果连接失败，删除这程序
    if (linkStatus[0] == 0) {
        GLES20.glDeleteProgram(programHandle);
        programHandle = 0;
    }
}

if (programHandle == 0) {
    throw new RuntimeException("Error creating program.");
}
```

在我们使用顶点和片段着色器之前，我们需要将它们绑定到一个程序中，它连接了顶点着色器的输出和片段着色器的输入。这也是让我们从程序传递输入并使用着色器绘制形状的原因。

我们创建一个程序对象，如果成功绑定着色器。我们想要将位置和颜色作为属性传递进去，因此我们需要绑定这些属性。然后我们将着色器连接到一起。

``` java
// 新类成员
/** 这将用于传递变换矩阵*/
private int mMVPMatrixHandle;
/** 用于传递model位置信息*/
private int mPositionHandle;
/** 用于传递模型颜色信息*/
private int mColorHandle;
@Override
public void onSurfaceCreated(GL10 gl, EGLConfig config) {
    ...
    // 设置程序引用，这将在之后传递值到程序时使用
    mMVPMatrixHandle = GLES20.glGetUniformLocation(programHandle, "u_MVPMatrix");
    mPositionHandle = GLES20.glGetAttribLocation(programHandle, "a_Position");
    mColorHandle = GLES20.glGetAttribLocation(programHandle, "a_Color");

    // 告诉OpenGL渲染的时候使用这个程序
    GLES20.glUseProgram(programHandle);
}
```

在我们成功连接程序后，我们还要完成几个任务，以便我们能实际使用它。
第一个任务是获取引用，因为我们要传递数据到程序中。
然后我们要告诉OpenGL在绘制时使用我们这个程序。
由于本课我们仅使用了一个程序，我们可以将它放到`onSurfaceCreated()`方法中而不是`onDrawFrame()`

### 设置透视投影

``` java
// 新类成员
// 存放投影矩阵，用于将场景投影到2D视角
private float[] mProjectionMatrix = new float[16];

@Override
public void onSurfaceChanged(GL10 gl, int width, int height) {
    // 设置OpenGL界面和当前视图相同的尺寸
    GLES20.glViewport(0, 0, width, height);

    // 创建一个新的透视投影矩阵，高度保持不变，而高度根据纵横比而变换
    final float ratio = (float) width / height;
    final float left = -ratio;
    final float right = ratio;
    final float bottom = -1.0F;
    final float top = 1.0F;
    final float near = 1.0F;
    final float far = 10.0F;

    Matrix.frustumM(mProjectionMatrix, 0, left, right, bottom, top, near, far);
}
```

`onSurfaceChanged()`方法至少被调用一次，每当界面改变也会被调用。因为我们需要每当界面改变的时候重置投影矩阵，那么`onSurfaceChanged()`方法中是个理想的地方。

### 绘制东西到屏幕上！

``` java
// 新类成员
// 存放模型矩阵，该矩阵用于将模型从对象空间（可以认为每个模型开始都位于宇宙的中心）移动到世界空间
private float[] mModelMatrix = new float[16];

@Override
public void onDrawFrame(GL10 gl) {
    GLES20.glClear(GLES20.GL_DEPTH_BUFFER_BIT | GLES20.GL_COLOR_BUFFER_BIT);

    // 每10s完成一次旋转
    long time = SystemClock.uptimeMillis() % 10000L;
    float angleDegrees = (360.0F / 10000.0F) * ((int)time);

    // 画三角形
    Matrix.setIdentityM(mModelMatrix, 0);
    Matrix.rotateM(mModelMatrix, 0, angleDegrees, 0.0F, 0.0F, 1.0F);
    drawTriangle(mTriangle1Verticels);
    ...
}
```

这是实际显示在屏幕上的内容。我们清理屏幕，因此不会得到任何奇怪的[镜像效应][7]影响，我们希望我们的三角形在屏幕上能有平滑的动画，通常使用时间而不是帧率更好。

> 实际绘制在`drawTriangle()`方法中完成

``` java
// 新的类成员
/** 为最终的组合矩阵分配存储空间，这将用来传入着色器程序*/
private float[] mMVPMatrix = new float[16];

/** 每个顶点有多少字节组成，每次需要迈过这么一大步（每个顶点有7个元素，3个表示位置，4个表示颜色，7 * 4 = 28个字节）*/
private final int mStrideBytes = 7 * mBytePerFloat;

/** 位置数据偏移量*/
private final int mPositionOffset = 0;

/** 一个元素的位置数据大小*/
private final int mPositionDataSize = 3;

/** 颜色数据偏移量*/
private final int mColorOffset = 3;

/** 一个元素的颜色数据大小*/
private final int mColorDataSize = 4;

/**
 * 从给定的顶点数据中绘制一个三角形
 * @param aTriangleBuffer 包含顶点数据的缓冲区
 */
private void drawTriangle(FloatBuffer aTriangleBuffer) {
    aTriangleBuffer.position(mPositionOffset);
    GLES20.glVertexAttribPointer(
            mPositionHandle, mPositionDataSize, GLES20.GL_FLOAT, false,
            mStrideBytes, aTriangleBuffer);

    GLES20.glEnableVertexAttribArray(mPositionHandle);

    // 传入颜色信息
    aTriangleBuffer.position(mColorOffset);
    GLES20.glVertexAttribPointer(mColorHandle, mColorDataSize, GLES20.GL_FLOAT, false,
            mStrideBytes, aTriangleBuffer);

    GLES20.glEnableVertexAttribArray(mColorHandle);

    // 将视图矩阵乘以模型矩阵，并将结果存放到MVP Matrix（model * view）
    Matrix.multiplyMM(mMVPMatrix, 0, mViewMatrix, 0, mModelMatrix, 0);

    // 将上面计算好的视图模型矩阵乘以投影矩阵，并将结果存放到MVP Matrix（model * view * projection）
    Matrix.multiplyMM(mMVPMatrix, 0, mProjectionMatrix, 0, mMVPMatrix, 0);

    GLES20.glUniformMatrix4fv(mMVPMatrixHandle, 1, false, mMVPMatrix, 0);
    GLES20.glDrawArrays(GLES20.GL_TRIANGLES, 0, 3);

}
```

您还记得我们最初创建渲染器时定义的那些缓冲区吗？我们终于可以使用它们了。
我们需要使用`GLES20.glVertexAttribPointer()`来告诉OpenGL怎样使用这些数据。
> 我们来看第一个使用

``` java
aTriangleBuffer.position(mPositionOffset);
GLES20.glVertexAttribPointer(
        mPositionHandle, mPositionDataSize, GLES20.GL_FLOAT, false,
        mStrideBytes, aTriangleBuffer);
GLES20.glEnableVertexAttribArray(mPositionHandle);
```

我们设置缓冲区的位置偏移，它位于缓冲区的开头。然后我们告诉OpenGL使用这些数据并将其提供给顶点着色器并将其应用到位置属性（a_Position）。我们也需要告诉OpenGL每个顶点或迈幅之间有多少个元素。

> 注意：迈幅（Stride）需要定义为字节（byte），尽管每个顶点之间我们有7个元素（3个是位置，4个是颜色），但我们事实上有28个字节，因为每个浮点数（float）就是4个字节（byte）。忘记此步骤您可能没有任何错误，但是你会想知道为什么您的屏幕上看不到任何内容。

最终，我们使用了顶点属性，往下我们使用了下一个属性。再往后点我们构建一个组合矩阵，将点投影到屏幕上。我们也可以在顶点着色器中执行此操作，但是由于它只需要执行一次我们也可以只缓存结果。
我们使用`GLES20.glUniformMatrix4fv()`方法将最终的矩阵传入顶点着色器。
`GLES20.glDrawArrays()`将我们的点转换为三角形并将其绘制在屏幕上。

## 总结

呼呼！这是重要的一课，如果您完成了本课，感谢您！
我们学习了怎样创建OpenGL上下文，传入形状数据，加载顶点和片段着色器，设置我们的转换矩阵，最终放在一起。
如果一切顺利，您因该看到了类似下面的截屏。
![screenshot](blog/learn-opengl/20190122233309.png)

这一课有很多需要消化的内容，您可能需要多次阅读这些步骤才能理解它。
OpenGL ES 2需要更多的设置才能开始，但是一旦您完成了这个过程几次，您就会记住这个流程。

## 在Android市场上发布

当开发的应用我们不想在无法运行这些应用程序的人在市场上看到它们，否则当应用程序在其设备上崩溃时，我们可能会收到大量糟糕的评论和评分。
要防止OpenGL ES 2 应用程序出现在不支持它的设备上，你可以在清单文件中添加：

``` xml
<uses-feature
    android:glEsVersion="0x00020000"
    android:required="true" />
```

这告诉市场您的app需要有OpenGL ES 2支持，不支持的设备将会隐藏您的app。

## 进一步探索

尝试更改动画速度，顶点或颜色，看看会发生什么！
可以在Github下载本课程源代码：[下载项目][8]  
本课的编译版本也可以再Android市场下：[google play 下载apk][9]  
“我”也编译了个apk，方便大家下载：[github download][15]

## 教程目录

- [OpenGL Android课程一：入门][10]
- [OpenGL Android课程二：环境光和漫射光][11]
- [OpenGL Android课程三：使用每片段照明][12]
- [OpenGL Android课程四：介绍纹理基础][13]
- [OpenGL Android课程五：介绍混合（Blending）][14]
- [OpenGL Android课程六：介绍纹理过滤][16]
- [OpenGL Android课程七：介绍Vertex Buffer Objects（顶点缓冲区对象，简称：VOB）][17]

[1]: http://developer.android.com/reference/android/opengl/GLSurfaceView.html
[2]: https://en.wikipedia.org/wiki/EGL_(API)
[3]: http://developer.android.com/reference/android/opengl/GLSurfaceView.Renderer.html
[4]: https://issuetracker.google.com/issues/36921128
[5]: http://www.songho.ca/opengl/gl_transform.html
[6]: http://www.khronos.org/opengles/sdk/docs/reference_cards/OpenGL-ES-2_0-Reference-card.pdf
[7]: https://en.wikipedia.org/wiki/Noclip_mode#.22Hall_of_mirrors.22_effect
[8]: https://github.com/learnopengles/Learn-OpenGLES-Tutorials
[9]: https://market.android.com/details?id=com.learnopengles.android
[10]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-One
[11]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Two
[12]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Three
[13]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Four
[14]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Five
[15]: https://github.com/xujiaji/LearnOpenGL/releases
[16]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Six
[17]: https://blog.xujiaji.com/post/Learn-OpenGL-Lesson-Seven
