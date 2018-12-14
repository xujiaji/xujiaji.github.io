---
title: Android 无缝换肤深入了解与使用
date: 2018-4-21 09:03:41
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/skin_home.jpg
categories:
 - Android
tags:
    - android
    - 分析框架
---

> 思路整体结构

![Android 换肤](image/android-skin/android-skin.svg)
## 方案及轮子
1. 内部资源加载方案
    - 通过在BaseActivity中setTheme
    - 不好实时的刷新，需要重新创建页面
    - 存在需要解决哪些Vew需要刷新的问题
2. 自定义View
    - [MultipleTheme](https://github.com/dersoncheng/MultipleTheme)
    - 通过自定义View配合setTheme后立即刷新资源。
    - 需要替换所有需要换肤的view
3. 自定义xml属性，Java中绑定view
    - [Colorful](https://github.com/hehonghui/Colorful)
    - 首先通过在java代码中添加view
    - 然后setTheme设置当前页面主题
    - 最后通过内部引用的上下文getTheme遍历view来修改资源
4. 动态资源加载方案
    - [Android-Skin-Loader](https://github.com/fengjundev/Android-Skin-Loader)
    - [ThemeSkinning](https://github.com/burgessjp/ThemeSkinning)（是上面那个框架的衍生，整篇就是研究的这框架）
    - resource替换：通过单独打包一个资源apk，只用来访问资源，资源名得与本身对应
    - 无需关心皮肤多少，可下载，等等
    - 准备采用该方案

## 采用方案的技术点
1. 获取皮肤资源包apk的资源
2. 自定义xml属性，用来标记需要换肤的view
3. 获取并相应有换肤需求的布局
    - [LayoutInflater Factory使用基础与进阶](https://blog.csdn.net/u013085697/article/details/53898879)
    - [Android 探究 LayoutInflater setFactory](https://blog.csdn.net/lmj623565791/article/details/51503977)
4. 其他
    - 扩展可自行添加所支持换肤的属性
    - 改变状态栏颜色
    - 改变字体

## 采用方案的实现过程
![实现过程](image/android-skin/换肤框架流程.svg)

## 加载皮肤apk获取里面的资源（为了得到皮肤apk  Resources对象）
> 下面所有的代码位置，包括处理一些特殊问题的方案等等！

https://github.com/xujiaji/ThemeSkinning

> 通过皮肤apk的全路径，可知道其包名（需要用包名来获取它的资源id）

- `skinPkgPath`是apk的全路径，通过`mInfo.packageName`就可以得到包名
- 代码位置：[SkinManager.java](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/loader/SkinManager.java)

``` java
    PackageManager mPm = context.getPackageManager();
    PackageInfo mInfo = mPm.getPackageArchiveInfo(skinPkgPath, PackageManager.GET_ACTIVITIES);
    skinPackageName = mInfo.packageName;
```

> 通过反射添加路径可以创建皮肤apk的AssetManager对象

- `skinPkgPath`是apk的全路径，添加路径的方法是AssetManager里一个隐藏的方法通过反射可以设置。
- 此时还可以用`assetManager`来访问apk里assets目录的资源。
- 想想如果更换的资源是放在assets目录下的，那么我们可以在这里动动手脚。
``` java
    AssetManager assetManager = AssetManager.class.newInstance();
    Method addAssetPath = assetManager.getClass().getMethod("addAssetPath", String.class);
    addAssetPath.invoke(assetManager, skinPkgPath);
```


> 创建皮肤apk的资源对象

- 获取当前的app的Resources，主要是为了创建apk的Resources
``` java
    Resources superRes = context.getResources();
    Resources skinResource = new Resources(assetManager, superRes.getDisplayMetrics(), superRes.getConfiguration());
```

> 当要通过资源id获取颜色的时候

1. 先获取内置的颜色`int originColor = ContextCompat.getColor(context, resId);`
2. 如果没有外置皮肤apk资源或就用默认资源的情况下直接返回内置颜色
3. 通过 `context.getResources().getResourceEntryName(resId);`获取资源id获取它的名字
4. 通过`mResources.getIdentifier(resName, "color", skinPackageName)`得到皮肤apk中该资源id。（resName：就是资源名字；skinPackegeName就是皮肤apk的包名）
5. 如果没有获取到皮肤apk中资源id（也就是等于0）返回原来的颜色，否则返回`mResources.getColor(trueResId)`

*通过`getIdentifier`方法可以通过名字来获取id，比如将第二个参数修改为`layout`、`mipmap`、`drawable`或`string`就是通过资源名字获取对应`layout目录`、`mipmap目录`、`drawable目录`或`string文件`里的资源id*

``` java
    public int getColor(int resId) {
        int originColor = ContextCompat.getColor(context, resId);
        if (mResources == null || isDefaultSkin) {
            return originColor;
        }

        String resName = context.getResources().getResourceEntryName(resId);

        int trueResId = mResources.getIdentifier(resName, "color", skinPackageName);
        int trueColor;
        if (trueResId == 0) {
            trueColor = originColor;
        } else {
            trueColor = mResources.getColor(trueResId);
        }
        return trueColor;
    }
```

> 当要通过资源id获取图片的时候

1. 和上面获取颜色是差不多的
2. 只是在图片在`drawable`目录还是`mipmap`目录进行了判断

``` java
    public Drawable getDrawable(int resId) {
        Drawable originDrawable = ContextCompat.getDrawable(context, resId);
        if (mResources == null || isDefaultSkin) {
            return originDrawable;
        }
        String resName = context.getResources().getResourceEntryName(resId);
        int trueResId = mResources.getIdentifier(resName, "drawable", skinPackageName);
        Drawable trueDrawable;
        if (trueResId == 0) {
            trueResId = mResources.getIdentifier(resName, "mipmap", skinPackageName);
        }
        if (trueResId == 0) {
            trueDrawable = originDrawable;
        } else {
            if (android.os.Build.VERSION.SDK_INT < 22) {
                trueDrawable = mResources.getDrawable(trueResId);
            } else {
                trueDrawable = mResources.getDrawable(trueResId, null);
            }
        }
        return trueDrawable;
    }
```

## 对所有view进行拦截处理
- 自己实现`LayoutInflater.Factory2`接口来替换系统默认的

> 那么如何替换呢？

- 就这样通过在Activity方法中super.onCreate之前调用
- 代码位置：[SkinBaseActivity.java](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/base/SkinBaseActivity.java)

``` java
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        mSkinInflaterFactory = new SkinInflaterFactory(this);//自定义的Factory
        LayoutInflaterCompat.setFactory2(getLayoutInflater(), mSkinInflaterFactory);
        super.onCreate(savedInstanceState);
    }
```

> 我们使用的Activity一般是`AppCompatActivity`在里面的onCreate方法中也有对其的设置和初始化，但是setFactory方法只能被调用一次，导致默认的一些初始化操作没有被调用，这么操作？

- 这是实现了`LayoutInflater.Factory2`接口的类，看`onCreateView`方法中。在进行其他操作前调用`delegate.createView(parent, name, context, attrs)`处理系统的那一套逻辑。
- `attrs.getAttributeBooleanValue`获取当前view是否是可换肤的，第一个参数是xml名字空间，第二个参数是属性名，第三个参数是默认值。这里相当于是`attrs.getAttributeBooleanValue("http://schemas.android.com/android/skin", "enable", false)`
- 代码位置：[SkinInflaterFactory.java](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/loader/SkinInflaterFactory.java)

``` java
public class SkinInflaterFactory implements LayoutInflater.Factory2 {

    private AppCompatActivity mAppCompatActivity;

    public SkinInflaterFactory(AppCompatActivity appCompatActivity) {
        this.mAppCompatActivity = appCompatActivity;
    }
    @Override
    public View onCreateView(String s, Context context, AttributeSet attributeSet) {
        return null;
    }

    @Override
    public View onCreateView(View parent, String name, Context context, AttributeSet attrs) {

        boolean isSkinEnable = attrs.getAttributeBooleanValue(SkinConfig.NAMESPACE, SkinConfig.ATTR_SKIN_ENABLE, false);//是否是可换肤的view
        AppCompatDelegate delegate = mAppCompatActivity.getDelegate();
        View view = delegate.createView(parent, name, context, attrs);//处理系统逻辑
        if (view instanceof TextView && SkinConfig.isCanChangeFont()) {
            TextViewRepository.add(mAppCompatActivity, (TextView) view);
        }

        if (isSkinEnable || SkinConfig.isGlobalSkinApply()) {
            if (view == null) {
                view = ViewProducer.createViewFromTag(context, name, attrs);
            }
            if (view == null) {
                return null;
            }
            parseSkinAttr(context, attrs, view);
        }
        return view;
    }
}
```

> 当内部的初始化操作完成后，如果判断没有创建好view，则需要我们自己去创建view

- 看上一步是通过`ViewProducer.createViewFromTag(context, name, attrs)`来创建
- 那么直接来看一下这个类`ViewProducer`，原理功能请看代码注释
- 在AppCompatViewInflater中你可以看到相同的代码
- 代码位置：[ViewProducer.java](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/loader/ViewProducer.java)

``` java
class ViewProducer {
    //该处定义的是view构造方法的参数，也就是View两个参数的构造方法：public View(Context context, AttributeSet attrs)
    private static final Object[] mConstructorArgs = new Object[2];
    //存放反射得到的构造器
    private static final Map<String, Constructor<? extends View>> sConstructorMap
            = new ArrayMap<>();
    //这是View两个参数的构造器所对应的两个参数
    private static final Class<?>[] sConstructorSignature = new Class[]{
            Context.class, AttributeSet.class};
    //如果是系统的View或ViewGroup在xml中并不是全路径的，通过反射来实例化是需要全路径的，这里列出来它们可能出现的位置
    private static final String[] sClassPrefixList = {
            "android.widget.",
            "android.view.",
            "android.webkit."
    };

    static View createViewFromTag(Context context, String name, AttributeSet attrs) {
        if (name.equals("view")) {//如果是view标签，则获取里面的class属性（该View的全名）
            name = attrs.getAttributeValue(null, "class");
        }

        try {
            //需要传入构造器的两个参数的值
            mConstructorArgs[0] = context;
            mConstructorArgs[1] = attrs;

            if (-1 == name.indexOf('.')) {//如果不包含小点，则是内部View
                for (int i = 0; i < sClassPrefixList.length; i++) {//由于不知道View具体在哪个路径，所以通过循环所有路径，直到能实例化或结束
                    final View view = createView(context, name, sClassPrefixList[i]);
                    if (view != null) {
                        return view;
                    }
                }
                return null;
            } else {//否则就是自定义View
                return createView(context, name, null);
            }
        } catch (Exception e) {
            //如果抛出异常，则返回null，让LayoutInflater自己去实例化
            return null;
        } finally {
            // 清空当前数据，避免和下次数据混在一起
            mConstructorArgs[0] = null;
            mConstructorArgs[1] = null;
        }
    }

    private static View createView(Context context, String name, String prefix)
            throws ClassNotFoundException, InflateException {
        //先从缓存中获取当前类的构造器
        Constructor<? extends View> constructor = sConstructorMap.get(name);
        try {
            if (constructor == null) {
                // 如果缓存中没有创建过，则尝试去创建这个构造器。通过类加载器加载这个类，如果是系统内部View由于不是全路径的，则前面加上
                Class<? extends View> clazz = context.getClassLoader().loadClass(
                        prefix != null ? (prefix + name) : name).asSubclass(View.class);
                //获取构造器
                constructor = clazz.getConstructor(sConstructorSignature);
                //将构造器放入缓存
                sConstructorMap.put(name, constructor);
            }
            //设置为无障碍（设置后即使是私有方法和成员变量都可访问和修改，除了final修饰的）
            constructor.setAccessible(true);
            //实例化
            return constructor.newInstance(mConstructorArgs);
        } catch (Exception e) {
            // We do not want to catch these, lets return null and let the actual LayoutInflater
            // try
            return null;
        }
    }
}
```

- 当然还有另外的方式来创建，就是直接用LayoutInflater内部的那一套
- 将`view = ViewProducer.createViewFromTag(context, name, attrs);`删除，换成下方代码：
- 代码位置：[SkinInflaterFactory.java](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/loader/SkinInflaterFactory.java)

``` java
    LayoutInflater inflater = mAppCompatActivity.getLayoutInflater();
    if (-1 == name.indexOf('.'))//如果为系统内部的View则，通过循环这几个地方来实例化View，道理跟上面ViewProducer里面一样
    {
        for (String prefix : sClassPrefixList)
        {
            try
            {
                view = inflater.createView(name, prefix, attrs);
            } catch (ClassNotFoundException e)
            {
                e.printStackTrace();
            }
            if (view != null) break;
        }
    } else
    {
        try
        {
            view = inflater.createView(name, null, attrs);
        } catch (ClassNotFoundException e)
        {
            e.printStackTrace();
        }
    }
```

- `sClassPrefixList`的定义

``` java
    private static final String[] sClassPrefixList = {
            "android.widget.",
            "android.view.",
            "android.webkit."
    };
```

> 最后是最终的拦截获取需要换肤的View的部分，也就是上面`SkinInflaterFactory`类的`onCreateView`最后调用的`parseSkinAttr`方法

 - 定义类一个成员来保存所有需要换肤的View, SkinItem里面的逻辑就是定义了设置换肤的方法。如：View的setBackgroundColor或setColor等设置换肤就是靠它。

``` java
private Map<View, SkinItem> mSkinItemMap = new HashMap<>();
```

- SkinAttr: 需要换肤处理的xml属性，如何定义请参照官方文档：https://github.com/burgessjp/ThemeSkinning

``` java
    private void parseSkinAttr(Context context, AttributeSet attrs, View view) {
        //保存需要换肤处理的xml属性
        List<SkinAttr> viewAttrs = new ArrayList<>();
        //变量该view的所有属性
        for (int i = 0; i < attrs.getAttributeCount(); i++) {
            String attrName = attrs.getAttributeName(i);//获取属性名
            String attrValue = attrs.getAttributeValue(i);//获取属性值
            //如果属性是style，例如xml中设置：style="@style/test_style"
            if ("style".equals(attrName)) {
                //可换肤的属性
                int[] skinAttrs = new int[]{android.R.attr.textColor, android.R.attr.background};
                //经常在自定义View时，构造方法中获取属性值的时候使用到。
                //这里通过传入skinAttrs，TypeArray中将会包含这两个属性和值，如果style里没有那就没有 - -
                TypedArray a = context.getTheme().obtainStyledAttributes(attrs, skinAttrs, 0, 0);
                //获取属性对应资源的id，第一个参数这里对应下标的就是上面skinAttrs数组里定义的下标，第二个参数是没有获取到的默认值
                int textColorId = a.getResourceId(0, -1);
                int backgroundId = a.getResourceId(1, -1);
                if (textColorId != -1) {//如果有颜色属性
                    //<style name="test_style">
                        //<item name="android:textColor">@color/colorAccent</item>
                        //<item name="android:background">@color/colorPrimary</item>
                    //</style>
                    //以上边的参照来看
                    //entryName就是colorAccent
                    String entryName = context.getResources().getResourceEntryName(textColorId);
                    //typeName就是color
                    String typeName = context.getResources().getResourceTypeName(textColorId);
                    //创建一换肤属性实力类来保存这些信息
                    SkinAttr skinAttr = AttrFactory.get("textColor", textColorId, entryName, typeName);
                    if (skinAttr != null) {
                        viewAttrs.add(skinAttr);
                    }
                }
                if (backgroundId != -1) {//如果有背景属性
                    String entryName = context.getResources().getResourceEntryName(backgroundId);
                    String typeName = context.getResources().getResourceTypeName(backgroundId);
                    SkinAttr skinAttr = AttrFactory.get("background", backgroundId, entryName, typeName);
                    if (skinAttr != null) {
                        viewAttrs.add(skinAttr);
                    }

                }
                a.recycle();
                continue;
            }
            //判断是否是支持的属性，并且值是引用的，如：@color/red
            if (AttrFactory.isSupportedAttr(attrName) && attrValue.startsWith("@")) {
                try {
                    //去掉属性值前面的“@”则为id
                    int id = Integer.parseInt(attrValue.substring(1));
                    if (id == 0) {
                        continue;
                    }
                    //资源名字，如:text_color_selector
                    String entryName = context.getResources().getResourceEntryName(id);
                    //资源类型，如:color、drawable
                    String typeName = context.getResources().getResourceTypeName(id);
                    SkinAttr mSkinAttr = AttrFactory.get(attrName, id, entryName, typeName);
                    if (mSkinAttr != null) {
                        viewAttrs.add(mSkinAttr);
                    }
                } catch (NumberFormatException e) {
                    SkinL.e(TAG, e.toString());
                }
            }
        }
        //是否有需要换肤的属性？
        if (!SkinListUtils.isEmpty(viewAttrs)) {
            SkinItem skinItem = new SkinItem();
            skinItem.view = view;
            skinItem.attrs = viewAttrs;
            mSkinItemMap.put(skinItem.view, skinItem);
            //是否换肤
            if (SkinManager.getInstance().isExternalSkin() ||
                    SkinManager.getInstance().isNightMode()) {//如果当前皮肤来自于外部或者是处于夜间模式
                skinItem.apply();//应用于这个view
            }
        }
    }
```

## 采用方案的注意事项和疑问

1. 可能系统会更改相关方法，但好处大于弊端
2. 插件化也是外置apk来加载，如何做到呢？
    - 占时不去研究
3. 皮肤从网络上下载到哪个目录？如何断定皮肤已经下载？
    - 可以通过`SkinFileUtils`工具类调用`getSkinDir`方法获取皮肤的缓存目录
    - 下载的时候可以直接下载到这个目录
    - 有没有某个皮肤就判断该文件夹下有没有这个文件了
4. 如何不打包之前可以直接预览？
    - 想要能在打包前提前预览效果，而不每次想看一看效果就要打一个apk包
    - 首先，大家都应该知道分渠道的概念。通过分渠道打包，因为我们能把资源也分成不同渠道的，运行不同渠道，所得到的资源是不一样的。
    - 然后，我们在:`项目目录\app\src`，创建一个和渠道相同名字的目录。比如说有个`red`渠道。![渠道定义](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/qudao.png) ![red渠道png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/red.png)
    - 最后，我们选编译的渠道为red，然后直接运行就可以看到效果了。如果可以直接把res拷贝到皮肤项目打包就行了。![选择编译渠道](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/choose_build.png)
5. 换肤对应的属性需要是View提供了set方法的的属性！
    - 如果没有提供则不能在java代码中设置值
    - 如果是自定义View那么就添加对应方法
    - 如果是系统或类库View，额(⊙o⊙)…
6. 换肤的属性值需要是@开头的数据引用，如：@color/red
    - 原因是因为固定的值一般不可能是需要换肤的属性，在`SkinInfaterFactory`的方法`parseSkinAttr`中有这样一句来进行过滤没有带@的属性值：![过滤没带@的属性值](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/guo_lv_@.png)
    - 但此时，正好有一个自定义View没有按照常路出牌，它的值就是图片名字没有类型没有引用，通过java代码`context.getResources().getIdentifier(name, "mipmap", context.getPackageName())`来获取图片资源（[参考这奇葩方式的库](https://github.com/xujiaji/FlycoTabLayout)）。但由于这个属性是需要换肤更换的属性，于是没办法，专门为这两个属性在`SkinInfaterFactory`的`parseSkinAttr`方法中写了个判断![单独判断这两属性](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/dan_du_get_attr.png)。[参考这代码](https://github.com/xujiaji/ThemeSkinning/blob/master/skinlibrary/src/main/java/solid/ren/skinlibrary/loader/SkinInflaterFactory.java)

## 其他参考
1. [Android主题换肤 无缝切换](https://www.jianshu.com/p/af7c0585dd5b) *(主要参考对象，用的也是他修改`Android-Skin-Loader`后的框架`ThemeSkinning`）*
2. [Android换肤技术总结](http://blog.zhaiyifan.cn/2015/09/10/Android%E6%8D%A2%E8%82%A4%E6%8A%80%E6%9C%AF%E6%80%BB%E7%BB%93/)
3. [Android apk动态加载机制的研究](https://blog.csdn.net/singwhatiwanna/article/details/22597587)

## 涉及及其延生
1. 插件化开发，既然能这样获取资源，也能获取class文件
2. 通过对view的拦截可以把某个控件整体替换掉。
比如AppCompatActivity将TextView偷偷替换成了AppCompatTextView等等。


---
> 其他一些帮助信息：

上面对应的代码片段都有对应路径哦！

这篇文章的全部代码，测试项目位置：https://github.com/xujiaji/ThemeSkinning

测试项目中的首页底部导航测试和修改位置：https://github.com/xujiaji/FlycoTabLayout

下面这张Gif图片是测试项目运行的效果图：
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/android-skin/skin_run.gif)
