---
title: iOS开发-零碎笔记
date: 2018-07-16 08:08:16
author: xujiaji
thumbnail: blog/ios-note/20190319220203.jpg
categories:
 - 笔记
tags:
 - Swift
 - 学习
 - 笔记
 - iOS
---

记录一些iOS学习过程中的笔记
<!-- more -->

# iOS开发-零碎笔记

## 创建项目目录结构

1. AppDelegate.swift:生命周期及变量的定义
2. ViewController.swift: MVC的C
3. Assets.xcasset:放资源文件，如图片等
4. info.plist：配置文件
5. xxxTest: 单元测试
6. Products:生成的文件
7. Main.storyboard: 视图

## 快捷添加注释

``` c
option + command + /
```

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

1. 方法一
``` swift
if #available(iOS 11.0, *) {
    tableView.contentInsetAdjustmentBehavior = .never
}
```
2. 方法二，内容上部分区域向上偏移一个状态栏的高度
``` swift
collectionView?.contentInset.top = -UIApplication.shared.statusBarFrame.height
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

## UIButton 相关

### UIButton`.isEnabled = false`后图片按钮的背景图片被改变

``` swift
UIButton.adjustsImageWhenDisabled = false
```

### 扩展添加圆角、边框、边框颜色

``` Swift
@IBDesignable extension UIButton {

    @IBInspectable var borderWidth: CGFloat {
        set {
            layer.borderWidth = newValue
        }
        get {
            return layer.borderWidth
        }
    }

    @IBInspectable var cornerRadius: CGFloat {
        set {
            layer.cornerRadius = newValue
        }
        get {
            return layer.cornerRadius
        }
    }

    @IBInspectable var borderColor: UIColor? {
        set {
            guard let uiColor = newValue else { return }
            layer.borderColor = uiColor.cgColor
        }
        get {
            guard let color = layer.borderColor else { return nil }
            return UIColor(cgColor: color)
        }
    }
}
```

### 扩展图片在上，文字在下

``` Swift
extension UIButton {
    func alignVertical(spacing: CGFloat = 6.0, imageBottom: CGFloat = 0.0) {
        guard let imageSize = self.imageView?.image?.size,
            let text = self.titleLabel?.text,
            let font = self.titleLabel?.font
            else { return }
        self.titleEdgeInsets = UIEdgeInsets(top: 0.0, left: -imageSize.width, bottom: -(imageSize.height + spacing), right: 0.0)
        let labelString = NSString(string: text)
        let titleSize = labelString.size(withAttributes: [NSAttributedStringKey.font: font])
        self.imageEdgeInsets = UIEdgeInsets(top: -(titleSize.height + spacing), left: 0.0, bottom: imageBottom, right: -titleSize.width)
        let edgeOffset = abs(titleSize.height - imageSize.height) / 2.0;
        self.contentEdgeInsets = UIEdgeInsets(top: edgeOffset, left: 0.0, bottom: edgeOffset, right: 0.0)
    }
}
```

### 给UIButton图片染色

``` swift
let button = UIButton(type: .custom)
let image = UIImage(named: "image_name")?.withRenderingMode(.alwaysTemplate)
button.setImage(image, for: .normal)
button.tintColor = UIColor.red
```

## UITableView或UICollectionView被TabBar遮盖

![图片](blog/ios-note/note-screen1.png)

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

## 获取app版本

``` swift
/// 获取版本名
let appVersion = Bundle.main.infoDictionary!["CFBundleShortVersionString"] as? String

/// 获取版本号
let versionNumber = Bundle.main.infoDictionary!["CFBundleVersion"] as? String
```

## 打开网页本软件的appstore

``` swift
// App Store URL.
let appStoreLink = "https://itunes.apple.com/cn/app/id1144351773?mt=8"

/* First create a URL, then check whether there is an installed app that can
 open it on the device. */
if let url = URL(string: appStoreLink), UIApplication.shared.canOpenURL(url) {
    // Attempt to open the URL.
    UIApplication.shared.open(url, options: [:], completionHandler: {(success: Bool) in
        if success {
            print("Launching \(url) was successful")
        }})
}
```

## 设置圆形展示图像

1. 设置`UIImageView`宽度和高度，假如设置为60*60
2. 设置运行时属性，设置圆弧为30（正方形边长度一半）![图片](blog/ios-note/20181102144521.png)
3. 勾选`Clip to Bounds`，![图片](blog/ios-note/20181102145029.png)

## UIScrollView填充到顶部（去掉状态栏到空白间距）
1. `Content Insets` 选择`Never`
2. 去掉选中的`Safe Area Relative Margins`
![图片](blog/ios-note/20181225153159.png)

## UIImage 高斯模糊扩展

``` swift
extension UIImage {
    func blurred(radius: CGFloat) -> UIImage {
        let ciContext = CIContext(options: nil)
        guard let cgImage = cgImage else { return self }
        let inputImage = CIImage(cgImage: cgImage)
        guard let ciFilter = CIFilter(name: "CIGaussianBlur") else { return self }
        ciFilter.setValue(inputImage, forKey: kCIInputImageKey)
        ciFilter.setValue(radius, forKey: "inputRadius")
        guard let resultImage = ciFilter.value(forKey: kCIOutputImageKey) as? CIImage else { return self }
        guard let cgImage2 = ciContext.createCGImage(resultImage, from: inputImage.extent) else { return self }
        return UIImage(cgImage: cgImage2)
    }
}
```

## 两个UIImage 合并扩展

``` swift
extension UIImage {

  func overlayWith(image: UIImage, posX: CGFloat, posY: CGFloat) -> UIImage {
    let newWidth = size.width < posX + image.size.width ? posX + image.size.width : size.width
    let newHeight = size.height < posY + image.size.height ? posY + image.size.height : size.height
    let newSize = CGSize(width: newWidth, height: newHeight)

    UIGraphicsBeginImageContextWithOptions(newSize, false, 0.0)
    draw(in: CGRect(origin: CGPoint.zero, size: size))
    image.draw(in: CGRect(origin: CGPoint(x: posX, y: posY), size: image.size))
    let newImage = UIGraphicsGetImageFromCurrentImageContext()!
    UIGraphicsEndImageContext()

    return newImage
  }

}
```

## SDWebImageView 下载图片

1. 方式一
``` swift
img.sd_setImage(with: URL(string: "http://url"),
  placeholderImage: #imageLiteral(resourceName: "default_square")) { image, error, cacheType, url in

}
```
2. 方式二
``` Swift
SDWebImageDownloader
  .shared()
  .downloadImage(with: URL(string: "http://url"),
    options: SDWebImageDownloaderOptions.init(rawValue: 0),
    progress: nil,
    completed: { image, data, error, finished in
    if finished {

    }
})
```

## AVPlayerViewController 视频播放

``` Swift
import AVKit
func playVideoByUrl(string: String) {
    let videoURL = URL(string: string)
    let player = AVPlayer(url: videoURL!)
    let playerViewController = AVPlayerViewController()
    playerViewController.player = player
    self.present(playerViewController, animated: true) {
        playerViewController.player!.play()
    }
}
```

## 为UIImageView添加的点击手势无效

1. 勾选上`User Interaction Enabled`
![图片](blog/ios-note/20181226174028.png)
2. 代码中设置`uiimageview.userInteractionEnabled = true`

## PHAsset获取文件路径

``` Swift
extension PHAsset {

    func getURL(completionHandler : @escaping ((_ responseURL : URL?) -> Void)){
        if self.mediaType == .image {
            let options: PHContentEditingInputRequestOptions = PHContentEditingInputRequestOptions()
            options.canHandleAdjustmentData = {(adjustmeta: PHAdjustmentData) -> Bool in
                return true
            }
            self.requestContentEditingInput(with: options, completionHandler: {(contentEditingInput: PHContentEditingInput?, info: [AnyHashable : Any]) -> Void in
                completionHandler(contentEditingInput!.fullSizeImageURL as URL?)
            })
        } else if self.mediaType == .video {
            let options: PHVideoRequestOptions = PHVideoRequestOptions()
            options.version = .original
            PHImageManager.default().requestAVAsset(forVideo: self, options: options, resultHandler: {(asset: AVAsset?, audioMix: AVAudioMix?, info: [AnyHashable : Any]?) -> Void in
                if let urlAsset = asset as? AVURLAsset {
                    let localVideoUrl: URL = urlAsset.url as URL
                    completionHandler(localVideoUrl)
                } else {
                    completionHandler(nil)
                }
            })
        }
    }
}
```

## UIView 相关

### 通过UIView获取父UIViewController

``` Swift
extension UIView {
    var parentViewController: UIViewController? {
        var parentResponder: UIResponder? = self
        while parentResponder != nil {
            parentResponder = parentResponder!.next
            if let viewController = parentResponder as? UIViewController {
                return viewController
            }
        }
        return nil
    }
}
```

## String 相关

### html的字符串，将代码转成对应效果

``` Swift
extension String {
    var htmlToAttributedString: NSAttributedString? {
        guard let data = data(using: .utf8) else { return NSAttributedString() }
        do {
            return try NSAttributedString(data: data, options: [.documentType: NSAttributedString.DocumentType.html, .characterEncoding:String.Encoding.utf8.rawValue], documentAttributes: nil)
        } catch {
            return NSAttributedString()
        }
    }
    var htmlToString: String {
        return htmlToAttributedString?.string ?? ""
    }
}
```

### 正则表达式匹配

``` swift
/// 正则表达式匹配
extension String {
    func matchingStrings(regex: String) -> [String] {
        do {
            let regex = try NSRegularExpression(pattern: regex)
            let results = regex.matches(in: self,
                                        range: NSRange(self.startIndex..., in: self))
            return results.map {
                String(self[Range($0.range, in: self)!])
            }
        } catch let error {
            print("invalid regex: \(error.localizedDescription)")
            return []
        }
    }
}
```

## Data拼接数据

``` Swift
extension Data {
    mutating func append(_ string: String, using encoding: String.Encoding = .utf8) {
        if let data = string.data(using: encoding) {
            append(data)
        }
    }
}
```

## 打乱数组顺序

``` Swift
extension Array{
    mutating func randamArray() {
        var list = self
        for index in 0..<list.count {
            let newIndex = Int(arc4random_uniform(UInt32(list.count-index))) + index
            if index != newIndex {
                list.swapAt(index, newIndex)
            }
        }
        self = list
    }
}
```

## UIImage相关

### 高斯模糊图片

``` Swift
extension UIImage {
    func blurred(radius: CGFloat) -> UIImage {
        let ciContext = CIContext(options: nil)
        guard let cgImage = cgImage else { return self }
        let inputImage = CIImage(cgImage: cgImage)
        guard let ciFilter = CIFilter(name: "CIGaussianBlur") else { return self }
        ciFilter.setValue(inputImage, forKey: kCIInputImageKey)
        ciFilter.setValue(radius, forKey: "inputRadius")
        guard let resultImage = ciFilter.value(forKey: kCIOutputImageKey) as? CIImage else { return self }
        guard let cgImage2 = ciContext.createCGImage(resultImage, from: inputImage.extent) else { return self }
        return UIImage(cgImage: cgImage2)
    }
}
```

### 两张图片叠加成一张图片

``` Swift
extension UIImage {

    func overlayWith(image: UIImage, posX: CGFloat, posY: CGFloat) -> UIImage {
        let newWidth = size.width < posX + image.size.width ? posX + image.size.width : size.width
        let newHeight = size.height < posY + image.size.height ? posY + image.size.height : size.height
        let newSize = CGSize(width: newWidth, height: newHeight)

        UIGraphicsBeginImageContextWithOptions(newSize, false, 0.0)
        draw(in: CGRect(origin: CGPoint.zero, size: size))
        image.draw(in: CGRect(origin: CGPoint(x: posX, y: posY), size: image.size))
        let newImage = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()

        return newImage
    }

}
```

### 缩放图片

``` Swift
extension UIImage {

    func scaled(withSize size: CGSize) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(size, false, 0.0)
        defer { UIGraphicsEndImageContext() }
        draw(in: CGRect(x: 0.0, y: 0.0, width: size.width, height: size.height))
        return UIGraphicsGetImageFromCurrentImageContext()!
    }

}
```

## Json相关

### Json编码

``` Swift
extension JSONEncoder {

    /// 将实体类转换成Json数据
    func toJson<T: Encodable>(_ entity: T) -> String? {
        guard let encodedData = try? encode(entity) else {
            return nil
        }
        return String(data: encodedData, encoding: .utf8)
    }
}
```

### Json解码

``` Swift
extension JSONDecoder {
    func from<T: Decodable>(_ type: T.Type, json: String) -> T? {
        do {
            return try decode(type, from: json.data(using: .utf8)!)
        }
        catch {
            return nil
        }
    }
}
```

## 请求字段编码为字符串，形式如：key=value&key=value&key=value

``` Swift
extension Dictionary {
    func percentEscaped() -> String {
        return map { (key, value) in
            let escapedKey = "\(key)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            let escapedValue = "\(value)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            return escapedKey + "=" + escapedValue
            }
            .joined(separator: "&")
    }
}

extension CharacterSet {
    static let urlQueryValueAllowed: CharacterSet = {
        let generalDelimitersToEncode = ":#[]@" // does not include "?" or "/" due to RFC 3986 - Section 3.4
        let subDelimitersToEncode = "!$&'()*+,;="

        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "\(generalDelimitersToEncode)\(subDelimitersToEncode)")
        return allowed
    }()
}
```

## UIViewController 相关

### 添加子UIViewController

``` Swift
extension UIViewController {

    /// 添加子ViewController
    func addSubController(child: UIViewController, to: UIView? = nil) {
        addChildViewController(child)
        if let to = to {
            child.view.frame = to.frame
            to.addSubview(child.view)
        }
        else {
            child.view.frame = view.frame
            view.addSubview(child.view)
        }
        child.didMove(toParentViewController: self)
    }
}
```

### 移除子UIViewController

``` Swift
extension UIViewController {
    /// 移除子ViewController
    func removeSubController(child: UIViewController) {
        child.willMove(toParentViewController: nil)
        child.removeFromParentViewController()
        child.view.removeFromSuperview()
    }
}
```

### 关闭页面

#### 关闭当前页面

``` Swift
extension UIViewController {
    /// 关闭当前页面
    func closePage() {
        self.dismiss(animated: true, completion: nil)
    }
}
```

#### 关闭所有页面，除开最下级的那个页面

``` Swift
extension UIViewController {
    func closeAllPage() {
        //获取根VC
        var rootVC = self.presentingViewController
        while let parent = rootVC?.presentingViewController {
            rootVC = parent
        }
        //释放所有下级视图
        rootVC?.dismiss(animated: true, completion: nil)
    }
}
```

### 显示和关闭菊花等待加载

``` Swift
extension UIViewController {
    class func displaySpinner(onView : UIView) -> UIView {
        let spinnerView = UIView.init(frame: onView.bounds)
        spinnerView.backgroundColor = UIColor.init(red: 0.5, green: 0.5, blue: 0.5, alpha: 0.5)
        let ai = UIActivityIndicatorView.init(activityIndicatorStyle: .whiteLarge)
        ai.startAnimating()
        ai.center = spinnerView.center

        DispatchQueue.main.async {
            spinnerView.addSubview(ai)
            onView.addSubview(spinnerView)
        }

        return spinnerView
    }

    class func removeSpinner(spinner :UIView) {
        DispatchQueue.main.async {
            spinner.removeFromSuperview()
        }
    }
}
```

> 显示

``` Swift
let sp = UIViewController.displaySpinner(onView: self.view)
```

> 关闭

``` Swift
UIViewController.removeSpinner(spinner: sp)
```

## IAP 内购

> 使用

1. 除代码外的内购准备工序已OK
2. 获取产品数据：通过`IAPHelper.shared.fetchAvailableProducts`从苹果服务器获取所有传入的产品id的产品信息，传入的参数是产品的id字符串数组
3. 支付：`IAPHelper.shared.purchase(id: id)`，id是产品id

  ``` Swift
  IAPHelper.shared.purchase(id: selectItem!.product_id) {alert, product, transaction in
    if alert == .purchased { //购买成功
        if let receiptUrl = Bundle.main.appStoreReceiptURL, let receiptData = NSData(contentsOf: receiptUrl) {
            let receiptString = receiptData.base64EncodedString(options: NSData.Base64EncodingOptions(rawValue: 0))
            // 对receiptString加密字符串进行验证
        }
    }
    else if alert == .restored {

    }
    else if alert == .purchasing {

    }
    else {

    }
  }
  ```

> IAPHelper 代码

``` Swift
import StoreKit

enum IAPHelperAlertType{
    case disabled
    case restored
    case purchased
    case purchasing
    case setProductIds

    func message() -> String{
        switch self {
        case .setProductIds: return "未设置产品id，请调用 fetchAvailableProducts()"
        case .disabled: return "购买已取消"
        case .restored: return "您已成功恢复购买"
        case .purchased: return "您已成功购买此商品"
        case .purchasing: return "正在购买..."
        }
    }
}


class IAPHelper: NSObject {
    static let shared = IAPHelper()

    private override init() { }

    fileprivate var productID = ""
    fileprivate var productsRequest = SKProductsRequest()
    fileprivate var productDict = [String:SKProduct]()
    fileprivate var fetchProductCompletion: (([SKProduct])->Void)?

    fileprivate var productToPurchase: SKProduct?
    var purchaseProductCompletion: ((IAPHelperAlertType, SKProduct?, SKPaymentTransaction?) -> Void)?

    // MARK: - 购买产品
    func canMakePurchases() -> Bool {  return SKPaymentQueue.canMakePayments()  }

    func purchase(id: String, completion: @escaping ((IAPHelperAlertType, SKProduct?, SKPaymentTransaction?)->Void)) {
        self.purchaseProductCompletion = completion
        self.productToPurchase = productDict[id]

        guard let product = self.productToPurchase else {
            print(IAPHelperAlertType.setProductIds.message())
            fatalError(IAPHelperAlertType.setProductIds.message())
        }

        if self.canMakePurchases() {
            let payment = SKPayment(product: product)
            SKPaymentQueue.default().add(self)
            SKPaymentQueue.default().add(payment)

            print("采购产品: \(product.productIdentifier)")
            productID = product.productIdentifier
        }
        else {
            completion(.disabled, nil, nil)
        }
    }

    // MARK: - 恢复购买
    func restorePurchase(){
        SKPaymentQueue.default().add(self)
        SKPaymentQueue.default().restoreCompletedTransactions()
    }

    // MARK: - 获取可用的iap产品
    func fetchAvailableProducts(by ids: [String], completion: @escaping (([SKProduct])->Void)){
        self.fetchProductCompletion = completion
        // 把您的IAP产品id放到这里面

        guard !ids.isEmpty else {
            print("没有设置产品id")
            fatalError(IAPHelperAlertType.setProductIds.message())
        }

        productsRequest = SKProductsRequest(productIdentifiers: Set(ids))
        productsRequest.delegate = self
        productsRequest.start()
    }

}

extension IAPHelper: SKProductsRequestDelegate, SKPaymentTransactionObserver{
    // MARK: - 请求IAP产品
    func productsRequest (_ request:SKProductsRequest, didReceive response:SKProductsResponse) {

        if (response.products.count > 0) {
            for product in response.products {
                print("product.productIdentifier = \(product.productIdentifier)")
                self.productDict[product.productIdentifier] = product
            }
            self.fetchProductCompletion?(response.products)
        }
    }

    func paymentQueueRestoreCompletedTransactionsFinished(_ queue: SKPaymentQueue) {
        self.purchaseProductCompletion?(.restored, nil, nil)
    }

    // MARK:- IAP付款队列
    func paymentQueue(_ queue: SKPaymentQueue, updatedTransactions transactions: [SKPaymentTransaction]) {
        print("调用了几次啊！！！")
        for transaction:AnyObject in transactions {
            if let trans = transaction as? SKPaymentTransaction {
                switch trans.transactionState {
                case .purchased:
                    print("产品已购买")
                    SKPaymentQueue.default().finishTransaction(transaction as! SKPaymentTransaction)
                    self.purchaseProductCompletion?(.purchased, self.productToPurchase, trans)
                    break

                case .failed:
                    print("产品购买失败\(trans.error.debugDescription)")
                    SKPaymentQueue.default().finishTransaction(transaction as! SKPaymentTransaction)
                    self.purchaseProductCompletion?(.disabled, self.productToPurchase, trans)
                    break
                case .purchasing:
                    print("正在购买...")
                    self.purchaseProductCompletion?(.purchasing, self.productToPurchase, trans)
                    break
                case .restored:
                    print("产品已恢复购买")
                    SKPaymentQueue.default().finishTransaction(transaction as! SKPaymentTransaction)
                    self.purchaseProductCompletion?(.restored, self.productToPurchase, trans)
                    break

                default: break
                }
            }
        }
    }
}
```

## 判断退格符"\b"

<https://stackoverflow.com/a/29505548/9724892>

``` swift
func textField(textField: UITextField, shouldChangeCharactersInRange range: NSRange, replacementString string: String) -> Bool {
    if let char = string.cString(using: String.Encoding.utf8) {
        let isBackSpace = strcmp(char, "\\b")
        if (isBackSpace == -92) {
            print("Backspace was pressed")
        }
    }
    return true
}
```

## CocoaPods单独为一些库设置版本

在Podfile末尾加入

``` swift
swift_versions_of_pods = { 'swiftScan' => '4.0', 'CWActionSheet' => '4.0' }
post_install do |installer|
  installer.pods_project.targets.each do |target|
    defined_swift_version = swift_versions_of_pods[target.name]
    next if defined_swift_version.blank?
    target.build_configurations.each do |config|
      config.build_settings['SWIFT_VERSION'] = defined_swift_version
    end
  end
end
```

## 代码中为label添加点击事件

``` swift
override func viewDidLoad() {
    super.viewDidLoad()
    let tap = UITapGestureRecognizer(target: self, action: #selector(tapFunction))
    label.isUserInteractionEnabled = true
    label.addGestureRecognizer(tap)
}

@objc func tapFunction(sender: UITapGestureRecognizer) {
    print("tap working")
}
```

## 需要给手势传入额外的数据

1. 创建一个tap手势子类
``` swift
class TopicUITapGestureRecognizer : UITapGestureRecognizer {
    var id = Int()
    var title = String()
}
```
2. 处理数据
``` swift
@objc func tapFunction(sender: TopicUITapGestureRecognizer) {
    print("点击了: \(sender.id), \(sender.title)")
}
```
3. 添加事件设置数据
``` swift
let tap = TopicUITapGestureRecognizer(target: self, action: #selector(tapFunction))
tap.id = topic.id ?? 0
tap.title = topic.topic ?? ""
label.isUserInteractionEnabled = true
label.addGestureRecognizer(tap)
```

## 当Swift的枚举类型传入数组到OC中时报错

异常信息

``` swift
'NSInvalidArgumentException', reason: '-[__SwiftValue iconNormal]: unrecognized
```

解决: 传入枚举类型`.rawValue`

<https://stackoverflow.com/questions/39643394/swift-3-error-swiftvalue-unsignedintegervalue-unrecognized-selector/>

## 获取App缓存大小、清理App缓存

``` swift
class AppCacheCleanUtil {

    /// 获取app缓存大小
    static func getCacheSize() -> String {
        // 取出cache文件夹目录
        let cachePath = NSSearchPathForDirectoriesInDomains(.cachesDirectory, .userDomainMask, true).first

        // 取出文件夹下所有文件数组
        let fileArr = FileManager.default.subpaths(atPath: cachePath!)

        //快速枚举出所有文件名 计算文件大小
        var size = 0
        for file in fileArr! {

            // 把文件名拼接到路径中
            let path = cachePath! + ("/\(file)")
            // 取出文件属性
            let floder = try! FileManager.default.attributesOfItem(atPath: path)
            // 用元组取出文件大小属性
            for (key, fileSize) in floder {
                // 累加文件大小
                if key == FileAttributeKey.size {
                    size += (fileSize as AnyObject).integerValue
                }
            }
        }

        let totalCache = Double(size) / 1024.00 / 1024.00
        return String(format: "%.2f", totalCache)
    }


    /// 清理app缓存文件
    static func clearCache() {
        let cachePath = NSSearchPathForDirectoriesInDomains(.cachesDirectory, .userDomainMask, true).first

        // 取出文件夹下所有文件数组
        let fileArr = FileManager.default.subpaths(atPath: cachePath!)

        // 遍历删除
        for file in fileArr! {

            let path = cachePath?.appendingFormat("/\(file)")
            if FileManager.default.fileExists(atPath: path!) {

                do {
                    try FileManager.default.removeItem(atPath: path!)
                } catch {

                }
            }
        }
    }
}
```

## 使用UIVebView展示本地html

1. 创建并添加一个UIVebView到ViewController
2. 将html文件拖入项目中（对话框选择“Copy items if needed”）
3. 加载
``` swift
let url = Bundle.main.url(forResource: "privacy", withExtension: "html")
webView.loadRequest(URLRequest(url: url!))
```

## NavigationBar透明情况下，挡住了底部按钮点击事件

> 就是说NavigationBar的下面有个按钮，你去点击这个按钮没有反应

1. 继承`UINavigationBar`覆写`point`方法
``` swift
import UIKit

class NavigationEvent: UINavigationBar {

    var viewsToIgnoreTouchesFor:[UIView] = []

    override func point(inside point: CGPoint, with event: UIEvent?) -> Bool {
        var pointInside = super.point(inside: point, with: event)

        for each in viewsToIgnoreTouchesFor {
            let convertedPoint = each.convert(point, from: self)
            if each.point(inside: convertedPoint, with: event) {
                pointInside = false
                break
            }
        }
        return pointInside
    }
}
```

2. 在navigationController设置上面的自定义`UINavigationBar`

``` swift
navigationController.setValue(NavigationEvent(), forKey: "navigationBar")
```

3. 在你的UIControllerView中添加被挡住了的按钮(在这里有个顶部有个注册按钮`registerBtn`被NavigationBar挡住了点击无效)

在`viewDidLoad()`中添加就可以了

``` swift
if let navBar = self.navigationController?.navigationBar as? NavigationEvent {
    navBar.viewsToIgnoreTouchesFor = [registerBtn]
}
```

## CocoaPods公有库上传相关记录
> 创建Pod库
```
pod lib create 库名
```

> 注册CocoaPods账号，运行下发命令写入信息后，会收到一封邮件点击验证

```
$ pod trunk register 邮箱地址 '用户名' --description='当前设备描述'
```

> 查看当前账号信息

```
$ pod trunk me
```

> 发布，在pod项目中执行

```
1. Pod验证
pod repo lint --allow-warnings

2. 项目打版本tag
git tag "0.1.0"
git push --tags

3. 推送到公有仓库
pod repo push Specs SPEC_NAME.podspec --allow-warnings
```
