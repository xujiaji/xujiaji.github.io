---
title: 面向对象设计-里氏替换原则(LSP)
date: 2016.04.23 11:02
author: xujiaji
thumbnail: http://upload-images.jianshu.io/upload_images/1552955-214b1eec4a45c991.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240
tags:
    - Java
    - 面向对象设计
---

![探索神秘未知](http://upload-images.jianshu.io/upload_images/1552955-214b1eec4a45c991.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 主目录：[一个面向对象设计(OOD)的学习思路设计](http://www.jianshu.com/p/fab09d064846)

引子：
> 有一只小麻雀在大平原上，飞呀飞～。飞累了，看见前方一个大鸟...
`小麻雀：`大鸟兄你好，本鸟叫麻雀！请问您怎么称呼？
`大鸵鸟：`原来是麻雀小弟呀！本鸟叫鸵鸟！
`小麻雀：`鸵鸟哥耶！小弟飞的累的不行！让兄弟在您雄伟的身躯上歇歇脚么？
`大鸵鸟：`不行！本鸟还走累了呢！那我咋办？
`小麻雀：`你飞呗！难道我还拖着你不成？
`大鸵鸟：`前提是我要是能飞的起来呀！
`小麻雀：`开什么玩笑！咱们都是鸟，你飞不起来？“飞”是咋们鸟类的特征，想到飞就想到咋们鸟～。


----

![LSP.png](http://upload-images.jianshu.io/upload_images/1552955-d1c7423eabc9ec9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 1. 何为LSP？
- 全称：里氏替换原则（Liskov Substitution principle）
- 定义：`派生类（子类）`对象能够替换其`基类（超类）`对象被使用[^foot1]
 - Barbara Liskov对LSP定义是这么说的：若对每个类型`S`的对象`q1`，都存在一个类型`T`的对象`q2`，使得在所有对`T`编写的程序`P`中，用`q1`替换`q2`后，程序`P`行为功能不变，则`S`是`T`的子类型。
 听着有些绕，我将它画一个类图便于理解：
![LSP定义理解dsf
在类P中将T的对象q2，换成S的对象q1行为功能不变
则S继承T，得如图所示的关系](http://upload-images.jianshu.io/upload_images/1552955-dce323ccc6ad7d19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 2. 何为L？何为S？
**L:**`芭芭拉·利斯科夫（Barbara Liskov）`因为提出这个原则的女士姓里
**S:**`替换（Substitution）`父类能被子类**替换**
 - `替换`如上述定义所述，子类替换父类后不会影响其行为和功能。

## 3. 为何要有LSP？

> ①首先谈谈要是违反LSP

- 来张违反LSP的类图

![违反LSP.png](http://upload-images.jianshu.io/upload_images/1552955-2abece71be1dde9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 分析
 - 现在我说天上飞着一只鸟。。。
 - 子类麻雀替换父类：天上飞着一只麻雀。
 - 子类鸵鸟替换父类：天上飞着一只鸵鸟。

- 由上因为违反了里氏替代原则，导致整个设计存在严重逻辑错误。
- 由于违反了里氏替代原则，间接的违反了OCP原则[^foot2]。因为明显可以看出飞翔对于鸵鸟因该是封闭的。

> ②再来看一些代码（LSP的违反导致OCP的违反）

- 代码如下

`有三个类：鸟、鸵鸟、麻雀。鸵鸟和麻雀都有要去北京的方法`

``` java

/**
 * 鸟
 */
class Bird{
    public static final int IS_OSTRICH = 1;//是鸵鸟
    public static final int IS_SPARROW = 2;//是麻雀 
    public int isType;
    public Bird(int isType) {
        this.isType = isType;
    }
}
/**
 * 鸵鸟
 */
class Ostrich extends Bird{
    public Ostrich() {
        super(Bird.IS_OSTRICH);
    }
    public void toBeiJing(){
        System.out.print("跑着去北京！");
    }
}

/**
 * 麻雀
 */
class Sparrow extends Bird{
    public Sparrow() {
        super(Bird.IS_SPARROW);
    }
    public void toBeiJing(){
        System.out.print("飞着去北京！");
    }
}

```

`现在有一个方法birdLetGo，统一处理去北京的行为`

``` java
    public void birdLetGo(Bird bird) {
        if (bird.isType == Bird.IS_OSTRICH) {
            Ostrich ostrich = (Ostrich) bird;
            ostrich.toBeiJing();
        } else if (bird.isType == Bird.IS_SPARROW) {
            Sparrow sparrow = (Sparrow) bird;
            sparrow.toBeiJing();
        }
    }
```
- 分析
大家可以看出，birdLetGo方法明显的违反了开闭原则[^foot2]，它必须要知道所有Bird的子类。并且每次创建一个Bird子类就得修改它一次。

> ③结论

由上面的分析可以大致的了解了遵守LSP的重要性了吧！
- 如果不遵守，导致逻辑设计缺陷
- 如果不遵守，导致同时违反开闭原则
- 单个模型，孤立时并不具有设计意义。当多个模型出现时，抽象提取共同特征作为父类（基类），使之任何子类能替代于父类
- 如果试图预测所有假设，我们所得到的结果可能会充满很多不必要的复杂性。通常最好的办法是只预测那些最明显的LSP的违反状态，直到设计开始出现脆弱的状态，才去处理它们。[^foot3]

## 4. 基于契约设计能支持LSP？
 - 什么是契约设计？
  - 通过为每个方法声明的前置条件和后置条件[^foot4]来指定的。要是使一个方法得以执行，前置条件必须要为真。执行完毕后，该方法要保证后置条件为真。
 - 一个例子

> 几个继承关系的类

``` java
//动物
public class Animal {
    private String food;
    public Animal(String food) {
        this.food = food;
    }
    public String getFood() {
        return food;
    }

}

//鸟
class Bird extends Animal{
    public Bird(String food) {
        super(food);
    }
}

//鸵鸟
class Ostrich extends Bird{
    public Ostrich() {
        super("草");
    }
}

//麻雀
class Sparrow extends Bird{
    public Sparrow() {
        super("虫子");
    }
}

```
> 在动物园对象中调用吃的方法

``` java
class Zoo {
    /**
     * 吃早餐
     */
    public String eatBreakfast(Animal animal) {
        return animal.getFood();
    }
}
```

> 分析

 - 这里的满足前置条件就是调用方需满足能接受String这个食物类型
 - 满足后置条件可以看做是参数和返回类型
 - 前置条件不能更强，只能更弱，比如可以这样调用：

``` java
Object food = new Zoo().eatBreakfast(new Animal("肉"));
```
 - 后置条件可以更强，比如可以这样写：

``` java
String food = new Zoo().eatBreakfast(new Ostrich());
```

 - 这样我们就可以说是前置条件和后置条件就都得以满足




## 5. 结论总结
 - 如果LSP有效运用，程序会具有更多的可维护性、可重用性和健壮性

 - LSP是使OCP成为可能的主要原则之一

 - 正是因为子类的可替换性，才使得父类模块无须修改的情况就得以扩展

## 6. 参考文章
- [里氏替换原则-维基百科](https://zh.wikipedia.org/wiki/%E9%87%8C%E6%B0%8F%E6%9B%BF%E6%8D%A2%E5%8E%9F%E5%88%99)
- [OCP](http://www.jianshu.com/p/0fe6ab955842)
- 敏捷软件开发  第10章  里氏替换原则(LSP)
- [前置条件和后置条件是什么？](http://blog.csdn.net/q345852047/article/details/7955792)