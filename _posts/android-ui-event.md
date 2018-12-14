---
title: Android-UI事件传递就是这么个事儿
date: 2016-04-16 15:31
author: xujiaji
categories:
 - Android
tags:
    - android
    - view
---
> 我们寻找的，也只不过是内心世界的片刻安宁，
以及，那样一场盛大的清欢。

## 聊聊UI事件传递

![Android UI事件传递.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/ui-event.png)

## 什么是UI事件？
- 触摸屏幕中UI控件的那一刻即为事件发生
- MotionEvent对象包含了所有的触摸事件，如`触摸的位置、多指触摸等`
- MotionEvent描述了当前的操作类型，以下为常见类型(数字代表对应的值)：
 - `ACTION_DOWN = 0` 按下
 - `ACTION_UP = 1` 抬起
 - `ACTION_MOVE = 2` 移动
 - `ACTION_CANCEL = 3` 动作取消
 - `ACTION_OUTSIDE = 4`  动作超出边界
 - `ACTION_POINTER_DOWN = 5` 已有一个点被按住，此时再按下一个点
 - `ACTION_POINTER_UP = 6` 多个点被按住，非最后放开的点都会调用

## 事件如何传递？
> 自定义的父布局和子布局，用来观察事件的变化(View1和Button1为自定义View和自定义Button，默认以自定义View1举例

![1](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/1.png)

上图简略关系如下：
![布局简略关系.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/2.png)

**×** 之前一直以为事件是从子布局开始传递到父布，因为以直观的角度我们先碰到的是子布局`得到错误的事件顺序：view1 --> ViewGroup2 --> ViewGroup1`

**√** 后来才知道事件是从父布局传递到子布局，是由父布局判断点击位置上面有子布局然后向子布局传递。如果事件向子布局传递没有被拦截和消费，那么事件又会向父布局传递。`正确的没有被拦截和消费的事件顺序：Activity --> ViewGroup1 --> ViewGroup2 --> View1 --> ViewGroup2 --> ViewGroup1 --> Activity`


    以下的Log为当手指对view1点击、滑动、抬起时，
    发生的一系列事件传递（0.按下；1.抬起； 2.移动）：


-
``` java
    E/MainActivity: ----------- dispatchTouchEvent = 0
    E/ViewGroup1: ------------- dispatchTouchEvent = 0
    E/ViewGroup1: ------------- onInterceptTouchEvent = 0
    E/ViewGroup2: ------------- dispatchTouchEvent = 0
    E/ViewGroup2: ------------- onInterceptTouchEvent = 0
    E/View1: ------------------ dispatchTouchEvent = 0
    E/View1: ------------------ onTouchEvent = 0
    E/ViewGroup2: ------------- onTouchEvent = 0
    E/ViewGroup1: ------------- onTouchEvent = 0
    E/MainActivity: ----------- onTouchEvent = 0
    E/MainActivity: ----------- dispatchTouchEvent = 2
    E/MainActivity: ----------- onTouchEvent = 2
    E/MainActivity: ----------- dispatchTouchEvent = 2
    E/MainActivity: ----------- onTouchEvent = 2
    E/MainActivity: ----------- dispatchTouchEvent = 2
    E/MainActivity: ----------- onTouchEvent = 2
    E/MainActivity: ----------- dispatchTouchEvent = 1
    E/MainActivity: ----------- onTouchEvent = 1
    E/MainActivity: ----------- dispatchTouchEvent = 1
    E/MainActivity: ----------- onTouchEvent = 1
```



| `观察`|
| :----  |
|`可以看出事件由外层大布局到内部子布局传进去，在从子布局传出去（Activity --> ViewGroup1 --> ViewGroup2 --> View1 --> ViewGroup2 --> ViewGroup1 --> Activity）`|
|`由此log还可以看出：当按下的事件没有被拦截，那么所有状态的事件都由Activity进行处理`|

> 没有拦截事件时

![没有拦截事件时.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/3.png)

## 如何拦截？
- 通过dispatchTouchEvent对事件进行拦截，**当返回值为`true`的时候拦截事件**
- 拦截后事件将不会传到子布局
        现在以ViewGroup1为例：
        让ViewGroup1中的dispatchTouchEvent直接返回true
        当手指对View1点击、移动、抬起时
        发生的一系列事件传递（0.按下；1.抬起； 2.移动）

     ``` java
E/MainActivity: ----------------  dispatchTouchEvent = 0
E/ViewGroup1: ------------------  dispatchTouchEvent = 0
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 1
E/ViewGroup1: ------------------  dispatchTouchEvent = 1
       ```

| `观察`|
| :----  |
|`可以看出事件传递到ViewGroup1后被拦截，没有被任何布局消费`|
|`也就是说事件还没被消费就被拦截会导致触摸无效`|
|`我们可以在dispatchTouchEvent判断哪些情况需要拦截，哪些不需要拦截就放事件过去（以上直接返回了true拦截了所有情况的事件）`|

> 拦截ViewGroup1的所有事件

![拦截ViewGroup1的所有事件.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/4.png)

## 如何获取？
- 通过onInterceptTouchEvent获取事件，**当返回值为`true`的时候获取事件**
- 获取事件后会调用onTouchEvent方法，调用这个方法后，如果我们设置了OnTouchListener，那么触摸监听将会被调用。
        现在以ViewGroup2为例：
        让ViewGroup2中的onInterceptTouchEvent直接返回true
        当手指对View1点击、移动、抬起时
        发生的一系列事件传递（0.按下；1.抬起； 2.移动）

-
``` java
E/MainActivity: ----------------  dispatchTouchEvent = 0
E/ViewGroup1: ------------------  dispatchTouchEvent = 0
E/ViewGroup1: ------------------  onInterceptTouchEvent = 0
E/ViewGroup2: ------------------  dispatchTouchEvent = 0
E/ViewGroup2: ------------------  onInterceptTouchEvent = 0
E/ViewGroup2: ------------------  onTouchEvent = 0
E/ViewGroup1: ------------------  onTouchEvent = 0
E/MainActivity: ----------------  onTouchEvent = 0
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  onTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  onTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/MainActivity: ----------------  onTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 1
E/MainActivity: ----------------  onTouchEvent = 1
```

| `观察问题`|`原因`|`解决`|
| --------   | :-----:  | :----:  |
|`哎呀呀~！为啥我获取到了的事件之后，移动和抬起手指的事件被MainActivity吃了！愤怒！！`|`原来onTouchEvent如果处理按下事件DOWN的时候没有返回true。如果onTouchEvent处理DOWN时候返回false，则表示没有消费事件，事件将会回到父布局，并且后续事件将不会再传递过来。`|`onTouchEvent方法中判断为按下DOWN事件的时候，返回true即下面要说的消费`|

> 当ViewGroup2事件获取到了，但没有消费

![当ViewGroup2事件获取到了，但没有消费.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/5.png)

## 如何消费？
- 上边已经提到过，就是获取事件遗留下来一个问题：获取到了按下事件，为啥没继续获取到后续的事件？就是因为按下时onTouchEvent没有返回true，导致事件从新回到父布局，也就是没有消费事件。

        现在接着以ViewGroup2为例：
        还是让ViewGroup2中的onInterceptTouchEvent直接返回true
        添加：在onTouchEvent方法中添加判断if (event.getAction() == MotionEvent.ACTION_DOWN) {return true;}
        当手指对View1点击、移动、抬起时
        发生的一系列事件传递（0.按下；1.抬起； 2.移动）

    ``` java
E/MainActivity: ----------------  dispatchTouchEvent = 0
E/ViewGroup1: ------------------  dispatchTouchEvent = 0
E/ViewGroup1: ------------------  onInterceptTouchEvent = 0
E/ViewGroup2: ------------------  dispatchTouchEvent = 0
E/ViewGroup2: ------------------  onInterceptTouchEvent = 0
E/ViewGroup2: ------------------  onTouchEvent = 0
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  onInterceptTouchEvent = 2
E/ViewGroup2: ------------------  dispatchTouchEvent = 2
E/ViewGroup2: ------------------  onTouchEvent = 2
E/MainActivity: ----------------  onTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  dispatchTouchEvent = 2
E/ViewGroup1: ------------------  onInterceptTouchEvent = 2
E/ViewGroup2: ------------------  dispatchTouchEvent = 2
E/ViewGroup2: ------------------  onTouchEvent = 2
E/MainActivity: ----------------  onTouchEvent = 2
E/MainActivity: ----------------  dispatchTouchEvent = 1
E/ViewGroup1: ------------------  dispatchTouchEvent = 1
E/ViewGroup1: ------------------  onInterceptTouchEvent = 1
E/ViewGroup2: ------------------  dispatchTouchEvent = 1
E/ViewGroup2: ------------------  onTouchEvent = 1
E/MainActivity: ----------------  onTouchEvent = 1
```


| `观察`|
|-|
|`由上边log可以看出，现在在ViewGroup2中的onTouchEvent的按下事件返回一个true后，按下事件并没有在传递回父布局中，使得后续事件都将能得到`|
|`可以看出当后续事件传递过来时，ViewGroup2已经没有再次调用onInterceptTouchEvent方法`|
|`我们只是将按下DOWN的事件返回true，所以除了按下事件其他移动或抬起的事件activity都也能获取到。当onTouchEvent不管三七二十一直接返回一个true时，activity就不会获取到事件`|

> 当消费ViewGroup2的按下DOWN事件时

![当消费ViewGroup2的按下DOWN事件时.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/6.png)

> 当ViewGroup2中onTouchEvent直接返回true时

![当ViewGroup2中onTouchEvent直接返回true时.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/7.png)
## Button获取事件是怎么回事？
- 现在将View1换成Button1，其他的恢复最初状态，先来看看触摸的log
``` java
E/MainActivity: -------------  dispatchTouchEvent = 0
E/ViewGroup1: ---------------  dispatchTouchEvent = 0
E/ViewGroup1: ---------------  onInterceptTouchEvent = 0
E/ViewGroup2: ---------------  dispatchTouchEvent = 0
E/ViewGroup2: ---------------  onInterceptTouchEvent = 0
E/Button1: ------------------  dispatchTouchEvent = 0
E/Button1: ------------------  onTouchEvent = 0
E/MainActivity: -------------  dispatchTouchEvent = 2
E/ViewGroup1: ---------------  dispatchTouchEvent = 2
E/ViewGroup1: ---------------  onInterceptTouchEvent = 2
E/ViewGroup2: ---------------  dispatchTouchEvent = 2
E/ViewGroup2: ---------------  onInterceptTouchEvent = 2
E/Button1: ------------------  dispatchTouchEvent = 2
E/Button1: ------------------  onTouchEvent = 2
E/MainActivity: -------------  dispatchTouchEvent = 2
E/ViewGroup1: ---------------  dispatchTouchEvent = 2
E/ViewGroup1: ---------------  onInterceptTouchEvent = 2
E/ViewGroup2: ---------------  dispatchTouchEvent = 2
E/ViewGroup2: ---------------  onInterceptTouchEvent = 2
E/Button1: ------------------  dispatchTouchEvent = 2
E/Button1: ------------------  onTouchEvent = 2
E/MainActivity: -------------  dispatchTouchEvent = 1
E/ViewGroup1: ---------------  dispatchTouchEvent = 1
E/ViewGroup1: ---------------  onInterceptTouchEvent = 1
E/ViewGroup2: ---------------  dispatchTouchEvent = 1
E/ViewGroup2: ---------------  onInterceptTouchEvent = 1
E/Button1: ------------------  dispatchTouchEvent = 1
E/Button1: ------------------  onTouchEvent = 1
```

- 在来看看序列图

> Button获取触摸事件

![Button获取触摸事件.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/8.png)

- 这一看，这不是和上面那张图`当ViewGroup2中onTouchEvent直接返回true时`的效果一样的吗？也就是说button默认就是直接获取了事件，没有让事件返回主布局中。

- 等等还有一个！！！大家都知道布局有个属性**clickable**吧！当设置它的值为true时，使得这个布局事件如button所述！

- 更深入的理解的话这里博客已经介绍的很详细了
 -  [Android事件分发机制完全解析，带你从源码的角度彻底理解(上)](http://blog.csdn.net/guolin_blog/article/details/9097463)
 -  [Android事件分发机制完全解析，带你从源码的角度彻底理解(下)](http://blog.csdn.net/guolin_blog/article/details/9153747)

## 实际的应用
-
来一个简单的应用

xml布局
``` xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="10dp">
    <CheckBox
        android:id="@+id/checkbox_lock"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Lock Selection" />
    <RadioGroup
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">
        <RadioButton
            android:id="@+id/selection_first"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="First"/>
        <RadioButton
            android:id="@+id/selection_second"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Second"/>
        <RadioButton
            android:id="@+id/selection_third"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Third"/>
    </RadioGroup>
</LinearLayout>
```

activity代码
``` java
package com.examples.customtouch;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.CheckBox;

/**
 * Created by Dave Smith
 * Double Encore, Inc.
 * Date: 9/25/12
 * TouchListenerActivity
 */
public class TouchListenerActivity extends Activity implements View.OnTouchListener {

    /* Views to display last seen touch event */
    CheckBox mLockBox;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.touch_listener);

        mLockBox = (CheckBox) findViewById(R.id.checkbox_lock);

        findViewById(R.id.selection_first).setOnTouchListener(this);
        findViewById(R.id.selection_second).setOnTouchListener(this);
        findViewById(R.id.selection_third).setOnTouchListener(this);
    }

    @Override
    public boolean onTouch(View v, MotionEvent event) {
        /*
         * Consume the events here so the buttons cannot process them
         * if the CheckBox in the UI is checked
         */
        Log.e("TouchListenerActivity", getNameForEvent(event));
        return mLockBox.isChecked();
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        Log.e("onTouchEvent", getNameForEvent(event));
        return super.onTouchEvent(event);
    }

    private String getNameForEvent(MotionEvent event) {
        String action = "";
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                action = "ACTION_DOWN";
                break;
            case MotionEvent.ACTION_CANCEL:
                action = "ACTION_CANCEL";
                break;
            case MotionEvent.ACTION_MOVE:
                action = "ACTION_MOVE";
                break;
            case MotionEvent.ACTION_UP:
                action = "ACTION_UP";
                break;
            default:
                return null;
        }

        return String.format("%s\n%.1f, %.1f", action, event.getX(), event.getY());
    }
}

```


![效果图](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-ui-event/9.png)

|`状态`|`描述`|
|:-:|:-:|
|`当Lock Selection没有勾选时`|`下边的单选能正常选择`|
|`当Lock Selection勾选时`|`下边的单选无法点击`|

- 大家是否疑惑了，为什么复选框选中状态，ontouch返回了true反而不能点击了。为什么不是返回false无法点击，返回true时才能点击呢？其实这些控件默认可以点击的都是默认获取事件的，如上面说的button为什么获取事件一样，所以返回true和false和预想的结果相反。

# 所用知识和资料
1. Android studio插件plantUml画序列图和类图
2. [PlantUML快速指南](http://archive.3zso.com/archives/plantuml-quickstart.html#sec-5-3) 和 [PlantUML官网](http://plantuml.com/classes.html)
3. [Android事件分发机制完全解析，带你从源码的角度彻底理解(上)](http://blog.csdn.net/guolin_blog/article/details/9097463)
[Android事件分发机制完全解析，带你从源码的角度彻底理解(下)](http://blog.csdn.net/guolin_blog/article/details/9153747)
4. [公共技术点之 View 事件传递](http://a.codekk.com/detail/Android/Trinea/%E5%85%AC%E5%85%B1%E6%8A%80%E6%9C%AF%E7%82%B9%E4%B9%8B%20View%20%E4%BA%8B%E4%BB%B6%E4%BC%A0%E9%80%92)
5. [最后的那个例子来自于这儿](https://github.com/devunwired/custom-touch-examples)
