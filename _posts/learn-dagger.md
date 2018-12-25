---
title: Dagger2 的深入分析与使用
date: 2018-06-27
author: xujiaji
thumbnail: https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/home.jpg
categories:
 - Android
tags:
    - Android
    - 分析框架
    - Dagger
---

![脑图](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/main-mind.png)

听闻Dagger大名很久，但一直没有去学，直到不得不学 〒▽〒。<br>这个框架开始的时不是很好理解，看了一些文章还是没有理解到精髓，似懂非懂，于是自己做了些简单的测试代码观察Dagger注解的作用。将学习和理解的过程分享出来，希望能帮到一些学些Dagger的朋友，同时我也巩固总结一下。

本篇文章不讲，Dagger哪里好哪里好！只讲怎么用的和一些原理！

## Dagger是什么？
- Dagger是一个依赖注入框架（Dependency injection），简称DI。假如有A和B两个对象（B相当于是DI），A中并没有对自己内部的成员进行初始化，它的成员初始化全部是B类注入进来。

- 大部分注入框架是基于反射实现的，Dagger旨在解决许多困扰基于反射的解决方案的开发和性能问题，Dagger的依赖注入是通过java代码来实现的。相当于你自己可以用java手写依赖注入代码，但这样的话就会更大的工作量，于是Dagger通过注解等帮我们自动生成相关的依赖注入逻辑代码。

- 额...，有点一头雾水的感觉吧！如果大家想知道详细概念的话，可以去搜索一下啦！

- 在下面所讲的都是以实际的代码操作为主，来去观察结果，代码本篇不会涉及Android 页面，只想通过简单的代码来理清楚Dagger生成DI的逻辑。

## 需要添加的依赖
官方Dagger2项目地址：https://github.com/google/dagger

```
dependencies {
    implementation 'com.google.dagger:dagger:2.15'
    annotationProcessor 'com.google.dagger:dagger-compiler:2.15'
}
```

## 注解使用
欢迎来到本篇最精彩的地方！参考自[官方的使用指南](https://google.github.io/dagger/users-guide)

> 符号含义参考表：

|符号══▶|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-private.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-m-private.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-protected.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/v-m-protected.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611140949.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141014.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141038.png)|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141100.png)|
|-|-|-|-|-|-|-|-|-|
|**含义**══▶|private变量|private方法|protected变量|protected方法|包私有 变量|包私有方法|public 变量|public 方法|

|符号|含义|简单例子|
|-|-|-|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141212.png)|继承|`class A{}`<br><br>`class B extend A{}` |
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141236.png)|实现接口|`interface I{}`<br><br>`class A implements I{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141305.png)|依赖|`class A{}`<br><br>`class B{`<br>　　`void fun(A c) {}`<br><br>`}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141339.png)|并联|`class A{}`<br><br>`class B{`<br><br>　　`A a;`<br><br>`}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141403.png)|class|`class A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141425.png)|abstract|`abstract class A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141449.png)|interface|`interface A{}`|
|![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141508.png)|enum|`enum A{}`|
|`...`|省略代码|`class A {...}`|

### 咖啡机
用咖啡机的例子来演示，首先我们来看一下主要的几个类，下面是简单咖啡机UML关系图！（查考自Dagger2项目example）

![咖啡机UML](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611141527.png)

> 正常情况下，我们大概会写成这样：

``` java
/**
 * 定义汞接口
 */
interface Pump {
    void pump();
}
---------------------------------------------------------------------------------
/**
 * 定义加热器接口
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
**[测试文件位置](https://github.com/xujiaji/learn-android/tree/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee2_test_inject)**

1. 其名：注入，@Inject的用法是标记成员变量、构造方法或成员方法。

2. 标记了注解`@Inject`的成员变量或方法，Dagger会自动为其提供实例；标记了`@Inject`的构造方法表示Dagger将会自动实例化该类提供给其他需要注入的类。

3. 像这这样一个需要注入的成员，一个提供该对象就这样对应起来了。但是还差一个将它们联系起来的东西，它叫`Componnet`。下面的例子将会提前用到`@Component`注解您可以先不去深入理解，占时理解为Dagger必要写的的且是注入的关系连接纽带。

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

> `@Component`起纽带作用，用接口或抽象类来定义。`Thermosiphon getPump()`表示其他地方需要提供`new Thermosiphon()`

``` java
@Component
public interface PumpComponent {
    Thermosiphon getPump();
}
```
> `@Inject`标记在成员变量上，表示其他地方需要提供`ElectricHeater`对象，也就是上上面代码中`@Inject`标记在构造方法的作用。`@Inject`标记在构造方法上，可以看做`new Thermosiphon()`，也就是上面接口中需要的对象。

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
> 我们直接创建一个CoffeeApp类中进行测试，`DaggerPumpComponent`是通过apt自动生成的类（需要在Android studio中点击：Build -> Make Module）。

``` java
//运行测试
public class CoffeeApp {
    public static void main(String[] args) {
        // 全写：Thermosiphon pump = DaggerPumpComponent.builder().build().getPump();
        Thermosiphon pump = DaggerPumpComponent.create().getPump();
        pump.heater.on();
        pump.pump();
    }
}
```
> `CoffeeApp`运行结果

```
~~~~heating~~~~
=>=> 抽水 =>=>
```
> 测试一下将`@Inject`标记在方法上，修改`Thermosiphon`类，如下所示：

``` java
/**
 * 热虹吸
 */
public class Thermosiphon implements Pump {
...
    @Inject
    public void funTest()
    {
        System.out.println("funTest()");
    }

    @Inject
    public void funTest(ElectricHeater heater)
    {
        System.out.println("heater: " + this.heater.hashCode());
        System.out.println("funTest(): " + heater.hashCode());
    }
...
}
```

> `CoffeeApp`运行结果

```
funTest()
heater: 692404036
funTest(): 1554874502
~~~~heating~~~~
=>=> 抽水 =>=>
```


> 一些结论

1. 通过`DaggerPumpComponent.create().getPump();`既可以得到`Thermosiphon`对象。
2. 我们看到在`Thermosiphon`中`heater`是以`ElectricHeater`来接收的，并没有向上转型为接口`Heater`引用，`@Inject`标记需要是确切的类型。等我们学习了下面` @Provides丶@Module`部分，我们就能间接的用`Heater`接口来接收。
3. 通过上面例子我们明显看到，我们并没有new 对象，然而却有`ElectricHeater`和`Thermosiphon`被实例化，这就是Dagger生成java代码中帮我们进行了实例化的操作。
4. 注意`@Inject`标记的成员变量、方法和构造方法不能以`private`修饰。因为如果我们用private，Dagger以java代码注入，自然不能帮我们注入对象，会报错!你可以试试看哦！(￣▽￣)~*
5. 也许你想问`DaggerPumpComponent`是哪来的？用`@Component`标记的接口会生成一个以`“Dagger + 接口名”`的类。
6. 经测试，如果将成员变量上的`@Inject`去掉，不会报错，只是没有引用的对象，变量为null。如果成员变量上标记了`@Inject`，而没有对应的注入实例，则会编译错误。
7. Dagger生成代码的位置：`项目目录 -> app -> build -> generated -> source -> apt`
8. 如果我们将`@Inject`标记在方法上，如果有参，Dagger提供该实例，然后自动调用该方法；如果无参则直接调用；如果有参没有对应的实例提供，则报错。

> *接下来将从Dagger生成的注入代码上进行分析（这部分跳过也可以滴！(｀・ω・´)）*

> 这是上面整体的UML关系图，“绿色”的是Dagger自动生成的代码。

![inject uml](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/inject-uml.png)
**1.** 通过我们对Dagger的使用，它为我们生成了4个类。![生成的类](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/build-class.png)
**2.** 他们这样对应：

||||
|-|-|-|
|PumpComponent|----->|DaggerPumpComponent|
|@Inject public ElectricHeater() { }|----->|ElectricHeater_Factory|
|@Inject public Thermosiphon() { }|----->|Thermosiphon_Factory|
|@Inject ElectricHeater heater;|----->|Thermosiphon_MembersInjector|
通过观察我们可以得出这些结论：
- ①`PumpComponent`接口生成的类的名字以：`Dagger` + `接口名`。*（我们需要使用生成的这个类，进行Dagger初始化的操作）*
- ②`@Inject`标记了构造方法生成类名以：`构造名` + `_Factory`，的命名生一个工厂类。*（该工厂类将用来创建对应的实例）*
- ③类中有`@Inject`标记成员变量或方法的类，会生成一个以：`该类名` + `_MembersInjector`，的命名生成一个注入类。*（该类实现了将实例传递到用`@Inject`标记的成员变量或方法）*

**3.** 来看看`ElectricHeater`的工厂类`ElectricHeater_Factory`（这是一个工厂设计模式中的一种实现方式），实现一个工厂接口`Factory<T>`(`Factory<T>`又继承`Provider<T>`接口)。通过`get()`获取一个ElectricHeater实例，通过`create()`获取`ElectricHeater_Factory`实例（这个类并未被使用，当你看到下面介绍`DaggerPumpComponent`就明白了）![ElectricHeater_Factory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/ElectricHeater_Factory.png)
**4.** 接下来看看`Thermosiphon_MembersInjector`，这个类实现了为`@Inject`泛型标记的成员变量或方法传递值的操作。大家看`injectHeater`方法，这里就是为`Thermosiphon`的成员变`heater`添加依赖的地方!![Thermosiphon_MembersInjector.java](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/Thermosiphon_MembersInjector.png)
**5.** 再看看`Thermosiphon_Factory`，这个类比上一个`ElectricHeater_Factory`复杂一点。因为它在实例化`Thermosiphon`时，需要注入`ElectricHeater`对象。这比`ElectricHeater_Factory`多了个方法并且实例该工厂类时必须传入`ElectricHeater`的工厂类实例。
- 构造参数是`ElectricHeater`的工厂，是为了通过工厂类获得`ElectricHeater`对象；
- 工厂方法`get()`中创建实例的同时，通过`Thermosiphon_MembersInjector`的静态方法(`injectHeater`)向`Thermosiphon`注入`ElectricHeater`对象，然后得到最终的`Thermosiphon`实例；
- 最后一个静态方法`newThermosiphon()`返回一个没有注入`ElectricHeater`实例的`Thermosiphon`对象。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142100.png)

**6.** 最后看`DaggerPumpComponent`这个类，主要看`getPump()`、`injectThermosiphon`和`Builder`类
- `getPump()`是我们在接口中定义的方法，在这里实现接口方法，通过调用`injectThermosiphon`方法并传入一个没有注入`ElectricHeater`实例的`Thermosiphon`，得到最终的`Thermosiphon`
- `injectThermosiphon`方法中得到上面传进来的`Thermosiphon`，然后通过`Thermosiphon_MembersInjector`注入`ElectricHeater`实例。看到这里我们会发现第“3.”中介绍的`ElectricHeater_Factory`居然没有用到，这里直接就new了（这也是上面提到的并没有使用`ElectricHeater_Factory`）。
- `Builder`就是用来创建`DaggerPumpComponent`的类，学到后面，这个类会根据需求变得复杂！
![DaggerPumpComponent.java](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142127.png)

### @Provides丶@Module丶@Binds
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee3_test_provides_module)**

> 由于`@Inject`注解无法做到以下几点：

- 接口类型无法做为接收类型
- 第三方类无法添加`@Inject`注解（因为这个类不是自己掌控的）

这种情况下我们可以用`@Provides`注释去满足依赖，方法的返回类型确定了它提供给谁的依赖。

> 使用

1. 创建一个类作用是存放提供实例的方法，约定该类以`Module`结尾（便于统一分辨，就像我们安卓Activity命名以Activity结尾）
2. 在类名上标记`@Module`注解
3. 使用静态或普通有返回的方法来提供实例
    - 在这些方法前需要标记`@Provides`注解
    - 这些方法以`provide`开头，也是一种约定

> 看下方这个`DripCoffeeModule`类，它提供了两个实例，并且它们的返回类型指向的是接口。也就是说有某个地方可能需要`Heater`和`Pump`的实例。

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
> 在`@Component`注解中添加`DripCoffeeModule.class`，如果有多个可写为：`@Component(modules = {DripCoffeeModule.class, ....class,....class})`

```
@Component(modules = DripCoffeeModule.class)
public interface CoffeeShop
{
    Pump getPump();
}
```
> 其他类

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
> 测试类：

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
> CoffeeApp的输出结果：

``` java
provideHeater
ElectricHeater()
Thermosiphon() heater = com.example.jiaji.daggertest.coffee3.ElectricHeater@29453f44
providePump
pump = com.example.jiaji.daggertest.coffee3.Thermosiphon@5cad8086
```
- 首先，我们调用`DaggerCoffeeShop.create().getPump()`想要得到一个Pump对象，于是`DripCoffeeModule`中的`providePump`方法为我们提供一个Pump实例。
- 然后，我们看到`providePump`方法有参数`Thermosiphon`那么这个这个实例从哪来呢？我们在`Thermosiphon`的构造方法上标记`@Inject`就表示提供该对象了。
- 接下来，我们深入到`Thermosiphon`类又会发现，`Thermosiphon`类的构造方法要求提供`Heater`对象，那么问题来了Heater实例从哪来？您能想到！我们可以看到在`DripCoffeeModule`的`provideHeater`方法提供了该实例。
- 最后，我们可以得出来个容易理解的大概流程：![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143230.png)

**我们需要注意，当`@Inject`提供了实例并且`Module`中也提供该实例的情况下，Dagger会优先`Module`中提供的实例。**

*通过上面的例子，我们可以注意到：`@Inject`可以为`Module`方法的参数提供实例*

> 我们可以将Module中的方法分到多个Module中，只需要在`@Component`注释中添加一下，如下所示：

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
> 其实还有种写法，意思是表示某一个Module包含另一个Module。最终效果一样的。如下所示：

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

> @Binds可以简化`DripCoffeeModule`中提供`Pump`实例的写法，效果是一样的。

``` java
@Module
public abstract class BModule
{
    @Binds
    abstract Pump bindPump(Thermosiphon pump);
}
---------------------------------------------------------------------------------
@Component(modules = {DripCoffeeModule.class, BModule.class})
public interface CoffeeShop
{
    ...
}

```

> *接下来是对Dagger生成的代码进行分析（这部分可以选择性跳过！(｀・ω・´)）*

> 这是整体的UML关系图，“绿色”是自动生成的代码。(由于生成的`Thermosiphon_Factory`并没有被使用，于是就不放进来了。)

![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142208.png)
**1.** 通过上面的三部分代码，Dagger也为我们生成了4个类。![dagger生成的四个类](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142229.png)
**2.** 他们这样对应：

||||
|-|-|-|
|CoffeeShop|----->|DaggerCoffeeShop|
|@Provides static Heater provideHeater()|----->|DripCoffeeModule_ProvideHeaterFactory|
|@Provides static Pump providePump(Thermosiphon pump)|----->|DripCoffeeModule_ProvidePumpFactory|
|@Inject public Thermosiphon() { }|----->|Thermosiphon_Factory|
从名字上我们可以看出：`@Provides`标记的提供实例的方法对应生成了一个类名以：`所在类名` + `_` + `方法名(首字大写)` + `Factory`，命名生成一个对应的工厂类。

**3.** 我们先来看看`Thermosiphon_Factory`这个没有被使用的类，如果您是从上面挨着看下来的，就一定明白，其他地方是直接`new Thermosiphon`，接着往下看您就会看到！
- 这个类和上面生成的`Thermosiphon_Factory`有些不一样，因为之前`Thermosiphon`是无参构造，现在添加了`Heater`作为构造的参数（该实例在DripCoffeeModule提供）。
- 可以看到要实例化这个工厂类，必须要传入`Heater`的工厂类。然后在创建`Thermosiphon`实例时通过`Heater`工厂类创建一个`Heater`对象传入构造方法中。
- 并且它还添加了`一个newThermosiphon`的静态方法，允许传入`heater`对象来创建`Thermosiphon`。

![Thermosiphon_Factory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142247.png)
**4.** 我们在来看`Heater`工厂类`DripCoffeeModule_ProvideHeaterFactory`，它相对比较简单点。
- 可以看到在创建`Heater`实例时，直接通过`DripCoffeeModule.provideHeater()`调用我们定义的相对应的静态方法。
- 通过`Preconditions.checkNotNull`又检测了是否提供得有实例，没有将会报第二参数传入的错误信息。
- 工厂实例化是通过静态方法`create()`实例；静态方法`newThermosiphon`，可不创建工厂类的情况下，直接创建`Heater`实例。

![DripCoffeeModule_ProvideHeaterFactory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142310.png)

- `DripCoffeeModule`中提供实例的方法不仅可以是静态方法！还可以是普通方法或抽象方法。那如果我们将`DripCoffeeModule`中的静态方法的static去掉改为普通方法生成的代码又是怎么样的呢？(`@Provides static Heater provideHeater()`改为`@Provides Heater provideHeater()`)看下图：
    - 可以看到`DripCoffeeModule_ProvideHeaterFactory`的创建须传入`DripCoffeeModule`实例，`get()`方法通过该实例获取`Heater`实例
    - 创建`Heater`的静态方法`proxyProvideHeater`须传入`DripCoffeeModule`实例。

    ![DripCoffeeModule_ProvideHeaterFactory](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142330.png)

**5.** 我们来看看`Pump`对应生成的工厂类：`DripCoffeeModule_ProvidePumpFactory`
- 在Module中这样定义：`@Provides static Pump providePump(Thermosiphon pump) { return pump; }`
- 这个方法又必须提供`Thermosiphon`实例，因此`DripCoffeeModule_ProvidePumpFactory`的构造参数是`Thermosiphon`的工厂对象来提供该实例（`get()`方法中通过调用静态方法`providePump`得到Pump实例的时候需要该工厂类提供）
- 我们看到`proxyProvidePump`方法，也是可在不创建工厂类实例的情况下调用。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142349.png)
- 如果我们也把Module中的static修饰去掉又会发生什么样的变化呢？我猜您也应该能想到了！看下图：
    - 比4中去掉static多了划线的地方
    - 也就是说当我们定义的方法是普通方法时，我们就必须要提供`Module`的实例
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142412.png)

**6.** 最后，我们来看`DaggerCoffeeShop`是如何将这些东东组合在一起的。
- 我们看到`getPump()`方法，它在接口`CoffeeShop`中定义，里面如何实现的呢？
- 它直接调用了上面`5`所讲到的静态方法`proxyProvidePump`来创建`Pump`实例，但是需要提供`Thermosiphon`实例作为参数。（如果是用的@Binds方式，则getPump()的实现为：  `public Pump getPump() { return getThermosiphon(); }`）
- 于是，它定义了方法`getThermosiphon()`来创建该实例。看到该方法了吗？里面是直接`new Thermosiphon`，这就是`Thermosiphon_Factory`没有用到的原因。创建`Thermosiphon`的构造参数`Heater`由`DripCoffeeModule_ProvideHeaterFactory`类名直接调用静态方法`proxyProvideHeater()`它又调用`DripCoffeeModule.provideHeater()`来提供。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142434.png)

- 接下来看到创建`DaggerCoffeeShop`的`Builder`静态内部类，这里面可要比我们上次生成的`DaggerPumpComponent`要多了一个方法，它出现的原因就是因为我们定义了Module类。
    - 这个方法的命名方式是将我们定义的Module类的类名开头小写来作为名字。
    - 它的作用是我们可以自己创建Module，如果不自己创建，将会自动创建。
    - 但为什么这里标记为弃用呢？那是因为我们Module中全是静态方法，完全不需要实例化，实例化也白搭！那我们来看看，如果将`DripCoffeeModule`中的方法改为普通方法是什么样的呢？
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142457.png)
    - 看到了吧！如果build()方法中判断了我们已经调用`dripCoffeeModule`方法传进来Module实例，那么就不去实例化了。
    - 还记得上面Module中我们去掉提供方法static后需要的Module实例吗？实例就是开始于这里的。
    - `dripCoffeeModule`的调用方式就是：`DaggerCoffeeShop.builder().dripCoffeeModule(new DripCoffeeModule()).build();`（如果我们的`@Component`连接了多个`Module`那么就可以这样传入这么多个`Module`实例）
    - 那么这个方法到底有什么神奇的作用呢？我们想想看，如果`Module`的构造方法需要传参，此时我们该怎么办呢？如下：
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
    - 输入结果：`TestModuleAttr{str='Hello world'}`
    - 当我们想向提供的对象传递一些动态的东西时，就可以通过这种方式，当然你也不用向我这样绕了个圈子，这里只想说`Module`里面可以相互提供实例。这里可以直接`@Provides TestModuleAttr provideTestModuleAttr() { return new TestModuleAttr(str); }`搞定。
    - 需要注意的是，如果`Module`实例是有参构造创建，我们必须自己实例化`Module`。否则则会抛出异常。原因，如下：![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142517.png)

### @Component
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee4_test_component)**

上面都涉及到了它，想必大家也有些熟悉了。ヾ(๑╹◡╹)ﾉ"

官方把这个定义叫做建立图表，它起到的作用是连接依赖关系，通过上面的分析，我们可以直观的看到在`DaggerXXX`(`@Component`修饰的类所对应生成的文件)类中，主要就是将各个工厂类和Module连接起来。

> 如果我们像下面这样定义一个Component，Dagger将会为我们生成一个类：`DaggerFoo_Bar_BazComponent`

``` java
class Foo {
  static class Bar {
    @Component
    interface BazComponent {}
  }
}
```

> `@Component`不仅可以装饰接口还可以是抽象类，比如上面的`CoffeeShop`接口可以改成这样：

``` java
@Component(modules = {DripCoffeeModule.class})
public abstract class CoffeeShop
{
    abstract Pump getPump();
    abstract TestModuleAttr getTestModuleAttr();
}
```

在Component中定义的方法我们在对应生成的DaggerXXX实例调用得到对应实例，于是我们需要为其提供对应返回实例。

> 接下来我们来通过模拟安卓中Activity的启动，该代码大概模拟了一下MVP。为了简单，MNActivity作为View层，我没有写MVP接口的M层。这里主要是想解释为什么在Compnent接口中需要定义一个`void inject(XXXActivity activity);`，看到别人这么写的！但我当时真心不知道这是啥意思！于是这里我想通过简单的代码去理解它。

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
2. Presenter层，在presenter中一般我们是引用的view的接口，这里我们直接引用activity。
    - `@Inject`标记构造，表明这里提供MNPresenter实例
    - 我们看到有构造方法参数为`MNActivity`，表明需要实例化我们又需要为它提供`MNActivity`（我们通过Module提供）
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
3. 实例提供部分类：Module
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
4. 组装纽带部分：Component
    - inject方法返回值为void
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
> 为什么这么神奇呢？居然就这样就将`MNPresenter`的实例注入到`MNActivity`了！`DaggerTestComponent`实现我们定义的`void inject(MNActivity me);`，然后在方法里进行了如这样的操作（简化后）：`me.presenter = new Presenter(...);`

> 我们将`void inject(MNActivity me);`的实现代码和上面测试`@Inject`时定义的`Thermosiphon getPump();`的实现代码进行比较，来看看有何区别。

- 我们先来看`Thermosiphon getPump();`是如何实现的呢？重温一下，看下图：
    - 它首先通过`Thermosiphon_Factory.newThermosiphon()`直接`new Thermosiphon()`。
    - 然后调用`injectThermosiphon`方法将实例化的`Thermosiphon`通过`Thermosiphon_MembersInjector.injectHeater`将一个`ElectricHeater`赋值到对应的成员变量。
    - 最后将一个完成的`Thermosiphon`返回。
![getPump() 实现](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142542.png)
- 我们再来看`void inject(MNActivity me);`是如何实现的呢？看下图：
    - 这里`inject(MNActivity me)`的实现省略掉了创建`MNActivity`的过程，直接调用`injectMNActivity`进行注入。
    - 为什么呢？因为当前`MNActivity`对象已经存在，只需要注入标有`@Inject`的成员变量就行了。
    - 我们想想Android中打开一个Activity，他是通过系统去实例化的！我们既然在Activity实例之中，又何必去实例化它呢？对吧！
![inject方法的实现](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142555.png)

### 将上面所学运用到一开始的咖啡机实现
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
- 大家有木有发现，当调用`heater.on()`后调用`pump.pump()`居然没有出水(没有打印：`=>=> 抽水 =>=>`)
- 通过输出结果我们看到`provideheater`被调用两次也就是两次new，我们还会会发现：`Thermosiphon`中的`Heater`对象和`CoffeeMaker`中的`Heater`对象打印的`hashCode`不一样，这根本就是两个实例。怪不得`CoffeeMaker`中`heater.on()`后`pump.pump()`不出水，原因就是`Pump`中又是另一个`Heater`实例。

> 看来通过上面的学习，我们的咖啡机还有点缺陷。我们需要通过下面所讲的`@Singleton`来拯救一下这个多次实例化的问题。

> 最后我将上面这些大致理解思路画了如下流程图，希望能帮助您理解：

![dagger-liu-cheng](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142614.png)

### @Singleton丶@Scope
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee5_test_scope)**

> Singleton：直接翻译过来是独生子的意思。我们可以这样去理解，标记了`@Singleton`提供的类，在同一个Component实例中(这是条件)只存在一个该实例，多次需要时，提供的实例也只是第一次创建的那个实例。

- 我们只需要将上面咖啡机的实现代码加两个`@Singleton`就可以解决问题！如下代码：
    - 在提供实例那里加个`@Singleton`
    - 在`Component`那里加个`@Singleton`
    - 也就是说`@Singleton`起效，得添加两处

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
> 那么如果是`@Inject`标记的构造方法的方式来提供的对象，`@Singleton`该如何标记呢？如下代码：

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

> 为什么说上面条件是需要在一个Component实例中？原因是如果Component被多次实例化，那么不同的Component中@Singleton标记的实例也将不同！

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
- 从输出信息中我们可看出，第一次和第二次都是同一个heater实例，第三次却是不同的实例，因为我们重新实例化了一个Component。
- 如果我们想在多个地方调用的时候也得到同一个Component实例，我们可以将Component作为抽象类，并改为单例。如下：
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
- 我们的使用的时候，直接这样：`CoffeeShop.getInstance().maker().brew()`
- 我们在Android中，可以把这种全局的定义放到`Application`中也可以确保在该进程中的唯一。

> 上面讲了`@Singleton`，那么`@Scope`又是什么呢？`@Scope`是用来标识注解的。我们看一下，`@Singleton`的源码你就明白了！

``` java
@Scope
@Documented
@Retention(RUNTIME)
public @interface Singleton {}
```
- 用`@Scope`标识的注解都有`@Singleton`的功能，于是我们可以定义我们自己想要的名字来实现相同功能。
- 但需要注意一点就是用的时候相对应的注解必须是同一个（比方说我定义了一个`@MySingle`，就不能在Component那里用`@MySingle`的同时，对应的提供对象那里却用的是`@Singleton`）

> 又到了我们分析生成代码的环节，大家可以选择性跳过哦！(〃'▽'〃)

1. 我们直接来看`DaggerCoffeeShop`这个类，其他都和上面讲解的一样，变化就在该类！
    - 我们看到下图画红线的部分！他将`@Singleton`标记的对象直接放到了`DaggerCoffeeShop`作为成员变量（由于代码太多，我将`CoffeeMaker`中的`SingletonTest`都注释了）。
    - 等等！`Provider<Heater>`根据上面我们对工厂代码的研究！每次调用`get()`不都会重新实例化一个对象吗？为什么每次`get()`都是同一个实例？这就是第二根红线`DoubleCheck`的封装起的作用了！
![DaggerCoffeeShop](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142629.png)
2. `DoubleCheck.provider`搞了什么名堂？大家跟着我点进去悄悄！
    - 我们看到这个静态方法！很明显，它是为了创建一个`DoubleCheck`对象，如果传进来的就是`DoubleCheck`对象，则直接返回实例。
    ``` java
    public static <P extends Provider<T>, T> Provider<T> provider(P delegate) {
        checkNotNull(delegate);
        if (delegate instanceof DoubleCheck) {
            return delegate;
        }
        return new DoubleCheck<T>(delegate);
    }
    ```
    - 我们看到`DoubleCheck`类也是实现了`Provider`接口的，所以在`DaggerCoffeeShop`中才能直接用`Provider`来引用。它既然也是一个`Provider`却又要传入一个`Provider`，它起了一个代理的作用。
    - 为什么`get()`调用后是同一个实例？原因是`get()`中进行了处理，如果`get()`过一次实例，那么下次将返回上一次的实例。下面是这部分源码：
        - 我们可以看到它不仅仅简单写了只返回一个实例的的代码，还写了一堆关于多线程同步相关代码。
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
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee5_test_scope/CoffeeApp.java)**

它和`@Singleton`达到的效果差不多，而且逻辑也差不多，但是它却不保证是单实例！

它的用法比`@Singleton`还简单点，只需要在提供实例的地方加个`@Reusable`就可以了，如下代码：

> 就像下面这么简单就OK了，不用在Component中添加。

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

> 我们再来看看，生成的代码和@Singleton的不同！

1. 我们改用`@Reusable`后，`DaggerCoffeeShop`有什么变化？
    - 唯一发生变化了地方就是这个方法里面的实现由`DoubleCheck.provider`变成了`SingleCheck.provider`
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142648.png)
2. 那我们来到`SingleCheck`这个类，它和`DoubleCheck`不同点就在于`get()`方法的实现上，请看下面`SingleCheck`的`get()`源代码：
    - 可以看到它省去了`DoubleCheck`中一堆关于线程同步的代码
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
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee6_test_lazy_provider)**

通过它可以实现惰性实例化，也就是当我们第一次调用的时候才会创建实例。并且多次调用不会再次创建实例，只会返回第一次调用创建的实例。

> 我们来看看它的用法！

1. 首先我们创建一个需要提供的对象
```
public class LazyEntity
{
    @Inject
    public LazyEntity()
    {
        System.out.println("LazyEntity()");
    }
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
        System.out.println("此时LazyEntity还没有实例化");
        for (int i = 0; i < 3; i++)
        {
            System.out.println(main.entityLazy.get().hashCode());
        }
    }
}
```
4. 输出结果，也就是说我们重复调用都是一个实例。
```
此时LazyEntity还没有实例化
LazyEntity()
1625635731
1625635731
1625635731
```

> 来吧！进入生成代码分析阶段（当然可以选择跳过哈！）ヾ(◍°∇°◍)ﾉﾞ

1. 我们看到Dagger生成的`DaggerMyComponent`，需要值得注意的就是下面图片上划线的部分。
    - 可以看到这里也使用了`DoubleCheck`类（大家通过上面的学习应该熟悉了），也就是说我们得到的`Lazy`对象其实就是一个`DoubleCheck`。
    - 所以说我们能多次调用也只能返回相同的实例，而且也能在多线程调用也不担心重复实例化。
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
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee6_test_lazy_provider)**

当您需要多个实例时，可以通过`Provider<T>`作为成员变量，您只需要每次调用它的`get()`方法就会返回不同的实例。

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
此时LazyEntity还没有实例化
LazyEntity()
692404036
LazyEntity()
1554874502
LazyEntity()
1846274136
```

> 来吧！生成代码分析阶段(｡･ω･｡)

1. 我们看`DaggerMyComponent`中是怎么注入的！看到划线部分传入的参数是`LazyEntity`的工厂类，意思说我们定义的成员变量指向的就是一个工厂类
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142728.png)

2. 我们来看看这个工厂类吧！相信大家也相当熟悉了！(于是就不做说明了！！！)
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142745.png)

### @Named丶@Qualifier
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee7_test_named_qualifier)**

大家可以先思考一个问题：一个机器人对象有两只手的实例（假如有手实现类：`Hand`），那么Dagger在提供实例时，如何才能区分这是提供给左的实例还是提供给右手的实例呢？

> 解决这个问题的办法可以用`@Named`分别在变量名和提供实例的地方都标记一下名字。该名字作为`@Named()`的参数，如：`@Named("who am i")`。请看下面的例子演示！

1. 我们定义手实现类
    - `toString()`输出描述信息。
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
    - 使用`@Named`标记该实例是哪只手，参数为机器人左手还是右手
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
3. 我们定义一个`Robot`（当然这里Robot只看这两只手(～￣▽￣)～ ），顺便我就直接在这个类中测试了。
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

> 那么`@Qualifier`又是什么呢？其实它和上面讲的`@Scope`一样，是标记在注解上的，就像`@Singleton`是官方为我们写好的一个用`@Scope`标记好的注解。`@Named`也是官方为我们准备好的用`@Qualifier`标注的注解。看@Named源码：

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

- 通过标记名字Dagger知道我们哪个变量对应哪个实例

![DaggerRobotComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142803.png)

### @BindsOptionalOf
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee8_test_optional_binding)**

可选绑定，我们知道如果某个变量标记了`@Inject`，那么必须要为它提供实例，否则无法编译通过。现在我们可以通过将变量类型放入`Optional<T>`泛型参数，则可以达到：即使没有提供它的实例，也能通过编译。

`Optional`这个类是什么呢？它的引入是为了解决Java中空指针的问题，您可以去这里了解一下：[Java 8 Optional 类](http://www.runoob.com/java/java8-optional-class.html)

> 我们还是拿代码说话！这里有一个杯子，杯子里可以有咖啡，也可以没有咖啡！

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

> 这就是可选绑定的作用，`Optional`这个类在java 8中，并且最低Android Api 24。或者你可以选择导入`guava`这个类库，不过我去喵了一眼，它呀的太大了！！

![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142833.png)

> Optional还可以这样用！

- `Optional<Coffee>`
- `Optional<Provider<Coffee>>`
- `Optional<Lazy<Coffee>>`
- `Optional<Provider<Lazy<Coffee>>>`

> 下面我们来看一看生成的代码长什么样吧! ヾ(=･ω･=)o

目前我们直接看`Component`就够了，于是我们看到`DaggerCComponent`
- 这是没有提供`Coffee`实例的情况下
    - 我们可以看到注入的时候，直接通过`Optional.<Coffee>empty()`创建了了一个没有内容的`Optional`
    ![DaggerCComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142852.png)
- 来看提供了`Coffee`实例的情况
    - 我们需要知道`Optional.of()`是向`Optional`里面添加实例的意思，它将返回一个包含有该实例的`Optional`类
    ![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142915.png)

### @BindsInstance
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee9_test_bindsinstance)**

绑定实例，大家可以想象一下：如果我们提供实例的时候，需要在运行时提供参数去创建，那么该如何做呢？

> 我们可以使用Builder绑定实例来做！这里我们举例一个需要参数名字和爱好才能创建的`User`对象。

1. 名字和爱好都是String类型，定义了两个`@Scope`注解来标识
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
    - 由于姓名和爱好都属于String类型，所以我们需要标记一下区分
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
3. 创建Component，这里是关键部分了
    - 首先我们需要在该接口内部在定义Builder接口，该接口用`@Component.Builder`标记，表示该接口会由Component的`Builder`静态内部类实现。
    - 然后我们需要为定义方法`name()`和`love()`，加上注解`@BindsInstance`，返回类型为Builder。传入的参数需要用注解标识，去对应`User`构造参数。需要注意一点的就是方法只有一个参数，如果多个参数就会报错：只能有一个参数。
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

可以看出BindsInstance就是就是改造了`Component`里面的`Builder`类，Builder类实现了用`@Component.Builder`标注的接口。

> 接下来来看一下生成的相关代码！

- 可以看到Component中的`Builder`实现了`UComponent.Builder`接口，并将传递进来的参数进行空检测与成员变量引用
- 并且参数的实例也将会作为`Component`的成员变量，当创建`User`时作为其参数传入。
![DaggerUComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611142933.png)

### Component dependencies
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee10_test_subcomponent_dependencies)**

`dependencies`是注解`@Component`中的一个参数可以引用其他`Component`，我们看一下它的源码：
- 可以看到它的定义和`modules`是一模一样
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
它的主要作用就是将需要依赖的Component，放到自己的Component中当做成员变量直接引用。被依赖的Component就可以为主Component提供它在接口中定义的需要返回的实例。
- 如果有`AComponent dependencies BComponent`
- 那么则生成`public class DaggerAComponent implements AComponent { BComponent bComponent;...}`
- 并且这个`bComponent`实例是我们在`Builder`类里面传进去的。

`Component dependency`只允许您通过组件依赖关系访问接口中公开的类型，既：你只能访问到Component接口中定义的返回类型。

> 我们来实际操作！例子：咖啡和水

1. 定义咖啡和水的实例，在Coffee中我们覆写`toString()`把Coffee和Water的hashCode打印出来。
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
2. 定义两个的Module分别提供实例
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
3. 我们定义`WComponent`为Water的Component，定义`CComponent`为Coffee的Component。`CComponent`依赖于`WComponent`
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
> 但这也许不能保证您得到的一定是同一个实例，我们可以加上`@Singleton`注解，但是这里却是一个坑！因为这些Component的生命周期是不一样的，所以不能跨多个Component用同一个`@Singleton`来标记。如果这样做将会抛出一个错误信息：`This @Singleton component cannot depend on scoped components`[stackoverflow](https://stackoverflow.com/questions/39709317/dagger-2-singleton-component-depend-on-singleton/39710308)

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


> 我们来分析一下Dagger所生成的代码，主要我们看到`DaggerComponentDependency_CComponent`这个类，主要变化了在这里！

1. 我们看到`DaggerComponentDependency_CComponent`的内部Builder静态类
    - 从下面划线的地方我们可以看出，必须要传入依赖的Component的实例，否则会抛异常。
![Builder](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143001.png)
2. 我们看`DaggerComponentDependency_CComponent`里面的实现
    - 看到第一根划线处，它会把Builder中依赖的Component实例的引用传递给成员变量。
    - 看到第二根划线处，这里就跟我们平常调用接口中的方法一样能获得需要的实例，但是这里实例是通过依赖的Component来获取的实例。
![DaggerComponentDependency_CComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143021.png)
3. 当我们用了Scope的时候，`DaggerComponentDependency_CComponent`还会生成一个静态类内部类
    - 可以看出它实现了`Provider<T>`因该就是为了通过`Provider`的`get()`方法来提供`Water`实例。
    - 并且这里它将依赖的Component放这里面了
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143105.png)
4. 我们再来看此时的`DaggerComponentDependency_CComponent`
    - 它依赖的则是上面的静态内部类。
    - 并且通过我们熟悉的`DoubleCheck.provider`来对`get()`内逻辑进行的转变，使我们只获取一个实例。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143123.png)

### @Subcomponent
**[测试文件位置](https://github.com/xujiaji/learn-android/blob/master/LearnDagger/app/src/main/java/com/example/jiaji/daggertest/coffee10_test_subcomponent_dependencies)**

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

`SubComponent`可以在声明它时从父级访问整个绑定图，即可以使用在其`Modules`中提供的实例。

> 怎么使用，我们就直接用上个咖啡和水的代码！重新写一下他们的Component就行。

- 这里我们将`CComponent`作为子Component用`Subcomponent`来标记
- 然后我们还得在它的父Component中添加，如下面代码中的`CComponent cComponent(CModule cModule);`，如果`@Subcomponent`有多个Module，那么可以就要传递多个Module的参数。假如有：`@Subcomponent(modules = {CModule.class, CModule2.class})`，那么可以这样：`CComponent cComponent(CModule cModule, CModule2 cModule2);`
- 我们在使用的时候需要先创建父`Component`，然后才能去创建子`Component`，如下`main()`方法中

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

- `@Subcomponent`实例是通过父Component创建。`Component dependencies`可以依赖多个Component，并且各个Component单独创建且分离。
- `Component dependencies`只运行您访问接口中公开定义提供的实例，`@Subcomponent`可访问其`Modules`中声明的所有对象
- `Component dependencies`存在生命周期的不同，`@Subcomponent`却是同一个周期。

> 来看一下生成的代码`DaggerSubComponent_WComponent`，我们将其分成三部分来看

1. 首先我们看到`DaggerSubComponent_WComponent`内部类：子Component的定义
    - 它实现了我们定义的接口，并且和我们之前所生成的Component是类似的，只不过内部没有Builder静态类了。
    - 由于是内部类，所以它能访问所有父`Component`成员。
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143142.png)
2. 我们来看Builder，Builder好说的，跳过！
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143155.png)
3. 我们来看`DaggerSubComponent_WComponent`的方法
    - 可以看到，当我们调用`cComponent`时就会创建一个子Component现在类实例
    - 这是由于子Component是没有Builder去创建的也没有默认创建`Module`的功能。当然子Component也是需要他的`Module`的，于是要创建它需要的`Module`给它。
![DaggerSubComponent_WComponent](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/learn-dagger/20180611143210.png)

[Subcomponent和Component dependencies的关系区别](https://stackoverflow.com/questions/29587130/dagger-2-subcomponents-vs-component-dependencies)

### 安卓扩展的相关框架
如果有机会，如果希望看我这种啰嗦介绍的人多的话，在写一篇关于这个的吧！

---
### 结束
好了，神不知鬼不觉的一星期码了这么多字。能挨着看到这里的同学，能有多少咧Σ(っ°Д°;)っ

想起来，我以前写了一个MVP框架[XMVP](https://github.com/xujiaji/XMVP)就是通过获取配置的泛型参数类型然后再通过反射去实例化的自动完成它们之间的依赖关系。也可以说是这就是依赖注入了吧！哈哈！有兴趣的朋友可以去看一看用一用非常简洁哦！(｀・ω・´)

|相关信息|链接|
|-|-|
|文章中所有代码的地址|https://github.com/xujiaji/learn-android/tree/learn-dagger |
|本文作者（欢迎关注）|[奏响曲](https://juejin.im/user/5829eafe2f301e0057799f1a)|
|Github|https://github.com/xujiaji/ |
|个人博客|https://blog.xujiaji.com |
|本文地址|https://blog.xujiaji.com/post/learn-dagger |


如果文中内容有误或不合适欢迎您的指正！

over
