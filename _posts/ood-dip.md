---
title: 面向对象设计-依赖倒置原则（DIP）
date: 2016-05-29 12:08
author: xujiaji
categories:
 - 设计模式
tags:
    - Java
    - 面向对象设计
---

# 简介
![DIP.png](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/ood/dip.png)

> 引入：
高层的决定不能因为某一个低层次模块的变动而影响全局，导致整个系统的变动。

## 什么是DIP？
- 全称：依赖倒置原则（Dependency inversion principle）
- 定义：
 1. 高层次的模块不应该依赖于低层次的模块，两者都应该依赖于**抽象接口**
 2. 抽象接口不应该依赖于具体实现，而具体实现则因该依赖于抽象接口。

## 我们如何理解DIP？
1. 知道依赖倒置的由来
 - 由于过去传统软件开发方法倾向于高层依赖于低层
 - 如今**依赖倒置**通过接口隔离，高层和底层都依赖于接口后
 - 结论：从结构上相对于传统编程方式而言就是**倒置**了。
2. 依赖倒置反面教材

 > 结构如下：没有遵循依赖倒置

 ![没有遵循依赖倒置](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog/ood/dip-err.png)

 > 代码如下：

 ``` java
/**
 * 高层
 */
class GaoCeng {
    ZhongCeng mZhongCeng;
    public GaoCeng(ZhongCeng mZhongCeng) {
        this.mZhongCeng = mZhongCeng;
    }
}
/**
 * 中层
 */
class ZhongCeng{
    DiCeng mDiCeng;
    public ZhongCeng(DiCeng mDiCeng){
        this.mDiCeng = mDiCeng;
    }
}
/**
 * 底层
 */
class DiCeng{
}```

3. 依赖倒置正面教材

 > 结构如下：

 ![遵循依赖倒置.png](http://upload-images.jianshu.io/upload_images/1552955-33a2d00c5821ea72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 > 代码如下：

 ``` java
/**
 * 中层接口
 */
interface ZhongCengInterface{   
}
/**
 * 高层接口
 */
interface GaoCengInterface{   
}
/**
 * 高层
 */
class GaoCeng {
    GaoCengInterface mGaoCengInterface;
    public GaoCeng(GaoCengInterface mGaoCengInterface) {
        this.mGaoCengInterface = mGaoCengInterface;
    }
}
/**
 * 中层
 */
class ZhongCeng implements GaoCengInterface{
    ZhongCengInterface mZhongCengInterface;
    public ZhongCeng(ZhongCengInterface mZhongCengInterface){
        this.mZhongCengInterface = mZhongCengInterface;
    }
}
/**
 * 底层
 */
class DiCeng implements ZhongCengInterface{
}
```
4. 结论
 - 可以从结构图上明确看出两种方式依赖结构是相反的，所以叫依赖倒置
 - 通过这种结构我们可以肆意的更改具体的接口实现类，而不会影响高层

## 遵循DIP有什么好处？
既然我们理解了DIP，那么DIP的好处不言而喻。
1. 通过依赖于接口，隔离了具体实现类
2. 低一层的变动并不会导致高一层的变动
3. 提高了代码的容错性、扩展性和易于维护

既然有好处，那么就必定有坏处：代码的增加，学习成本和代码思考时间的增加。（不过相对于后期的好处，这点我们还是能理解的）

## 例子
其实**理解DIP的例子**就是一个很好的对比例子。
现在来一个实际一点的例子：超重提价
- 需求：编写一个称重提价装置，物体2元/斤（物体重量 <= 100）计算。当物体超过100kg提醒，然后超出部分以10元/斤（物体重量 > 100）计算。

> 以传统方式编程

``` java
/**
 * 称重器传统编程
 */
class Scales{
    private double readValue;//获取到的物体的重量
    private double highestValue;
    private double inPrice;
    private double outPrice;
    public Scales(double highestValue, double inPrice, double outPrice) {
        this.highestValue = highestValue;
        this.inPrice = inPrice;
        this.outPrice = outPrice;
    }

    /**
     * 当有物体放上去后称重
     */
    public void startScales() {
        //...readValue = ？ （这里获取称重器计算的重量）
        showWeigh(readValue);
        double price = 0;
        double diff = readValue - highestValue;
        if (diff > 0) {
            outWeighWarn(diff);
            price += highestValue * inPrice;
            price += diff * outPrice;
        } else {
            price += readValue * inPrice;
        }
        showPrice(price);
    }
    /**
     * 显示重量
     */
    private void showWeigh(double weigh) {
    }

    /**
     * 超重提醒
     */
    private void outWeighWarn(double outWeigh) {}

    /**
     * 显示价格
     */
    private void showPrice(double price) {
    }
}
```

> 依赖倒置后

```java
/** 称重接口*/
interface Weigh {
    double read();
}

/** 最大重量、范围内价格、范围外价格的设置*/
interface Value{
    double highestValue();
    double inPrice();
    double outPrice();
}

/** 显示器接口*/
interface Show {
    void outWeighWarn(double diff);
    void showWeigh(double weigh);
    void showPrice(double price);
}


class Scales{
    private Weigh mWeigh;
    private Show mShow;
    private Value mValue;
    public Scales(Weigh mWeigh, Show mShow, Value mValue) {
        this.mShow = mShow;
        this.mWeigh = mWeigh;
        this.mValue = mValue;
    }

    /**
     * 当有物体放上去后称重
     */
    public void startScales() {
        mShow.showWeigh(mWeigh.read());
        double price = 0;
        double diff = mWeigh.read() - mValue.highestValue();
        if (diff > 0) {
            mShow.outWeighWarn(diff);
            price += mValue.highestValue() * mValue.inPrice();
            price += diff * mValue.outPrice();
        } else {
            price += mWeigh.read() * mValue.inPrice();
        }
        mShow.showPrice(price);
    }
}
```
我们可以看出依赖倒置后使代码可复用，可以是任意的称重装置，可以是任意的显示装置，只要它们实现对应的接口即可。高层不必在意底层具体是什么东西。

## 总结
- DIP的规则：依赖于抽象，不应该依赖于具体类。
- 任何变量都不应该持有一个指向具体类的指正或这引用
- 任何类都不应该从具体类派生
- 任何方法都不应该覆写它的任何基类中已经实现了的方法

每个程序都会有违反这些规则的情况，有时必须创建具体类的实例。此外，这些规则对于那些具体但却稳定的类来说似乎不太合理。如果一个具体类不太会改变，并且也不会创建其他类似的派生类，那么依赖于它并不会造成损害，比如说String类型。

- 然而，我们编写的大多数具体类都是不稳定的，我们将它们隐藏在抽象接口后面，隔离它们的不稳定性。

- 由于抽象将高层和细节彼此隔离，所以代码也非常容易维护

## 参考文献
敏捷软件开发 第12章 依赖倒置原则（DIP）
