---
title: Note-Learn-Kotlin
categories:
 - Kotlin
tags:
 - Kotlin
---

# Learn Kotlin

## 基本语法

### 包的定义

和java定义方式一样，只是没有分号

### 定义方法

> a,b求和

``` kotlin
fun sum(a: Int, b: Int): Int {
    return a + b
}
```

> 如果是上面这种一个表达式有返回值，可简写：

``` kotlin
fun sum(a: Int, b: Int) = a + b
```

> 没有返回值的时候，Unit可省略：

``` kotlin
fun printSum(a: Int, b: Int):Unit {
    println("sum of $a and $b is ${a + b}")
}
```

### 变量定义

> 使用关键字的`val`定义只读局部变量，它们的值只能被赋值一次，就和加了java中加了final一样

``` kotlin
val a = 1 // a不可再次被改变
```

> 使用关键字`var`能再次被赋值

``` kotlin
var x = 5
x += 1
```

### 注释

和java中没有区别

### 使用字符串模板

在字符串中可通过`$`直接引用变量的值，如果是一个表达式需要用`${}`

``` kotlin
var a = 1
val s1 = "a is $a"

a = 2
val s2 = "${s1.replace("is", "was")}, but now is $a"
```

### 使用条件表达式

``` kotlin
fun maxOf(a: Int, b: Int): Int {
    if (a > b) {
        return a
    } else{
        return b
    }
}
```

上面的`if`可以简化成一个表达式，就和java中的三目运算符一样

``` kotlin
fun maxOf(a: Int, b: Int) = if (a > b) a else b
```

### 使用可能是null的值和检查为null的值

一个引用可能是null时必须要明确指定能为null

``` kotlin
fun main(args: Array<String>) {
    var x: String? = "b"
    println("parse: ${x?.toIntOrNull()}") // null
    x = null
    println("parse: ${x?.toIntOrNull()}") // null
}
```

### 使用类型检查和自动转化

`is`关键字用来判断表达式是否是某个类型的实例，如果一个局部变量或属性被检查是某个类型，它们不需要再明确的转化它们：

``` kotlin
fun getStringLength(obj: Any): Int? {
    if (obj is String) return obj.length
    return null
}
```

### for 循环

> 循环值：

``` kotlin
val items = listOf("apple", "banana", "kiwifruit")
for (item in items) {
    println(item)
}
```

> 循环下标：

``` kotlin
val items = listOf("apple", "banana", "kiwifruit")
for (index in items.indices) {
    println("items[$index] = ${items[index]}")
}
```

### while 循环

``` kotlin
val items = listOf("apple", "banana", "kiwifruit")
var index = 0
while (index < items.size) {
    println("item at $index is ${items[index]}")
    index++
}
```

### 使用when表达式

> 可以包含各种类型判断：

``` kotlin
fun describe(obj: Any): String =
    when (obj) {
        1          -> "One"
        "Hello"    -> "Greeting"
        is Long    -> "Long"
        !is String -> "Not a string"
        else       -> "Unknown"
    }
```

### 使用范围

> 使用`in`操作符检测一个数是否在范围内：

``` kotlin
print(1 in 0..2) // true
```

> 检测是否超出范围：

``` kotlin
print(3 !in 0..2) // true
```

> 迭代一个范围：

``` kotlin
for (x in 1..5) {
        print(x)
}
```

> 跨越进度和递减：

``` kotlin
for (x in 1..10 step 2) {
    print(x)
}
println()
for (x in 9 downTo 0 step 3) {
    print(x)
}
```

### 使用集合

> 迭代一个集合

``` kotlin
val items = listOf("a", "b", "c")
 for (item in items) {
     println(item)
 }
```

> 使用`in`检测结合中是否包含此对象:

``` kotlin
val items = listOf("a", "b", "c")

when {
    "d" in items -> print("D")
    "a" in items -> print("A")
}

// A
```

> 使用lambda表达式过滤和映射集合：

``` kotlin
val fruits = listOf("banana", "avocado", "apple", "kiwifruit")
fruits
    .filter { it.startsWith("a") }
    .sortedBy { it }
    .map { it.toUpperCase() }
    .forEach { println(it) }

// APPLE
// AVOCADO
```

### 创建一个基本的类和实例

``` kotlin
val rectangle = Rectangle(5.0, 2.0) // 不需要用new
```

## 惯常用法

### 创建数据传输对象DTO（POJO/POCO）

``` kotlin
data class Customer(val name: String, val email: String)
```

提供了一个Customer类和以下功能：

- `equals()`
- `hashCode()`
- `toString()`
- `copy()`
- `component1(), component2()...`，为所有属性都有

### 为方法参数设置默认值

``` kotlin
fun foo(a: Int = 0, b: String = "") { ... }
```

### 过滤列表

``` kotlin
val list = listOf(-1, -2, 3, 4)
val positives = list.filter { x -> x > 0 }
print(positives)
```

> 或者甚至更短

``` kotlin
val positives = list.filter { it > 0 }
```

### 字符串插值

``` kotln
println("Name $name")
```

### 类型检测

``` kotlin
when (x) {
    is Foo -> ...
    is Bar -> ...
    else   -> ...
}
```

### 遍历成对列表

``` kotlin
for ((k, v) in map) {
    println("$k -> $v")
}
```

### 范围的使用

``` kotlin
for (i in 1..100) { ... }  // 包括100
for (i in 1 until 100) { ... } // 不包括100
for (x in 2..10 step 2) { ... }
for (x in 10 downTo 1) { ... }
if (x in 1..10) { ... }
```

### 只读list

``` kotlin
val list = listOf("a", "b", "c")
```

### 只读map

``` kotlin
val map = mapOf("a" to 1, "b" to 2, "c" to 3)
```

### map访问

``` kotlin
println(map["key"])
map["key"] = value
```

### lazy属性

``` kotlin
val p: String by lazy {
    // 计算字符串
}
```

### 扩展方法

``` kotlin
fun String.spaceToCamelCase() { ... }

"Convert this to camelcase".spaceToCamelCase()
```

### 创建一个单例

``` kotlin
object Resource {
    val name = "Name"
}
```

### 如果不为null简写

``` kotlin
val files = File("Test").listFiles()

println(files?.size)
```

### 如果不为null和为null简写

``` kotlin
var a: String? = null
print(a?.length ?: "empty") // emtpy
```

### 如果为null执行一个语句

``` kotlin
val values = ...
val email = values["email"] ?: throw IllegalStateException("Email is missing!")
```

### 获取集合第一个可能为空的时候

``` kotlin
val emails = listOf<Int>()
print(emails.firstOrNull() ?: "")
```

### 如果不是null执行

``` kotlin
val value = ...

value?.let {
    ... // 如果不是null执行的代码块
}
```

### 如果map可能为null的情况下

``` kotlin
val value = ...

val mapped = value?.let { transformValue(it) } ?: defaultValueIfValueIsNull
```

### 返回when语法

``` kotlin
fun transform(color: String): Int {
    return when (color) {
        "Red" -> 0
        "Green" -> 1
        "Blue" -> 2
        else -> throw IllegalArgumentException("Invalid color param value")
    }
}
```

### ‘try/catch’表达

``` kotlin
fun test() {
    val result = try {
        count()
    } catch (e: ArithmeticException) {
        throw IllegalStateException(e)
    }

    // 使用result
}
```

### 'if'表达式

``` kotlin
fun foo(param: Int) {
    val result = if (param == 1) {
        "one"
    } else if (param == 2) {
        "two"
    } else {
        "three"
    }
}
```

### 方法使用建造者风格返回一个规格单元

``` kotlin
fun arrayOfMinusOnes(size: Int): IntArray {
    return IntArray(size).apply { fill(-1) }
}
```

### 单一个表达式的方法

``` kotlin
fun theAnswer() = 42
```

可有效的和其他惯用语结合，弄出更精简的代码：

``` kotlin
fun transform(color: String): Int = when (color) {
    "Red" -> 0
    "Green" -> 1
    "Blue" -> 2
    else -> throw IllegalArgumentException("Invalid color param value")
}
```

### 在对象实例上调用多个方法

``` kotlin
class Turtle {
    fun penDown(){}
    fun penUp(){}
    fun turn(degrees: Double){}
    fun forward(pixels: Double){}
}

fun main(args: Array<String>) {
    val myTurtle = Turtle()
    with(myTurtle) {
        penDown()
        for (i in 1..4) {
            forward(100.0)
            turn(90.0)
        }
        penUp()
    }
}
```

### Java7尝试使用资源

``` kotlin
val stream = Files.newInputStream(Paths.get("/some/file.txt"))
stream.buffered().reader().use { reader ->
    println(reader.readText())
}
```

### 方便的泛型方法，要求泛型信息

``` kotlin
//  public final class Gson {
//     ...
//     public <T> T fromJson(JsonElement json, Class<T> classOfT) throws JsonSyntaxException {
//     ...

inline fun <reified T: Any> Gson.fromJson(json: JsonElement): T = this.fromJson(json, T::class.java)
```

### 使用可能为null的布尔值

``` kotlin
val b: Boolean? = ...
if (b == true) {
    ...
} else {
    // `b` 为false或null
}
```

### 交换两个变量

``` kotlin
var a = 1
var b = 2
a = b.also { b = a }
```

## 代码约定

下面是kotlin语言现在的编码风格。

- 源代码组织
- 命名规则
- 板式
- 文档注释
- 避免冗余结构
- 习惯用语言特性
- 类库编码约定

### 应用样式指引

这些风格指南可配置到intellij的排版格式化，请安装kotlin插件1.2.20或更高的版本，
去 Settings | Editor | Code Style | Kotlin，点击右上角的“Set from...”，
然后在菜单中选择“Predefined style/Kotlin style guide”

更具样式指南验证您的代码是否已经格式化，然后在设置的检查中启动检查
“Settings | Editor | Inspection | Kotlin |
Style issues | File is not formatted according to project settings”
默认情况下不会启动额外的检查与验证其它的风格问题（如命名规范）

### 源代码组织

#### 目录结构

在语言混用的项目中，kotlin源码文件因该在java源文件根目录旁，并有着同样的目录结构（每个文件存放在每个包声的相应目录里）

在纯Kotlin项目，推荐目录结构跟随包结构，并省略根包（例如：如果项目中所有的代码在“org.example.kotlin”包和子包下，带有“org.example.kotlin”的包放在根目录，如果文件放在“org.example.kotlin.foo.bar”包中，那么文件放到源根目录“foo/bar”）

#### 源文件命名

如果一个Kotlin文件包含一个类，那么文件名和类名一样，并加上`.kt`扩展。如果一个文件包含多个类，选择一个描述文件内容的名字作为文件名。使用首字母大写的驼峰命名（例如：`ProcessDeclarations.kt`）

文件名因该描述文件里面的代码，因此你需要避免使用无意义的单词，例如文件名中包含“Util”

#### 源文件组织

鼓励放置多个声明（类，顶层方法或属性）到同一个Kotlin文件，只要这些声明在语义上密切相关，并且文件保持合理大小（不超过几百行）。

特别当定义一个类的扩展方法时，将它们放在与类被定义的那个文件中。当仅为一个特定的类定义一个方法时，将其放到该代码下面。不必再创建一个文件去定义扩展。

#### Class如何分布

通常，一个类的内容按如下排列：

- 属性声明和初始化块
- 二级构造函数
- 方法声明
- 伴生对象

#### 接口实现代码如何分布

#### 重载如何分布

### 命名规则

### 板式

### 文档注释

### 避免冗余结构

### 习惯用语言特性

### 类库编码约定
