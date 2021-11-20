---
title: 面向对象设计-接口隔离(ISP)
date: 2016-05-07 10:12
author: xujiaji
categories:
 - 设计模式
tags:
    - Java
    - 面向对象设计
---

引入：

> `老手机：` 你们这些年轻手机光溜溜的，全身上下只有两个插孔几个按钮，为啥这么受欢迎？
`新手机：`老前辈，您虽然占了一半都是按钮，可以快速的点到，但是多数情况下都没用呀！我虽然只有几个按钮，但都是经常用到滴。我也能达到和你一样的效果，而且更简洁。
`老手机：`恩，人们只有打字的时候才用到那些按钮。
`新手机：`所以在平常时候，我这几个按钮就可以满足大部分需要了。
`老手机：`真是一代比一代强咯！

---

> ISP

![ISP](blog/ood/isp.png)

## 1.何为ISP？
 - 全称：接口隔离原则（Interface Segregation Principle）
 - 定义：客户程序不应该被迫依赖于它们不使用的方法

## 2.如何理解ISP？
 - 比如`图2-1.违反了ISP`中的鸵鸟类不应该被迫依赖于不使用的飞翔方法
 ![2-1.违反了ISP](blog/ood/isp-no.png)

- 现在将`2-1.满足ISP`的例子中的`接口鸟`进行拆分，能飞的`鸟类麻雀`实现`接口飞鸟`，不能飞的`鸟类鸵鸟`实现`接口鸟`，如下`图2-2`所示。

![2-2.满足ISP](blog/ood/isp-yes.png)

- 可能到这里大家有个疑惑：接口变多了！对！就是接口变多了。不是上面还举例了手机的例子吗？阐明了减少接口的好处。
 - 其实我们减少并不是接口，而是接口中的抽象方法。
 - 通过分离来满足客户端的需求，使客户端程序中只存在需要的方法。
 - 客户端的不同需求才是导致接口改变的原因。


## 3.遵循ISP有什么好处？
- 不遵循ISP而导致的一些问题，在`图2-1`中，鸵鸟是不需要飞的，但保留了飞的方法。
 - 现在接口中的`飞()`方法需要进行改动，假如改成：`boolean fly()`---可以理解为调用一次向上飞，再调用一次向下飞，依次循环。
 - 现在不仅会飞的鸟需要改动，连鸵鸟这些不会飞的鸟都要莫名奇妙的跟着去改动。
 - 显然这导致了程序之间的耦合增强，影响到了不应该影响的客户程序

- 现在正过来看遵循ISP接口，如`图2-2`所示的例子，分离了方法`飞`，使得更改时并不会影响到不相干的客户程序`（鸵鸟类）`
 - 需要尽可能避免这种耦合，因此我们希望分离接口。
 - 可以看出，分离接口有利于我们对需求变更时的快速高效的执行行动。
 - 并且使之解构层次更加的分明

## 4.循序渐进的例子（来自敏捷软件开发[^foot1]）
> 以ATM用户界面为例

1. ATM的用户界面有不同的交易模式，现将从ATM的基类`Transaction`（交易类）中派生子类：
 - `DepositTransaction`存款
 - `WithdrawalTransaction`取款
 - `TransferTransaction`转账

2. 每一个子类交易都有一个界面，因此要依赖于UI，调用的不同方法，如：DepositTransaction会调用UI类中的RequestDepositAmount()方法，当前ATM结果如下`图4-2-1.ATM操作解构`所示。
 ![4-2-1.ATM操作解构](blog/ood/isp-atm.png)
 - 这样做是ISP告诉我们应当避免的情形
 - 每个操作使用的UI方法，其他的操作都不会使用
 - 当每次`Transaction`子类的改动都会迫使对UI进行改动，从而影响到了其他所有`Transaction`子类及其他所有依赖于UI接口的类。
 - 当要增加一个支付煤气费的交易时，为了处理该操作想要显示的特定消息，就需要在UI中加入新的方法。糟糕的是，由于`Transaction`的子类全部依赖于UI接口，所以它们都需要重新编译。

3. 因此现在有一个办法，将UI接口分解成像`DepositUI`、`WithdrawalUI`以及`TransferUI`这样的单独接口，可以避免这种不合适的耦合，最终的UI接口可以去多重继承这些单独的接口。`图5-3-1.分离的ATM接口`和之后的代码展示了这个模型。
 ![5-3-1.分离的ATM接口](blog/ood/isp-atm-yes.png)

 > 定义交易接口

 ``` java
    /** 存款UI接口*/
    interface DepositUI {
        void RequestDepositAmount();
    }

    /** 取款UI接口*/
    interface WithdrawalUI {
        void RequestWithdrawalAmount();
    }

    /** 转账UI接口*/
    interface TransferUI {
        void RequestTransferAmount();
    }

    /** UI接口继承所有的交易接口*/
    interface UI extends DepositUI, WithdrawalUI, TransferUI{

    }
```

 >交易抽象类

 ``` java
    /** 交易类*/
    abstract class Transaction {
        public abstract void Execute();
    }
```

 > 交易派生类

 ``` java
    /** 存款交易类*/
    class DepositTransaction extends Transaction {
        private DepositUI mDepositUI;
        public DepositTransaction(DepositUI mDepositUI) {
            this.mDepositUI = mDepositUI;
        }

        @Override
        public void Execute() {
            //...
            mDepositUI.RequestDepositAmount();
            //...
        }
    }

    /** 取款交易类*/
    class WithdrawalTransaction extends Transaction {
        private WithdrawalUI mWithdrawalUI;
        public WithdrawalTransaction(WithdrawalUI mWithdrawalUI) {
            this.mWithdrawalUI = mWithdrawalUI;
        }
        @Override
        public void Execute() {
            //...
            mWithdrawalUI.RequestWithdrawalAmount();
            //...
        }
    }

    /** 转账交易类*/
    class TransferTransaction extends Transaction {
        private TransferUI mTransferUI;
        public TransferTransaction(TransferUI mTransferUI) {
            this.mTransferUI = mTransferUI;
        }
        @Override
        public void Execute() {
            //...
            mTransferUI.RequestTransferAmount();
            //...
        }
    }
```

 > 创建交易对象：由于每个操作都必须以特定的方式知晓UI版本，如`TransferTransaction`必须知道`TransferUI`。在程序中，使每个操作的构造时给它传入指向特定于它的UI的引用，从而解决这个问题。如下进行初始化

 ``` java
    UI GUI;
    void fun() {
        DepositTransaction mDepositTransaction = new DepositTransaction(GUI);
    }
```

 >虽然这样很方便，但同样要求每个操作都有一个指向对应UI的引用成员。另外一种解决这个问题的方法是创建一组全局常量。全局变量并不总是意味着拙劣的设计，在这种情况下，它们有着明显的易于访问的有点。

 ``` java
/** UI全局变量*/
class UIGlobals {
    public static DepositUI mDepositUI;
    public static WithdrawalUI mWithdrawalUI;
    public static TransferUI mTransferUI;
    public UIGlobals(UI lui) {
        UIGlobals.mDepositUI = lui;
        UIGlobals.mWithdrawalUI = lui;
        UIGlobals.mTransferUI = lui;
    }
}
```

 ``` java
/** 转账交易类*/
class TransferTransaction extends Transaction {
    @Override
    public void Execute() {
        //...
        UIGlobals.mTransferUI.RequestTransferAmount();
        //...
    }
}
```

 ``` java
/**
 * UI的实现类
 */
class UIEntity implements UI {

    @Override
    public void RequestDepositAmount() {
        //...
    }

    @Override
    public void RequestTransferAmount() {
        //...
    }

    @Override
    public void RequestWithdrawalAmount() {
        //...
    }
}
```
 ``` java
/**
 * 使用
 */
class A {
    //初始化UI静态类
    UIGlobals mUIGlobals = new UIGlobals(new UIEntity());

    //调用姿势
    void fun() {
        Transaction mTransaction = new TransferTransaction();
        mTransaction.Execute();
    }
}
```

---

`由于敏捷软件开发举的例子是c++的，知识有限，表示很多看不懂，可能有些地方偏差较大，想了解更多建议亲自去看看( ¯▽¯；) `

## 5.总结

- 胖类（fat class）：就是上边讲解的不满足ISP的类型

- 可以看出胖类增强了类之间的耦合，使得对该胖类进行改动会影响到所有其他类。

- 通过将胖类接口分解成多个特定类（客户端程序）的接口，使得强耦合得以解决

- 然后该胖类继承所有特定类的接口，并实现它们。就解除了这个特定类和它没有调用方法间的依赖关系，并使得这些特定类之间互不依赖。

## 6.参考文献
- 敏捷软件开发  第12章   接口隔离原则（ISP）
- [如何向妻子解释OOD](http://blog.jobbole.com/32122/)
