---
title: Dagger2 的深入分析与使用
date: 2018-06-11 13:58:41
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/home.jpg
categories:
 - 文章
tags:
    - android
    - 分析框架
---

![脑图](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/main-mind.png)

听闻Dagger大名很久，但一直没有去学，直到不得不学 〒▽〒。<br>这个框架一开始的时候还真的是很不好理解，看了很多文章还是有很多没有理解到，看得似懂非懂，于是自己做了很多简单的测试代码观察Dagger注解的作用。在这里将学习和理解的过程分享出来，希望能帮到一些学些Dagger的朋友，同时我也巩固总结一下。

本篇文章不讲，Dagger哪里好哪里好！只讲怎么用的和一些原理！

## 是什么？
Dagger是一个依赖注入框架（Dependency injection），简称DI。依赖注入是一种技术称呼，假如有A和B两个对象，A中没有对自己内部的成员变量进行初始化，它的成员变量初始化全部是B类注入进来的。

Dagger旨在解决许多困扰基于反射的解决方案的开发和性能问题，Dagger的依赖注入是通过java代码来实现的，由于代码都是相同的逻辑，于是Dagger通过注解等帮我们自动生成相关的依赖注入逻辑代码。

额...，有点一头雾水的感觉吗？如果大家想详细知道概念的话，看来只有自行去搜索了。

在下面所讲的大部分都是以实际的代码操作为主来理解，代码本篇不会涉及Android 页面，只想通过简单的Java代码来理清楚这些知识。

## 需要添加的依赖
大家可以关注一下官方的最新版本：https://github.com/google/dagger

```
dependencies {
    implementation 'com.google.dagger:dagger:2.15'
    annotationProcessor 'com.google.dagger:dagger-compiler:2.15'
}
```

## 注解使用
> 欢迎来到本篇最精彩的地方，官方的使用指南：https://google.github.io/dagger/users-guide

>您可能需要的一些参考：

|符号══▶|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-private.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-m-private.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-protected.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-m-protected.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611140949.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141014.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141038.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141100.png)|
|-|-|-|-|-|-|-|-|-|
|**含义**══▶|private变量|private方法|protected变量|protected方法|包私有 变量|包私有方法|public 变量|public 方法|

|符号|含义|简单例子|
|-|-|-|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141212.png)|继承|`class A{}`<br>`class B extend A{}` |
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141236.png)|实现接口|`interface I{}`<br>`class A implements I{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141305.png)|依赖|`class A{}`<br>`class B{`<br>　　`void fun(A c) {}`<br>`}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141339.png)|并联|`class A{}`<br>`class B{`<br>　　`A a;`<br>`}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141403.png)|class|`class A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141425.png)|abstract|`abstract class A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141449.png)|interface|`interface A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141508.png)|enum|`enum A{}`|
|`...`|省略代码|`class A {...}`|

### 先看一下一个咖啡机事例
主要用了一个咖啡机的例子来演示，首先我们来看一下主要的几个类，下面是UML关系图！

![咖啡机UML](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141527.png)

> 如果以我们正常写代码的操作

``` java
/**
 * 汞接口
 */
interface Pump {
    void pump();
}
---------------------------------------------------------------------------------
/**
 * 加热器接口
 */
interface Heater {
    void on();
    void off();
    boolean isHot();
}
---------------------------------------------------------------------------------
/**
 * 电子加热器
 */
public class ElectricHeater implements Heater {
    boolean heating;
    @Override
    public void on() {
        System.out.println("~~~~heating~~~~");
        this.heating = true;
    }
    @Override
    public void off() {
        this.heating = false;
    }
    @Override
    public boolean isHot() {
        return heating;
    }
}
---------------------------------------------------------------------------------
/**
 * 热虹吸
 */
public class Thermosiphon implements Pump {
    private final Heater heater;
    Thermosiphon(Heater heater) {
        this.heater = heater;
    }
    @Override
    public void pump() {
        if (heater.isHot()) {
            System.out.println("=>=> 抽水 =>=>");
        }
    }
}
---------------------------------------------------------------------------------
/**
 * 咖啡机
 */
public class CoffeeMaker {
    Heater heater;
    Pump pump;
    public CoffeeMaker(Heater heater, Pump pump) {
        this.heater = heater;
        this.pump = pump;
    }
    public void brew() {
        heater.on();
        pump.pump();
        System.out.println("[_]P coffee! [_]P");
        heater.off();
    }
}
---------------------------------------------------------------------------------
/**
 * 出咖啡测试
 */
public class CoffeeApp {
    public static void main(String[] args) {
        Heater heater = new ElectricHeater();//实例化加热器
        Pump pump = new Thermosiphon(heater);//实例化汞
        CoffeeMaker coffeeMaker = new CoffeeMaker(heater, pump);//实例化咖啡机
        coffeeMaker.brew();//出咖啡
    }
}
```
### @Inject
> 如其名：注入，通过@Inject标记成员变量和对应对象的构造方法，一个实例化操作就省了。下面的例子将会提前用到`@Component`注解您可以先不去理解，它就是一个连接纽带。

> 这里在构造方法上加`@Inject`可以理解为：提供`new ElectricHeater()`

``` java
/**
 * 电子加热器
 */
public class ElectricHeater implements Heater {
    @Inject
    public ElectricHeater() {
    }
    ...
}
```

> `@Component`起纽带作用，这个类用接口来定义。`Thermosiphon getPump()`表示其他地方需要提供`new Thermosiphon()`（一个Thermosiphon的实例对象）

``` java
@Component
public interface PumpComponent {
    Thermosiphon getPump();
}
```
> 一个`@Inject`标记在成员变量上，表示其他地方需要提供`ElectricHeater`对象，也就是上上面代码中`@Inject`标记在构造方法的作用。第二个`@Inject`标记在构造方法上，可以看做表示提供一个`new Thermosiphon()`，也就是上面接口中需要的对象。

``` java
/**
 * 热虹吸
 */
public class Thermosiphon implements Pump {
    @Inject
    ElectricHeater heater;

    @Inject
    public Thermosiphon()
    {}

    @Override
    public void pump() {
        if (heater.isHot()) {
            System.out.println("=>=> 抽水 =>=>");
        }
    }
}
```

``` java
//运行测试
public class CoffeeApp {
    public static void main(String[] args) {
        Thermosiphon pump = DaggerPumpComponent.create().getPump();
        pump.heater.on();
        pump.pump();
    }
}
```
- 最后我们直接在CoffeeApp中进行测试，`DaggerPumpComponent`是通过apt自动生成的类（需要在Android studio中点击：Build -> Make Module）。通过`DaggerPumpComponent.create().getPump();`既可以得到`Thermosiphon`对象。 也可以写作`DaggerPumpComponent.builder().build().getPump();`效果是一样的。
- 可以看到在`Thermosiphon`中`heater`是以`ElectricHeater`来接收，并不是向上面用接口`Heater`，因为`@Inject`标记需要是确切的类型，需要在往下学，我们才能有方法用`Heater`接口来接收。
- 通过上面例子我们明显看到，我们并没有new 对象，然而却有`ElectricHeater`和`ElectricHeater`被实例化，这就是Dagger生成的模板中帮我们进行了实例化的操作。
- 还有就是成员变量和构造方法不能以`private`修饰，因为如果我们用private，Dagger不能帮我们注入对象，会报错!你可以试试看哦！(￣▽￣)~*
- 也许你想问`DaggerPumpComponent`是哪来的？用`@Component`标记的接口会生成一个以`“Dagger + 接口名”`的类。
- 经测试，如果将成员变量上的`@Inject`去掉，不会报错，只是没有引用的对象，变量为null。如果成员变量上标记了`@Inject`，而没有对应的注入实例，则会编译错误。
- Dagger生成代码的位置：`项目目录 -> app -> build -> generated -> source -> apt`

> *接下来从生成的代码上分析（这部分不用了解也是可以的哦！(｀・ω・´)）*

> 这是整体的UML关系图，“绿色”的是Dagger和它自动生成的代码。

![inject uml](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/inject-uml.png)
1. 通过上面的三部分代码，Dagger为我们生成了4个类。![生成的类](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/build-class.png)
2. 他们这样对应：

||||
|-|-|-|
|PumpComponent|----->|DaggerPumpComponent|
|@Inject public ElectricHeater() { }|----->|ElectricHeater_Factory|
|@Inject public Thermosiphon() { }|----->|Thermosiphon_Factory|
|@Inject ElectricHeater heater;|----->|Thermosiphon_MembersInjector|
从名字上我们可以看出：
- ①`PumpComponent`接口生成的类的名字以：`Dagger` + `接口名`，命名生成一个组装类。
- ②`@Inject`标记的构造会生成类名以：`构造名` + `_Factory`，命名生一个工厂类。
- ③类中有`@Inject`标记成员变量的类，会生成一个以：`该类名` + `_MembersInjector`，命名生成一个注入类。
3. 来看看`ElectricHeater`的工厂类`ElectricHeater_Factory`，这是一个工厂设计模式中的一种，实现一个工厂接口`Factory<T>`(`Factory<T>`又继承`Provider<T>`接口)。通过`get()`获取一个ElectricHeater实例，通过`create()`获取`ElectricHeater_Factory`实例（这个类并未被使用，当你看到下面介绍`DaggerPumpComponent`你就明白了）![ElectricHeater_Factory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/ElectricHeater_Factory.png)
4. 接下来看看`Thermosiphon_MembersInjector`，这个类里面写的是关于，将`ElectricHeater`对象注入到`Thermosiphon`的成员变量`heater`的逻辑。大家看`injectHeater`方法，瞬间能明白这就是为`Thermosiphon`的成员变`heater`添加依赖的地方了吧!![Thermosiphon_MembersInjector.java](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/Thermosiphon_MembersInjector.png)
5. 再看看`Thermosiphon_Factory`，这个类比上一个`ElectricHeater_Factory`复杂一点，因为它需要注入`ElectricHeater`对象。很明显这比`ElectricHeater_Factory`多两个方法并且创建时也多了个参数。
    - 构造参数是`ElectricHeater`的工厂，是为了通过工厂类获得`ElectricHeater`对象；
    - 工厂方法`get()`中创建并通过上面`Thermosiphon_MembersInjector`的静态方法(`injectHeater`)向`Thermosiphon`注入`ElectricHeater`对象，最后返回`Thermosiphon`实例
    - 最后一个静态方法`newThermosiphon()`返回一个没有注入`ElectricHeater`的`Thermosiphon`对象。
    
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142100.png)
6. 最后看`DaggerPumpComponent`这个类，主要是`getPump()`、`injectThermosiphon`和一个`Builder`类
    - `getPump()`是我们在接口中定义的方法，在这里实现了这个方法，通过`injectThermosiphon`方法返回`Thermosiphon`实例。
    - `injectThermosiphon`方法需要一个`Thermosiphon`参数，这个参数就是上面5.`Thermosiphon_Factory`的静态方法`newThermosiphon`创建的。然后通过4.`Thermosiphon_MembersInjector`注入`ElectricHeater`。看到这里我们会发现第3.介绍的`ElectricHeater_Factory`居然没有用到，这里直接就new了。
    - `Builder`就是一个创建`DaggerPumpComponent`的建造类，学到后面，这个类会更具需求变复杂！
    - 还记得上面介绍`ElectricHeater_Factory`时提到的没有被使用吗？看看`injectThermosiphon`方法中，并没有通过`ElectricHeater_Factory`来创建`ElectricHeater`实例，而是直接new的。
    
    ![DaggerPumpComponent.java](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142127.png)

### @Provides丶@Module
> 通过上面对注释`@Inject`的了解，我们可以知道它有以下几点无法做到：

- 接口类型无法做为接收类型
- 第三方类无法注释`@Inject`（因为这个类不是自己掌控的）

> 为了弥补`@Inject`注入无法做到的尴尬情况，可以用`@Provides`注释的方法去满足依赖，方法的返回类型定义了它满足哪个依赖关系。

> 使用

- 创建一个以`Module`结尾的类（便于分辨，就像我们安卓Activity命名以Activity结尾）
- 在类名上标记`@Module`
- 使用静态或普通返回方法，返回实例
    - 在这些方法前需要标记`@Provides`
    - 这些方法以`provide`开头，也是一种约定
- 看下方这个`DripCoffeeModule`类，提供了两个实例，并且它们的返回类型指向的是接口

``` java
@Module
public class DripCoffeeModule
{
    @Provides
    static Heater provideHeater() {
        System.out.println("provideHeater");
        return new ElectricHeater();
    }

    @Provides
    static Pump providePump(Thermosiphon pump) {
        System.out.println("providePump");
        return pump;
    }
}
```
- 在`@Component`注释中添加`DripCoffeeModule.class`，如果有多个可写为：`@Component(modules = {DripCoffeeModule.class, ...class,...class})`
```
@Component(modules = DripCoffeeModule.class)
public interface CoffeeShop
{
    Pump getPump();
}
```
- 其他类
```
/**
 * 电子加热器
 */
public class ElectricHeater implements Heater
{

    public ElectricHeater()
    {
        System.out.println("ElectricHeater()");
    }
    ...
}
---------------------------------------------------------------------------------
/**
 * 热虹吸
 */
public class Thermosiphon implements Pump
{
    private Heater heater;
    @Inject
    public Thermosiphon(Heater heater) {
        System.out.println("Thermosiphon() heater = " + heater);
        this.heater = heater;
    }
    ...
}

```
- 测试：
``` java
/**
 * 测试
 */
public class CoffeeApp
{
    public static void main(String[] args) {
        Pump pump = DaggerCoffeeShop.create().getPump();
        System.out.println("pump = " + pump);
        pump.pump();
    }
}
```
- 运行输出结果：
``` java
provideHeater
ElectricHeater()
Thermosiphon() heater = com.example.jiaji.daggertest.coffee3.ElectricHeater@29453f44
providePump
pump = com.example.jiaji.daggertest.coffee3.Thermosiphon@5cad8086
```
- 
    - 通过输出的结果我们可以看出一些眉目
    - 首先，我们调用`DaggerCoffeeShop.create().getPump()`想要得到一个Pump对象，于是找到了`DripCoffeeModule`中的`providePump`方法。
    - 然后，我们会看到`providePump`方法需要提供`Thermosiphon`这个对象，于是我们在`Thermosiphon`的构造方法上标记了`@Inject`表示提供该对象。
    - 接下来，我们又会发现，要提供`Thermosiphon`对象的构造方法要求提供`Heater`对象，于是我们可以看到在`DripCoffeeModule`的`provideHeater`方法提供了该实例。
    - 最后，我们可以得出来个容易理解的大概流程：![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143230.png)

> 我们需要注意，当构造方法上标有`@Inject`并且它的`Module`中又提供了实例的情况下，会优先选择`Module`中提供的实例。

> 通过上面的例子，我们可以注意到：`@Inject`可以为`Module`方法的参数提供实例

> 我们还可以将Module中的方法分类到多个Module中写，只需要在`@Component`注释中添加一下（这样的好处是当提供的实例多了后，我们可以把不同类型的对象归类或者说我们当前的需要某一系列的对象。），如下所示：

``` java
@Module
public class DripCoffeeModule
{
    @Provides
    static Heater provideHeater() {
        System.out.println("provideHeater");
        return new ElectricHeater();
    }

}
---------------------------------------------------------------------------------
@Module
public class DripCoffeeModule2
{
    @Provides
    static Pump providePump(Thermosiphon pump) {
        System.out.println("providePump");
        return pump;
    }
}
---------------------------------------------------------------------------------
@Component(modules = {DripCoffeeModule.class, DripCoffeeModule2.class})
public interface CoffeeShop
{
    Pump getPump();
}
```
> 其实还有种写法，意思是表示某一个Module包含另一个Module。概念不一样，效果和上面是一样的。如下所示：

``` java
@Module
public class DripCoffeeModule2
{
    @Provides
    static Pump providePump(Thermosiphon pump) {
        System.out.println("providePump");
        return pump;
    }
}
---------------------------------------------------------------------------------
@Module(includes = DripCoffeeModule2.class)
public class DripCoffeeModule
{
    @Provides
    static Heater provideHeater() {
        System.out.println("provideHeater");
        return new ElectricHeater();
    }
}
---------------------------------------------------------------------------------
@Component(modules = DripCoffeeModule.class)
public interface CoffeeShop
{
    Pump getPump();
}
```

> *接下来又是生成的代码上分析（这部分可以选择性跳过哦！(｀・ω・´)）*

> 这是整体的UML关系图，“绿色”的是Dagger和它自动生成的代码。(由于生成的`Thermosiphon_Factory`并没有被使用，于是就不放进来了。)

![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142208.png)
1. 通过上面的三部分代码，Dagger也为我们生成了4个类。![dagger生成的四个类](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142229.png)



2. 他们这样对应：

||||
|-|-|-|
|CoffeeShop|----->|DaggerCoffeeShop|
|@Provides static Heater provideHeater()|----->|DripCoffeeModule_ProvideHeaterFactory|
|@Provides static Pump providePump(Thermosiphon pump)|----->|DripCoffeeModule_ProvidePumpFactory|
|@Inject public Thermosiphon() { }|----->|Thermosiphon_Factory|
从名字上我们可以看出：
- `@Provides`标记的提供实例的方法对应生成了一个类名以：`所在类名` + `_` + `方法名(首字大写)` + `Factory`，命名生成一个对应返回实例的工厂类。
3. 我们先来看看`Thermosiphon_Factory`这个类，生成的这个类并没有被使用，如果您是从上面挨着看下来的，就一定明白，其他地方是直接`new Thermosiphon`，接着往下看您就会看到！
    - 这个类和上面生成的`Thermosiphon_Factory`有些不一样，因为之前`Thermosiphon`构造是无参的，现在添加了`Heater`作为必须传入的构造参数，而不是靠`@Inject`来注入到成员变量。
    - 可以看到要创建这个工厂类，必须要传入`Heater`的工厂类。然后在创建`Thermosiphon`实例时通过`Heater`工厂类创建一个`Heater`对象传入构造方法中。
    - 并且它还添加了`一个newThermosiphon`的静态方法，允许传入`heater`对象来创建`Thermosiphon`。

    ![Thermosiphon_Factory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142247.png)
4. 我们在来看`Heater`工厂类`DripCoffeeModule_ProvideHeaterFactory`，它相对比较简单点。
    - 可以看到在创建`Heater`实例时，直接通过`DripCoffeeModule.provideHeater()`调用我们定义的相对应的静态方法。
    - 通过`Preconditions.checkNotNull`又检测了是否提供得有实例，没有将会报第二参数传入的错误信息。
    - 工厂本身的实例是通过静态方法`create()`创建，它还定义了一个静态方法，可不创建工厂类的情况下，直接获取`Heater`对象。
    
    ![DripCoffeeModule_ProvideHeaterFactory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142310.png)
    
    - 其实`DripCoffeeModule`中的方法可以不用静态方法！普通方法也是可以的。那如果我们将`DripCoffeeModule`中的静态方法的static去掉改为普通方法生成的代码又是怎么样的呢？(`@Provides static Heater provideHeater()`改为`@Provides Heater provideHeater()`)看下图。
        - 可以看到此时我们的`Heater`工厂类`DripCoffeeModule_ProvideHeaterFactory`的创建必须传入`DripCoffeeModule`对象，然后我们才能通过`DripCoffeeModule`对象在`get()`方法获取`Heater`实例
        - 同样创建`Heater`的静态方法`proxyProvideHeater`也必须传入`DripCoffeeModule`作为参数。
    
        ![DripCoffeeModule_ProvideHeaterFactory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142330.png)
5. 接下来，我们来看看`Pump`的工厂类`DripCoffeeModule_ProvidePumpFactory`
    - 首先我们知道在Module中是这样定义的：`@Provides static Pump providePump(Thermosiphon pump) { return pump; }`
    - 要调用这个方法又必须得到`Thermosiphon`的实例传进去，所以`DripCoffeeModule_ProvidePumpFactory`的构造参数是`Thermosiphon`的工厂对象，这样我们才能在调用`get()`方法，然后它又通过调用`providePump`创建Pump实例的时候我们能得到一个`Thermosiphon`对象。
    - 我们看到`proxyProvidePump`方法，也是可在不创建工厂类的情况下，通过类名点方法获取一个对象。开始说为什么没有使用到`Thermosiphon_Factory`呢？因为Dagger直接调用的这个静态方法。
    
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142349.png)
    
    - 如果我们也把Module中的static修饰去掉又会发生什么样的变化呢？我猜您也应该能想到了！看下图。
        - 它就是多了图上划线的地方，跟上面去掉后的情况是一样的
        - 也就是说当我们定义的方法是普通方法时，我们就必须要提供`Module`的实例
        
        ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142412.png)
6. 最后，我们来看`DaggerCoffeeShop`是如何将这些东东组合在一起的。
    - 我们直接看到`getPump()`方法，它是我们接口`CoffeeShop`中定义的方法，它是如何实现的呢！
    - 它直接调用了上面`5`所讲到的静态方法`proxyProvidePump`来创建`Pump`实例，但是需要提供参数`Thermosiphon`。
    - 于是，它定义了方法`getThermosiphon()`来创建。看到该方法了吗？里面是直接`new Thermosiphon`，这就是`Thermosiphon_Factory`没有用到的根本原因。创建`Thermosiphon`的构造参数`Heater`由`DripCoffeeModule_ProvideHeaterFactory`类名直接调用静态方法`proxyProvideHeater()`它又调用`DripCoffeeModule.provideHeater()`来提供。
    
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142434.png)
    
    - 接下来看到创建`DaggerCoffeeShop`的`Builder`类，这里面可要比我们上次生成的`DaggerPumpComponent`要多了一个方法，它出现的原因就是因为我们定义了Module类。
        - 这个方法的命名方式是将我们定义的Module类的类名开头小写来作为名字。
        - 它的作用是我们可以自己创建Module，如果不传入，将会自动创建。
        - 但为什么这里标记为弃用呢？那是因为我们Module中全是静态方法，完全不需要实例化，实例化也白搭！那我们来看看，将`DripCoffeeModule`中的方法改为普通方法是什么样的呢！
    
        ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142457.png)
        
        - 看到了吧！如果build()中判断了我们已经调用`dripCoffeeModule`方法传进来了Module对象，那么它就不去实例化了。
        - 还记得上面我们去到static后的工厂方法中需要Module对象吧！它们就是来自于这里的。
        - 可以看出`dripCoffeeModule`的调用方式就是：`DaggerCoffeeShop.builder().dripCoffeeModule(new DripCoffeeModule()).build();`（如果我们的`@Component`连接了多个`Module`那么就可以这样传入这么多个`Module`实例）
        - 那么这个方法到底有什么神奇的作用呢？我们想想看，如果`Module`的构造方法需要传参，此时我们该怎么办呢？看一下下面这个例子你就明白了！
        ``` java
        public class TestModuleAttr {
            private String str;
            public TestModuleAttr(String str) { this.str = str; }
            @Override
            public String toString() {return "TestModuleAttr{" + "str='" + str + '\'' +'}';}
        } 
        ------------------------------------------
        @Module
        public class DripCoffeeModule {
            private String str;
            public DripCoffeeModule(String str) { this.str = str; }
            ...
            @Provides String provideStr() { return str; }
            @Provides TestModuleAttr provideTestModuleAttr(String s) { return new TestModuleAttr(s); }
        }
        ------------------------------------------
        @Component(modules = {DripCoffeeModule.class})
        public interface CoffeeShop{
            Pump getPump();
            TestModuleAttr getTestModuleAttr();
        }
        ------------------------------------------
        /**
         * 测试
         */
        public class CoffeeApp{
            public static void main(String[] args) {
                System.out.println(
                        DaggerCoffeeShop
                                .builder()
                                .dripCoffeeModule(new DripCoffeeModule("Hello world"))
                                .build()
                                .getTestModuleAttr());
        //        Pump pump = DaggerCoffeeShop.create().getPump();
        //        System.out.println("pump = " + pump);
        //        pump.pump();
            }
        }
        ```
        - 最后的输入结果为：`TestModuleAttr{str='Hello world'}`
        - 当我们想向提供的对象传递一些缺少东西时，就可以通过这种方式，当然你也不用向我这样绕了个圈子，这里只想说`Module`里面可以相互提供实例。这`DripCoffeeModule`里可以直接`@Provides TestModuleAttr provideTestModuleAttr() { return new TestModuleAttr(str); }`搞定。
        - 需要注意的是，如果`Module`是这样的有参构造时，我们必须自己实例化`Module`。如果不，则会抛出异常。原因，看下图：![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142517.png)

### @Component
> 上面这么多地方涉及到它，看到这里大家恐怕都已经熟悉这东东了。ヾ(๑╹◡╹)ﾉ"

> 官方把这个定义叫做建立图表，我们可以把它理解为“桥”，连接两岸。它起到的作用是连接依赖关系，通过上面详情的分析，我们就可以直观的看到在`DaggerXXX`(`@Component`修饰的类对应所生成的文件)类中，主要就是将各个工厂类和Module连接起来。

> 如果我们像下面这样定义一个Component，Dagger将会为我们生成一个类：`DaggerFoo_Bar_BazComponent`

``` java
class Foo {
  static class Bar {
    @Component
    interface BazComponent {}
  }
}
```

> `@Component`不仅可以装饰接口还可以是抽象类，比如上面的`CoffeeShop`类还可以像下面这样写：

``` java
@Component(modules = {DripCoffeeModule.class})
public abstract class CoffeeShop
{
    abstract Pump getPump();
    abstract TestModuleAttr getTestModuleAttr();
}
```

> 在Component中所定义有返回类型的方法，他们的返回类型就是我们需要提供的实例。只有我们提供了实例，Dagger才能帮助我们将它们自动连接起来。

> 接下来我们来通过模拟安卓中Activity的启动，该代码大概模拟了一下MVP，为了简单，我没有写MVP接口和M层。这里主要是想解释为什么在Compnent接口中需要定义一个`void inject(XXXActivity activity);`，看到别人这么写，说这样才能OK，但我当时真心不知道这是啥意思！于是这里我想通过简单的代码去理解它。

1. 模拟一个Activity，一般我们在Activity的`onCreate()`方法中是这样写的。
``` java
public class MNActivity
{
    @Inject
    MNPresenter presenter;
    public void onCreate()
    {
        System.out.println("MNActivity hashCode = " + hashCode());
        DaggerTestComponent
                .builder()
                .mNModule(new MNModule(this))
                .build()
                .inject(this);
        System.out.println(presenter);
    }
}
```
2. 一个Presenter类，在presenter中一般我们是依赖的view的接口，这里我们之间依赖activity。
    - 用被`@Inject`标记构造，表明需要提供该类的实例
    - 我们又看到有构造方法参数为`MNActivity`，表明我们又需要为它提供`MNActivity`
``` java
public class MNPresenter
{
    MNActivity mnActivity;
    @Inject
    MNPresenter(MNActivity mnActivity)
    {
        this.mnActivity = mnActivity;
        System.out.println("MNPresenter mnActivity = " + mnActivity.hashCode());
    }
}
```
3. 依赖注入部分类：Module
    - `MNModule`是有参构造，通过上面的学习，我们知道这种情况必须我们自己实例化Module
    - 通过`provedesActivity`我们可以将传递进来的`MNActivity`实例，提供出去（这里提供给`MNPresenter`）
    
``` java
@Module
public class MNModule
{
    MNActivity mnActivity;
    public MNModule(MNActivity mnActivity)
    {
        this.mnActivity = mnActivity;
    }

    @Provides
    MNActivity provedesActivity()
    {
        return mnActivity;
    }
}
```
4. 依赖注入部分类：Component
    - 这里方法返回值为void
``` java
@Component(modules = MNModule.class)
public interface TestComponent
{
    void inject(MNActivity me);
}
```
5. 启动Activity类
``` java
public class Main
{
    public static void main(String[] args)
    {
        MNActivity injectMe = new MNActivity();
        injectMe.onCreate();
    }
}
```
6. 运行Main的结果
``` java
MNActivity hashCode = 21685669
MNPresenter mnActivity = 21685669
com.example.jiaji.daggertest.coffee4.MNPresenter@61bbe9ba
```
> 为什么这么神奇呢？居然就这样就将`MNPresenter`的实例注入到`MNActivity`了，其实`DaggerTestComponent`实现我们定义的`void inject(MNActivity me);`，然后在方法里进行了如这样的操作（简化后）：`me.presenter = new Presenter(...);`

> 我们可以将`void inject(MNActivity me);`的实现代码和上面测试`@Inject`时定义的`Thermosiphon getPump();`实现代码进行比较，来看看有何区别。

- 我们先来看`Thermosiphon getPump();`是如何实现的，看下图：
    - 它首先通过`Thermosiphon_Factory.newThermosiphon()`直接`new Thermosiphon()`。
    - 然后调用`injectThermosiphon`方法将实例化的`Thermosiphon`通过`Thermosiphon_MembersInjector.injectHeater`将一个`ElectricHeater`链接到对应的成员变量。
    - 最后将一个完成的`Thermosiphon`返回。
![getPump() 实现](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142542.png)
- 我们再来看`void inject(MNActivity me);`是如何实现的，看下图：
    - 这里`inject(MNActivity me)`的实现直接省略掉了创建`MNActivity`的过程，直接调用`injectMNActivity`进行注入。
    - 为什么呢？因为当前`MNActivity`对象已经存在，只需要注入标有`@Inject`的成员变量就行了。
    - 我们想想Android中一个Activity打开，不就是通过其他流程来创建的吗！我们既然在Activity实例之中，又何必去实例化。
![inject方法的实现](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142555.png)

### 将所学运用到一开始的咖啡机实现
``` java
--------------------------------------------------------
interface Heater {
    void on();
    void off();
    boolean isHot();
}
--------------------------------------------------------
interface Pump {
    void pump();
}
--------------------------------------------------------
public class Thermosiphon implements Pump {
    private final Heater heater;
    @Inject
    Thermosiphon(Heater heater) {
        System.out.println("Thermosiphon(Heater heater) - heaterHash = " + heater.hashCode());
        this.heater = heater;
    }
    @Override
    public void pump() {
        if (heater.isHot()) {
            System.out.println("=>=> 抽水 =>=>");
        }
    }
}
--------------------------------------------------------
public class ElectricHeater implements Heater {
    public ElectricHeater() { System.out.println("ElectricHeater()"); }
    boolean heating;
    @Override
    public void on() {
        System.out.println("~~~~heating~~~~");
        this.heating = true;
    }
    @Override
    public void off() { this.heating = false; }
    @Override
    public boolean isHot() { return heating; }
}
--------------------------------------------------------
@Module
public class DripCoffeeModule {
    @Provides
    Heater provideheater() {
        System.out.println("provideheater()");
        return new ElectricHeater();
    }
    @Provides
    Pump providePump(Thermosiphon pump) {
        System.out.println("providePump");
        return pump;
    }
}
--------------------------------------------------------
/**
 * 咖啡机
 */
public class CoffeeMaker {
    @Inject
    Heater heater;//当我们要使用它时才创建一个加热器
    @Inject
    Pump pump;//汞

    @Inject
    CoffeeMaker() { }

    public void brew() {
        System.out.println("CoffeeMaker - heaterHash = " + heater.hashCode());
        heater.on();
        pump.pump();
        System.out.println("[_]P coffee! [_]P");
        heater.off();
    }
}
--------------------------------------------------------
@Component(modules = {DripCoffeeModule.class})
public interface CoffeeShop {
    CoffeeMaker maker();
}
--------------------------------------------------------
public class CoffeeApp
{
    public static void main(String[] args)
    {
        CoffeeShop coffeeShop = DaggerCoffeeShop.builder()
                .build();
        coffeeShop.maker().brew();
    }
}
```
> 我们来看一下输出结果

``` java
provideheater()
ElectricHeater()
provideheater()
ElectricHeater()
Thermosiphon(Heater heater) - heaterHash = 1625635731
providePump
CoffeeMaker - heaterHash = 1580066828
~~~~heating~~~~
[_]P coffee! [_]P
```
- 大家有没有发现，当我`heater.on()`后调用`pump.pump()`居然没有出水(没有打印：`=>=> 抽水 =>=>`)
- 通过日志看到`provideheater`被调用两次也就是两次new，我们还会会发现：`Thermosiphon`中的`Heater`对象和`CoffeeMaker`中的`Heater`对象打印的`hashCode`不一样，这根本就是两个实例。怪不得`CoffeeMaker`中`heater.on()`后`pump.pump()`不出水，原因就是`Pump`中又是另一个`Heater`实例。

> 看来通过上面的学习，我们的咖啡机还有点缺陷。通过下面所讲的`@Singleton`我们将可以解决这个多次实例化的问题。

> 最后我将上面这些大致理解思路画了如下流程图，希望能帮助您理解：

![dagger-liu-cheng](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142614.png)

### @Singleton丶@Scope
> Singleton:独生子的意思。我们可以这样去理解，标记了`@Singleton`提供的类，在一个Component实例中(这是条件)只提供一次，多次需要时，提供的实例也只是第一次创建的那个实例。

- 我们只需要将上面咖啡机的实现代码加两个`@Singleton`就可以解决问题了，如下代码：
    - 在提供那里加个`@Singleton`
    - 在`Component`那里加个`@Singleton`
    - 也就是说`@Singleton`我们最起码得添加两个地方

```
@Singleton
@Component(modules = {DripCoffeeModule.class})
public interface CoffeeShop {
    CoffeeMaker maker();
}
--------------------------------------------------------
@Module
public class DripCoffeeModule {
    @Singleton
    @Provides
    Heater provideheater() {
        System.out.println("provideheater()");
        return new ElectricHeater();
    }
    ...
}
--------------------------------------------------------
--------------------------------------------------------
输出日志：
provideheater()
ElectricHeater()
Thermosiphon(Heater heater) - heaterHash = 1872034366
providePump
CoffeeMaker - heaterHash = 1872034366
~~~~heating~~~~
=>=> 抽水 =>=>
[_]P coffee! [_]P
```
- 那么如果是`@Inject`标记的构造方法的方式来提供的对象，`@Singleton`该如何标记呢？如下代码：
    - 放到类名之上
```
@Singleton
public class SingletonTest{
    @Inject
    public SingletonTest(){}
}
--------------------------------------------------------
public class CoffeeMaker {
    ...
    @Inject
    SingletonTest singletonTest1;
    @Inject
    SingletonTest singletonTest2;
    @Inject
    SingletonTest singletonTest3;
    ...
    public void brew() {
        ...
        System.out.println(
                "singletonTest1 = " + singletonTest1.hashCode() + "\n"
                + "singletonTest2 = " + singletonTest2.hashCode() + "\n"
                + "singletonTest3 = " + singletonTest3.hashCode() + "\n");
    }
}
--------------------------------------------------------
--------------------------------------------------------
输出日志：
...
singletonTest1 = 1581781576
singletonTest2 = 1581781576
singletonTest3 = 1581781576
```

> 为什么说上面条件是在一个Component实例中，原因是因为如果，Component被创建多次，那么在Component中`@Singleton`标记的实例会生成它们所对应的不同实例。也就是在一个`Component`实例中是处于单例的。

- 来看看下面我们如果有多个Component实例的情况
- 我们修改一下`CoffeeApp`这个类，让他重复调用`brew()`方法和重新创建Component
``` java
public class CoffeeApp
{
    public static void main(String[] args)
    {
        CoffeeShop coffeeShop = DaggerCoffeeShop.builder()
                .build();
        coffeeShop.maker().brew();
        System.out.println("*************************************");
        coffeeShop.maker().brew();
        System.out.println("*************************************");
        DaggerCoffeeShop.builder()
                .build()
                .maker()
                .brew();
    }
}
```
- 输出结果(我们只看一些关键部分)：
```
...
CoffeeMaker - heaterHash = 1872034366
...
singletonTest1 = 1581781576
...
*************************************
...
CoffeeMaker - heaterHash = 1872034366
...
singletonTest1 = 1581781576
...
*************************************
...
CoffeeMaker - heaterHash = 1725154839
...
singletonTest1 = 1670675563
...
```
- 通过输出我们很明显的看出，第一次和第二次都是同一个实例。但是第三次就是不同的实例了，因为我们重新实例化了一个Component。
- 如果我们想在其他地方调用的时候也得到同一个Component实例，我们可以将Component作为抽象类，并设置为单例。如下：
``` java
@Component(modules = {DripCoffeeModule.class})
public abstract class CoffeeShop {
    private static CoffeeShop instance;
    abstract CoffeeMaker maker();
    public static CoffeeShop getInstance()
    {
        if (instance == null)
        {
            synchronized (CoffeeShop.class)
            {
                instance = DaggerCoffeeShop.create();
            }
        }
        return instance;
    }
}
```
- 当我们的使用的时候就不去build了，直接像这样：`CoffeeShop.getInstance().maker().brew()`
- 我们在Android中，可以把这种全局的定义放到`Application`中。

> 讲了这么多`@Singleton`，那么`@Scope`又是什么呢？其实`@Scope`是用来标识注解的。我们看一下，注解`@Singleton`的定义你就明白了！

``` java
@Scope
@Documented
@Retention(RUNTIME)
public @interface Singleton {}
```
- 也就是说用`@Scope`标识的注解都有`@Singleton`的功能，于是我们可以定义我们自己想要的注解名字来实现相同功能。
- 但需要注意一点就是用的时候相对应的注解必须是同一个（比方说我定义了一个`@MySingle`，就不能在Component那里用`@MySingle`的同时，对应的提供对象那里又没有`@MySingle`注解是`@Singleton`）

> 又到了我们分析生成代码的环节，大家可以选择性跳过哦！(〃'▽'〃)

1. 首先我们直接来看`DaggerCoffeeShop`这个类，其他都和上面讲解的一样，变化就在该类！
    - 我们先看到下图画红线的部分，看到了吧！他将`@Singleton`标记的对象直接放到了`DaggerCoffeeShop`作为成员变量（由于代码太多，我将`CoffeeMaker`中的`SingletonTest`都注释了）。
    - 等等！`Provider<Heater>`根据上面我们队工厂代码的研究！每次调用`get()`不都会重新实例化一个对象吗？这就是第二根红线那句代码起的作用了！
![DaggerCoffeeShop](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142629.png)
2. 来看看`DoubleCheck.provider`起了什么名堂，大家跟着我点进去悄悄！
    - 首先我们看一下调用的这个静态方法什么作用！很明显，它是为了创建一个`DoubleCheck`对象，如果传进来的就是`DoubleCheck`对象，则直接返回实例。
    ``` java
    public static <P extends Provider<T>, T> Provider<T> provider(P delegate) {
        checkNotNull(delegate);
        if (delegate instanceof DoubleCheck) {
            return delegate;
        }
        return new DoubleCheck<T>(delegate);
    }
    ```
    - 我们看到`DoubleCheck`类其实也是实现了`Provider`接口的，所以在`DaggerCoffeeShop`中才能直接用`Provider`来引用。它既然是也是一个`Provider`却又要传入一个`Provider`，说明它要起的是一个代理的作用。
    - 为什么`get()`调用后是同一个实例，就是因为它在`get()`中进行了处理，如果`get()`过一次实例，那么下次将返回上一次的实例，也就是一个单例模式。下面是这部分源码：
        - 我们可以看到它不仅仅进行了只返回一个实例的的代码，还写了一堆关于多线程需要的同步锁相关代码。
        - 也就是说我们在多线程的情况下也可以放心的调用`get()`方法，而不用担心因为多线程而创建额外的实例。
        ``` java
        public T get() {
           Object result = instance;
           if (result == UNINITIALIZED) {
               synchronized (this) {
                   result = instance;
                  if (result == UNINITIALIZED) {
                        result = provider.get();
                        Object currentInstance = instance;
                        if (currentInstance != UNINITIALIZED && currentInstance != result) {
                            throw new IllegalStateException("Scoped provider was invoked recursively returning "
                                    + "different results: " + currentInstance + " & " + result + ". This is likely "
                                    + "due to a circular dependency.");
                        }
                        instance = result;
                        provider = null;
                    }
                }
            }
            return (T) result;
        }
        ```

### @Reusable
> 它的用法和`@Singleton`达到的效果，差不多，而且逻辑也差不多。也是实现了单实例，但是它却不保证是单实例！

> 它的用法比`@Singleton`还简单点，只需要在提供的地方加个`@Reusable`就可以了，如下代码：

- 就这么简单就OK了，不用在Component中添加。

``` java
@Module
public class DripCoffeeModule {
    @Reusable
    @Provides
    Heater provideheater() {
        System.out.println("provideheater()");
        return new ElectricHeater();
    }
    ...
}
```

> 我们还是来看看，生成的代码吧！

1. 我们直接看当我们用`@Reusable`后，`DaggerCoffeeShop`有什么变化！
    - 唯一发生变化了地方就是这个方法里面的实现由`DoubleCheck.provider`变成了`SingleCheck.provider`
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142648.png)
2. 那我们来到`SingleCheck`这个类，它和`DoubleCheck`不同点就在于`get()`方法的实现上，请看下面`SingleCheck`的`get()`源代码：
    - 可以看到它省去了`SingleCheck`中一堆关于线程同步的代码
    - 也就是说我们在单线程中是可以放心使用`@Reusable`而不用担心重复实例化。
    ``` java
    public T get() {
        Provider<T> providerReference = provider;
        if (instance == UNINITIALIZED) {
            instance = providerReference.get();
            provider = null;
        }
        return (T) instance;
    }
    ```

### Lazy 注入
> 通过它可以实现惰性实例化，也就是当我们第一次调用的时候才会创建实例，并且多次调用不会再次创建实例，只会返回第一次创建的实例。

> 我们来看看它的用法！

1. 首先我们创建一个需要提供的对象
```
public class LazyEntity
{
    @Inject
    public LazyEntity(){}
}
```
2. 然后我们创建一个Component，需要提供提供一个`Main`类
```
@Component
public interface MyComponent
{
    Main getMain();
}
```
3. 我们来看看这个`Main`类。Lazy的使用方法就是将要使用的对象作为Lazy的泛型参数，如下所示
```
public class Main
{
    @Inject
    Lazy<LazyEntity> entityLazy;

    @Inject
    public Main() {}

    public static void main(String[] args)
    {
        Main main = DaggerMyComponent.builder()
                .build()
                .getMain();

        for (int i = 0; i < 3; i++)
        {
            System.out.println(main.entityLazy.get().hashCode());
        }
    }
}
```
4. 输出结果，也就是说我们重复调用都是一个实例。
```
1872034366
1872034366
1872034366
```

> 来吧！进入生成代码分析阶段（当然可以选择跳过哈！）ヾ(◍°∇°◍)ﾉﾞ

1. 我们直接看生成的`DaggerMyComponent`，需要值得注意的就是下面图片上划线的部分。
    - 可以看到这里也使用了`DoubleCheck`类，也就是说我们得到的`Lazy`对象就是一个`DoubleCheck`。
    - 所以说我们能多次调用也只能返回相同的实例，而且我能也能在多线程调用也不担心重复实例化。
![DaggerMyComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142703.png)
2. 那么我们来看一下`DoubleCheck.lazy`这个静态方法，源代码如下：
    - 可以看到和之前介绍的`DoubleCheck.provider`一个模子刻出来的，那这里大家就自行了解咯！！
``` java
    public static <P extends Provider<T>, T> Lazy<T> lazy(P provider) {
        if (provider instanceof Lazy) {
            @SuppressWarnings("unchecked") final Lazy<T> lazy = (Lazy<T>) provider;
            return lazy;
        }
        return new DoubleCheck<T>(checkNotNull(provider));
    }
```

### Provider 注入
> 当您需要多个实例时，可以通过`Provider<T>`作为成员变量，您只需要每次调用它的`get()`方法就会返回不同的实例。

> 我们直接将上面例子的`Lazy`改成Provider，其他都不变，如下：

``` java
public class Main
{
    @Inject
    Provider<LazyEntity> entityLazy;
    ...
}
```

> 来看一下输出的结果：

- 我们循环调用了三次`get()`方法，产生了三个不同的实例
``` java
692404036
1554874502
1846274136
```

> 来吧！生成代码分析阶段(｡･ω･｡)

1. 我们就直接看`DaggerMyComponent`中是怎么注入的吧！
    - 看到划线部分传入的参数是`LazyEntity`的工厂类，意思说我们定义的成员变量指向的就是一个工厂类
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142728.png)

2. 我们来看看这个工厂类吧！相信大家也相当熟悉了！(于是就不做说明了！！！)
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142745.png)

### @Named丶@Qualifier
> 这里大家需要先思考一个问题：一个机器人对象有两只手的实例（假如有手类：`Hand`），那么Dagger在提供实例时，如何才能区分这是提供给左的实例还是提供给右手的实例呢？

> 解决这个问题的办法就是用`@Named`分别在变量名和提供对象的地方都标记一下名字。该名字作为`@Named`的参数，如：`@Named("who am i")`。请看下面的例子演示！

1. 我们定义手的对象，`toString()`输出描述信息。
``` java
public class Hand
{
    private String desc;
    public Hand(String desc)
    {
        this.desc = desc;
    }

    @Override
    public String toString()
    {
        return desc;
    }
}
```
2. 我们定义`Module`类提供手的实例
    - 使用`@Named`标记该实例是哪只手，参数为机器人手的名字
``` java
@Module
public class RobotModule
{
    @Named("left")
    @Provides
    static Hand provideLeftHand()
    {
        return new Hand("left hand");
    }

    @Named("right")
    @Provides
    static Hand provideRightHand()
    {
        return new Hand("right hand");
    }
}
```
3. 我们定义一个简单`Robot`（当然这里Robot只看这两只手(～￣▽￣)～ ），顺便我就直接在这个类总测试了。
    - 通过`@Named("left")`标记这里要引用左手的实例
    - 通过`@Named("right")`标记这里要引用右的实例
``` java
public class Robot
{
    @Named("left")
    @Inject
    Hand leftHand;

    @Named("right")
    @Inject
    Hand rightHand;

    @Inject
    public Robot()
    {

    }

    public static void main(String[] args)
    {
        Robot robot = DaggerRobotComponent.create().getRobot();
        System.out.println(robot.leftHand);
        System.out.println(robot.rightHand);
    }
}
```
4. 创建一个Component
``` java
@Component(modules = RobotModule.class)
public interface RobotComponent
{
    Robot getRobot();
}
```

5. 我们来看一看运行结果，可以看出跟我们标记的一样。
```
left hand
right hand
```

> 那么`@Qualifier`又是什么呢？其实它和上面讲的`@Scope`一样，是标记在注解上的，就像`@Singleton`是官方为我们写好的一个用`@Scope`标记好的注解。`@Named`也是官方为我们准备好的用`@Qualifier`标注的注解。看源码：

``` java
@Qualifier
@Documented
@Retention(RUNTIME)
public @interface Named {

    /** The name. */
    String value() default "";
}
```

>  因此我们可以定义自己`@Qualifier`，我们可以定义不传参数的，像下面这样：

``` java
@Qualifier
@Retention(RUNTIME)
public @interface Left { }
---------------------------------------------------
@Qualifier
@Retention(RUNTIME)
public @interface Right { }
```

> 使用（结果是一样的效果）：

``` java
@Module
public class RobotModule
{
    @Left
    @Provides
    static Hand provideLeftHand()
    {
        return new Hand("left hand");
    }

    @Right
    @Provides
    static Hand provideRightHand()
    {
        return new Hand("right hand");
    }
}
---------------------------------------------------
public class Robot
{
    @Left
    @Inject
    Hand leftHand;

    @Right
    @Inject
    Hand rightHand;

    @Inject
    public Robot()
    {

    }
    ...
}
```

> 生成的代码分析：

- 我们看到Dagger知道我们哪个变量对应哪个实例

![DaggerRobotComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142803.png)

### @BindsOptionalOf
> 可选绑定，我们知道如果某个变量标记了`@Inject`，那么必须要为它提供实例，否则无法编译通过。现在我们可以通过将变量类型放入`Optional<T>`泛型参数，则可以达到：即使没有提供相应对象，也能通过编译。

> 也许你想了解一下`Optional`这个类是什么，它的引入是为了解决Java中空指针的问题，您可以去这里了解一下：[Java 8 Optional 类](http://www.runoob.com/java/java8-optional-class.html)

> 我们还是拿实际的代码说话！这里有一个杯子，杯子里可以有咖啡，也可以没有咖啡！

> 我们先来看有咖啡的时候的代码

1. 我们首先我们定义一个咖啡类
``` java
public class Coffee { }
```
2. 我们将`Coffee`类定义为可选的绑定
    - 创建一个`Module`抽象类来定义，返回类型就是咖啡
    - 用`@BindsOptionalOf`来标记
``` java
@Module
public abstract class CModule
{
    @BindsOptionalOf
    public abstract Coffee optionalCoffee();
}
```
3. 我们在定义一个有提供`Coffee`实例的`Module`
``` java
@Module
public class CoffeeModule
{
    @Provides
    public Coffee provideCoffee()
    {
        return new Coffee();
    }
}
```
4. 定义杯子类和Component
    - 我们直接在`Cup`添加`main`方法进行测试
    - Component将两个Module添加进来
``` java
public class Cup
{
    @Inject
    Optional<Coffee> coffee;

    @Inject
    public Cup()
    {

    }

    public static void main(String[] args)
    {
        Cup cup = DaggerCComponent.create().getCup();
        System.out.println(cup.coffee);
        if (cup.coffee.isPresent())
        {
            System.out.println("有咖啡");
        } else
        {
            System.out.println("无咖啡");
        }
    }
}
------------------------------------------------------------------
@Component(modules = {CoffeeModule.class, CModule.class})
public interface CComponent
{
    Cup getCup();
}
```

> 输出结果：

``` java
Optional[com.example.jiaji.daggertest.coffee8_optional_binding.Coffee@4b1210ee]
有咖啡
```
5. 如果我们将`CoffeeModule`提供`Coffee`实例的方法注释掉
``` java
@Module
public class CoffeeModule
{
//    @Provides
//    public Coffee provideCoffee()
//    {
//        return new Coffee();
//    }
}
```
> 输出结果：

``` java
Optional.empty
无咖啡
```

> 这就是可选绑定的作用，但遗憾的是`Optional`这个类在java 8中，并且最低Android Api 24。或者你可以选择导入`guava`这个类库，不过我去喵了一眼，它呀的太大了！！

![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142833.png)

> Optional还可以这样用！

- `Optional<Coffee>`
- `Optional<Provider<Coffee>>`
- `Optional<Lazy<Coffee>>`
- `Optional<Provider<Lazy<Coffee>>>`

> 下面我们来看一看生成的代码长什么样吧! ヾ(=･ω･=)o

1. 目前我们直接看`Component`就够了，于是我们看到`DaggerCComponent`
    - 这是没有提供`Coffee`实例的情况下
        - 我们可以看到注入的时候，直接通过`Optional.<Coffee>empty()`创建了了一个没有内容的`Optional`
        ![DaggerCComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142852.png)
    - 来看提供了`Coffee`实例的情况
        - 我们需要知道`Optional.of()`是向`Optional`里面添加实例的意思，它将返回一个包含有该实例的`Optional`类
        ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142915.png)

### @BindsInstance
> 绑定实例，大家先想一个问题：如果我们提供实例的时候，需要在运行时提供参数去创建，那么该如何做呢？

> 此时我们就可以使用绑定实例来做到！这里我们举例一个需要参数名字和爱好才能创建的`User`对象。

1. 因为名字和爱好都是String类型，所以我定义了两个`@Scope`注解来标识
``` java
@Qualifier
@Retention(RUNTIME)
public @interface Name { }
----------------------------------------------------------
@Qualifier
@Retention(RUNTIME)
public @interface Love { }
```
2. 创建一个`User`类
    - 该类为需要提供的对象，在构造方法上用`@Inject`标识
    - 由于姓名和爱好都属于String类型，所以我们需要标记一下
``` java
public class User
{
    private String name;
    private String love;

    @Inject
    public User(@Name String name, @Love String love)
    {
        this.name = name;
        this.love = love;
    }

    @Override
    public String toString()
    {
        return "User{" +
                "name='" + name + '\'' +
                ", love='" + love + '\'' +
                '}';
    }
}
```
3. 创建Component，这里是我们的关键部分了
    - 首先我们需要在该接口内部在定义一个接口，内部接口用`@Component.Builder`标记，表示该接口会由Component的`Builder`实现。
    - 然后我们需要为定义方法`name()`和`love()`，前面加上注解`@BindsInstance`，返回类型为Builder。传入的参数需要用注解标识，这样才能对应`User`。需要注意一点的就是只有有一个参数，如果多个就会报错，说：只能有一个参数。
    - 最后`UComponent build();`就是我们通常最后调用的那个`build()`方法，创建返回Component实例。
``` java
@Component
public interface UComponent
{
    User getUser();

    @Component.Builder
    interface Builder
    {
        @BindsInstance Builder name(@Name String name);
        @BindsInstance Builder love(@Love String love);
        UComponent build();
    }
}
```
4. 使用测试：
```
public class Main
{
    public static void main(String[] args)
    {
        UComponent uComponent = DaggerUComponent.builder()
                .name("奏响曲")
                .love("beautiful girl")
                .build();
        System.out.println(uComponent.getUser());
    }
}
```
> 输出结果：

```
User{name='奏响曲', love='beautiful girl'}
```

> 可以看出BindsInstance就是就是改造了`Component`里面的`Builder`类，Builder类实现了用`@Component.Builder`标注的接口。

> 接下来来看一下生成的相关代码！

- 可以看到`Component`中的`Builder`实现了`UComponent.Builder`接口，并将传递进来的参数进行空检测与保存
- 并且参数的实例也将会作为`Component`的成员变量，当创建`User`时作为其参数传入。
![DaggerUComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142933.png)

### Component dependencies
`dependencies`是注解`@Component`中定义的参数可以引用其他`Component`，我们去看一下它的源码：
- 可以看到它的定义和我们之前用的`modules`是一模一样
- 也就是说我们可以依赖一个或多个`Component`
``` java
@Retention(RUNTIME) 
@Target(TYPE)
@Documented
public @interface Component {
  Class<?>[] modules() default {};
  Class<?>[] dependencies() default {};
  ...
}
```
> 它的主要作用就是将依赖的Component，放到自己的Component中当做成员变量直接引用。被依赖的Component就可以为主Component提供它在接口中定义的需要返回的实例。<br>如果有`AComponent dependencies BComponent`<br>那么则生成`public class DaggerAComponent implements AComponent { BComponent bComponent;...}`<br>并且这个`bComponent`实例是我们在`Builder`类里面传进去的。

> `Component dependency`只允许您通过组件依赖关系访问接口中公开的类型，既：你只能访问到Component接口中定义的返回类型。

> 我们来看一下实际操作！例子：咖啡和水

1. 定义咖啡和水的实例
    - 在Coffee中我们覆写`toString()`把Coffee和Water的hashCode打印出来。
``` java
public class Water { }
---------------------------------------------------
public class Coffee
{
    private Water water;
    public Coffee(Water water)
    {
        this.water = water;
    }

    @Override
    public String toString()
    {
        return "coffee:" + hashCode() + "; water:" + water.hashCode();
    }
}
```
2. 定义它两的Module提供实例
``` java
@Module
public class WModule
{
    @Provides
    public Water provideWater()
    {
        return new Water();
    }
}
---------------------------------------------------
@Module
public class CModule
{
    @Provides
    public Coffee provideCoffee(Water water)
    {
        return new Coffee(water);
    }
}
```
3. 我们定义`WComponent`为Water的Component，定义`CComponent`为`Coffee`的Component。`CComponent`依赖于`WComponent`
    - 如下代码我们只需要在注解`@Component`中添加`dependencies = WComponent.class`就可以产生依赖。
    - 在使用的时候，我们只需要在创建CComponent的`Builder`对象中传入`WComponent`就可以了。
``` java
public class ComponentDependency
{
    @Component(modules = WModule.class)
    public interface WComponent
    {
        Water water();
    }

    @Component(modules = CModule.class, dependencies = WComponent.class)
    public interface CComponent
    {
        Coffee coffee();
    }

    public static void main(String[] args)
    {
        WComponent wComponent = DaggerComponentDependency_WComponent
                .create();
        System.out.println("water:" + wComponent.water().hashCode());

        CComponent cComponent = DaggerComponentDependency_CComponent
                .builder()
                .wComponent(wComponent)
                .build();

        System.out.println(cComponent.coffee());
    }
}
```
> 输出结果：

``` java
water:1846274136
coffee:1639705018; water:1627674070
```

> 通过结果我们可以看到，`Water`被重复实例化了，最简单的解决方法就是直接在`provideWater()`加上`@Reusable`注解。OK，达到效果

``` java
@Module
public class WModule
{
    @Reusable
    @Provides
    public Water provideWater()
    {
        return new Water();
    }
}
---------------------------------------------------
运行结果：
water:491044090
coffee:644117698; water:491044090
```
> 但这也许不能保证您得到的一定是同一个实例，我们可以加上`@Singleton`注解，但是这里却又一个坑！因为这些Component的生命周期是不一样的，所以不能跨多个Component用同一个`@Singleton`来标记。如果这样做将会抛出一个错误信息：`This @Singleton component cannot depend on scoped components`[stackoverflow](https://stackoverflow.com/questions/39709317/dagger-2-singleton-component-depend-on-singleton/39710308)

1. 我们可这样做，自定义一个`Scope`
``` java
@Scope
@Documented
@Retention(RUNTIME)
public @interface MySingle { }
```
2. 我们在Water这边用`@Singleton`
``` java
    @Singleton
    @Provides
    public Water provideWater()
---------------------------------------------------
    @Singleton
    @Component(modules = WModule.class)
    public interface WComponent
```
3. 我们在Coffee这边用`@MySingle`
``` java
    @MySingle
    @Provides
    public Coffee provideCoffee(Water water)
---------------------------------------------------
    @MySingle
    @Component(modules = CModule.class, dependencies = WComponent.class)
    public interface CComponent
```
4. 输出结果OK：
``` java
water:1625635731
coffee:1580066828; water:1625635731
```


> 我们来分析一下Dagger所生成的代码，主要我们看到`DaggerComponentDependency_CComponent`这个类，主要变化了的就是这里了。

1. 我们先看`DaggerComponentDependency_CComponent`的内部Builder静态类
    - 从下面划线的地方我们可以看出，必须要传入依赖的Component的实例，否则会抛异常。
![Builder](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143001.png)
2. 我们在看`DaggerComponentDependency_CComponent`里面的实现
    - 看到第一根划线处，这里将会把Builder中的依赖Component实例引用传递给它的成员变量。
    - 看到第二根划线处，这里就跟我们平常调用接口中的方法一样获得了需要的实例，注意实例是通过Component接口来获取的实例。
![DaggerComponentDependency_CComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143021.png)
3. 当我们用了Scope的时候，`DaggerComponentDependency_CComponent`还会生成一个静态类内部类
    - 可以看出它实现了`Provider<T>`因该就是为了通过`Provider`的`get()`方法来提供`Water`实例。
    - 并且这里它将依赖的Component放这里面了
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143105.png)
4. 我们再来看此时`DaggerComponentDependency_CComponent`
    - 它依赖的则是上面的静态内部类。
    - 并且通过我们熟悉的`DoubleCheck.provider`来对`get()`内逻辑进行的转变，使我们只获取一个实例。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143123.png)

### @Subcomponent
最后我们来研究一下`@Subcomponent`，就如它名字一样，可以看做是一个Component的子类。
> 我们来看一下它的源码：

- 除了没有`Class<?>[] dependencies() default {};`长得和`@Component`一样。
- 也就是说`Subcomponent`就不能依赖其他Component了
``` java
@Retention(RUNTIME)
@Target(TYPE)
@Documented
public @interface Subcomponent {
  Class<?>[] modules() default {};
  @Target(TYPE)
  @Documented
  @interface Builder {}
}
```

> `SubComponent`您可以在声明它时从父级访问整个绑定图，即您可以访问在其`Modules`中声明的所有对象。

> 怎么使用，这里我们就直接用上个咖啡和水的代码吧！我们重新写一下他们的Component就行了。

- 这里我们将`CComponent`作为子类用`Subcomponent`来标记
- 然后我们还得在它的父Component中添加，如下面代码中的`CComponent cComponent(CModule cModule);`，如果`@Subcomponent`有多个Module，那么可以就要传递多个Module的参数。加入我们有`@Subcomponent(modules = {CModule.class, CModule2.class})`那么我们这样玩`CComponent cComponent(CModule cModule, CModule2 cModule2);`
- 我们在使用的时候需要先创建父`Component`，然后才能通过它去创建子`Component`，如下`main()`方法中

``` java
public class SubComponent
{
    @Component(modules = WModule.class)
    public interface WComponent
    {
        CComponent cComponent(CModule cModule);
    }
    @Subcomponent(modules = CModule.class)
    public interface CComponent
    {
        Coffee coffee();
    }

    public static void main(String[] args)
    {
        WComponent wComponent = DaggerSubComponent_WComponent
                .create();

        CComponent cComponent = wComponent
                .cComponent(new CModule());

        System.out.println(cComponent.coffee());
    }
}
```

> `@Subcomponent` 和`Component dependencies`的一些对比

- 一个`@Subcomponent`实例是通过父Component创建，并且只有一个父Component。`Component dependencies`可以依赖多个Component，并且各个Component需要单独创建且分离。
- `Component dependencies`只运行您访问接口中公开定义提供的实例，`@Subcomponent`可访问其'Modules`中声明的所有对象
- `Component dependencies`存在生命周期的不同，`@Subcomponent`确是同一个周期。

> 我们来看一下生产的代码，这里只有Component：`DaggerSubComponent_WComponent`，我们将`DaggerSubComponent_WComponent`分成三部分来看

1. 首先我们看到`DaggerSubComponent_WComponent`内部类：子Component的定义
    - 它实现了我们定义的接口，并且和我们之前所生成的Component是类似的，只不过内部没有Builder静态类了。
    - 由于是内部类，所以我们能访问所有父`Component`能访问的所有东西。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143142.png)
2. 我们来看Builder，Builder没有任何变化，跳过！
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143155.png)
3. 我们来看`DaggerSubComponent_WComponent`的方法
    - 可以看到，当我们调用`cComponent`时就会创建一个子Component对象
    - 由于子Component是没有Builder去创建的也没有默认创建`Module`的功能。当然子Component也是需要他的`Module`的，于是我们需要创建一个它的`Module`给它。
![DaggerSubComponent_WComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143210.png)

[Subcomponent和Component dependencies的关系区别](https://stackoverflow.com/questions/29587130/dagger-2-subcomponents-vs-component-dependencies)

### 安卓扩展的相关框架
这个有机会，如果希望看我这种啰嗦介绍的人多的话，在写一篇关于这个的！

---
### 结束
好了，神不知鬼不觉的一星期码了这么多字。能挨着看到这里的同学，能有多少咧Σ(っ°Д°;)っ

想起来，我以前写了一个MVP框架[XMVP](https://github.com/xujiaji/XMVP)就是通过获取配置的泛型参数类型然后再通过反射去实例化的自动完成它们之间的依赖关系。也可以说是这就是依赖注入了吧！哈哈！有兴趣的朋友可以去看一看用一用非常简洁哦！(｀・ω・´)

文章中所有代码的地址：https://github.com/xujiaji/DaggerTest

本文作者（欢迎关注）：[奏响曲](https://juejin.im/user/5829eafe2f301e0057799f1a)

Github: https://github.com/xujiaji/

如果文中内容有误或不合适欢迎您的指正！

over