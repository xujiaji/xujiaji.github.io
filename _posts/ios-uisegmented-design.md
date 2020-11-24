---
title: iOS用UISegmentedControl设计一个顶部分页导航-Swift（翻译文）
date: 2018-07-23 14:36:32
author: xujiaji
thumbnail: blog/ios-uisegmented-design/display.gif
categories:
  - iOS
tags:
  - iOS
  - UI
  - Swift
  - 翻译
---

> 原文：《[Designing a Button Bar-Style UISegmentedControl in Swift](https://www.codementor.io/kevinfarst/designing-a-button-bar-style-uisegmentedcontrol-in-swift-cg6cf0dok)》

<!-- more -->

我正在做一个项目，项目里面我想用`UISegmentedControl`做一个简洁的“底部条形样式”的设计。它没有边框，所选下方有一个小长条，当你选择一个元素后他会相应的移动过去。我找到几个非常好的第三方库来处理这个问题，但是我在这些类库上遇到了一些麻烦，于是我尝试自己做。我以自动布局约束，以swift代码方式构建视图，并为了简单起见，将所有主题内联完成。

## 准备开始
我们在Swift playground中做这些事情，因此让我们从基本的东西开始，创建一个新的UIView并且添加一个带有3个片段的UISegmentedControl，另外需要注意，我构建约束的方式是假设所有片段长度想等的情况。如果不是的话，会导致底部长条在相应的位置上变得太宽或不够宽。

``` swift
import UIKit
import PlaygroundSupport

// 容器View
let view = UIView(frame: CGRect(x: 0, y: 0, width: 400, height: 100))
view.backgroundColor = .white

let segmentedControl = UISegmentedControl()
// 添加片段
segmentedControl.insertSegment(withTitle: "One", at: 0, animated: true)
segmentedControl.insertSegment(withTitle: "Two", at: 1, animated: true)
segmentedControl.insertSegment(withTitle: "Three", at: 2, animated: true)
// 让第一个片段默认选中
segmentedControl.selectedSegmentIndex = 0

// 设置为false，我们才能使用自动布局约束
segmentedControl.translatesAutoresizingMaskIntoConstraints = false

// 添加UISegmentedControl到容器View
view.addSubview(segmentedControl)

// 约束到容器的顶部
segmentedControl.topAnchor.constraint(equalTo: view.topAnchor).isActive = true
// 限制为容器view的宽度
segmentedControl.widthAnchor.constraint(equalTo: view.widthAnchor).isActive = true
// 设置高度
segmentedControl.heightAnchor.constraint(equalToConstant: 40).isActive = true

PlaygroundPage.current.liveView = view
```
此时实时窗口已经为我们展示了基本的`UISegmentedControl`。不要忘记将`isActive`属性附加到每个自动布局约束，其值为true，否则他们将不起作用。
![Basic UISegmentedControl](blog/ios-uisegmented-design/basic-uisegmentedcontrol.png)

## 颜色、字体和边框Oh My！
接下来，让我们删除掉`backgroundColor`和`tintColor`，删除后边框和已选择的片段背景颜色将会消失。
``` swift
// 将下面的代码添加到 selectedSegmentIndex下面
segmentedControl.backgroundColor = .clear
segmentedControl.tintColor = .clear
```

如果你看实时窗口，我们删除了`tintColor`后，`UISegmentedControl`已经消失，现在没有颜色了。要恢复标签，让我们更改所选片段和未选片段的字体、文本颜色和大小。
``` swift
// 添加这些代码到 segmentedControl.tintColor = .clear 后
segmentedControl.setTitleTextAttributes([
    NSAttributedStringKey.font: UIFont(name: "DINCondensed-Bold", size: 18)!,
    NSAttributedStringKey.foregroundColor: UIColor.lightGray
    ], for: .normal)

segmentedControl.setTitleTextAttributes([
    NSAttributedStringKey.font : UIFont(name: "DINCondensed-Bold", size: 18)!,
    NSAttributedStringKey.foregroundColor: UIColor.orange
    ], for: .selected)
```
![change-color-font](blog/ios-uisegmented-design/change-color-font.png)
到这儿差不多了！现在我们必须在所选段下方添加一个长条栏。

## 为选定片段底部添加长条
这个长条只是一个简单的UIView，然后将其`backgroundColor`与其所选片段字体的颜色相匹配。我们将选择的片段字体颜色和长条都设置为橙色。并且我们要为长条设置`translatesAutoresizingMaskIntoConstraints`为false。
``` swift
let buttonBar = UIView()
// 设置为false，我们才能使用自动布局约束
buttonBar.translatesAutoresizingMaskIntoConstraints = false
buttonBar.backgroundColor = UIColor.orange
```

接下来，将`buttonBar`作为子View添加到容器view中
``` swift
// 添加到 view.addSubview(segmentedControl)之后
view.addSubview(buttonBar)
```

最终，我们需要给它个宽度、高度和位置，在`segmentedControl`之后添加这些约束
``` swift
// 约束它的顶部位置在片段的底部位置
buttonBar.topAnchor.constraint(equalTo: segmentedControl.bottomAnchor).isActive = true
// 设置长条的高度
buttonBar.heightAnchor.constraint(equalToConstant: 5).isActive = true
// 约束它的左侧和片段的左侧重合
buttonBar.leftAnchor.constraint(equalTo: segmentedControl.leftAnchor).isActive = true
// 约束它的宽度 = 片段容器宽度 / 片段个数
buttonBar.widthAnchor.constraint(equalTo: segmentedControl.widthAnchor, multiplier: 1 / CGFloat(segmentedControl.numberOfSegments)).isActive = true
```

正如最后那条注释所说，我们需要长条的宽度为`segmentedControl`的宽度除以片段个个数。这保证了长条宽度将与单个片段的宽度完全匹配，同样这里是假设所有的段都是想等的宽度。
![added-bar](blog/ios-uisegmented-design/added-bar.png)
初始视图现在已完成！最后一步，我们需要让长条随所选的片段移动。

## 长条栏动画
当所选片段发生改变时，`segmentedControl`需要调用一个函数来处理长条栏在x轴上的位置转换，使其跑到选择的片段下方。定义个`Responder`类，并添加方法，然后在`segmentedControl`变量上添加回调，`segmentedControl`的值改变时会触发。
``` swift
// 在import声明下方
class Responder: NSObject {
    @objc func segmentedControlValueChanged(_ sender: UISegmentedControl) {

    }
}

let responder = Responder()
...
// 在PlaygroundPage.current.liveView = view声明的上方
segmentedControl.addTarget(responder, action: #selector(responder.segmentedControlValueChanged(_:)), for: UIControlEvents.valueChanged)
```

一定要确保`sender`作为方法参数类型，因为我们需要在调用函数时访问它。最后让我们来完成最后一块拼图，`buttonBar`在x轴的移动，它将移动到被选中的片段下
``` swift
@objc func segmentedControlValueChanged(_ sender: UISegmentedControl) {
  UIView.animate(withDuration: 0.3) {
      buttonBar.frame.origin.x = (segmentedControl.frame.width / CGFloat(segmentedControl.numberOfSegments)) * CGFloat(segmentedControl.selectedSegmentIndex)
  }
}
```
长条因该去的x轴位置 = (`segmentedControl`的宽度 / 片段个数) * 当前片段的下标

瞧瞧！我们的动画按钮栏出来了
![finished](blog/ios-uisegmented-design/display.gif)

## 结论
我希望这篇文章所提供的信息，能作为你在看了许多类库或iOS应用后的一个DIY解决方案。你可以将这里的`UISegmentedControl`连接到`UIPageViewController`或`UIScrollView`作为分段内容直接移动的方式。你这可以在[这里](https://gist.github.com/kfarst/9f8a1eb59cce2004b15f0b682c92eeed)找到playgroud代码在Github Gist，祝您iOS开发顺利！

---

> 补充说明：下面链接到的是我在练习的时候写的代码，供参考！

https://github.com/xujiaji/Learn-iOS/blob/master/TabSegmentedControl.playground/Contents.swift
