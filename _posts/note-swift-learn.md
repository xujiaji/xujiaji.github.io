---
title: Swift学习笔记
date: 2018-07-09 21:21:34
author: xujiaji
categories:
 - Swift
tags:
 - Swift
 - 学习
 - 笔记
---

记录一些swift的基本特性，以便使用的时候方便查阅。
<!-- more -->

学习地址：https://www.imooc.com/t/108955

## 元组
> 定义：可放入各种类型数据，元组长度自由

``` swift
var point = (5, 2)
var httpResponse = (404, "Not Found")
```

> 可先预定类型来定义

``` swift
var point2: (Int, Int, Int) = (10, 5, 2)
var httpResponse2: (Int, String) = (200, "OK")
let point4: (x: Int, y: Int) = (10, 5)
```

> 取值

``` swift
// 第一种方式
var point = (5, 2)
var(xx, yy) = point

// 第二种方式
point.0
point.1

// 第三种方式
let point3 = (x: 3, y: 2)
point3.x
point3.y

// 第四种方式（只取相关数据 是否登录）
let loginResult = (true, "xujiaji")
let (isLoginSuccess, _ ) = loginResult

```

## print打印

> 正常情况下

``` swift
print("a message")
```

> 拼接，（结果：1 2 3 4）

``` swift
print(1, 2, 3, 4)
```

> 插值：在拼接的中间插入值，默认是空格

``` swift
// 结果：1-2-3-4
print(1, 2, 3, 4, separator:"-")
```

> 结尾：默认是回车“`\n`”

``` swift
// 结果：1 -- 2 -- 3 -- 4:)hello
print(1, 2, 3, 4, separator:" -- ", terminator:":)")
```

> 另一种拼接方式：`\()`

``` swift
let y = 2, z = 4
// 结果：2 * 4 = 8
print("\(y) * \(z) = \(y*z)")
```

## if条件判断

> 基本用法，条件必须是Bool类型，可写表达式，但结果必须是Bool

``` swift
let imTrue:Bool = true
let imFalse = false

if imFalse {
    print("I'm True")
}
else {
    print("I'm False")
}
```

> 支持三目运算符

## for循环

> 基本用法

``` swift
// 从2打印到10
for index in 2...10 {
    print(index)
}
```

> 前闭后开，经常用于循环数组

``` swift
// 从0打印到9
for index in 0..<10 {
    print(index)
}
```
> 下划线忽略值

``` swift
for _ in 1...10 {

}
```
> 反向遍历

``` swift
// 结果：从10打印到1
for i in (1...10).reversed() {
    print(i)
}
```

> stride，`from`开始数，`to`结尾数（不包括结尾数），`through`结尾数（包括结尾数），`by`每次循环的跨度(可以是浮点数)

``` swift
// 结果： 0 2 4 6 8
for i in stride(from: 0, to: 10, by: 2) {
    print(i)
}

// 结果：0 2 4 6 8 10
for i in stride(from: 0, through: 10, by: 2) {
    print(i)
}

// 结果：从10遍历到1
for i in stride(from: 10, to: 0, by: -1) {
    print(i)
}
```

## while循环
> 和java没什么区别，只是没有小括号

> 至少执行一次循环，相当于java中的do while

``` swift
repeat {
  语句
} while 条件
```

## switch
**1.** 注意switch case中不用写`break`， `case`后可以匹配多个值逗号隔开
**2.** 不可以穷举（是否知道所有可能性），必须加上`default: `如果没有语句可以用`break`显示跳出或`()`表示空语句
**3.** 可以用字符串，浮点数，布尔等swift基础数据结构
**4.** `case`后面可以跟区间，如 `1 ..< 60`
**5.** `case`还可以对元组进行判断，并且元组可以通过`_`进行忽略；元组中还可以用区间，如`case (-2...2, -2...2):`；还可以和元组解包一起用，如`case (let x, let y):`
**6.** 语句结束后加上`fallthrough`关键字，可让条件向下判断
**7.** `case`中用`where`可以加上条件判断进行限制
``` swift
let point = (3, 3)
switch point {
case let(x, y) where x == y:
    print("It's on the line x == y!")
case let(x, y) where x == -y:
    print("It's on the line x == -y")
case let(x, y):
    print("It's just an ordinary point.")
    print("The point is (\(x), \(y)")
}
```
**8.** switch case还可以用if case 来简化代码
``` swift
let age = 19
switch age {
case 10...19:
    print("You're a teenage.")
default:
    print("You're not a teenage.")
}

// 用 if case 简化后
if case 10...19 = age {
    print("You're a teenage.")
}

// 还可以加上where条件判断，where可直接省略通过逗号隔开
if case 10...19 = age, age >= 18 {
    print("You're a teenage and in a college")
}

```
**9.** `case`关键字还可以用于for
``` swift
for i in 1...100 {
    if i % 3 == 0 {
        print(i)
    }
}

// 用case来写
for case let i in 1...100 where i%3 == 0 {
    print(i)
}
```

## 控制转移
> 给循环起名字

``` swift
// 表示如果得到结果，不仅break内部循环，也结束外部循环
findAnswer: for m in 1...300 {
    for n in 1...300 {
        if m*m*m*m - n*n == 15*m*n {
            print(m, n)
            break findAnswer
        }
    }
}
```

## guard
> 守卫，如果条件不成立，那么将会执行else

``` swift
func fun(money:Int, price: Int, capacity:Int, volume: Int) {
    guard money >= price else {
        print("Not enough money")
        return
    }
    guard capacity >= volume else {
        print("Not enough capacity")
        return
    }
    print("I can buy it")
}
```

## 字符串
``` swift
var str = "Hello, playground"
```
**1.** 判断是否为空
``` swift
var emptyString = ""
emptyString.isEmpty
```
**2.** 插值
``` swift
let name = "xujiaji"
let age = 24
let height = 1.7
let s = "My name is \(name). I'm \(age) years old. I'm \(height) meters tall."
```
**3.** 循环字符串
``` swift
for c in str {
    print(c)
}
```
**4.** 声明字符
``` swift
let mark: Character = "!"
```
**5.** 拼接字符
``` swift
str.append(mark)
```
**6.** 字符串长度
``` swift
str.count
```
**7.** 得到字符串开头下标： `str.startIndex` ；得到末尾下标：`str.endIndex`
**8.** 得到字符串前5个字符（`offsetBy`表示偏移量）
``` swift
str[str.index(str.startIndex, offsetBy: 5)]
```
**9.** 得到字符串某下标的前一个字符或后一个字符
``` swift
let spaceIndex = str.index(str.startIndex, offsetBy: 6)
str[str.index(before: spaceIndex)]
str[str.index(after: spaceIndex)]
```
**10.** 得到开始到`spaceIndex`下标之间的字符串
``` swift
str[str.startIndex..<spaceIndex]
```
**11.** 得到一个下标范围
``` swift
let  range = startIndex..<str.index(before: spaceIndex)
```
**12.** 将上面范围替换成Hi
``` swift
str.replaceSubrange(range, with: "Hi")
```
**13.** 末尾插入问号
``` swift
str.insert("?", at: str.endIndex)
```
**14.** 移除对应下标的字符
``` swift
str.remove(at: str.index(before: str.endIndex))
```
**15.** 移除某个下标范围字符
``` swift
str.removeSubrange(str.index(str.endIndex, offsetBy:-2)..<str.endIndex)
```
**16.** 大小写转换
``` swift
// 转大写
str.uppercased()
// 转小写
str.lowercased()
// 首字大写
str.capitalized
```
**17.** 是否包含
``` swift
// 是否包含Hi
str.contains("Hi")
// 前缀是否是Hi
str.hasPrefix("Hi")
// 后缀是否是!!
str.hasSuffix("!!")
```
**18.** 格式化字符串
``` swift
// 结果： 0.33333...
let ss0 = "one third is \(1.0/3.0)"
// 结果： 0.33
let ss1 = String(format: "one third is %.2f", 1.0/3.0)
// 结果： 0.33
let ss2 = NSString(format: "one third is %.2f", 1.0/3.0) as String
```
**19.** 字符串截取
``` swift
var ss3:NSString = "one third is 0.33"
// 从下标4开始截取到最后
ss3.substring(from: 4)
// 从开始截取到下标3
ss3.substring(to: 3)
// 截取下标从4开始，截取5个长度
ss3.substring(with: NSMakeRange(4, 5))
```
**20.** String 和 NSString的区别
> 有一个表情的时候String长度为1， NSString长度为2

**21.** 去除前后多余无效字符
``` swift
let s6 = "   --- Hello -----    " as NSString
// 去除前后空格和下划线
s6.trimmingCharacters(in: CharacterSet(charactersIn: " -"))
```

## Optional
**1.** 定义可选型
``` swift
var errorCode: Int? = 404
errorCode = nil
var imOptional: String? = nil
```
**2.** 具体类型可以赋值给可选项型，但反过来可选型是不能赋值给具体类型的。
**3.** 强制解包，但不能为`nil`否则会抛出异常
``` swift
var errorCode: Int? = nil
errorCode = 404
// errorCode! 强制解包
print("code", errorCode!)
```
**4.** 加上`nil`判断
``` swift
// 第一种写法
var errorCode: String? = nil
if errorCode != nil {
    "The errorCode is " + errorCode!
}
else {
    "No error"
}

// 第二种写法（简化），用两个问号
"The errorCode is \(errorCode ?? "no error")"
```
**5.** 可选型解包
``` swift
var errorCode: String? = "404"
if let errorCode = errorCode {
    "The errorCode is " + errorCode
}
else {
    "No error"
}

var errorMessage: String? = "Not found"
// errorCode有值，并且errorMessage有值
if let errorCode = errorCode, let errorMessage = errorMessage {
    "The errorCode is " + errorCode + "\nThe errorMessage is " + errorMessage
}

// errorCode有值，并且errorMessage有值，并且errorCode等于404
if let errorCode = errorCode, let _ = errorMessage, errorCode == "404" {
    print("Page not found")
}
```
**6.** 可选型调用
``` swift
var errorMessage: String? = "Not Found"
// 普通判断调用
if let errorMessage = errorMessage {
    errorMessage.uppercased()
}

// ?. 方式调用，和上面效果是一样的
errorMessage?.uppercased()

// 定义不用写“? =”方式，可选型的调用的结果也是可选型的
var uppercaseErrorMessage = errorMessage?.uppercased()

// 也可以调用后，如果存在使用该对象
if let errorMessage = errorMessage?.uppercased() {
    errorMessage
}
```
**6.** 实际运用
``` swift
var ageInput: String = "16"
var age = Int(ageInput) // 返回的是：Int?
if let age = Int(ageInput), age < 20 {
    print("You're a teenage")
}
```
**7.** 隐式可选类型，运用在能肯定的表示有值的情况下
``` swift
// 后面跟！表示是隐式可选类型
var errorMessage: String! = nil
errorMessage = "Not Found"
"The message is " + errorMessage

errorMessage = nil
// 会抛出异常，所以隐式可选类型危险的
//"The message is " + errorMessage
```

## Array
**1.** 空数组的定义
``` swift
// 有数据时的定义， 注意类型必须统一
var numbers = [1, 2, 3, 4, 5]
var vowels = ["A", "B", "C"]
// 定义的时确定好类型
//var numbers: [Int] = [0,1,2,3,4,5]

// 定义空数组
var emptyArr1:[Int] = []
var emptyArr2:Array<Int> = []
var emptyArr3 = [Int]()
var emptyArr4 = Array<Int>()

// 定义时统一赋值
var allZeros = Array<Int>(repeating: 0, count: 5) // [0, 0, 0, 0, 0]
var allZeros2 = [Int](repeating: 0, count: 5) // [0, 0, 0, 0, 0]
```
**2.** 数组查询基本使用方式
``` swift
var numbers = [1, 2, 3, 4, 5]
var vowels = ["A", "E", "I", "O", "U"]
var emptyArr = [Int]()

// 获取数组长度
vowels.count

// 判断是否为空
numbers.isEmpty // false
emptyArr.isEmpty // true

// 获取首元素或末元素
vowels.first // "A"
vowels.last // "U"
emptyArr.first // nil

// 可选型解包
if let firstVomel = vowels.first {
    print("The first vowel is " + firstVomel)
}

// 强制解包，由自己保证安全
vowels.first!

// 获取数组的最大值或最小值
numbers.min()
numbers.max()

// 从原数组中取出子数组
numbers[2..<4] // [3, 4]
numbers[2..<numbers.count] // [3, 4, 5]

// 包含
vowels.contains("A") // true
vowels.contains("B") // false

// 获取下标
vowels.index(of: "E") // 1
if let index = vowels.index(of: "E") {
    print("E is vowel in position \(index+1).")
}
else {
    print("E is not a vowel.")
}

// 通过下标遍历
for i in 0..<numbers.count {
    numbers[i]
}

// 直接遍历元素
for number in numbers {
    print(number)
}

// 同时遍历下标和元素
for (i, vowel) in vowels.enumerated() {
    print("\(i + 1): \(vowel)")
}

// 比较，与java不同，swift比较的是元素
var oneToFive = [1, 2, 3, 4, 5]
numbers == oneToFive // true

// 由于比较数组时与元素的顺序有关，所以下方结果为false
var oneToFive2 = [1, 2, 4, 3, 5]
numbers == oneToFive2 // false
```
**3.** 数组插入值的基本操作
``` swift
var courses = ["A course", "B course", "C course"]

// 添加元素
courses.append("D course") //["A course", "B course", "C course", "D course"]

courses += ["E course"] //["A course", "B course", "C course", "D course", "E course"]

// 根据位置插入元素
courses.insert("a course", at: 1) //["A course", "a course", "B course", "C course", "D course", "E course"]
```
**4.** 数组删除元素的基本操作
``` swift
var courses = ["A course", "B course", "C course", "D course"]
// 删除最后一个元素
courses.removeLast() //"D course"
// 删除第一个元素
courses.removeFirst() //"A course"
courses // ["B course", "C course"]
// 从下标0开始删除1个
courses.removeSubrange(0..<1) //["C course"]
// 删除所有元素
courses.removeAll()
```
**5.** 修改元素的基本操作
``` swift
var courses = ["A course", "B course", "C course", "D course"]
// 修改下标为0的元素
courses[0] = "1 course"
courses // ["1 course", "B course", "C course", "D course"]

// 修改下标1到2的元素
courses[1...2] = ["2 course", "3 course"]
courses // ["1 course", "2 course", "3 course", "D course"]

// 合并并修改0到2的元素
courses[0...2] = ["A course"]
courses // ["A course", "D course"]
```
## NSArray
**1.** NSArray是一个类，Array是一个结构
**2.** NSArray里可以放不同类型的元素，如：`var arr: NSArray = [1, "Hello", 3.0]`

## Dict
**1.** 字典的初始化和查询的基本使用方式
``` swift
// 创建一个有数据的字典
var dict = ["swift": "雨燕；快速", "python": "大蟒", "java":"爪哇岛", "groovy": "绝妙的；时髦的"]

// 创建空字典
var emptyDict1: [String:Int] = [:]
var emptyDict2: Dictionary<Int, String> = [:]
var emptyDict3 = [String:String]()
var emptyDict4 = Dictionary<Int, Int>()

// 通过key获取字典数据
dict["swift"] // "雨燕；快速"
dict["C++"] // nil

// 可选型解包
if let value = dict["swift"] {
    print("swift 的意思是：\(value)")
}

//字典数据的数量
dict.count // 4

dict.isEmpty // false
emptyDict1.isEmpty // true

//遍历所有key
for key in dict.keys {
    print(key)
}

// 遍历所有value
for value in dict.values {
    print(value)
}

// 遍历key和value
for (key, value) in dict {
    print("\(key): \(value)")
}

// 两个字典对比：比较的key和对应的value，由于字典是无序的，因此下方等式也成立
let dict1 = [1: "A", 2: "B", 3: "C"]
let dict2 = [1: "A", 3: "C", 2: "B"]
dict1 == dict2 // true

```
**2.** 字典的修改和删除
``` swift
// let的字典不可修改
var user = ["name": "xujiaji", "password": "123456", "occupation": "programmer"]

// 修改值
user["occupation"] = "freelancer"
// 调用方法修改值会返回之前的值
user.updateValue("abcdefg", forKey: "password") // "123456"
user //["name": "xujiaji", "password": "abcdefg", "occupation": "freelancer"]

let oldPassword = user.updateValue("abcdefg", forKey: "password")
if let oldPassword = oldPassword, let newPassword = user["password"], oldPassword == newPassword {
    print("注意：修改后的密码和之前的一样，可能导致安全问题")
}

// 直接添加新的key和value
user["email"] = "jiajixu@qq.com"
user // ["name": "xujiaji", "occupation": "freelancer", "email": "jiajixu@qq.com", "password": "abcdefg"]

// 通过方法添加新的key和value
user.updateValue("https://blog.xujiaji.com", forKey: "website") // nil
user // ["name": "xujiaji", "occupation": "freelancer", "email": "jiajixu@qq.com", "password": "abcdefg", "website": "https://blog.xujiaji.com"]

// 删除key和value
user["website"] = nil

// 通过调用方法删除key和value
if let email = user.removeValue(forKey: "email") {
    print("电子邮箱\(email)删除成功")
}

// 删除所有数据
user.removeAll()
```

## Set
**1.** 初始化和基本使用
``` swift
// 创建一个有数据的Set集合，和数组定义方式差不多，但是加上了类型申明
var skillsOfA: Set<String> = ["swift", "OC"]

// 创建空Set集合
var emptySet1: Set<String> = []
var emptySet2 = Set<String>()

//集合是无序的，并且没有重复
var vowels = Set(["A", "E", "I", "O", "U", "U"]) //{"O", "A", "I", "U", "E"}

var skillsOfB: Set = ["HTML", "CSS", "JavaScript"]

// 集合元素个数
skillsOfA.count // 2

var set: Set = [2, 2, 2, 2]
set.count // 1

// 集合是否为空
skillsOfB.isEmpty // false
emptySet1.isEmpty // true

// 快速获取集合中的第一个元素
skillsOfA.first // "swift"

// 包含
skillsOfA.contains("swift") // true

// 遍历
for skill in skillsOfB {
    print(skill)
}

// 比较的值，和顺序无关
let setA: Set = [1, 2, 3]
let setB: Set = [3, 2, 1, 1, 1, 1]
setA == setB // true
```
**2.** 元素的插入和删除
``` swift
var skillsOfA: Set<String> = ["swift", "OC"]
var skillsOfB: Set<String> = ["HTML", "CSS", "Javacript"]
var skillsOfC: Set<String> = []

// 添加元素
skillsOfC.insert("swift")
skillsOfC.insert("HTML")
skillsOfC.insert("CSS")
skillsOfC //{"swift", "CSS", "HTML"}
// 重复添加
skillsOfC.insert("CSS")
skillsOfC //{"swift", "CSS", "HTML"}


// 删除元素
skillsOfC.remove("CSS")
skillsOfC //{"swift", "HTML"}
// 删除没有的元素
skillsOfC.remove("Javascript") //nil

if let _ = skillsOfC.remove("HTML") {
    print("HTML is removed")
}
```
**3.** 集合之间的操作：并集、交集、减集、异或
``` swift
var skillsOfA: Set<String> = ["swift", "OC"]
var skillsOfB: Set<String> = ["HTML", "CSS", "Javacript", "Java"]
var skillsOfC: Set<String> = ["swift", "Java"]

// 并集
skillsOfA.union(skillsOfC) //{"swift", "OC", "Java"}
skillsOfA //{"swift", "OC"}
// 并集操作后改变skillsOfA的值
skillsOfA.formUnion(skillsOfC) //{"swift", "OC", "Java"}
skillsOfA //{"swift", "OC", "Java"}

// 交集
skillsOfB.intersection(skillsOfC) // {"Java"}
skillsOfB // {"Java", "HTML", "CSS", "Javacript"}
skillsOfB.formIntersection(skillsOfC) // {"Java"}
skillsOfB // {"Java"}

// 减集
skillsOfA.subtracting(skillsOfC)
skillsOfA // {"swift", "OC", "Java"}
skillsOfA.subtract(skillsOfC)
skillsOfA // {"OC"}

// 异或
skillsOfA.symmetricDifference(skillsOfC)
skillsOfA // {"OC"}
skillsOfA.formSymmetricDifference(skillsOfC)
skillsOfA // {"OC", "swift", "Java"}

// 可操作数组
skillsOfA.union(["Java", "Android"])
```
**4.** 集合中的子集，超集合相离的判断
``` swift
var skillsOfA: Set<String> = ["swift", "OC"]
var skillsOfB: Set<String> = ["HTML", "CSS", "Javacript", "Java"]
var skillsOfC: Set<String> = ["swift", "Java"]
var skillsOfD: Set = ["swift"]

// 是否是子集（D是否包含A）
skillsOfD.isSubset(of: skillsOfA) // true
// 是否是真子集 （D是否包含A，并且D != A）
skillsOfD.isStrictSubset(of: skillsOfA) // true

// 是否是超集（与子集相反）
skillsOfA.isSuperset(of: skillsOfD) // true
// 是否是真超集
skillsOfA.isStrictSuperset(of: skillsOfD) // true

// 判断相离(两集合没有共有元素)
skillsOfA.isDisjoint(with: skillsOfB) // true
skillsOfA.isDisjoint(with: skillsOfC) // false
```

## Function
### 参数部分
**1.** 方法的基本定义
``` swift
//  函数的基本构建
func sayHelloTo(name: String) -> String {
    return "Hello " + name
}

// 调用
sayHelloTo(name: "xujiaji")

// 通过添加下划线，调用的时候可以省略参数名
func sayHelloTo(_ name: String) -> String {
    return "Hello " + name
}

sayHelloTo("xujiaji")


// 函数参数中包含可选型
func sayHelloTo(name: String?) -> String {
    return "Hello " + (name ?? "Guest")
}
var nickname: String? = nil
sayHelloTo(name: nickname)

// 没有参数与没有返回值的参数
func printHello() {
    print("Hello")
}
// 显示的说明没有返回值
//func printHello() -> () {
//}
// Void = ()
//func printHello() -> Void {
//}
```
**2.** 写一个得到数组中最大和最小值的方法
``` swift
func findMaxAndMin(numbers: [Int]) -> (max: Int, min: Int)? {
    guard !numbers.isEmpty else {
        return nil
    }
    var minValue = numbers[0]
    var maxValue = numbers[0]

    for number in numbers {
        minValue = min(minValue, number)
        maxValue = max(maxValue, number)
    }

    return (maxValue, minValue)
}

var scores: [Int]? = [202, 1234, 5678, 334, 982, 555]
scores = scores ?? []
if let result = findMaxAndMin(numbers: scores!) {
    print("The max value is \(result.max)")
    print("The min value is \(result.min)")
}
```
**3.** 方法的外部参数名和内部参数名
``` swift
// 一般写法，内部参数名同时也是外部参数名
func sayHelloTo(name: String, greeting: String) -> String {
    return "\(greeting), \(name)"
}
sayHelloTo(name: "Playground", greeting: "Hello")

// 为参数提供外部参数名，让语义更加的明确
func sayHello(to name: String, withGreetingWord greeting: String) -> String {
    return "\(greeting), \(name)"
}
sayHello(to: "Playground", withGreetingWord: "Hello")

// 一个计算乘法的方法
func mutiply(num1: Int, x num2: Int) -> Int {
    return num1 * num2
}
mutiply(num1: 4, x: 2)

// 下方乘法虽语义明确但是，确显得复杂，直接传入两个值会更加得当。于是我们可以通过下划线忽略参数名
func mutiply(_ num1: Int, _ num2: Int) -> Int {
    return num1 * num2
}
mutiply(4, 2)
```
**4.** 默认参数和可变参数
``` swift
// 默认参数的使用
func sayHello(to name: String = "Playground", withGreetingWord greeting: String = "Hello", punctuation: String = "!") -> String {
    return "\(greeting), \(name)\(punctuation)"
}

sayHello() // "Hello, Playground!"
sayHello(to: "Bob") // "Hello, Bob!"
sayHello(to: "Bob", withGreetingWord: "Bye") //"Bye, Bob!"

// 可变参数的使用
// 计算平局值
func mean(_ numbers: Double ... ) -> Double {
    var sum: Double = 0
    for number in numbers {
        sum += number
    }
    return sum / Double(numbers.count)
}

mean(1, 2, 3.4, 7.5)

// print是一个非常好的有默认参数和可变参数的函数，可变参数不一定放在最后
print("Hello", 1, 2, 3, separator: ",", terminator: ".") // "Hello,1,2,3."
```
**5.** 常量参数、变量参数
``` swift
// 函数的参数默认都是不可变的
func toBinary(_ num: Int) -> String {
    // 让传入的参数num称为可变参数
    var num = num
    var res = ""
    repeat {
        res = String(num%2) + res
        num /= 2
    } while num != 0
    return res
}

toBinary(12) // "1100"
```
**6.** inout
``` swift
// var 参数是值传递，不能延续到函数体外面
var x = 100
toBinary(x)
x

// 如果需要延续到外面
func swapTwoInt(a: inout Int, b: inout Int) {
//    let t: Int = a
//    a = b
//    b = t
// 通过元组可直接交换值
    (a, b) = (b, a)
}


var a: Int = 1
var b: Int = 2

// 传入a和b的引用
swapTwoInt(a: &a, b: &b)
a
b

// swift提供的交换方法
swap(&a, &b)
a
b
```
### 类型部分
**1.** 函数类型的基本概念
``` swift
// 函数类型
func add(_ a: Int, _ b: Int) -> Int {
    return a + b
}

// 方法也可以赋值
let anotherAdd = add
// 也可以声明类型
// let anotherAdd: (Int,Int)->Int = add
anotherAdd(3, 4)


func sayHello(to name: String) {
    print("Hello, \(name)!")
}

let anotherSayHello1 = sayHello
let anotherSayHello2: (String) -> () = sayHello
let anotherSayHello3: (String) -> Void = sayHello
```
**2.** 如何使用函数类型？
``` swift
var arr: [Int] = []
for _ in 0..<100 {
    arr.append(Int(arc4random() % 1000))
}
arr

// 默认排序
arr.sort()
arr

// 在排序中使用函数参数
func biggerNumberFirst(_ a: Int, _ b: Int) -> Bool {
    return a > b
}
// 排序使用我们自己定义的规则
arr.sort(by: biggerNumberFirst)
arr

func cmpByNumberString(_ a: Int, _ b: Int) -> Bool {
    return String(a) < String(b)
}
arr.sort(by: cmpByNumberString)

func near500(_ a: Int, _ b: Int) -> Bool {
    return abs(a - 500) < abs(b - 500)
}
// 返回排序结果，排序不会影响arr的顺序
arr.sorted(by: near500)
arr
```
**3.** 定义函数类型参数
``` swift
func changeScores(_ scores: inout [Int], by changeScore: (Int)->Int) {
    for (i, score) in scores.enumerated() {
        // 不需要知道方法的具体定义
        scores[i] = changeScore(score)
    }
}

func change1(score: Int) -> Int {
    return Int(sqrt(Double(score)) * 10)
}

func change2(score: Int) -> Int {
    return score + 3
}

var scores1 = [36, 61, 78, 89, 99]
changeScores(&scores1, by: change1) // [60, 78, 88, 94, 99]

var scores2 = [88, 101, 124, 137, 150]
changeScores(&scores2, by: change2) // [91, 104, 127, 140, 153]
```
**4.** 高阶函数map、filter、reduce
``` swift

func change(num: Int) -> Int {
    return num + 2
}

var numbers = [65, 91, 45, 89, 99]
// map
numbers.map(change) //[67, 93, 47, 91, 101]

func isPassOrFail(num: Int) -> String {
    return num < 60 ? "Fail" : "Pass"
}
numbers.map(isPassOrFail) //["Pass", "Pass", "Fail", "Pass", "Pass"]

// filter
func fail(num: Int) -> Bool {
    return num < 60
}
numbers.filter(fail) //[45]

// reduce
func add(num1: Int, num2: Int) -> Int {
    return num1 + num2
}
numbers.reduce(0, add) //389
numbers.reduce(0, +) //389

func concatenate(str: String, num: Int) -> String {
    return str + String(num) + " "
}
numbers.reduce("", concatenate) //"65 91 45 89 99 "
```
**5.** 函数作为函数的返回类型
``` swift
func tier1MailFee(weight: Int) -> Int {
    return 1 * weight
}

func tier2MailFee(weight: Int) -> Int {
    return 3 * weight
}

func feeByUnitPrice(price: Int, weight: Int) -> Int {
    // 函数作为函数的返回类型
    func chooseMailFee(by weight: Int) -> (Int) -> Int {
        return weight <= 10 ? tier1MailFee : tier2MailFee
    }

    let mailFeeByWeight = chooseMailFee(by: weight)
    return mailFeeByWeight(weight) + price * weight
}

feeByUnitPrice(price: 50, weight: 8)
```
## 闭包
**1.** 基本使用方式
``` swift
var arr = [3, 2, 4, 5, 8]

// 之前的写法
func bigger(a: Int, b: Int) -> Bool {
    return a > b
}
arr.sort(by: bigger) // [8, 5, 4, 3, 2]

// 闭包的写法
arr.sort(by: { (a: Int, b: Int) -> Bool in
    return a >  b
}) // [8, 5, 4, 3, 2]
```
**2.** 上面的代码可简写
``` swift
// 如果闭包只有一行代码，可放在同一行
arr.sort(by: { (a: Int, b: Int) -> Bool in return a > b })

// 由于自动会得到参数和返回值类型， 可这样写
arr.sort(by: { a, b in return a > b})

// 由于知道需要return，可简写为
arr.sort(by: { a, b in a > b})

// 由于参数是一个元组，元组有标识，可简写为
arr.sort(by: { $0 > $1 })

// 由于“>”本身就是一个函数
arr.sort(by: >)
```
**3.** 结尾闭包的使用
``` swift
var arr = [3, 2, 4, 5, 8]

arr.sort(by: { a, b in return a > b })

// 如果函数参数在最后，我们可以是使用结尾闭包
arr.sort() { a, b in
    return a > b
}

// 如果没有其他参数，可将小括号夜省略了
arr.sort { a, b in
    return a > b
}

// 将数组中的十进制数字全部改为二进制
arr.map{ number -> String in
    // 将number的不可变改为可变
    var number = number
    var res = ""
    repeat {
        res = String(number % 2) + res
        number /= 2
    } while number != 0
    return res
}
```
**4.** 尾闭包在IOS动画中的运用
``` swift
let showView = UIView(frame: CGRect(x: 0, y: 0, width: 300, height: 300))
let rectangle = UIView(frame: CGRect(x: 0, y: 0, width: 50, height: 50))
rectangle.center = showView.center
rectangle.backgroundColor = UIColor.red
showView.addSubview(rectangle)

UIView.animate(withDuration: 2.0) {
    rectangle.backgroundColor = UIColor.blue
    rectangle.frame = showView.frame
}

import PlaygroundSupport
PlaygroundPage.current.liveView = showView
```
**5.** 闭包，内容捕获
``` swift
// 数值捕获
// 申明变量
var num = 300
arr.sort{ a , b in
    abs(a-num) < abs(b-num)
}
```
**6.** 闭包和函数是引用类型
``` swift
func runningMetersWithMetersPerDay(_ metersPerDay: Int) -> () -> Int {
    var totalMeters = 0
    return {
        totalMeters += metersPerDay
        return totalMeters
    }
}

var planA = runningMetersWithMetersPerDay(2000)
// 注意每次都不是从0开始相加，因为返回的是闭包的引用
planA() //2000
planA() //4000
planA() //6000
```
## enum
**1.** 枚举的基本使用
``` swift
// 定义枚举类型
enum Month {
    case January
    case February
    case March
    case April
    case May
    case June
    case July
    case August
    case September
    case October
    case November
    case December
}

// 定义枚举也可以写成一行
enum Season {
    case Spring, Summer, Autumn, Winter
}

// 如果确定了枚举类型，则可以省略枚举名字，如：Month.March 写成 .March
func season(month: Month) -> Season {
    switch month {
    case .March, .April, .May:
        return .Spring
    case .June, .July, .August:
        return .Summer
    case .September, .October, .November:
        return .Autumn
    case .December, .January, .February:
        return .Spring
    }
}

season(month: Month.April) //Spring
```
**2.** 枚举的原始值
``` swift
// enum Month: Int 表名Month的原始值是int类型的，并且原始值会自动递增
enum Month: Int{
    case January = 1, Febuary, March, April, May, June, July, August, September, October, November, December
}

// 返回距离新的一年还有多少个月，rawValue得到原始值
func monthBeforeNewYear(month: Month) -> Int {
    return 12 - month.rawValue
} // 4

// 可以通过原始值获取到对应的枚举值
if let theMonth = Month(rawValue: 8) {
    print("\(monthBeforeNewYear(month: theMonth)) months before New Year!") //4 months before New Year!
}

// raw value为整型的枚举类型，如果不显示给出整型值，则从0开始
enum Grade: Int{
    case F,E,D,C,B,A
}

// 枚举类型的raw value值不一定是顺序的
enum Coin: Int{
    case Penny = 1
    case Nickel = 5
    case Dime = 10
    case Quarter = 25
}

let coin: Coin = .Quarter
print("It's \(coin.rawValue) cents") //It's 25 cents

// 使用String作为raw value，如果我们没有确定原始值，那么swift会自动以枚举值的名字作为原始值
enum ProgrammingLanguage2: String{
    case Swift
    case ObjectiveC = "Objective-C"
    case C
    case Java
}

let myFavoriteLanguage2: ProgrammingLanguage2 = .Swift
print( "\(myFavoriteLanguage2.rawValue) is my favorite language.") //Swift is my favorite language.
```
**3.** 并联值
``` swift

// Associate Value 和 Raw value 只能存在一个
enum ATMStatus {
    case Success(Int)
    case Error(String)
    case Waiting // 也可以没有Associate Value
}

// 余额
var balance = 1000

// 获取ATMStatus
func withdraw(amount: Int) -> ATMStatus {
    if balance >= amount {
        balance -= amount
        return .Success(balance)
    }
    else {
        return .Error("Not enough money")
    }
}

// 解包相应的 Associate Value，也可忽略，就像.Waiting那样就行了
switch withdraw(amount: 100) {
case let .Success(newBlance):
    print("\(newBlance) Yuan left in your account")
case let .Error(errorMesssage):
    print("Error:\(errorMesssage)")
case .Waiting:
    print("Waiting for processing")
}
```
**4.** 有多个并联值的情况
``` swift
// Associate value其实只有一个，其实下面表示的是一个元组，并且为元组类型取了个名字
enum Shape {
    case Square(side: Double)
    case Rectangle(width: Double, height: Double)
    case Circle(centerx: Double, centery: Double, radius: Double)
    case Point
}

// 初始化一些图形
let square = Shape.Square(side: 10)
let rectangle = Shape.Rectangle(width: 20, height: 30)
let circle = Shape.Circle(centerx: 0, centery: 0, radius: 15)
let point = Shape.Point

// 计算表面积
func area(shape: Shape) -> Double {
    switch shape {
    case let .Square(side):
        return side * side
    case let .Rectangle(width, height):
        return width * height
    case let .Circle(_, _, r): // 通过下划线忽略不用的参数
        return .pi * r * r
    case .Point:
        return 0
    }
}

// 得出表面积的结果
area(shape: square)
area(shape: rectangle)
area(shape: circle)
area(shape: point)

// ====================================================================
// enum可以有方法
enum Shape{
    case Square(side: Double)
    case Rectangle(width: Double, height: Double)
    case Circle(centerx: Double, centery: Double, radius: Double)
    case Point

    func area() -> Double{

        switch self {
        case let .Square(side):
            return side*side
        case let .Rectangle( width , height ):
            return width * height
        case let .Circle( _ , _ , r ):
            //swift 2: return M_PI*r*r
            //swift3中PI放在了Double类下。这样是不是更方便记忆？
            return .pi*r*r      //swift 3
        case .Point:
            return 0
        }
    }
}

// 使用
let square = Shape.Square(side: 10)
square.area()

```
**5.** 可选型实际上是枚举类型
``` swift
var age: Int? = 17
print(age!)
age = nil
// 可以看到可选类型可以通过枚举的方式赋值
age = .some(2) // 2

var website: Optional<String> = Optional.some("blog.xujiaji.com")
website = .none // nil

// 以enum的角度来进行解包
switch website {
case .none:
    print("No website")
case let .some(website):
    print("The website is \(website)")
}

// 以Optional的方式解包
if let website = website {
    print("The website is \(website)")
}
else {
    print("No website")
}
```
**6.** 枚举的递归调用
``` swift
// 枚举递归，使用indirect关键字。也可以直接加在enum关键字后面（如：enum indirect ArithmeticExpression），此时case关键字前面就不必加了
enum ArithmeticExpression {
    case Number(Int)
    indirect case Addition(ArithmeticExpression, ArithmeticExpression)
    indirect case Multiplication(ArithmeticExpression, ArithmeticExpression)
}

// 计算 (5 + 4) * 2
let five = ArithmeticExpression.Number(5)
let four = ArithmeticExpression.Number(4)
let sum = ArithmeticExpression.Addition(five, four)
let two = ArithmeticExpression.Number(2)
let prouct = ArithmeticExpression.Multiplication(sum, two)

func evaluate(_ expression: ArithmeticExpression) -> Int {
    switch expression {
    case let .Number(value):
        return value
    case let .Addition(left, right):
        return evaluate(left) + evaluate(right)
    case let .Multiplication(left, right):
        return evaluate(left) * evaluate(right)
    }
}

// 计算结果
evaluate(prouct)
```
**7.** 枚举是值类型

## struct
**1.** 结构体的基本使用
``` swift

// 声明一个结构体
struct Location {
    let latitude: Double
    let longitude: Double
}

// 初始化结构体
let appleHeadQuarterLocation = Location(latitude: 37.3230, longitude: -122.0322)
let googleHeadQuarterLocation: Location = Location(latitude: 37.4220, longitude: -122.0841)

// 获取属性值
appleHeadQuarterLocation.latitude
googleHeadQuarterLocation.longitude

// 结构体中有结构体
struct Place {
    let location: Location
    var name: String
}

var googleHeadQuarter = Place(location: googleHeadQuarterLocation, name: "Google")
// 因为声明的是var，所以可修改
googleHeadQuarter.name = "G"
```
**2.** 结构体的初始化
结构体重定义的常量或变量都必须初始化。可选型可以不用初始化，因为默认初始值为`nil`，试了下可选型需要是var，如果是let，则必须直接赋值。
``` swift
struct Location {
    let latitude: Double
    let longitude: Double
    // 自定义构造， 当自己写了构造函数后就没有了默认的构造函数
    init(coordinateString: String) {
        let commaIndex = coordinateString.range(of: ",")!.lowerBound //得到逗号的下标
        let firstElement = coordinateString[..<commaIndex]
        let secondElement = coordinateString[coordinateString.index(after: commaIndex)...]
        latitude = Double(firstElement)!
        longitude = Double(secondElement)!
    }

    // 当没有默认的构造的时候，我们可以自己添加这个构造
    init(latitude: Double, longitude: Double) {
        self.latitude = latitude
        self.longitude = longitude
    }

    init() {
        latitude = 0.0
        longitude = 0.0
    }

    // 默认初始值为nil
    var placeName: String?

    init(latitude: Double, longitude: Double, placeName: String) {
        self.latitude = latitude
        self.longitude = longitude
        self.placeName = placeName
    }
}

let location = Location(coordinateString: "111.1234,222.3333")
location.latitude // 111.1234
location.placeName // nil
```
**3.** 失败的构造函数
 - 就是说构造函数可以是失败的，当我们`return nil`时候。也就是说我们初始化结构体的时候得到的是可选型
 - 用guard可以轻松简化if else嵌套的判断代码

``` swift
struct Location {
    let latitude: Double
    let longitude: Double

    init?(coordinateString: String) {
        guard let commaIndex = coordinateString.range(of: ",")?.lowerBound else {
            return nil
        }
        guard let firstElement = Double(coordinateString[..<commaIndex]) else {
            return nil
        }
        guard let secondElement = Double(coordinateString[coordinateString.index(after: commaIndex)...]) else {
            return nil
        }

        latitude = firstElement
        longitude = secondElement
    }
}
```
 - guard还可以将上面的代码优化

``` swift
struct Location {
    let latitude: Double
    let longitude: Double

    init?(coordinateString: String) {
        guard
            let commaIndex = coordinateString.range(of: ",")?.lowerBound,
            let firstElement = Double(coordinateString[..<commaIndex]),
            let secondElement = Double(coordinateString[coordinateString.index(after: commaIndex)...])
        else {
            return nil
        }
        latitude = firstElement
        longitude = secondElement
    }
}
```
**4.** 结构体中可定义方法， 这里直接在上面代码中添加方法
``` swift
struct Location {
    ...
    func printLocation() {
        print("The Location is \(self.latitude), \(self.longitude)")
    }

    func isNorth() -> Bool {
        return self.latitude > 0
    }

    func isSouth() -> Bool {
        return !self.isNorth()
    }

    func distanceTo(location: Location) -> Double {
        return sqrt(pow(self.latitude - location.latitude, 2) + pow(self.longitude - location.longitude, 2))
    }
}
```
**5.** 结构体是值类型的，就是当做值来出来，赋值即是拷贝
**6.** Int, Float, Double, Bool, String, Array, Dictionary, Set 等都是结构体

## class
**1.** 类的基本使用方式
类不像结构体一样，类不能自动初始化，因此我们需要自己为变量赋值
``` swift
class Person {
    var firstName: String
    var lastName: String

    init(firstName: String, lastName: String) {
        self.firstName = firstName
        self.lastName = lastName
    }

    // 类和结构体一样，也可以定义可以失败的构造
    init?(fullName: String) {
        guard let spaceIndex = fullName.range(of: " ")?.lowerBound else {
            return nil
        }
        firstName = String(fullName[..<spaceIndex])
        lastName = String(fullName[fullName.index(after: spaceIndex)...])
    }

    func fullName() -> String {
        return "\(self.firstName) \(self.lastName)"
    }
}

let person1 = Person(firstName: "Alexander", lastName: "Hamilton")
person1.fullName() // "Alexander Hamilton"

let person2 = Person(fullName: "Jiaji Xu")
person2?.firstName //"Jiaji"
```
**2.** 类是引用类型
``` swift
class Person {
    var name: String

    init(name: String) {
        self.name = name
    }
}

let person1 = Person(name: "Tom")
person1.name // Tom
let person2 = person1
person2.name = "Bob"
person2.name // Bob
person1.name // Bob
```
**3.** 方法的可变和不可变
 - 类的方法中可改变变量的值

``` swift
class Person {
    var name: String
    var career: String

    init(name: String, career: String) {
        self.name = name
        self.career = career
    }

    func change(career: String) {
        self.career = career
    }
}
let person = Person(name: "Bob", career: "Developer")
person.change(career: "Teacher")
```
 - 结构体由于是值传递，所以不可改变变量的值，像上面写会报错，提示immutable（不可变）。但是可以为方法加上关键字`mutating`，每次改变都会创建一个新的副本覆盖旧的值

``` swift
enum Switch{
    case On
    case Off

    mutating func click(){
        switch self{
        case .On:
            self = .Off
        case .Off:
            self = .On
        }
    }
}

var button = Switch.Off
button.click()

var button2 = Switch.On

button == button2
```
**4.** 类与类之间的等价，比较两个变量是否指向的同一个东西
``` swift
class Person {
    var name: String
    init(name: String) {
        self.name = name
    }
}

let person1 = Person(name: "Bob")
let person2 = person1

// 不能使用“==”判断：
// person1 == person2
person1 === person2 // true

let person3 = Person(name: "Bob")
person1 === person3 // false
person1 !== person3 // true
```
**5.** 什么时候用类什么时候用结构体
 - 把结构体看作是值
    - 位置 （经纬度）
    - 坐标 （二维，三维坐标）
    - 温度
    - ...
 - 把类看作是物体
    - 人
    - 车
    - 动物
    - ...
 - 如果不希望每次传递都创建一个新的副本，那么就用类，否则用结构体
 - 类可以被继承
 - 结构体比类更加“轻量级”

## 属性和方法
**1.** 计算型属性：自动更具其他信息计算出值
``` swift
struct Point {
    var x = 0.0
    var y = 0.0
}

struct Size {
    var width = 0.0
    var height = 0.0
}

class Rectangle {
    var origin: Point
    var size: Size

    init(origin: Point, size: Size) {
        self.origin = origin
        self.size = size
    }

    // 写法一
//    var center: Point {
//        let centerX = origin.x + size.width / 2
//        let centerY = origin.y + size.height / 2
//        return Point(x: centerX, y: centerY)
//    }

    // 写法二
//    var center: Point {
//        get {
//            let centerX = origin.x + size.width / 2
//            let centerY = origin.y + size.height / 2
//            return Point(x: centerX, y: centerY)
//        }
//    }

    // 写法三：上面的写法是只读的，无法为center赋值。如果要赋值，则需要些setter
    var center: Point{

        get{
            let centerX = origin.x + size.width/2
            let centerY = origin.y + size.height/2
            return Point(x: centerX, y: centerY)
        }

        // (newCenter)可以被省略
        // 在setter的{}中用默认名称newValue代替传入值
        set(newCenter){
            origin.x = newCenter.x - size.width/2
            origin.y = newCenter.y - size.height/2
        }
    }
}

var rect = Rectangle(origin: Point(), size: Size(width: 10, height: 5))
rect.center

// 写法三可为center赋值，并且会自动改变坐标
rect.center = Point(x: 10, y: 10)
rect
```
**2.** 类型属性（Type Property），静态变量
就和java中的静态变量差不多，写法也一样，不过必须通过类型名获取
``` swift
class Player {
    // 定义类型属性，不能通过self.来引用，类中也不可直接引用
    // 不论创建多少个实例，都只存在一个该变量
    static var highestScore = 0
}
```
**3.** 类型方法（Type Method），静态方法，这里举了一个创建单位矩阵的类型方法
``` swift

struct Matrix {
    var m: [[Int]]
    var row: Int
    var col: Int

    init?(_ arr2d: [[Int]]) {
        guard arr2d.count > 0 else {
            return nil
        }

        let row = arr2d.count
        let col = arr2d[0].count
        for i in 1..<row {
            if arr2d[i].count != row {
                return nil
            }
        }

        self.m = arr2d
        self.row = row
        self.col = col
    }

    static func identityMatrix(n: Int) -> Matrix? {
        if n < 0 {
            return nil
        }
        var arr2d: [[Int]] = []
        for i in 0..<n {
            var row = [Int](repeating: 0, count: n)
            row[i] = 1
            arr2d.append(row)
        }
        return Matrix(arr2d)
    }

    func printMatrix() {
        for i in 0..<row {
            for j in 0..<col {
                print(m[i][j], terminator: "\t")
            }
            print()
        }
    }
}

let m = Matrix([[1, 2], [3, 4]])
m?.printMatrix()

// 直接通过类型名直接调用
let e = Matrix.identityMatrix(n: 6)
e?.printMatrix()

//输出
//1    2
//3    4
//1    0    0    0    0    0
//0    1    0    0    0    0
//0    0    1    0    0    0
//0    0    0    1    0    0
//0    0    0    0    1    0
//0    0    0    0    0    1
```
**4.** 属性观察器
 - 注意willSet和didSet不会在变量直接初始化和构造方法中被调用
 - 一个电灯的案例

```
class LightBulb {
    static let maxCurrent = 30
    var current = 0 {
        // 可以不声明变量名newCurrent，可直接使用newValue
        // 如其名，此时是在设置新值之前被调用
        willSet(newCurrent) {
            // 此时， current还是以前的值
            print("|\(current)-\(newCurrent)| = \(abs(current - newCurrent))")
        }

        // Property observer 可以用来限制值或格式
        // 也可以用来并联逻辑
        // 可以不声明变量oldCurrent，可直接使用oldValue获取原来的值
        // 如其名，此时是已经设置好新的值后被调用
        didSet(oldCurrent) {
            if current == LightBulb.maxCurrent {
                print("Pay attention, the current value get to the maxinum point.")
            }
            else if current > LightBulb.maxCurrent{
                print("Current too high, falling back to previous setting.")
                current = oldCurrent
            }
            print("The current is \(current)")
        }
    }
}

let bulb = LightBulb()
bulb.current = 20
bulb.current = 30
bulb.current = 40

//结果
//|0-20| = 20
//The current is 20
//|20-30| = 10
//Pay attention, the current value get to the maxinum point.
//The current is 30
//|30-40| = 10
//Current too high, falling back to previous setting.
//The current is 30
```
 - 一个主题切换的案例

``` swift
enum Theme {
    case DayMode
    case NightMode
}

class UI {
    var fontColor: UIColor!
    var backgroundColor: UIColor!
    var themeMode: Theme = .DayMode {
        // 每当改变了主题的时候，就去改变对应的配色
        didSet {
            self.changeMode(themeMode)
        }
    }

    init() {
        self.themeMode = .DayMode
        self.changeMode(themeMode)
    }

    // 由于多处用到于是提取出来
    func changeMode(_ newMode: Theme) {
        switch newMode {
        case .DayMode:
            fontColor = UIColor.black
            backgroundColor = UIColor.white
        case .NightMode:
            fontColor = UIColor.white
            backgroundColor = UIColor.black
        }
    }
}

let ui = UI()
ui.themeMode
ui.fontColor //  黑
ui.backgroundColor // 白

ui.themeMode = .NightMode
ui.fontColor // 白
ui.backgroundColor // 黑
```
**5.** 延迟属性（Lazy Property）
``` swift
class ClosedRange {
    let start: Int
    let end: Int

    // 每次调用都会重新计算
    var width: Int {
        return end - start + 1
    }

    // 使用懒加载，只有第一次调用是才会计算，解决资源重复计算或读取等问题
    lazy var sum: Int = {
        var res = 0
        for i in self.start...self.end {
            res += i
        }
        return res
    }()

    init?(start: Int, end: Int) {
        if start > end {
            return nil
        }
        self.start = start
        self.end = end
    }
}

if let range = ClosedRange(start: 0, end: 10_000) {
    range.width
    range.sum
    range.sum
    range.sum
}
```
**6.** 访问控制
 - `private` 私有访问控制，标识了的变量和方法只能在同一个文件中才能访问
 - `internal` 默认访问控制，同一个目录下可访问
 - `public` 公有访问控制，标识后任何地方都可访问

**7.** 单例模式
``` swift
// Sources文件夹中 GameManager.swift
public class GameManager {
    public static let defaultManager = GameManager()
    public var score = 0
    public var level = 0

    private init() {

    }

    public func addScore() {
        score += 10
    }
}


// 主文件中
let gameManager = GameManager.defaultManager
gameManager.addScore()
gameManager.score // 10

let gm = GameManager.defaultManager
gm.addScore()
gm.score // 20
```

## 继承和构造函数
**1.** 继承基本使用方式
继承某个类使用冒号":"跟上继承的类
继承可以使用父类中非私有的属性（不在一个文件的情况下）
`final`关键字可以让该类不再有子类
``` swift
class Avatar {
    var name: String
    var life = 100 // 血条
    var isAlive: Bool = true // 是否存活

    init(name: String) {
        self.name = name
    }

    // 被攻击时调用
    func beAttacked(attack: Int) {
        life -= attack
        if life <= 0 {
            isAlive = false
        }
    }
}

// 继承
class User: Avatar {
    var leve = 0
}

let player = User(name: "Jiaji")
player.name
player.life
player.beAttacked(attack: 20)
player.life

// 使用final，表示最终的类，阻止进一步的继承
final class Magician: User {
    var magic = 100
}
```
**2.** 多态
``` swift
// 简化大量代码

class Avatar {
    var name: String
    init(name: String) {
        self.name = name
    }
}

class User: Avatar {}

final class Magician: User {}

class Monster: Avatar {}

// 多态
func printName(avatar: Avatar) {
    print("name is \(avatar.name)")
}

let user = User(name: "Bob")
let user2 = Magician(name: "Tom")
let mons = Monster(name: "no1")

// 只要都是继承Avatar那么就可以传入这个方法， 不在乎具体的类
printName(avatar: user)
printName(avatar: user2)
printName(avatar: mons)

//结果
//name is Bob
//name is Tom
//name is no1
```
**3.** 重载， 通过关键字`override`即可复写父类中的成员
私有成员无法覆写；
final成员无法覆写；
``` swift

class SuperClass {
    var description: String {
        return "This is SuperClass"
    }

    func fun1() {
        print("SuperClass fun1()")
    }

    // 标记了final后，无法被子类覆写
    final func fun2() {
        print("SuperClass fun2()")
    }
}

class SubClass: SuperClass {
    override var description: String {
        return "This is SubClass"
    }
    override func fun1() {
        print("SubClass fun1()")
    }
}

let claz = SuperClass()
let claz2 = SubClass()
let arr: [SuperClass] = [claz, claz2]

for c in arr {
    print(c.description)
    c.fun1()
    c.fun2()
}

//结果
//This is SuperClass
//SuperClass fun1()
//SuperClass fun2()
//This is SubClass
//SubClass fun1()
//SuperClass fun2()
```
**4.** 子类构造中调用父类构造
 - 必须将子类初始化完成，才能调用父类构造初始化父类
 - 通过`super.init`调用父类构造

**5.** 两段式构造
 - 第一段：构造初值
    - 在所有变量没有初始化完成之前，不能调用其他方法
    - 父类的成员变量，即使有初始值，也不能使用
    - 可以涉及逻辑，但逻辑不能涉及到self
    - 静态的可以使用
 - 调用super构造(如果需要的话)
 - 第二段：所有成员变量初始化完成以后，进行成员变量相关的逻辑调整

**6.** 方便的构造函数和指定的构造函数
一般的构造就是指定的构造函数；
加了convenience的构造就是方便的构造函数，方便的构造函数只能self调用该类的指定构造函数；
``` swift
class Avatar {
    var name: String
    // 这种叫做指定构造函数
    init(name: String) {
        self.name = name
    }
}

class User: Avatar {
    // 这种叫做指定构造函数
    override init(name: String) {
        super.init(name: name)
    }

    // 这种叫做方便的构造函数，convenience直接翻译过来就是：方便
    // 方便的构造函数只能调用该类自身的构造函数，不能调用super的
    // 要调用该类自身的构造，必须加上convenience
    convenience init(firstName: String, lastName: String) {
        self.init(name: "\(firstName) \(lastName)")
    }
}
```
**7.** 子类构造函数的继承
如果子类没有实现任何父类的指定构造函数，则自动继承父类的所有指定构造函数；
如果子类实现了父类所有的指定构造函数，则自动继承父类的所有便利构造函数；
``` swift
class Avatar {
    var name: String

    init(name: String) {
        self.name = name
    }

//    init(num: Int) {
//        self.name = String(num)
//    }

    convenience init(firstName: String, lastName: String) {
        self.init(name: "\(firstName) \(lastName)")
    }
}

//实现了父类所有指定构造的情况下，如果想看没有实现完的情况，将Avatar注释的代码放开
class User: Avatar {
    var group: String

    init(name: String, group: String) {
        self.group = group
        super.init(name: name)
    }

    convenience init(group: String) {
        let name = User.generateUserName()
        self.init(name: name, group: group)
    }

    convenience override init(name: String) {
        self.init(name: name, group: "")
    }

    static func generateUserName() -> String{
        return "Player" + String(Int(arc4random()%1_000_000))
    }
}

// 没有实现任何指定构造的情况
class Monster: Avatar {
    // 子类没有实现任何父类构造的情况,自动继承父类的所有指定构造函数
    // 可直接用self调用，相当于Monster已经有了init(name: type)
    convenience init(type: String){
        self.init(name: type)
    }

}

//如果将Avatar中的init(num: Int)的构造的注释解开该句实例化将会报错，因为放开后，子类User并没有实现父类的init(num: Int)
let user = User(firstName: "John", lastName: "Snow")

// 可以通过三种方式实例化，其中第二种继承自父类，第三种父类的方便构造能直接使用
let zombie = Monster(type: "Zombie")
let zombie2 = Monster(name: "Zombie")
let zombie3 = Monster(firstName: "Mr.", lastName: "Zombie")
```
**8.** required构造
```
class Avatar {
    var name: String
    // 表示子类必须实现该构造方法
    required init(name: String) {
        self.name = name
    }

    init(num: Int) {
        self.name = String(num)
    }
}

// 如果没有实现任何父类指定构造，那么默认会实现所有父类指定构造
class NPC:Avatar {

}

class User: Avatar {
    override init(num: Int) {
        super.init(num: num)
    }

    // 如果重写了一个父类构造（如上面的构造），那么必须实现父类强制要实现的构造
    required init(name: String) {
        super.init(name: name)
    }
}
```
**9.** 结构体中的构造
由于结构体中没有继承的关系，所以不用申明是方便的构造表示要调用自己的构造。
``` swift
struct TestInit {
    init(a: Int) {}
    init(b: Int, c: Int) {
        self.init(a: b + c) // 直接self调用就行了
    }
}
```

## 文档注释
**1.** 多行文档注释
```
/**
多行文档注释
多行文档注释
*/
```
**2.** 单行文档注释，多个单行合在一起和多行效果一样
```
/// 单行文档注释
```
**3.** 使用的是Markdown格式书写
**4.** 参数注释1
```
/// - Parameter item1: This is item1
/// - Parameter item2: This is item2
func show2(item1: String, item2: String) {}
```
**5.** 参数注释2
```
/// - Parameters:
///   - item1: This is item1
///   - item2: This is item2
func show2(item1: String, item2: String) {}
```
**6.** 返回信息、异常信息注释
```
/// - Returns: the result String.
/// - Throws: nil error
func show1() throws -> String {
    return ""
}
```
**7.** 一些对于算法或其他用途的一些关键字
```
/// 对于算法或其他用途的一些关键字 `Precondition`, `Postcondition`, `Requires`, `Invariant`, `Complexity`, `Important` and `Warning`.
///
/// 假设这是一个算法
///
/// - Precondition: 前置条件
/// - Postcondition: 后置条件
/// - Requires: 算法所需要的内容
/// - Invariant: 循环不变量
/// - Complexity: 复杂度
/// - Important: 一些重要的信息
/// - Warning: 一些警告信息
/// - Attention: 一些警告信息
/// - Note: 一些相应的记录
/// - Remark: 一些评论
///
/// - Parameter object: The algorithm will use this single object to change the world.
/// - Throws: `MyError.JustImpossible` if the algorithm's precondition can not be satisfied.
/// - Returns: the object contains all the information in the universe.
func mysteriousAlgorithm(object: AnyObject) {
    return
}
```
**8.** 一些元信息
```
/// - Author: 作者
/// - Author: 几个人一起完成...
/// - Copyright: 版权信息
/// - Date: 时间
/// - Since: 项目起始日期
/// - Version: 对应的版本号
func show() {

}
```
**9.** MARK
 - 分割类视图

```
// MARK: -
```
 - 添加分割类视图并添加该区域标题

```
// MARK: - Methods
```
**10.** TODO
在类视图中建立任务提醒
```
// TODO: 以后在这里要干嘛干嘛
```
**11.** FIXME
需要修复，但占时无关紧要，在类视图中会有提醒
```
// FIXME: Support Swift 2.2
```

## 下标
**1.** 基本使用方式
可以自己定义下标的类型，如同数组和字典一样访问方式；
需要关键字`subscript`；
``` swift
struct Vector3 {
    var x: Double = 0.0
    var y: Double = 0.0
    var z: Double = 0.0

    // 参数类型可以随意指定
    // 需要有个返回值
    // 如果需要通过下标来设置值，则需要添加set
    subscript(index: Int) -> Double? {
        get {
            switch index {
            case 0: return x
            case 1: return y
            case 2: return z
            default: return nil
            }
        }

        set {
            guard let newValue = newValue else { return }

            switch index {
            case 0: x = newValue
            case 1: y = newValue
            case 2: z = newValue
            default: return
            }
        }
    }

    subscript(axis: String) -> Double? {
        switch axis {
        case "x", "X": return x
        case "y", "Y": return y
        case "z", "Z": return z
        default: return nil
        }
    }
}


var v = Vector3(x: 1.0, y: 2.0, z: 3.0)
v[0] // 1
// 添加了set才能设置值
v[0] = 100.0 // 100
v["x"] // 100
```
**2.** 多维下标
可定义多个下标；
``` swift
struct Matrix {
    var data: [[Double]]
    let r: Int
    let c: Int

    init(row: Int, col: Int) {
        self.r = row
        self.c = col
        self.data = [[Double]]()
        for _ in 0..<r {
            let aRow = Array(repeating: 0.0, count: col)
            data.append(aRow)
        }
    }

    // 返回确切有值
    subscript(x: Int, y: Int) -> Double {
        get{
            assert( x >= 0 && x < r && y >= 0 && y < c , "Index Out of Range")
            return data[x][y]
        }

        set{
            assert( x >= 0 && x < r && y >= 0 && y < c , "Index Out of Range")
            data[x][y] = newValue
        }
    }

    // 如果想使用 m[1][1]
    subscript(row: Int) -> [Double]{

        get{
            assert( row >= 0 && row < r , "Index Out of Range")
            return data[row]
        }

        set(vector){
            assert( vector.count == c , "Column Number does NOT match")
            data[row] = vector
        }
    }
}

var m = Matrix(row: 2, col: 2)
//m[2,2]
m[1,1] = 1


// 如果想使用 m[1][1]
m[1][1]
m[1]

m[0] = [1.5,4.5]
```

## 运算符重载
运算符本身就是一个函数
**1.** 重载运算符基本操作
``` swift
// 重载运算符
func + (left: Vector3, right: Vector3) -> Vector3 {
    return Vector3(x: left.x + right.x, y: left.y + right.y, z: left.z + right.z)
}

// 重载单目运算符，prefix表示 - 是一个前置运算符，相对应的是postfix
prefix func - (v: Vector3) -> Vector3 {
    return Vector3(x: -v.x, y: -v.y, z: -v.z)
}

// 重载 += 这种运算
static func += (left: inout Vector3, right: Vector3) {
    left = left + right
}

let va = Vector3(x: 1.0, y: 2.0, z: 3.0)
let vb = Vector3(x: 3.0, y: 4.0, z: 5.0)

let vc = vb + va
vc.x
```
**2.** 重载比较运算符
``` swift
// 重载比较运算符
func == (left: Vector3, right: Vector3) -> Bool {
    return left.x == right.x && left.y == right.y && left.z == right.z
}

func != (left: Vector3, right: Vector3) -> Bool {
    return !(left == right)
}

let va = Vector3(x: 1.0, y: 2.0, z: 3.0)
let vb = Vector3(x: 3.0, y: 4.0, z: 5.0)

va == vb
va != vb
```
**3.** 自定义运算符
如果是ASCII字符，只能是：`/ = - + ! * % < > & | ^ ~`之开头 。或者是Unicode的字符
``` swift
struct Vector3 {
    var x: Double = 0.0
    var y: Double = 0.0
    var z: Double = 0.0

    func length() -> Double {
        return sqrt(x*x + y*y + z*z)
    }
}

func + (left: Vector3, right: Vector3) -> Vector3{
    return Vector3(x: left.x + right.x, y: left.y + right.y, z: left.z + right.z)
}

func * (left: Vector3, right: Vector3) -> Double{
    return left.x * right.x + left.y * right.y + left.z * right.z
}

func += (left: inout Vector3, right: inout Vector3){
    left = left + right
}

// 单目运算符的定义
postfix operator +++
postfix func +++ (vector: inout Vector3) -> Vector3 {
    var addOn = Vector3(x: 1.0, y: 1.0, z: 1.0)
    vector += addOn
    return vector
}

prefix operator +++
prefix func +++ (vector: inout Vector3) -> Vector3 {
    let res = vector
    var addOn = Vector3(x: 1.0, y: 1.0, z: 1.0)
    vector += addOn
    return res
}


// 双目运算符的定义
// 计算两个向量的夹角
infix operator ^
func ^ (left: Vector3, right: Vector3) -> Double {
    return acos((left * right) / (left.length() * right.length()))
}

//计算阶层，定义优先组
precedencegroup ExponentPrecedence{
    // 是从左向右计算还是从右向左计算
    associativity: left
    // 定义优先级，用lowerThan或higherThan来定义
    higherThan: MultiplicationPrecedence
}
infix operator **: ExponentPrecedence
func **(x: Double, p: Double) -> Double {
    return pow(x, p)
}

1+2**3**2 // 65

var va = Vector3(x: 1.0, y: 2.0, z: 3.0)
var vb = Vector3(x: 3.0, y: 4.0, z: 5.0)
va+++

+++vb

va ^ vb
```

## Extension
**1.** 基本使用方式
扩展；
扩展属性时，只能扩展计算型属性；
只能创建方便的构造函数`convenience`；
``` swift
class Test {
    var value: String
    init(value: String) {
        self.value = value
    }
}
// 扩展用方法上时
extension Test {
    func beautifulValue() -> String {
        return "beautiful " + self.value
    }
}

let test = Test(value: "girl")
test.beautifulValue() //"beautiful girl"

// 扩展用变量上时，必须是计算型变量
extension Test {
    var len: Int {
        return self.value.count
    }
}

test.len // 4

// 扩展用构造时，必须是方便构造
extension Test {
    convenience init (firstName: String, lastName: String) {
        self.init(value: "\(firstName) \(lastName)")
    }
}


let test2 = Test(firstName: "Jiaji", lastName: "Xu")
```
**2.** 嵌套类型
如果某类型只有在一个类型里面起作用，那么可以将该类型放到里面，如String的Index类型；
扩展，可扩展嵌套类型；
扩展可扩展下标；
``` swift
class Rectangle {
    var origin: (x: Double, y: Double)
    var width: Double
    var height: Double
    init(origin: (Double, Double), width: Double, height: Double) {
        self.origin = origin
        self.width = width
        self.height = height
    }

}

extension Rectangle {
    enum Vertex: Int {
        case LeftTop, RightTop, RightBottom, LeftBottom
    }

    subscript(index: Int) -> (Double, Double) {
        assert(index >= 0 && index < 4, "Index in Rectange Out of Range.")
        switch Vertex(rawValue: index)! {
        case .LeftTop:
            return origin
        case .RightTop:
            return (x: origin.x + width, y: origin.y)
        case .RightBottom:
            return (x: origin.x + width, y: origin.y + height )
        case .LeftBottom:
            return (x: origin.x, y: origin.y + height )
        }
    }
}

let rect = Rectangle(origin: (0.0, 0.0), width: 4, height: 3)
rect[0]
rect[1]
```
**3.** 扩展标准库
// Int还有很多可以做enxtension的地方
// 如 12345[2]
// 如 toBinary, toHex
// 如 isPrime
// extension在App开发中被经常使用
// 如 String, UIColor等基础类的使用
// 在App开发中, 一个界面可能需要处理多个事件: 表格显示, 用户输入, 导航, 动画, 数据存储...
// 此时可以使用extension分隔开;
``` swift
extension Int {
    var square: Int {
        return self * self
    }

    var cube: Int {
        return self * self * self
    }

    func inRange(start: Int, to: Int) -> Bool {
        return self >= start && self < to
    }

    func repetitions(task: (Int) -> Void) {
        for _ in 0..<self {
            task(self)
        }
    }
}

let num = 8
num.square
num.cube

num.inRange(start: 0, to: 10)

num.repetitions { index in
    print("hello \(index)")
}

// 输出
//hello 8
//hello 8
//hello 8
//hello 8
//hello 8
//hello 8
//hello 8
//hello 8
```
## Generic
泛型： 只关心具体操作，不关心具体类型
**1.** 用在方法上
``` swift
func swapTwoThings<T>(a: inout T, b: inout T) {
    (a, b) = (b, a)
}

var hello = "Hello"
var bye = "Bye"
swapTwoThings(a: &hello, b: &bye)
hello // "Bye"
bye // "Hello"
```
**2.** 用在类型上
``` swift
struct Stack<T> {
    var items = [T]()

    func  isEmpty() -> Bool {
        return items.count == 0
    }

    mutating func push(_ item: T) {
        items.append(item)
    }

    mutating func pop() -> T? {
        guard !self.isEmpty() else {
            return nil
        }
        return items.removeLast()
    }
}

extension Stack {
    func top() -> T? {
        return items.last
    }

    func count() -> Int {
        return items.count
    }
}

var s = Stack<Int>()
s.push(1)
s.push(2)
s.pop()
```

## protocol
**1.** 协议的基本使用
协议；
只定义，不实现；
不能为协议设置默认的参数值，变量也不能有默认值；
变量只能用var
``` swift
// protocol Pet: class {} 表示如果协议继承class，则该协议不能应用于结构体
protocol Pet {
    // 不能右初始值
    var name: String { get set }
    // 统一使用var关键字
    var birthPlace: String { get }

    // 对于方法，不能有实现
    func playWith()

    //对于方法，不能有默认参数（默认参数就是一种实现）
    // func fed(food: String = "leftover")

    func fed()
    func fed(food: String)

    // 可以使用mutating关键字，强调在结构体重应该修改其中内容
    mutating func changeName(newName: String)
}

// 协议可继承
protocol PetBird: Pet {
    var flySpeed: Double{ get }
    var flyHeight: Double{ get }
}

struct Dog: Pet {
    // 可以使用计算型属性
    //    private var myDoggyName = "Puppy"
    //    var name: String{
    //        get{
    //            return myDoggyName
    //        }
    //        set{
    //            myDoggyName = newValue
    //        }
    //    }
    var name: String

    // 协议中定义的只读，对于一个具体类的实现，不一定是只读，但是作为Pet时是只读的！
    // let birthPlace: String
    var birthPlace: String

    func playWith() {
        print("Wong!")
    }

    func fed() {
        print("I want a bone.")
    }

    // 在具体实现上可以加默认参数
    func fed(food: String = "Bone") {

    }

    mutating func changeName(newName: String) {
        name = newName
    }
}

var myDog: Dog = Dog(name: "summer", birthPlace: "beijing")
myDog.birthPlace = "beijing"
var aPet: Pet = myDog
// 当作为Pet来操作的时候，是无法为birthPlace赋值的
// aPet.birthPlace = "shanghai"
```
**2.** 协议和构造函数
``` swift
protocol Pet {
    var name: String { get set }
    init(name: String)
}

class Animal {
    var type: String = "mammal"
}

// 如果一个类有继承的类，则类必须放在前面
// 父类只能有一个， 协议可以有多个
class Dog: Animal, Pet {
    var name: String = "Pup"

    // 如果protocol有init， 则在class中必须声明required，强制让子类实现
    required init(name: String) {
        self.name = name
    }
}

final class Cat: Animal, Pet {
    var name: String

    // 如果是final class，init可以没有required，因为它不再会被继承
    init(name: String) {
        self.name = name
    }
}

class Bird: Animal {
    var name: String = "bird ..."
    init(name: String) {
        // 省略...
    }
}

class Parrot: Bird {
    // 如果只继承Bird，则只需要加override或Bird init是required，那么只需要required
    // 因为有Pet， 则required也不能省略
    required override init(name: String) {
        super.init(name: name + " " + name)
    }
}
```
**3.** 为什么使用协议
协议描述的是某种特性；
如下面的例子，通过协议，我们可以将继承自不同父类不同类型的东西，由于某种一样的特性，我们可以依这特性把它们归为一类。
``` swift
protocol Pet {
    var name: String { get set }
}

protocol Flyable {
    var flySpeed: Double { get }
    var flyHeight: Double { get }
}

class Animal {}

class Dog: Animal, Pet {
    var name: String = "Puppy"
}

class Cat: Animal, Pet {
    var name: String = "Kitten"
}

class Bird: Animal, Flyable {
    var flySpeed: Double
    var flyHeight: Double

    init(flySpeed: Double, flyHeight: Double) {
        self.flySpeed = flySpeed
        self.flyHeight = flyHeight
    }
}

class Parrot: Bird, Pet {
    var name: String
    init(name: String, flySpeed: Double, flyHeight: Double) {
        self.name = name + " " + name
        super.init(flySpeed: flySpeed, flyHeight: flyHeight)
    }
}

class Sparrow: Bird {
    var color = UIColor.gray
}

class Vehicle {

}

class Plane: Vehicle, Flyable {
    var model: String
    var flySpeed: Double
    var flyHeight: Double
    init(model: String, flySpeed: Double, flyHeight: Double) {
        self.model = model
        self.flyHeight = flyHeight
        self.flySpeed = flySpeed
    }
}

var dog = Dog()
var cat = Cat()
var parrot = Parrot(name: "hi", flySpeed: 10.0, flyHeight: 100.0)

let pets: [Pet] = [dog, cat, parrot]

var sparrow = Sparrow(flySpeed: 15.0, flyHeight: 80.0)
var plane = Plane(model: "Boeing 747", flySpeed: 200.0, flyHeight: 10_000)

let flyers: [Flyable] = [parrot, sparrow, plane]
for flyer in flyers {
    print("Fly speed: \(flyer.flySpeed), Fly Height: \(flyer.flyHeight)")
}
```
**3.** 类型别名(typealias)
``` swift
typealias Length = Double

extension Double {
    var m: Length { return self }
    var cm: Length { return self * 100.0 }
    var km: Length { return self / 1000.0 }
    var ft: Length { return self / 3.28084 }
}

let runningDistance: Length = 3.54.km
runningDistance

// 使用的时候直接使用AudioSample，如果需要改为UInt32或其它时直接改这里，而不必每个地方都去改
typealias AudioSample = UInt64
```
**4.** 并联类型(associatedtype)，在协议中使用别名
``` swift
protocol WeightCalculable {
    // 协议中声明实现类需要使用别名，用associatedtype
    associatedtype WeightType
    var weight: WeightType { get }
}

// 在具体实现类中，用typealias
class iPhone7: WeightCalculable {
    typealias WeightType = Double
    var weight: WeightType {
        return 0.114
    }
}

class Ship: WeightCalculable {
    typealias WeightType = Int
    var weight: WeightType
    init(weight: WeightType) {
        self.weight = weight
    }
}

extension Int {
    typealias Weight = Int
    var t: Weight { return 1_000 * self }
}

let titanic = Ship(weight: 46_328_000)
```
**5.** Swfit标准库中的常用协议
``` swift
struct Record: Equatable, Comparable, CustomStringConvertible {
    var wins: Int
    var losses: Int

    // 协议CustomStringConvertible中的定义，可直接被print打印
    var description: String {
        return "WINS: \(wins), LOSSES: \(losses)"
    }

    var boolValue: Bool {
        return wins > losses
    }
}
// 协议Equatable的作用，我们只需要实现==，我们就可以用!=
func ==(left: Record, right: Record) -> Bool {
    return left.wins == right.wins && left.losses == right.losses
}
// 协议Comparable的作用，当我们定义了<，上面右定义了==，此时我们可以使用<=,>,>=
func <(left: Record, right: Record) -> Bool {
    if left.wins != right.wins {
        return left.wins < right.wins
    }
    return left.losses > right.losses
}

let record = Record(wins: 10, losses: 5)
let record2 = Record(wins: 11, losses: 5)
record >= record2
print(record) //WINS: 10, LOSSES: 5


var records = [Record(wins: 10, losses: 3), Record(wins: 8, losses: 5), Record(wins: 8, losses: 8)]
// 当我们实现了Comparable，可直接排序
records.sort()
```

## 面向协议编程
**1.** 扩展协议和默认实现
``` swift
protocol Record: CustomStringConvertible {
    var wins: Int { get }
    var losses: Int { get }

    func winningPercent() -> Double
}

// 扩展一个协议的时候，可以对协议进行实现
extension Record {
    // 实现CustomStringConvertible协议中的description，实现Record的就可以不用实现这个
    var description: String {
        return "WINS: \(wins), LOSSES: \(losses)"
    }

    // 扩展协议中还可以写其他方法的实现
    func shoutWins() {
        print("WE WIN", wins, "TIMES!!!")
    }

    // 扩展中还可以对定义的变量进行计算，计算的是对应实现类中值
    var gamePlayed: Int {
        return wins + losses
    }
}

struct BaseballRecord: Record {
    var wins: Int
    var losses: Int

    func winningPercent() -> Double {
        return Double(wins) / Double(gamePlayed)
    }
}

let teamRecord = BaseballRecord(wins: 2, losses: 10)
print(teamRecord)
teamRecord.shoutWins()

// 扩展标准库中的协议
extension CustomStringConvertible {
    var descriptionWithDate: String {
        return NSData().description + " " + description
    }
}

print(teamRecord.descriptionWithDate)

// 输出
// WINS: 2, LOSSES: 10
// WE WIN 2 TIMES!!!
// <> WINS: 2, LOSSES: 10
```
**2.** 根据条件扩展协议
``` swift
protocol Record {
    var wins: Int {get}
    var losses: Int {get}
}
extension Record {
    var gamePlayed: Int {
        return wins + losses
    }
    func winningPercent() -> Double {
        return Double(wins) / Double(gamePlayed)
    }
}
protocol Tieable {
    var ties: Int {get set}
}
// 该扩展表示：实现该协议的实例又实现了Tieable协议会进入这个扩展
// 由于实现了Tieable扩展后的实体需要改变一些计算方式
extension Record where Self: Tieable {
    var gamePlayed: Int {
        return wins + losses + ties
    }

    // 如果不写覆写这个方法，实例会调用上面扩展中的方法，并调用上面扩展中的gamePlayed，会导致计算结果不对
    func winningPercent() -> Double {
        return Double(wins) / Double(gamePlayed) // gamePlayed = wins + losses + ties
    }
}
struct FootballRecord: Record, Tieable {
    var wins: Int
    var losses: Int
    var ties: Int
}

let footballTeam = FootballRecord(wins: 1, losses: 1, ties: 1)
footballTeam.gamePlayed
footballTeam.winningPercent()
```
**3.** 协议聚合
在方法的参数中聚合多个协议为传入条件
``` swift
protocol Prizable {
    func isPrizable() -> Bool
}

// 该方法表示实例必须同时实现了CustomStringConvertible和Prizable两个协议才能传入
func award(one: CustomStringConvertible & Prizable){

    if one.isPrizable(){
        print(one)
        print("Congratulation! You won a prize!")
    }
    else{
        print(one)
        print("You can not have the prize!")
    }
}

struct Student: CustomStringConvertible, Prizable {
    var score: Int

    init(score: Int) {
        self.score = score
    }

    var description: String {
        return "score = \(score)"
    }

    func isPrizable() -> Bool {
        return score > 60
    }
}

award(one: Student(score: 80))
```
**4.** 泛型约束
``` swift
// 传入数组，找出最大值
func topOne<T: Comparable>(seq:[T]) -> T {
    assert(seq.count > 0)
    return seq.reduce(seq[0]) { max($0, $1) }
}

topOne(seq: [1, 4, 7, 2, 3])
```
**5.** 创建自己的委托模式
``` swift
protocol TurnBaseGameDelegate {
    func gameStart()
    func playMove()
    func gameEnd()
    func gameOver() -> Bool
}

// 回合制游戏
protocol TurnBasedGame {
    var turn: Int { get set }
    func play()
}

// 实现了游戏的逻辑，但是具体是什么游戏不知道，委托出去别人实现
class SinglePlayerTurnBasedGame: TurnBasedGame {
    var delegate: TurnBaseGameDelegate!
    var turn = 0
    func play() {
        delegate.gameStart()
        while !delegate.gameOver() {
            print("ROUND", turn, ":")
            delegate.playMove()
            turn += 1
        }
        delegate.gameEnd()
    }
}

// 实现了委托的协议
// 掷骰子游戏
class RollNumberGame: SinglePlayerTurnBasedGame, TurnBaseGameDelegate {
    var score = 0

    override init() {
        super.init()
        delegate = self
    }

    func gameStart() {
        score = 0
        turn = 0
        print("Welcome to Roll Number Game.")
        print("Try to use least turn to make total 100 scores!")
    }

    func playMove() {
        let rollNumber = Int(arc4random() % 6) + 1
        score += rollNumber
        print("You rolled a", rollNumber, "! The score is", score, "now!")
    }

    func gameEnd() {
        print("Congratulation! You win the game in", turn, "ROUND!")
    }

    func gameOver() -> Bool {
        return score >= 30
    }
}

let rollingNumber = RollNumberGame()
rollingNumber.play()
```
**6.** 可选的协议方法
可选方法需要用@objc标记，实现的实体可实现，可不实现，用的时候当做可选类型来用
``` swift
@objc protocol TurnBaseGameDelegate {
    func gameStart()
    func playMove()
    func gameEnd()
    func gameOver() -> Bool

    @objc optional func turnStart()
    @objc optional func turnEnd()
}
```

## 错误处理
**1.** 强制退出程序
``` swift
assert(1<0, "Error msg") // 只在测试阶段才有效
// 输出：
// Assertion failed: Error msg: file LearnError.playground, line 5

//===========================================
assertionFailure()
//输出：
//Fatal error: file LearnError.playground, line 7

//===========================================
assertionFailure("Error msg")
//输出：
//Fatal error: Error msg: file LearnError.playground, line 7

//===========================================
precondition(1>0) // 满足条件也会退出
precondition(1>0, "Error")

fatalError("Error") // 严重的错误
```
**2.** 错误处理
``` swift
class VendingMachine {
    struct Item {
        enum ItemType: String {
            case Water
            case Cola
            case Juice
        }

        let type: ItemType
        let price: Int
        var count: Int
    }

    enum ItemError: Error, CustomStringConvertible {
        case NoSuchItem
        case NotEnoughMoney(Int)
        case OutOfStock

        var description: String {
            switch self {
            case .NoSuchItem:                 return "Not Such Item"
            case .NotEnoughMoney(let price) : return "Not Enough Money. \(price) Yuan needed."
            case .OutOfStock:                 return "Out of Stock"
            }
        }
    }

    private var items = ["MIneral Water": Item(type: .Water, price: 2, count: 10),
                         "Coca Cola": Item(type: .Cola, price: 3, count: 5),
                         "Orange Juice": Item(type: .Juice, price: 5, count: 3)]

    func vend(itemName: String, money: Int) throws -> Int {
        guard let item = items[itemName] else {
            throw ItemError.NoSuchItem
        }

        guard money >= item.price else {
            throw ItemError.NotEnoughMoney(item.price)
        }

        guard item.count > 0 else {
            throw ItemError.OutOfStock
        }
        items[itemName]!.count -= 1
        return money - item.price
    }

    func display() {
        print("Want something to drink?")
        for itemName in items.keys {
            print("*", itemName)
        }
        print("===========================")
    }
}

let machine = VendingMachine()
machine.display()

var pocketMoney = 6

// 可能抛出异常，但不管不顾，抛出异常后直接崩溃
pocketMoney = try! machine.vend(itemName: "Coca Cola", money: pocketMoney)

// 如果抛出异常，则得到一个nil
let p = try? machine.vend(itemName: "Coca Cola", money: pocketMoney)

// 异常处理，如果抛出异常则进入对应的异常处理，如果都没有捕获到，则进入最后一个处理
do{
    pocketMoney = try machine.vend(itemName: "Coca Cola", money: pocketMoney)
    print(pocketMoney,"Yuan left")
}
catch VendingMachine.ItemError.NoSuchItem{
    print("No Such Item")
}
catch VendingMachine.ItemError.NotEnoughMoney(let price){
    print("Not Enough Money." , price , "Yuan needed.")
}
catch VendingMachine.ItemError.OutOfStock{
    print("Out of Stock")
}
catch{
    print("Error occured during vending.")
}


// 捕获异常，并得到异常实例
do{
    pocketMoney = try machine.vend(itemName: "Coca Cola", money: pocketMoney)
    print(pocketMoney,"Yuan left")
}
catch let error as VendingMachine.ItemError{
    print(error)
}
catch{
    print("Error occured during vending.")
}
```
**3.** defer
相当于java中的fanally，用于抛出异常或没有抛出异常都需要执行的语句；
使用方式：
``` swift
func vend(itemName itemName: String, money: Int) throws -> Int{
    // 和代码平级
    defer{
        print("Have a nice day")
    }

    guard let item = items[itemName] else{
        throw VendingMachine.ItemError.NoSuchItem
    }
    ...

    // 如果有多个defer，则会倒叙执行
    // 如果前方就抛出异常，则该局不会执行
    defer{
        print("Thank you")
    }

    ...

    return money - item.price
}
```

## 内存管理
**1.** 析构函数，实例销毁前在这里做一些处理。由于内存自动销毁实例用的情况比较少
``` swift
class Person {
    init() {
        print("init...")
    }

    func doSomething() {
        print("doing something")
    }

    deinit {
        print("person is leaving!!!")
    }
}

var person: Person? = Person()
// 当赋值为nil后，实例会被销毁
person = nil

// 当实例超出作用域后，实例会被销毁
func inTheShop() {
    print("======")
    print("Welcome")
    let person: Person = Person()
    person.doSomething()
}

inTheShop()

// 输出
//init...
//person is leaving!!!
//======
//Welcome
//init...
//doing something
//person is leaving!!!
```
**2.** 引用计数
当引用实例的变量为0的时候，那么就会被释放；
ARC：Automatic Reference Count
**3.** 强引用循环和weak
weak必须是一个可选型的变量
``` swift
class Person{
    var apartment: Apartment?

    init(){
        print("Person is initialized")
    }

    deinit{
        print("Person is being deinitialized!")
    }
}

class Apartment{

    // 弱引用必须是可选型
    // weak必须是var
    // 当弱引用的实例被销毁的时候，tenant会被赋值为nil
    weak var tenant: Person?

    init(){
        print("Apartment is initialized!")
    }

    deinit{
        print("Apartment is being deinitialized!")
    }
}

var liuyubobobo: Person? = Person()
var imoocApartment: Apartment? = Apartment()
liuyubobobo!.apartment = imoocApartment
imoocApartment!.tenant = liuyubobobo

liuyubobobo = nil
imoocApartment?.tenant //nil
imoocApartment = nil
// 两种顺序内存都能够正确释放
```
**4.** unowned
和上面一样也是弱引用，区别在于它只能修饰常量let，不能是可选的；
添加了unowned的实例最好在unowned引用的对象之前销毁，因为如果不这样访问unowned常量时会抛出异常
**5.** 强引用循环
``` swift
class Country{

    let name: String
    //let capital: City
    var capital: City! // 由于定义成这种隐式的可选，表示占时不会赋值，但肯定会被赋值

    init(countryName: String, capitalName: String){
        self.name = countryName
        //-------两段构造从此分割-------
        self.capital = City(cityName: capitalName, country: self) // 由于占时不用赋值，所以到了第二段构造，于是可以使用self
        print("Country", name, "is intialized.")
    }

    deinit{
        print("Country",name,"is being deinitialized!")
    }
}

class City{

    let name: String
    unowned let country: Country

    init(cityName: String, country: Country){
        self.name = cityName
        self.country = country
        print("City", name, "is intialized.")
    }

    deinit{
        print("City",name,"is being deinitialized!")
    }
}

var china: Country? = Country(countryName: "China", capitalName: "Beijing")
china = nil
```
**6.** 闭包中的强引用循环
``` swift
class SmartAirConditioner{
    var temperature: Int = 26
    var temperatureChange: ((Int) -> ())!
    init(){
        temperatureChange = { [weak self]newTemperature in
            guard let `self` = self else {
                return
            }
            if abs(newTemperature - self.temperature) >= 10{
                print("It's not healthy to do it!")
            }
            else{
                self.temperature = newTemperature
                print("New temperature \(newTemperature) is set!")
            }
        }
    }

    deinit{
        print("Smart Air-conditioner is being deinitialized!")
    }
}

var airCon: SmartAirConditioner? = SmartAirConditioner()
airCon?.temperature
airCon?.temperatureChange(100)
airCon?.temperatureChange(24)
airCon = nil
```

## 类型检查和类型转换
**1.** 类型检查`is`
``` swift
class Person {}

class Student: Person {}

var person: Person = Student()

person is Student // true
```
**2.** 类型转换`as`
``` swift
// 确定类型（失败有风险）
let stu1 = person as! Student
// 可选类型（失败为nil）
let stu2 = person as? Student
```
**3.** 可以用在协议上
**4.** NSObject,AnyObject和Any
``` swift
class Person{
    var name: String
    init(name: String){
        self.name = name
    }
}

//var objects: NSArray = [
//    CGFloat(3.1415926),
//    "imooc",
//    UIColor.blueColor(),
//    NSDate(),
//    Int(32),
//    Array<Int>([1,2,3])
//]
//var objects = [
//    CGFloat(3.1415926),
//    "imooc",
//    UIColor.blueColor(),
//    NSDate(),
//    Int(32),
//    Array<Int>([1,2,3]),
//    Person(name: "liuyubobobo")
//]
//
//// a 为AnyObject
//let a = objects[0]

//var objects: [AnyObject] = [
//    CGFloat(3.1415926),
//    "imooc",
//    UIColor.blueColor(),
//    NSDate(),
//    Int(32),
//    Array<Int>([1,2,3]),
//    Person(name: "liuyubobobo")
//]
//
//objects.append( { (a:Int) -> Int in
//    return a*a} )

var objects: [Any] = [
    CGFloat(3.1415926),
    "imooc",
    //swift 2: UIColor.blueColor(),
    //swift3中，颜色从“xxxColor()”变成了"xxx"。直接调用UIColor.xxx即可
    UIColor.blue,                //swift 3
    NSDate(),
    Int(32),
    Array<Int>([1,2,3]),
    Person(name: "liuyubobobo")
]

objects.append( { (a:Int) -> Int in
    return a*a} )
```


## 一些注意事项
**1.** 变量可以用中文，支持Unicode字符，并且可以用表情
**2.** swift没有 `++` `--` 运算
**3.** 类型都需要显示的自己去转换
**4.** Array、Set、Dictionary、String等结构体都是值类型的
