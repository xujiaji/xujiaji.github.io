---
title: 一个项目如何编译多个不同签名、包名、资源等，的apk？
date: 2018-10-29 16:15:20
author: xujiaji
categories:
 - Android
tags:
    - android
    - 项目配置
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/one-for-more/banner.png
---
## 简介
如题所示！本篇文章就是为了解决这种问题。方便打包和运行的时候能做到无需手动替换配置，即可打包想要的apk。打包的时候，只需选一下想打哪种配置的apk就OK啦。 \(^o^)/~
> 先来看，有需求如下：

1. 同一个项目
2. 不同的apk图标
3. 不同的服务器域名
4. 不同的包名
5. 不同的名称
6. 不同的签名
7. 不同的第三方key
8. 不同的版本名版本号

> 解决思路

1. 当然最直接的方式不过于每次打不同包的时候都去替换对应的配置，这种方式的麻烦之处不言而喻。
2. 将所有配置，资源等都配置入项目中，打包的时候，根据选择渠道打包不同配置的apk。（本篇文章就是要讲怎么这么做的）
3. 相信还有其他的。。。

## 相关的几个要点
1. 首先我们需要知道`productFlavors`来配置渠道，这里我将渠道用来表示哪种apk，如下我需要配置四种应用:
``` groovy
productFlavors {
  userquhua {}
  quhua {}
  cuntuba {}
  xemh {}
}
```
2. 如果我们选择了某一个渠道，那么运行打包的时候会根据渠道名选择资源文件（可结合第6点一起看）
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/one-for-more/20181029171053.png)
3. 签名可在`signingConfigs`中配置多个（我将所有签名文件放在了项目跟目录的key文件夹中），这样我们就可以通过`signingConfigs`指定预制好的签名配置。
``` groovy
signingConfigs {
    userquhuaRelease {
        storeFile file("../key/xxx1.keystore")
        storePassword "xxxxxx"
        keyAlias "alias"
        keyPassword "xxxxxx"
    }

    quhuaRelease {
        storeFile file("../key/xxx2.keystore")
        storePassword "xxxxxx"
        keyAlias "alias"
        keyPassword "xxxxxx"
    }

    cuntubaRelease {
        storeFile file("../key/xxx3.keystore")
        storePassword "xxxxxx"
        keyAlias "alias"
        keyPassword "xxxxxx"
    }

    xemhRelease {
        storeFile file("../key/xxx4.keystore")
        storePassword "xxxxxx"
        keyAlias "alias"
        keyPassword "xxxxxx"
    }
}
```
4. 可在build.gradle中配置动态配置java代码调用的常量数据（如：通过该方式我们可根据不同渠道动态配置第三方appid，或其他需要根据渠道而改变的数据）
 - 比如：我们在`defaultConfig {}` 中定义了:
  ```
  buildConfigField "String", "SERVER_URL", '"http://xx.xxxx.com/"'
  ```
 - 此时，您看一下清单文件中`manifest`标签里的，`package`的值，假如是：
  ```
  com.xxx.xx
  ```
 - 那么，您就可以在java代码中通过导入文件：
  ```
  import com.xxx.xx.BuildConfig;
  ```
 - 然后调用
  ```
  BuildConfig.SERVER_URL
  ```
  它的值就是上边配置的字符串：`http://xx.xxxx.com/`。
 - 您可以进入`BuildConfig`看一看，里面还包含了一些当前的包名版本号等信息。
 ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/one-for-more/20181030234102.png)
5. 在渠道配置那里可以配置对应的包名版本名签名等等
如下所示：
 ``` groovy
// 省略其他配置...
android {
  // 省略其他配置...
  productFlavors {
      userquhua {
          applicationId "com.xxx.xx"
          versionCode 1
          versionName "1.0.0"
          signingConfig signingConfigs.userquhuaRelease // 配置签名

          String qq_id = '"xxxxxxxxx"' //配置qq appid
          buildConfigField "String",           "QQ_ID", qq_id
          buildConfigField "String",           "WX_ID", '"wxxxxxxxxxxxxxxxxx"' // 配置微信appid
          manifestPlaceholders = [
            qq_id: qq_id,
            JPUSH_PKGNAME : applicationId,
            JPUSH_APPKEY : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", //JPush 上注册的包名对应的 Appkey.
            JPUSH_CHANNEL : "developer-default",
          ]
      }
  }

  buildTypes {
    release {
      // 省略其他配置...
        signingConfig null  // 置空
    }

    debug {
      // 省略其他配置...
        signingConfig null // 置空
    }
  }
}

 ```
 - 这样，如果我们打包userquhua这个渠道，看第2点中介绍选择userquhuaDebug。
 - 然后，最好clean一下项目、然后我们运行项目。
 - 该app的包名就是`com.xxx.xx`，版本号为`1`，版本名为`1.0.0`。
 - 通过`BuildConfig`调用`QQ_ID`静态常量，就是该渠道里配置的值，`WX_ID`同理。
 - `manifestPlaceholders`配置也可以这样配置。
 - 签名问题经过个人反复尝试（然后半天就过去了￣へ￣），最终签名如上配置。**需要注意**`buildTypes`中的签名配置`signingConfig`如果不设置为`null`，那么打包的是有还是以内置的签名打包。
6. 资源文件替换
再看到第2点的介绍，我们选择运行渠道后，会默认匹配对应渠道下的资源。下面我将`xemh`渠道的资源目录全部展开一下。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/one-for-more/20181029233306.png)
 - 如上图这样，只需要资源名字和app目录对应的文件名字一样即可替换。
 - strings.xml里的应用名，只需要将对应`app_name`修改既可替换app下strings的`app_name`，其他不用替换的不用写就行。
7. 打正式包的时候选好渠道，就可以打包不同配置的apk，当然您也可以使用命令的方式。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/one-for-more/20181029234235.png)

## 其他配置记录
> 获取当前时间

``` groovy
static def releaseTime() {
    return new Date().format("yyyy-MM-dd-HH.mm", TimeZone.getTimeZone("GMT+8"))
}
```
> 打包的时候，修改文件名，以方便区别渠道和版本打包时间

``` groovy
applicationVariants.all {
    variant ->
        variant.outputs.all {
            outputFileName = "${variant.productFlavors[0].name}-v${variant.productFlavors[0].versionName}-${releaseTime()}.apk"
        }
}
```
- `${variant.productFlavors[0].name}`当前渠道名
- `${variant.productFlavors[0].versionName}`当前版本名
- `${releaseTime()}`当前时间

## 其他需要注意事项
如果您在清单文件`AndroidManifest.xml`中，有那种以包名开头命名的那种。因为如果包名都改了，有些也需要动态的改变。可以用`${applicationId}`代替。在打包的时候，会自动替换成当前包名。

> 比如，类似下配置：

``` xml
<permission
    android:name="com.xxx.xx.permission.JPUSH_MESSAGE"
    android:protectionLevel="signature" />
<uses-permission android:name="com.xxx.xx.permission.JPUSH_MESSAGE" />
<receiver
    android:name=".push.MyJPushMessageReceiver"
    android:enabled="true"
    android:exported="false" >
    <intent-filter>
        <action android:name="cn.jpush.android.intent.RECEIVE_MESSAGE" />
        <category android:name="com.xxx.xx" />
    </intent-filter>
</receiver>
<provider
    android:name="android.support.v4.content.FileProvider"
    android:authorities="com.xxx.xx.provider"
    android:exported="false"
    tools:replace="android:authorities"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

> 可改为：

``` xml
<permission
    android:name="${applicationId}.permission.JPUSH_MESSAGE"
    android:protectionLevel="signature" />
<uses-permission android:name="${applicationId}.permission.JPUSH_MESSAGE" />
<receiver
    android:name=".push.MyJPushMessageReceiver"
    android:enabled="true"
    android:exported="false" >
    <intent-filter>
        <action android:name="cn.jpush.android.intent.RECEIVE_MESSAGE" />
        <category android:name="${applicationId}" />
    </intent-filter>
</receiver>
<provider
    android:name="android.support.v4.content.FileProvider"
    android:authorities="${applicationId}.provider"
    android:exported="false"
    tools:replace="android:authorities"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```
> 当然值得注意的是，在代码中我们也不能把包名写死了，可通过`BuildConfig`得到当前包名

## 我的完整配置，供参考
> 有关隐私信息的都用xxx替换了

1. 项目根目录的`build.gradle`
``` groovy
// Top-level build file where you can add configuration options common to all sub-projects/modules.

buildscript {

    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.0.0'
        classpath "io.github.prototypez:save-state:0.1.7"

        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}

allprojects {
    repositories {
        google()
        jcenter()
        maven { url "https://jitpack.io" }
        maven { url 'http://oss.jfrog.org/artifactory/oss-snapshot-local/' }
        flatDir {
            dirs 'libs'
        }
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}

ext{
    minSdkVersion               = 16
    targetSdkVersion            = 27
    compileSdkVersion           = 27
    buildToolsVersion           = '27.1.1'

    supportLibraryVersion       = '27.1.1'
    xmvpVersion                 = '1.2.2'
    retrofit2Version            = '2.3.0'
    okhttp3Version              = '3.8.1'
    butterknifeVersion          = '8.6.0'
    rx2Version                  = '2.0.2'
    CircleProgressDialogVersion = '1.0.2'
    smarttabVersion             = '1.6.1@aar'
    adapterHelperVersion        = '2.9.41'
    glideVersion                = '4.7.1'
    roundedimageviewVersion     = '2.3.0'
    eventbusVersion             = '3.0.0'
    dispatcherVersion           = '2.4.0'
    picture_libraryVersion      = 'v2.2.3'
    statusbarutilVersion        = '1.5.1'
    okhttpUtilsVersion          = '3.8.0'
    constraintVersion           = '1.1.3'
    flexboxVersion              = '1.0.0'
}
```
2. app目录下的`build.gradle`
``` groovy
apply plugin: 'com.android.application'
apply plugin: 'save.state'

static def releaseTime() {
    return new Date().format("yyyy-MM-dd-HH.mm", TimeZone.getTimeZone("GMT+8"))
}

android {
    compileSdkVersion rootProject.compileSdkVersion
//    buildToolsVersion rootProject.buildToolsVersion
    defaultConfig {
        minSdkVersion rootProject.minSdkVersion
        targetSdkVersion rootProject.targetSdkVersion

        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
        multiDexEnabled true
        // config the JSON processing library
        javaCompileOptions {
            annotationProcessorOptions {
                arguments = [ serializer : "gson" ]
            }
        }

        ndk {
            abiFilters "armeabi-v7a"
        }
        renderscriptTargetApi 25
        renderscriptSupportModeEnabled true

    }
    signingConfigs {
        userquhuaRelease {
            storeFile file("../key/xxx.keystore")
            storePassword "xxxxxx"
            keyAlias "xxx"
            keyPassword "xxxxxx"
        }

        quhuaRelease {
            storeFile file("../key/xxx.keystore")
            storePassword "xxxxxxx"
            keyAlias "xxx"
            keyPassword "xxxxxxx"
        }

        cuntubaRelease {
            storeFile file("../key/xxx.keystore")
            storePassword "xxxxxxx"
            keyAlias "xxx"
            keyPassword "xxxxxxx"
        }

        xemhRelease {
            storeFile file("../key/xxx.keystore")
            storePassword "xxxxxxx"
            keyAlias "xxx"
            keyPassword "xxxxxxx"
        }
    }
    flavorDimensions "default"
    productFlavors {
        userquhua {
            applicationId "com.xxx.xx"
            versionCode 22
            versionName "1.7.5"
            signingConfig = signingConfigs.userquhuaRelease

            String qq_id = '"xxxxxx"'
            buildConfigField "String",           "QQ_ID", qq_id // qq appId
            buildConfigField "String",         "SINA_ID", '"xxxxxx"' // 新浪appId
            buildConfigField "String",           "WX_ID", '"xxxxxx"' // 微信 appId
            buildConfigField "String",           "UM_ID", '"xxxxxx"' // 友盟
            buildConfigField "String",       "WX_SECRET", '"xxxxxx"' // 微信 secret
            buildConfigField "String",   "SINA_REDIRECT", '"http://open.weibo.com/apps/xxxxxx/privilege/oauth"' // 新浪

            buildConfigField "String",   "ADHUB_INIT_ID", '"xxxxxx"' // 广告sdk初始化id
            buildConfigField "String", "ADHUB_SPLASH_ID", '"xxxxxx"' // 开屏广告id
            buildConfigField "String", "ADHUB_BANNER_ID", '"xxxxxx"' // banner广告id

            buildConfigField "String",      "SERVER_URL", '"http://xxx.xxx.com/"'
            buildConfigField "String",        "LOGO_URL", '"http://file.xxx.com/img/xxx.png"'

            manifestPlaceholders = [
                    qq_id: qq_id,
                    JPUSH_PKGNAME : applicationId,
                    JPUSH_APPKEY : "xxxxxx", //JPush 上注册的包名对应的 Appkey.
                    JPUSH_CHANNEL : "developer-default", //暂时填写默认值即可.
            ]
        }

        quhua {
            applicationId "com.xxx.xx"
            versionCode 1
            versionName "1.0.0"
            signingConfig = signingConfigs.quhuaRelease

            String qq_id = '"xxxxxx"'
            buildConfigField "String",           "QQ_ID", qq_id
            buildConfigField "String",         "SINA_ID", '"xxxxxx"'
            buildConfigField "String",           "WX_ID", '"xxxxxx"'
            buildConfigField "String",           "UM_ID", '"xxxxxx"'
            buildConfigField "String",       "WX_SECRET", '"xxxxxx"'
            buildConfigField "String",   "SINA_REDIRECT", '"http://open.weibo.com/apps/xxxxxx/privilege/oauth"'

            buildConfigField "String",   "ADHUB_INIT_ID", '"xxxxxx"' // 广告sdk初始化id
            buildConfigField "String", "ADHUB_SPLASH_ID", '"xxxxxx"' // 开屏广告id
            buildConfigField "String", "ADHUB_BANNER_ID", '"xxxxxx"' // banner广告id

            buildConfigField "String",      "SERVER_URL", '"http://xx.xxx.com/"'
            buildConfigField "String",        "LOGO_URL", '"http://file.xxx.com/img/xxx.png"'

            manifestPlaceholders = [
                    qq_id: qq_id,
                    JPUSH_PKGNAME : applicationId,
                    JPUSH_APPKEY : "xxxxxx", //JPush 上注册的包名对应的 Appkey.
                    JPUSH_CHANNEL : "developer-default", //暂时填写默认值即可.
            ]
        }

        cuntuba {
            applicationId "com.xxx.xx"
            versionCode 1
            versionName "1.0.0"
            signingConfig = signingConfigs.cuntubaRelease

            String qq_id = '"xxxxxx"'
            buildConfigField "String",           "QQ_ID", qq_id
            buildConfigField "String",         "SINA_ID", '"xxxxxx"'
            buildConfigField "String",           "WX_ID", '"xxxxxx"'
            buildConfigField "String",           "UM_ID", '"xxxxxx"'
            buildConfigField "String",       "WX_SECRET", '"xxxxxx"'
            buildConfigField "String",   "SINA_REDIRECT", '"http://open.weibo.com/apps/xxxxxx/privilege/oauth"'

            buildConfigField "String",   "ADHUB_INIT_ID", '"xxxxxx"' // 广告sdk初始化id
            buildConfigField "String", "ADHUB_SPLASH_ID", '"xxxxxx"' // 开屏广告id
            buildConfigField "String", "ADHUB_BANNER_ID", '"xxxxxx"' // banner广告id

            buildConfigField "String",      "SERVER_URL", '"http://xxx.xxxx.com/"'
            buildConfigField "String",        "LOGO_URL", '"http://file.xxx.com/img/xxx.png"'

            manifestPlaceholders = [
                    qq_id: qq_id,
                    JPUSH_PKGNAME : applicationId,
                    JPUSH_APPKEY : "xxxxxx", //JPush 上注册的包名对应的 Appkey.
                    JPUSH_CHANNEL : "developer-default", //暂时填写默认值即可.
            ]
        }

        xemh {
            applicationId "com.xxx.xx"
            versionCode 1
            versionName "1.0.0"
            signingConfig = signingConfigs.xemhRelease

            String qq_id = '"xxxxxx"'
            buildConfigField "String",           "QQ_ID", qq_id
            buildConfigField "String",         "SINA_ID", '"xxxxxx"'
            buildConfigField "String",           "WX_ID", '"xxxxxx"'
            buildConfigField "String",           "UM_ID", '"xxxxxx"'
            buildConfigField "String",       "WX_SECRET", '"xxxxxx"'
            buildConfigField "String",   "SINA_REDIRECT", '"xxxxxx"'

            buildConfigField "String",   "ADHUB_INIT_ID", '"xxxxxx"' // 广告sdk初始化id
            buildConfigField "String", "ADHUB_SPLASH_ID", '"xxxxxx"' // 开屏广告id
            buildConfigField "String", "ADHUB_BANNER_ID", '"xxxxxx"' // banner广告id

            buildConfigField "String",      "SERVER_URL", '"http://xx.xxx.com/"'
            buildConfigField "String",        "LOGO_URL", '"http://file.xxxxxx.com/img/xxxxxx.png"'

            manifestPlaceholders = [
                    qq_id: qq_id,
                    JPUSH_PKGNAME : applicationId,
                    JPUSH_APPKEY : "xxxxxx", //JPush 上注册的包名对应的 Appkey.
                    JPUSH_CHANNEL : "developer-default", //暂时填写默认值即可.
            ]
        }
    }

    applicationVariants.all {
        variant ->
            variant.outputs.all {
                outputFileName = "${variant.productFlavors[0].name}-v${variant.productFlavors[0].versionName}-${releaseTime()}.apk"
            }
    }

    buildTypes {
        release {
            // 不显示Log
            buildConfigField "boolean", "LOG_DEBUG", "false"
            signingConfig null
            minifyEnabled true
            zipAlignEnabled true
            // 移除无用的resource文件
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }

        debug {
            // 显示Log
            buildConfigField "boolean", "LOG_DEBUG", "true"
            signingConfig null
            minifyEnabled false
            zipAlignEnabled false
            shrinkResources false
        }
    }
    packagingOptions {
        exclude 'META-INF/DEPENDENCIES.txt'
        exclude 'META-INF/NOTICE'
        exclude 'META-INF/NOTICE.txt'
        exclude 'META-INF/LICENSE'
        exclude 'META-INF/LICENSE.txt'
    }
    compileOptions {
        targetCompatibility JavaVersion.VERSION_1_8
        sourceCompatibility JavaVersion.VERSION_1_8
    }

    dexOptions {

        javaMaxHeapSize "4g" //此处可根据电脑本身配置 数值越大 当然越快

        preDexLibraries = false

    }
}

repositories {
    flatDir {
        dirs 'libs', '../adpoymer/libs'
    }
}

dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation "com.android.support:appcompat-v7:$supportLibraryVersion"
    implementation "com.android.support:recyclerview-v7:$supportLibraryVersion"
    implementation "com.android.support:support-v4:$supportLibraryVersion"
    implementation "com.android.support:design:$supportLibraryVersion"
    implementation "com.android.support.constraint:constraint-layout:$constraintVersion"

    //添加retrofit2 的依赖 添加这个依赖就默认添加了okhttp依赖
    compile "com.squareup.retrofit2:retrofit:$retrofit2Version"
    compile "com.squareup.retrofit2:converter-gson:$retrofit2Version"
    compile "com.squareup.retrofit2:adapter-rxjava2:$retrofit2Version"
    compile "com.squareup.okhttp3:logging-interceptor:$okhttp3Version"
    compile "com.jakewharton:butterknife:$butterknifeVersion"
    annotationProcessor "com.jakewharton:butterknife-compiler:$butterknifeVersion"
    compile "io.reactivex.rxjava2:rxandroid:$rx2Version"
    compile "com.github.xujiaji:xmvp:$xmvpVersion"
    implementation "com.github.autume:CircleProgressDialog:$CircleProgressDialogVersion"
    compile "com.ogaclejapan.smarttablayout:library:$smarttabVersion"
    compile "com.github.CymChad:BaseRecyclerViewAdapterHelper:$adapterHelperVersion"

    compile "com.github.bumptech.glide:glide:$glideVersion"
    annotationProcessor "com.github.bumptech.glide:compiler:$glideVersion"

    compile "com.makeramen:roundedimageview:$roundedimageviewVersion"
    compile "org.greenrobot:eventbus:$eventbusVersion"
    annotationProcessor "com.github.hotchemi:permissionsdispatcher-processor:$dispatcherVersion"
    compile "com.jaeger.statusbarutil:library:$statusbarutilVersion"
    compile("com.github.hotchemi:permissionsdispatcher:$dispatcherVersion") {
        exclude module: "support-v13"
    }
    implementation "com.github.LuckSiege.PictureSelector:picture_library:$picture_libraryVersion"
    implementation 'me.drakeet.library:crashwoodpecker:2.1.1'
    implementation 'com.github.chenupt.android:springindicator:1.0.2@aar'
    debugImplementation 'com.amitshekhar.android:debug-db:1.0.4'
    implementation 'com.umeng.sdk:common:1.5.3'
    implementation 'com.umeng.sdk:analytics:7.5.3'

    implementation 'com.liulishuo.filedownloader:library:1.7.5'

    implementation project(':banner')
    implementation project(':xdialog')
    implementation project(':shareutil')
    implementation project(':update')
    implementation project(':pay')
//    implementation project(':adhub')
    implementation project(':imagewatcher')
    implementation files('libs/lite-orm-1.9.2.jar')
    implementation 'jp.wasabeef:blurry:2.1.1'
    implementation "com.google.android:flexbox:$flexboxVersion"

    implementation 'cn.jiguang.sdk:jpush:3.1.6'  // 此处以JPush 3.1.6 版本为例。
    implementation 'cn.jiguang.sdk:jcore:1.2.5'  // 此处以JCore 1.2.5 版本为例。

    compile(name: 'sdk-release', ext: 'aar')
    compile(name: 'open_ad_sdk', ext: 'aar')
    compile(name: 'adpoymer-3.4.35', ext: 'aar')
    implementation 'pl.droidsonroids.gif:android-gif-drawable:1.0.+'
}

```

## Demo 地址
https://github.com/xujiaji/OneForAllApk

## 结束
就这样就可以解放大量劳动力啦！每次项目打包各种软件，选一下就ojbk，哈哈哈~
如果有些配置在其他渠道没有的，也可通过BuildConfig在java中判断如果是某某渠道那么屏蔽。
over
