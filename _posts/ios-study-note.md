---
title: iOS学习笔记
date: 2018-07-16 08:08:16
categories:
 - iOS
tags:
 - swift
 - 学习
 - 笔记
 - iOS
---

记录一些iOS学习过程中的笔记
<!-- more -->

## 创建项目目录结构
1. AppDelegate.swift:生命周期及变量的定义
2. ViewController.swift: MVC的C
3. Assets.xcasset:放资源文件，如图片等
4. info.plist：配置文件
5. xxxTest: 单元测试
6. Products:生成的文件
7. Main.storyboard: 视图

## 关闭软键盘
> 关闭代码

``` swift
textField.resignFirstResponder()
```
> 关闭方式1：
在Controller中重写touchesEnded()方法，然后在这里面关闭软件盘，意思是点击空白处关闭

``` swift
override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
    name.resignFirstResponder()
}
```
> 关闭方式2：
点击下一步时，关闭软键盘；
Controller实现UITextFieldDelegate协议；
实现UITextFieldDelegate协议中的textFieldShouldReturn方法；

``` swift
func textFieldShouldReturn(_ textField: UITextField) -> Bool {
    textField.resignFirstResponder()
    return true
}
```

## UIDatePicker选择时间后计算年龄
``` swift
func calAge(by datePicker: UIDatePicker) -> Int? {
    let gregorian = NSCalendar(calendarIdentifier: .gregorian)
    let now = Date()
    let components = gregorian?.components(NSCalendar.Unit.year, from: datePicker.date, to: now, options: NSCalendar.Options.init(rawValue: 0))
    return components?.year
}
```

## 页面跳转，传递数据
有两个Controller：ViewController和GalleryViewController。从ViewController跳转到GalleryViewController。
ViewController重写方法：prepare，该方法在页面跳转时会被调用，我们需要在里面判断是跳转到哪个页面。
``` swift
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // 需要给Segue取名
        if segue.identifier == "GoToGallery" {
            let index = beautyPicker.selectedRow(inComponent: 0)
            var imageName: String?
            switch index {
            case 0:
                imageName = "fangbingbing"
            case 1:
                imageName = "libingbing"
            case 2:
                imageName = "wangfei"
            case 3:
                imageName = "yangmi"
            case 4:
                imageName = "zhouxu"
            default:
                imageName = nil
            }

            // 得到下一个页面的Controller
            let vc = segue.destination as! GalleryViewController
            vc.imageName = imageName
        }
    }
```

## 通过图片文件名设置图片
``` swift
 beautyImage.image = UIImage(named: imageName)
```

## unwind segue关闭页面
关闭页面后，Controller可以获得上个页面传回来的值
该方法写在前一个页面
``` swift
@IBAction func closedPrePage(segue: UIStoryboardSegue) {
    print("closed")
}
```

## TableView下移一个状态栏的高度解决
``` swift
if #available(iOS 11.0, *) {
    tableView.contentInsetAdjustmentBehavior = .never
}
```

## TableView 添加刷新
``` swift
let refreshControl = UIRefreshControl()

// 初始化刷新
refreshControl.backgroundColor = UIColor.blue //设置刷新的背景颜色
refreshControl.attributedTitle = NSAttributedString(string: "刷新一下：\(Data())", attributes: [NSAttributedStringKey.foregroundColor: UIColor.white]) // 设置字体颜色
refreshControl.tintColor = UIColor.green // 加载菊花颜色
refreshControl.tintAdjustmentMode = .dimmed // 色彩调整模式
refreshControl.addTarget(self, action: #selector(addcount), for: .valueChanged) //添加方法目标

// 添加该刷新
tableView.refreshControl = refreshControl
```

刷新方法
``` swift
@objc func addcount() {
    dataArrary.append(contentsOf: dataArrary)
    tableView.reloadData()
    refreshControl.endRefreshing()
}
```
## 向项目添加字体
https://developer.apple.com/documentation/uikit/text_display_and_fonts/adding_a_custom_font_to_your_app

由于iOS的用的字体名称并不是文件名称，而是字体本身名称。
下面代码搜索所有字体，然后我们在控制台，找到多出来的名称。

``` swift
for family: String in UIFont.familyNames
{
    print("\(family)")
    for names: String in UIFont.fontNames(forFamilyName: family)
    {
        print("== \(names)")
    }
}
```

## 设置tabbar 字体和字体大小
``` swift
override func viewDidLoad() {
    super.viewDidLoad()
    let appearance = UITabBarItem.appearance()
    appearance.setTitleTextAttributes([NSAttributedStringKey.font: UIFont(name: "Ubuntu-Light", size: 9)!], for: .normal)
}
```

## UIButton`.isEnabled = false`后图片按钮的背景图片被改变
``` swift
UIButton.adjustsImageWhenDisabled = false
```
## UITableView或UICollectionView被TabBar遮盖
![](https://raw.githubusercontent.com/xujiaji/xujiaji.github.io/pictures/blog%5Cios-note%5Cnote-screen1.png)

## UITableView调用`reloadData`导致移动到列表顶部失效
``` swift
UIView.animate(withDuration: 0, animations: {
    self.tableView.contentOffset = CGPoint.zero
}, completion: { _ in
    self.tableView.reloadData()
})
```

## NavigationBar导致CollectionViewCell或TableViewCell偏移
``` swift
self.collectionView?.contentInsetAdjustmentBehavior = .automatic
```
