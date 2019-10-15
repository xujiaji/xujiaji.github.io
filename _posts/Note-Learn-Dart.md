---
title: Dart学习笔记
date: 2019-03-29 16:45:28
tags:
 - Dart
---

# Dart笔记

## 变量

初始化一个变量

``` dart
var name = 'Bob';
```

`name`将自动判断为`String`类型，如果不想让其限制为了一个类型可以使用`Object`或`dynamic`类型。`Object`类型和java中差不多是一个道理。

``` dart
dynamic name = 'Bob';
```

如果想明确显示声明类型：

``` dart
String name = 'Bob';
```

## 默认值

dart中未初始化的值都是null，即使是数字也是一个对象。

``` dart
int lineCount;
print(lineCount);

//: null
```

## fianl 和 const

当你不想让变量可以再次改变的时候用`final`或`const`修饰，如下：

``` dart
final name = 'Bob'; // 或者： final String name = 'Bob'; const name = 'Bob';
```

此时name的值不可以在修改！

二者的区别是，`const`是编译时期常量，意思是说在编译后就有确切的值。

``` dart
// 如下表达式可以正常运行，但是将bar变量前面的修饰词const换掉，那么就会报错。去掉就代表了bar的值在编译时的不确定性。
const bar = 1000000;
// 如果atm前面的修饰const换成final后，即使bar是变量也是无所谓了
const double atm = 1.01325 * bar;
```

`const`关键字还可以用来修饰值

``` dart
var foo = const [];
final bar = const [];
const baz = [];
```

此时`foo`是变量，值是常量。意思是`foo`还可以引用其他同类型的值，`foo = [1, 2, 3];`是莫得问题的。但是如果让值`const []`改变就不行了~~`foo.add(1);`~~

`bar`变量虽然无法改变引用，但是值是可以改变的。`bar.add(1);`是OK的，但是 ~~`bar = [1];`~~ 是NO。

`baz`，上面两样都没得玩！

如果`const`的变量是类一个级别的，这样声明：`static const`

## 内置类型

以下类型是`Dart`中特殊支持的类型

- `数字 numbers`
- `字符串 strings`
- `布尔 booleans`
- `列表 lists`(也称为数组)
- `集合 sets`
- `映射 maps`
- `符文 runes`(用于在字符串中表示Unicode字符)
- `符号 symbols`

您可以使用字面文字初始化一些特别的类型对象，例如`'this is a string'`是一个string对象，`true`是一个boolean对象。

因为在Dart中每个变量都引用了一个对象（一个类的实例），您可以使用构造方法初始化变量，有些内置类型有它们自己的构造函数。例如，您可以使用`Map()`构造来创建一个map实例。

### 数字 Numbers

Dart有两种方式表示数字

**[int][1]**

整型最大不超过64bit，并依赖于平台。在Dart虚拟机上，值取值范围`[-2^63,2^63 - 1]`。编译为JavaScript时使用[JavaScript数字][2]，区间范围为`[-2^53,2^53-1]`。

**[double][2]**

64bit（双精度）浮点数由IEEE 754标准规定

`int`和`double`都是[num][4]的子类型，在`num`类型中包含了`+`、`-`、`*`、`/`基本运算符，在其他方法中您也可以找到`abs()`,`ceil()`,`floor()`。（位运算符，如`>>`，定义在`int`类）如果`num`和其子类没有您想要的，[dart:math][5]类库中可能有。

字符串和数字互转

``` dart
// String -> int
int.parse('1'); // 1

// String -> double
double.parse('1.1'); // 1.1

// int -> String
1.toString(); // 1

// double -> String 保留两位小数，四舍五入
3.14159.toStringAsFixed(2); // 1.14
```

### 字符串 Strings

Dart字符串是一系列UTF-16代码单元，您可以使用单引号或双引号创建一个字符串：

``` dart
// 单引号可以表示
var s1 = 'single quotes string';

// 双引号也可以表示
var s2 = "double quotes strings";

// 单引号表示时，里面有单引号需要转义
var s3 = 'i\'m a cool boy';

// 双引号表示时，里面有单引号不需要转义
var s4 = "i'm a cool boy";
```

可以将表达式放在字符串里面通过`${expression}`的形式，表达式只是变量时，您可以不要`{}`。如果是一个对象时Dart会通过调用`toString()`方法获取这对象的字符串。

``` dart
var v = 'bc';
print('a$v'); // abc
print('A${v.toUpperCase()}'); // ABC
print('$Set()'); // Set<dynamic>()
print('${Set().toString()}'); // {}
```

相邻的字符串会自己拼接或通过`+`号拼接

``` dart
var a = '1'
  '2'
  "3"
  '4';
print(a); // 1234

var b = '1' + '2' + "3";
print(b); // 123
```

可以使用三倍的单引号或双引号创建多行字符串：

``` dart
var s1 =
  '''
  1
    2\n3
  ''';
print(s1);

// 下面是输出，试了下双引号单引号效果一样
//    1
//      2
//3
```

您可以在引号前面加`r`表示字符串是原始(raw)类型：

``` dart
print(r'a\nb'); // a\nb
```

是什么就输出什么，不需要转义，单引号双引号三倍引号都可以用。

有关字符串中表达Unicode字符的详细信息，请参阅[字符 Runes][6]

字符串文字是一个编译期常量

更多字符串使用信息，请参阅[字符串和正则表达式][7]

### 布尔 Booleans

Dart用类型`bool`表示布尔值。只有两个对象表示`bool`类型：`true`和`false`，它们的文字表达都是编译时期常量。

Dart是类型安全的，意味着您不能使用像`if (非布尔值)`或`assert(非布尔值)`的代码。取而代之的是明确指出布尔值，如下：

``` dart
// 检查空字符串
var fullName = '';
assert(fullName.isEmpty);

// 检查0
var hitPoints = 0;
assert(hitPoints <= 0);

// 检查null
var unicorn;
assert(unicorn == null);

// 检查 NaN （Not a Number 不是一个数）
var iMeantToDoThis = 0 / 0;
assert(iMeantToDoThis.isNaN);
```

### 列表 Lists

也许几乎所有编程语言中最常见的集合是数组，或有序的对象组。在Dart中数组就是[List][8]对象，因此大多数人叫他们列表。

Dart的列表写法看起来就是其他语言数组的写法。下面是一个Dart列表的示例：

``` dart
var list = [1, 2, 3];
```

上面的类型为`List<int>`

更多关于列表的信息，请参阅[泛型][9]和[集合][10]

### 集合 Sets

set 在Dart中是一个无序集合，Dart支持通过文字表达和[Set][11]来创建集合。

简单的通过文字表达

``` dart
var halogens = {'fluorine', 'chlorine', 'bromine', 'iodine', 'astatine'};
```

上面类型为：`Set<String>`

创建一个空集合：

``` dart
var names1 = <String>{};
Set<String> names2 = {};

// var names3 = {}; //注意这样创建的不是一个Set，而是一个Map，具体来说是一个 Map<dynamic, dynamic>
```

### 映射 Maps

通常，一个map有key和value。key和value可以是任何对象，key只能出现一个，但值可以对应多个key。Dart创建映射也可以通过直接表达和[Set][12]类型表达。

``` dart
var aa = {
  'a': '1',
  'b': '2'
};

var bb = {
  1: 'a',
  2: 'b'
};
```

上面，第一个`aa`是`Map<String, String>`类型，第二个`bb`是`Map<int, String>`类型。

通过Map构造也可以创建同样的效果：

``` dart
var aa = Map();
aa['a'] = '1';
aa['b'] = '2';

var bb = Map();
bb[1] = 'a';
bb[2] = 'b';
```

### Runes

Dart中Runes是UTF-32字符集的字符串对象

Unicode为世界上的所有文字系统都定义了一个唯一数字代表文字、数字和符号。因为一个Dart字符串是一个UTF-16字符集序列，在字符串中表示32位Unicode值需要特殊语法。

常用来表达一个Unicode字符的方式是`\uXXXX`，这儿的`XXXX`是一个4位16进制值。例如，心字符（♥）是`\u2665`。如果是多余或少于4个16进制数字的，将值放进大括号里面。例如笑的emoji（😆）是`\u{1f600}`。

[String][13]类有几个属性使您可以将字符串转为符文runes。`codeUnitAt`和`codeUnits`返回16位字符集（数字编码）。使用`runes`返回一个字符串符文

下面说明了符文，16位和32位字符集之间的关系

``` dart
var clapping = '\u{1f44f}ab';
print(clapping); // 👏ab
print(clapping.codeUnitAt(0)); // 55357
print(clapping.codeUnits); // [55357, 56399, 97, 98]
print(clapping.runes.toList()); // [128079, 97, 98]

Runes input = new Runes(
    '\u2665  \u{1f605}  \u{1f60e}  \u{1f47b}  \u{1f596}  \u{1f44d}');
print(new String.fromCharCodes(input)); // ♥  😅  😎  👻  🖖  👍
```

### 符号 Symbols

在Dart程序中，[Symbol][14]对象表示声明运算符或标识符。您可能从来不会使用到Symbol，但是它们在按名字引用标识符的API非常有用，因为缩小到改变标识符名称而不更改标识符。

获取标识符的symbol，使用sybol表达式，只需`#`号后跟标识符：

``` dart
var map = Map();
map[#foo] = "foo's value";
print(map[#foo]); // foo's value
print(#foo); // Symbol("foo")
```

Symbol是编译器常量。

## 方法 Functions

Dart是一个真正的面向对象语言，因此甚至函数也是一个对象有一个类型，[Function][15]。这意味着方法能分配给变量或传入其他方法，你也可以好像调用一个函数一样，调用Dart类的实例。详情，请参阅[可调用的类][16]。

这儿有个实现方法的例子：

``` dart
bool isNoble(int atomicNumber) {
  return _nobleGases[atomicNumber] != null;
}
```

尽管[Effective Dart建议写上返回类型][17]，但是如果你不写也可以正常工作：

``` dart
isNoble(atomicNumber) {
  return _nobleGases[atomicNumber] != null;
}
```

这个方法里面只有一个表达式，于是可以简写：

``` dart
bool isNoble(int atomicNumber) => _nobleGases[atomicNumber] != null;
```

`=> 表达式`语法是`{ return 表达式;}`的简写。`=>`符号有时也被称为箭头语法。

一个方法可能有两个类型的参数：必须和可选。必要的参数在最前，随后是可选参数。

### 可选参数

可选参数可以是位置参数或命名参数，不能同时存在

#### 可选命名参数

当调用一个方法，您可以指定命名参数`paramName: value.`，例如：

``` dart
enableFlags(bold: true, hidden: false);
```

当定义一个方法时，使用`{param1, param2, ...}`来指定命名参数：

``` dart
/// 设置加粗和隐藏标记
void enableFlags({bool bold, bool hidden}) {...}
```

[Flutter][18]实例创建可能更复杂，因此widget构造器仅使用命名参数。这让实例的创建更加容易阅读。

您可以在任何Dard代码中标记注解[@required][19]，表面它是一个必传参数。例如：

``` dart
const Scrollbar({Key key, @required Widget child})
```

当`Scrollbar`被创建时，如果没有传入child那么解析器就会报告问题。

[Required][19]被定义在[meta][20]包中，要么直接导入`package:meta/meta.dart`，要么导入的其他包中导入过`meta`，例如Flutter的`package:flutter/material.dart`。

命名参数加了`@required`必传，其他可传可不传。

#### 可选位置参数

在`[]`中设置函数类型使它们作为可选位置参数，该参数可传可不传。

``` dart
String say(String from, String msg, [String device]) {
  var result = '$from says $msg';
  if (device != null) {
    result = '$result with a $device';
  }
  return result;
}
```

没有传入可选位置参数时：

``` dart
print(say('Bob', 'Howdy')); // Bob says Howdy
```

当传入可选位置参数的时候：

``` dart
print(say('Bob', 'Howdy', 'smoke signal')); // Bob says Howdy with a smoke a signal
```

#### 参数默认值

命名参数和位置参数都可以使用`=`来定义默认值，默认值必须是编译器常量。如果没有提供默认值，默认值为`null`

设置命名参数的默认值：

``` dart
void enableFlags({bool bold = false, bool hidden = false}) {...}
enableFlags(bold: true); // bold = true, hidden = false
```

设置可选位置参数的默认值：

``` dart
String say(String from, String msg,
    [String device = 'carrier pigeon', String mood]) { ... }
```

你也可以为列表或集合参数设置默认值，如下：

``` dart
void doStuff(
    {List<int> list = const [1, 2, 3],
    Map<String, String> gifts = const {
      'first': 'paper',
      'second': 'cotton',
      'third': 'leather'
    }}) {
  print('list:  $list');
  print('gifts: $gifts');
}
```

### `main()`方法

每个app必须有个顶级`main()`方法，它是app的入口点。`main()`方法返回`void`并且有一个可选参数`List<String>`。

这是一个web app的main()方法例子：

``` dart
void main() {
  querySelector('#sample_text_id')
  ..text = 'Click me!'
  ..onClick.listen(reverseText);
}
```

> 注意：这里的`..`语法被称为[级联][21]，通过级联您可以多次对一个对象进行操作。

下面是创建了一个命令行运行的app，在`main()`方法的参数可获得命令行的值：

``` dart
void main(List<String> arguments) {
  print(arguments);
}
```

首先需要配置好dart环境变量，然后在终端当前文件目录运行：`dart test.dart 1 test`，将会输出`[1, test]`。

您可以使用[args][21]类库定义或解析命令行参数。

### 方法看做类对象

您可以将一个方法作为参数传入另一个方法，例如：

``` dart
void main() {
  void printElement(int element) {
    print(element);
  }

  var list = [1, 2, 3];
  // 将方法作为参数传入
  list.forEach(printElement);
}

// 运行输出：
// 1
// 2
// 3
```

您也可以为变量分配一个方法，例如：

``` dart
var loudify = (msg) => '!!!${msg.toUpperCase()}!!!';
print(loudify('hello')); // !!!HELLO!!!
```

这个例子使用匿名方法，更多信息请接着看看下面哦！

### 匿名方法

很多方面都有名字，例如`main()`或`printElement()`。您也可以创建一个没有名字的方法，我们称之为匿名方法，或`lambda`，或`闭包(closure)`。您可以分配给变量一个匿名方法，例如，您可以在列表中添加或移除它。

匿名方法和命名方法差不多，一个或多个参数放在括号里，之间用逗号分隔。

代码样式看起来如下面的格式：

``` dart
([[类型] 参数1[, …]]) {
  代码块;
};
```

下面的例子中定义了一个无类型参数`item`的匿名方法，这个方法在列表轮询时被调用，打印对应的值和下标：

``` dart
var list = ['apples', 'bananas', 'oranges'];
list.forEach((item) {
  print('${list.indexOf(item)}:$item');
});

// 输出：
// 0:apples
// 1:bananas
// 2:oranges
```

由于这个方法只有一条指令，您可以用箭头表达：

``` dart
list.forEach((item) => print('${list.indexOf(item)}: $item'));
```

### 作用域语法

Dart也是一个作用域语法语言，这意味着变量的作用域是确定的，只需改变代码布局就可。您可以使用花括号外的变量来查看是否在作用域内。

下面是一个方法内嵌的例子，并且每个等级的作用域中都有一个变量：

``` dart
bool topLevel = true;

void main() {
  var insideMain = true;

  void myFunction() {
    var insideFunction = true;

    void nestedFunction() {
      var insideNestedFunction = true;

      assert(topLevel);
      assert(insideMain);
      assert(insideFunction);
      assert(insideNestedFunction);
    }
  }
}
```

注意`nestedFunction()`如何使用每个级别的变量，一直到顶级。

### 闭包语法

一个闭包是一个方法对象，它能访问在它作用域语法内的变量。即使当这个方法使用在原来的作用域之外。

方法能关联作用域范围的变量，在下面的例子中，`makeAdder()`获取的变量是`addBy`，返回一个方法，无论它返回在哪都会记住`addBy`。

``` dart
/// 返回一个方法
/// addBy + 方法的参数i
Function makeAdder(num addBy) => (i) => addBy + i;

void main() {
  // 创建一个加2的方法
  var add2 = makeAdder(2);

  // 创建一个加4的方法
  var add4 = makeAdder(4);

  print('${add2(3)}, ${add4(3)}'); // 5,  7
}
```

### 测试方法相等性

这儿有一个测试最外层方法，静态方法和实例方法的相等性的例子：

``` dart
void foo() {} // 最外层方法

class A {
  static void bar() {} // 静态方法
  void baz() {} // 实例方法
}

void main() {
  var x;

  // 比较静态方法
  x = foo;
  print(foo == x); // true

  // 比较实例方法
  x = A.bar;
  print(A.bar == x); // true

  var v = A(); // 第一个A实例
  var w = A(); // 第二个A实例
  var y = w;
  x = w.baz;

  // 由于这两个变量引用同一个实例，因此他们的闭包相等
  print(y.baz == x); // true
  // 由于这是两个实例，因此他们的闭包不等
  print(v.baz == w.baz); // false
}
```

### 返回值

所有方法都有一个返回值，如果没有指定返回值，那么在方法体中会隐式声明`return null;`

``` dart
foo() {}
print(foo()); // null
```

## 运算符

下面的表格中展示了Dart中定义的运算符，您可以覆盖下面大部分运算符，详情参照：[可覆盖运算符][23]

|描述|运算符|
|:-|:-|
|单目后置|`expr++` `expr--` `()` `[]` `.` `?.`|
|单目前置|`-expr` `!expr` `~expr` `++expr` `--expr`|
|乘法类|`*` `/` `%` `~/`|
|加减类|`+` `-`|
|位移|`>>` `<<` `>>>`|
|按位与|`&`|
|按位异或|`^`|
|按位或|`|`|
|关系和类型校验|`>=` `>` `<=` `<` `as` `is` 'is!'|
|等性|`==` `!=`|
|逻辑与|`&&`|
|逻辑或|`||`|
|是否是null|??|
|三目运算|`expr1 ? expr2 : expr2`|
|级联|`..`|
|赋值|`=` `*=` `/=` `+=` `-=` `&=` `^=` 等|

### 算数运算符

Dart支持常用算数运算符，如下表所示：

|运算符|解释|
|:-|:-|
|`+`|加|
|`-`|减|
|`-expr`|一元减，也称为否定（反转表达式的符号）|
|`*`|乘|
|`/`|除|
|`~/`|除以，并返回整数结果|
|`%`|求余|

``` dart
  print(5 / 2); // 2.5
  print(5 ~/ 2); // 2
```

Dart也支持单目递增和递减运算符

|运算符|解释|
|:-|:-|
|`++var`|`var = var + 1`(表达式的值为`var + 1`)|
|`var++`|`var = var + 1`(表达式的值为`var`)|
|`--var`|`var = var - 1`(表达式的值为`var - 1`)|
|`var--`|`var = var - 1`(表达式的值为`var`)|

### 等式和关系运算符

下面的表格列出了等式和关系运算符的含义

|运算符|含义|
|:-|:-|
|`==`|恒等于|
|`!=`|不等于|
|`>`|大于|
|`<`|小于|
|`>=`|大于或等于|
|`<=`|小于或等于|

使用`==`判断两个对象是否是同一个东西（在少数情况下您需要判断两个引用是否指向同一个对象时，使用[identical()][25]）

### 类型检测运算符

`as`,`is`和`is!`运算符用来检测运行时类型

|运算符|意思|
|:-|:-|
|`as`|类型转换（也经常用来指定[类库前缀][26]）|
|`is`|对象是否有指定的类型|
|`is!`|和上面相反|

`as` 强转类型， `is` 类型判断

### 赋值运算符

您已知道，您可以通过`=`运算符为变量赋值。如果要仅仅变量为`null`时才赋值，使用`??=`运算符

``` dart
void main() {
  int a = 5;
  int b;

  a ??= 10;
  b ??= 10;
  print('a = $a, b = $b'); // a = 5, b = 10
}
```

组合赋值运算符，如`+=`将运算符和赋值结合

|||||||
|:-|:-|:-|:-|:-|:-|
|`=`|`-=`|`/=`|`%=`|`>>=`|`^=`|
|`+=`|`*=`|`~/=`|`<<=`|`&=`|<code>&#124;=</code>|

### 逻辑运算符

您可以通过逻辑运算符颠倒或组合布尔表达式

|运算符|意思|
|:-|:-|
|`!expr`|颠倒是非|
|<code>&#124;&#124;</code>|逻辑或|
|`&&`|逻辑与|

### 按位运算和移位运算符

您可以在Dart中操作数字的位运算

|运算符|意思|
|:-|:-|
|`&`|与|
|<code>&#124;</code>|或|
|`^`|异或|
|`~expr`|取反|
|`<<`|左移|
|`>>`|右移|

### 条件表达式

Dart有两种表达式让您简明的表达需要使用到`if-else`的情景：

1.三目运算符

``` dart
condition ? expr1 : expr2
```

2.是否为null，如果为null则用后面的表达式

``` dart
expr1 ?? expr2
```

``` dart
void main() {
  print(1 > 2 ? "是的1>2" : "不不，1<2"); // 不不，1<2
  int value;
  print(value ?? 100); // 100
}
```

### 级联表示法

`..`允许您对同一个对象进行一系列连续的操作。不仅可以调用方法，您也可以为这个对象字段赋值。这通常为您节省了创建临时变量的不步骤，并能让你写成更多流畅的代码。

请参考下面代码：

``` dart
querySelector('#confirm') // 获得一个对象
  ..text = 'Confirm' // 使用它的成员变量
  ..classes.add('important')
  ..onClick.listen((e) => window.alert('Confirmed!'));
```

还有内部联结：

``` dart
final addressBook = (AddressBookBuilder()
      ..name = 'jenny'
      ..email = 'jenny@example.com'
      ..phone = (PhoneNumberBuilder()
            ..number = '415-555-0100'
            ..label = 'home')
          .build())
    .build();
```

### 其他操作符

您已在其他案例中看到了大多数的相关操作符

|操作符|名字|含义|
|:-|:-|:-|
|`()`|方法|表示方法调用|
|`[]`|列表访问|通过索引引用列表中的值|
|`.`|成员访问|引用一个属性；例如：`foo.bar`，引用foo对象中的bar属性|
|`?.`|条件成员访问|左边的变量可以是null|

``` dart
class A {
  var b;
}


void main() {
  A a;
  print(a?.b); // null, 如果不加“？”就会报错
}
```

更多关于`.`，`?.`和`..`的操作，请参考[类][27]

## 控制流语句

您可以使用下面的任意Dart代码控制流程

- `if` 和 `else`
- `for` 循环
- `while` 和 `do-while`循环
- `break` 和 `continue`
- `switch` 和 `case`
- `assert`

您也可以可以通过`try-catch`和`throw`影响流程，详细介绍在[异常][28]

### for循环

``` dart
void main() {
  var callback = [];
  for(var i = 0; i < 2; i++) {
    callback.add(() => print(i));
  }
  callback.forEach((c) => c());
}

// 输出：
// 0
// 1
```

列表中放入的是两个闭包，列表是一个迭代器，您可以使用[forEach()][29]方法来遍历。如果你不需要知道当前的迭代数量，使用`forEach()`是一个不错的选择：

``` dart
candidates.forEach((candidate) => candidate.interview());
```

可迭代的类如List和Set也支持`for-in`[iteration][30]：

``` dart
var collection = [0, 1, 2];
for (var x in collection) {
  print(x); // 0 1 2
}
```

### Switch和case

值得注意的是switch里面使用`==`作为判断整型，字符串或编译期常量。用法大致和java差不多，主要注意下面这样的写法有改进：

``` dart
var command = 'OPEN';
switch (command) {
  case 'OPEN':
    executeOpen();
    // 错误： 没有break （如果去掉executeOpen();也是没有问题的）
  case 'CLOSED':
    executeClosed();
    break;
}
```

改：

``` dart
var command = 'CLOSED';
switch (command) {
  case 'CLOSED':
    executeClosed();
    continue nowClosed;
  // 继续执行nowClosed标签

  nowClosed:
  case 'NOW_CLOSED':
    // Runs for both CLOSED and NOW_CLOSED.
    executeNowClosed();
    break;
}
```

## 断言

断言不会影响到生产代码，只应用在开发调试模式下

## 异常

您的Dart代码可以抛出或捕获异常，异常是发生了一些不希望的。如果异常没有捕获处理，会导致程序终止。Dart提供[Exception][31]和[Error][32]类型，以及许多预定义的子类型。当然，您也可以定义您自己的异常。然而对于异常，Dart程序能抛出任何非null对象，不仅仅是Exception和Error对象。

### Throw

下面是一个抛出异常的列子：

``` dart
throw FormatException('Expected at least 1 section');
```

您也可以随意抛出一个对象：

``` dart
throw '异常。。。';
```

由于抛出异常是一个表达式，可以通过`=>`如下表达：

``` dart
void distanceTo(Point other) => throw UnimplementedError();
```

### Catch

捕获一个异常

``` dart
try {
  breedMoreLlamas();
} on OutOfLlamasException {
  buyMoreLlamas();
}
```

捕获多个异常，`catch`可以得到异常对象的引用，如果不明确类型直接用`catch`：

``` dart
try {
  breedMoreLlamas();
} on OutOfLlamasException {
  // 一个特定异常
  buyMoreLlamas();
} on Exception catch (e) {
  // 任何其他类型Exception异常
  print('Unknown exception: $e');
} catch (e) {
  // 不指定类型，处理所有
  print('Something really unknown: $e');
}
```

`catch()`可指定两个参数，第一个是抛出的异常对象，第二个是堆栈（[StackTrace][33]）

``` dart
try {
  // ···
} on Exception catch (e) {
  print('Exception details:\n $e');
} catch (e, s) {
  print('Exception details:\n $e');
  print('Stack trace:\n $s');
}
```

既要处理异常，又要让异常重新跑出去使用`rethrow`关键字

``` dart
void misbehave() {
  try {
    dynamic foo = true;
    print(foo++); // 运行时错误
  } catch (e) {
    print('misbehave() partially handled ${e.runtimeType}.');
    rethrow; // 让调用者继续得到异常
  }
}
```

### Finally

和java一样

[1]: https://api.dartlang.org/stable/2.2.0/dart-core/int-class.html
[2]: https://stackoverflow.com/questions/2802957/number-of-bits-in-javascript-numbers/2803010#2803010
[3]: https://api.dartlang.org/stable/dart-core/double-class.html
[4]: https://api.dartlang.org/stable/dart-core/num-class.html
[5]: https://api.dartlang.org/stable/dart-math
[6]: https://www.dartlang.org/guides/language/language-tour#runes
[7]: https://www.dartlang.org/guides/libraries/library-tour#strings-and-regular-expressions
[8]: https://api.dartlang.org/stable/2.2.0/dart-core/List-class.html
[9]: https://www.dartlang.org/guides/language/language-tour#generics
[10]: https://www.dartlang.org/guides/libraries/library-tour#collections
[11]: https://api.dartlang.org/stable/2.2.0/dart-core/Set-class.html
[12]: https://api.dartlang.org/stable/dart-core/Map-class.html
[13]: https://api.dartlang.org/stable/2.2.0/dart-core/String-class.html
[14]: https://api.dartlang.org/stable/2.2.0/dart-core/Symbol-class.html
[15]: https://api.dartlang.org/stable/dart-core/Function-class.html
[16]: https://www.dartlang.org/guides/language/language-tour#callable-classes
[17]: https://www.dartlang.org/guides/language/effective-dart/design#prefer-type-annotating-public-fields-and-top-level-variables-if-the-type-isnt-obvious
[18]: https://flutter.dev/
[19]: https://pub.dartlang.org/documentation/meta/latest/meta/required-constant.html
[20]: https://pub.dartlang.org/packages/meta
[21]: https://www.dartlang.org/guides/language/language-tour#cascade-notation-
[22]: https://pub.dartlang.org/packages/args
[23]: https://www.dartlang.org/guides/language/language-tour#overridable-operators
[24]: https://www.dartlang.org/guides/language/language-tour#operators
[25]: https://api.dartlang.org/stable/2.2.0/dart-core/identical.html
[26]: https://www.dartlang.org/guides/language/language-tour#specifying-a-library-prefix
[27]: https://www.dartlang.org/guides/language/language-tour#classes
[28]: https://www.dartlang.org/guides/language/language-tour#exceptions
[29]: https://api.dartlang.org/stable/2.2.0/dart-core/Iterable/forEach.html
[30]: https://www.dartlang.org/guides/libraries/library-tour#iteration
[31]: https://api.dartlang.org/stable/2.2.0/dart-core/Exception-class.html
[32]: https://api.dartlang.org/stable/2.2.0/dart-core/Error-class.html
[33]: https://api.dartlang.org/stable/2.2.0/dart-core/StackTrace-class.html
