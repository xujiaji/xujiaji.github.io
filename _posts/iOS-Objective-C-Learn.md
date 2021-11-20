---
title: iOS Objective-C Learn Note
date: 2018-09-05 18:11:24
author: xujiaji
categories:
 - iOS
tags:
 - Objective-C
 - 学习
 - 笔记
 - iOS
---

## 源代码文件扩展名对比

||头文件|实现文件|
|:-|-|-|
|c语言|.h|.c|
|c++语言|.h|.cpp|
|oc语言|.h|.m|
|oc&c++|.h|.mm|

## 类的定义
> 定义一个`SimpleClass`类

``` objc
@interface SimpleClass: NSObject

@end
```

## 类的属性申明
> 通过`@property`

```objc
@property NSString *firstName;

@property NSString *lastName;

//指针类型，是一个对象
@property NSNumber *yearOfBirth;

//基础类型，是一个值类型
@property int yearOfBirth;

//一个只读的属性
@property (readonly) NSString *firstName;
```

## 减号方法和加号方法（本质就是一个函数）
1. 减号方法（普通方法又称对象方法）
2. 加号方法（类方法，又称静态方法）

## 完整的例子
> 接口`XYZPerson.h`

``` objc
@interface XYZPerson: NSObject
-(void)sayHello;
@end
```

> 实现`XYZPerson.m`

``` objc
#import "XYZPerson.h"
@implementation XYZPerson
-(void)sayHello {
  // 加了@符号，表示是OC类型的字符串。不加表示是纯C语言的字符数组
  NSLog(@"Hello, World!");
}
@end
```

## 简单的程序
``` objc
#import <Foundation/Foundation.h>
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // insert code here...
        NSLog(@"Hello, World!");
    }
    return 0;
}
```

## 基本数据类型
|类型|进制位|例子|
|-|-:|-:|
|int|32位|int a = 0;|
|float|32位|float f = 1.0;|
|double|64位|double num;|
|char|8位|char c = 'A';|

## 其他类型
&nbsp;|&nbsp;
-|-
NSString|@"hello world"
"hello world"|C语言字符串类型

## 限定词
|限定词|例子|描述|
|-|-:|-|
|long|long a;|//完整写法为：long int a;其实现在int已经32位了就相当于int a;|
|long long|long long int a;||
|short|short int a; short a;|// 16位整型|
|unsigned|unsigned int a;|// 无符号|
|signed|signed int a;|// 有符号|

## 算术表达式与运算符
|名称|表示|
|-:|:-|
|赋值|`=`|
|一元运算符|`++` `--`|
|二元运算符|`+` `-` `*` `/` `%`|
|三目运算符|2 > 3 `?` YES `:` NO|

## `if`语句（非0就是真）
||值|
|-:|:-|
|真|`YES` `所有非0的值`|
|假|`NO` `0`|

> 简单例子

``` objc
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        int a = 1;
        int b = 2;
        if (a > b) {
            NSLog(@"这句话是真的");
        } else {
            NSLog(@"这句话是假的 %hhd", NO);
        }
    }
    return 0;
}
```

## `goto` 跳转语句，跳转的前面定义的标签处
``` objc
#import <Foundation/Foundation.h>
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        int i = 0;
    // 定义标签a
    a:
        i ++;
        NSLog(@"i的值为%d", i);
//        if(i < 5) goto a;
        if (i < 5) {
            goto a; // 跳转到标签a
        } else {
            goto b; // 跳转到标签b
        }
        NSLog(@"============"); // 由于上面直接跳转到了b标签，因此该语句得不到执行

    b:{
        NSLog(@"跳到b了");
    }
    }
    return 0;
}

// 输出：
// 2018-09-05 22:23:53.800654+0800 les1[971:104767] i的值为1
// 2018-09-05 22:23:53.800827+0800 les1[971:104767] i的值为2
// 2018-09-05 22:23:53.800858+0800 les1[971:104767] i的值为3
// 2018-09-05 22:23:53.800876+0800 les1[971:104767] i的值为4
// 2018-09-05 22:23:53.800889+0800 les1[971:104767] i的值为5
// 2018-09-05 22:23:53.800902+0800 les1[971:104767] 跳到b了
```

## `while` 循环语句
``` objc
        int i = 0;
        while (i < 5) {
            i++;
            NSLog(@"Hello world! i = %d", i);
        }
// 输出
// Hello world! i = 1
// Hello world! i = 2
// Hello world! i = 3
// Hello world! i = 4
// Hello world! i = 5
```
## `do` `while` 循环，至少执行一次
``` objc
do {
    NSLog(@"hello!");
} while (0)

// 输出：
// hello!
```

## `for` 循环
``` objc
for (int i = 0; i < 5; i++) {
    NSLog(@"i = %d", i);
}

// 输出
// i = 1
// i = 2
// i = 3
// i = 4
// i = 5
```

## 循环控制`break`、`continue`
- break： 终止循环
- continue: 跳过当前循环

## `switch`分支语句
``` objc
int i = 2;
switch (i) {
    case 0:
        NSLog(@"i = 0");
        break;
    case 1:
        NSLog(@"i = 1");
        break;
    case 2:
        NSLog(@"i = 2");
        break;
    case 3:
        NSLog(@"i = 3");
        break;
    default:
        NSLog(@"NO");
        break;
}
```

## 函数的基本写法
``` c
#import <Foundation/Foundation.h>

/*
 * 求面积的函数
 * 传入值，计算并返回面积值
 */
double area(double a, double b) {
    return a * b;
}

// 无参无返回的函数
void show() {
    NSLog(@"this is a test!");
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"value = %f", area(5.0, 3.0));
        show();
    }
    return 0;
}
```

## main函数中的默认参数
``` objc
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"argc = %d", argc);
        for (int i = 0; i < argc; i++) {
            NSLog(@"%s", argv[i]);
        }
    }
    return 0;
}
```

> 终端运行

``` sh
$ ls -l
total 56
-rwxr-xr-x@ 1 username  staff  27984  9  5 23:21 les1

$ ./les1
2018-09-05 23:28:27.313 les1[1369:176584] argc = 1
2018-09-05 23:28:27.313 les1[1369:176584] ./les1

$ ./les1 -a -b -c
2018-09-05 23:28:39.782 les1[1370:176617] argc = 4
2018-09-05 23:28:39.782 les1[1370:176617] ./les1
2018-09-05 23:28:39.782 les1[1370:176617] -a
2018-09-05 23:28:39.782 les1[1370:176617] -b
2018-09-05 23:28:39.782 les1[1370:176617] -c
```

## 创建类
> 头文件`People.h`

``` objc
#import <Foundation/Foundation.h>

@interface People : NSObject

@end
```
> 实现文件`People.m`

``` objc
#import "People.h"

@implementation People

@end
```

## 实例化对象
1. 导入类的头文件
2. `[]`中写函数的调用
3. `alloc` 函数为对象分配内存空间
4. `init` 函数进行初始化操作

``` objc
#import <Foundation/Foundation.h>
#import "People.h" // 导入类头文件

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // 实例化对象
        // [] 函数的调用
        // [类名 方法名]
        // [对象名 方法名]
        // alloc - 为对象分配内存空间
        // init - 进行初始化操作
        People * p1 = [[People alloc] init];
        People * p2 = [[People alloc] init];
      }
    return 0;
}
```

## 属性和成员变量
1. 类内使用成员变量、类外使用属性
2. 定义成员变量，此时外部无法访问。如果要让外部可访问需要加上（不建议）：@public
3. 属性是为了让类外可以访问成员变量
4. 属性就是成员变量的外部接口
5. 可将属性拆开，写成`get`和`set`两部分

> People.h

``` objc
// 类内使用成员变量、类外使用属性
#import <Foundation/Foundation.h>

@interface People : NSObject
{
    // 定义成员变量，此时外部无法访问。如果要让外部可访问需要加上：@public
    // @public
    // NSString * _peopleName; // 如果定义了该成员变量的属性，那么可以不写。编译器会为我们自动生成一个叫_peopleName的成员变量
    int _peopleAge;
}
// 属性是为了让类外可以访问成员变量
// 属性就是成员变量的外部接口
@property(nonatomic, strong)NSString * peopleName;

// 将属性拆开
- (void) setAge:(int) age;
- (int) getAge;
@end
```
> People.m

``` objc
#import "People.h"
{
   int _peopleSex; // 也可以将成员变量定义在m文件中，没什么区别
}
@implementation People
- (instancetype)init
{
    self = [super init];
    if (self) {
        _peopleName = @"张三";
    }
    return self;
}

- (void) setAge:(int) age
{
    _peopleAge = age;
}

- (int) getAge
{
    return _peopleAge;
}
@end
```
> main.m

``` objc
#import <Foundation/Foundation.h>
#import "People.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        People * p1 = [[People alloc] init];
        p1.peopleName = @"李四"; // 通过属性设置名字
        NSLog(@"p1 name %@", [p1 peopleName]); // 通过属性获取名字
        [p1 setAge:23]; // 通过函数设置年龄
        NSLog(@"p1 age %d", [p1 getAge]); // 通过函数获取年龄
    }
    return 0;
}
```

## 函数
1. 调用方法是用中括号
2.  `-`、`+` 方法的类型（减号代表对象方法，加号代表类方法）
3. 加号方法和减号方法之间的相互调用逻辑和java一样
4. 方法名：去掉方法类型和参数类型就是方法名
5. `(int)` 返回值类型`int`
6. `:(int) x`     代表方法有参数，参数类型`int`，参数名`x`

> People.h

``` objc
#import <Foundation/Foundation.h>

@interface People : NSObject
/*
 申明方法
 -、+ 方法的类型（减号代表对象方法，加号代表类方法）
 加号方法和减号方法之间的相互调用逻辑和java一样

(int) 返回值类型

 :(int) x     代表方法有参数，参数类型int，参数名x

 方法名：去掉方法类型和参数类型就是方法名
 */
- (int) report;
+ (void) report1;
- (int) showWithA:(int) a;
- (int) showWithA:(int) a andB:(int) b;
@end

```
> People.m

``` objc
#import "People.h"

@implementation People
{
    NSString *_name;
}
static NSString *_name1;
- (int)report
{
    _name = @"abc";
    NSLog(@"-号方法:report");
    return 22;
}
+ (void)report1
{
//     _name = @"abc"; 编译错误，+号方法相当于java中的静态方法
    _name1 = @"abc";//静态方法可调用静态变量
    NSLog(@"+号方法：report1");
}

- (int) showWithA:(int) a
{
    return a;
}

- (int) showWithA:(int) a andB:(int) b{
    return a + b;
}
@end
```
> main.m

``` objc
#import <Foundation/Foundation.h>
#import "People.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // [] 调用方法
        People *p1 = [[People alloc] init];
//        NSLog(@"return value %d", [p1 report]);
//        [People report1];
        int a1 = [p1 showWithA:10];
        NSLog(@"a1 = %d", a1);
        int a2 = [p1 showWithA:10 andB:20];
        NSLog(@"a2 = %d", a2);
    }
    return 0;
}
```

## 初始化函数
> People.h

``` objc
#import <Foundation/Foundation.h>

@interface People : NSObject
// 初始化方法
//- (id) init;//任意类型
//虽然上面的也可以但是推荐下面
- (instancetype) init; // 当前类型，当前是People类型

// 自定义初始化方法
- (instancetype) initPeople:(NSString *) name age:(int) age;
@end
```
> People.m

``` objc
#import "People.h"

@implementation People
{
    int _age;
    int _name;
}
// 重写初始化方法
- (instancetype)init
{
    self = [super init];
    if (self) {
        _age = 23;
        NSLog(@"age = %d", _age);
    }
    return self;
}

- (instancetype)initPeople:(NSString *)name age:(int)age
{
    self = [super init];
    if (self) {
        _age = age;
        _name = name;
        NSLog(@"age = %d, name = %@", _age, name);
    }
    return self;
}
@end
```

> main.m

``` objc
#import <Foundation/Foundation.h>
#import "People.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        People *p1 = [[People alloc] init];
        People * p2 = [[People alloc] initPeople:@"xu" age:24];
    }
    return 0;
}
```
> 输出

```
age = 23
age = 24, name = xu
```

## 封装
> 访问修饰符

|声明|作用|
|-|-|
|`@public`|公有的， 在类中和类外都可以使用并且可以被继承|
|`@private`|私有的，在类中可以使用，类外无法调用，不可以被继承|
|`@protected`|受保护的（默认），在类中可以使用，类外无法调用，但是可以被继承|
|`@package`|框架权限，在框架内相当于受保护，在框架外相当于私有|

> 方法是没有访问修饰符的同c语言一样，如果不想让外部访问，去掉`.h`中的方法定义就可以了。


> MyClass.h

``` objc
#import <Foundation/Foundation.h>

@interface MyClass : NSObject
{
    @public
    int _classInt;
}
@property(nonatomic, strong) NSString * className;
-(void) report;
@end
```
> MyClass.m

``` objc
#import "MyClass.h"

@implementation MyClass
- (void)report
{
    NSLog(@"class name = %@", _className);
    NSLog(@"class name = %d", _classInt);
}
@end
```
> main.m

``` objc
#import <Foundation/Foundation.h>
#import "MyClass.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        MyClass *c = [[MyClass alloc] init];
        c.className = @"My Class";
        // 使用指向来调用类中的公有成员变量
        c->_classInt = 22;
        [c report];
    }ß
    return 0;
}
```

## 继承
> interface 时候 冒号 代表继承

> 父类

``` objc
#import <Foundation/Foundation.h>
@interface MyClass : NSObject
{
    int _claseInt;
}
@property(nonatomic, strong) NSString * name;
- (void) report;
@end


#import "MyClass.h"
@implementation MyClass
- (void)report
{
    _claseInt = 23;
    NSLog(@"name = %@, value = %d", _name, _claseInt);
}
@end
```
> 子类

``` objc
#import "MyClass.h"
// interface 时候 冒号 代表继承
@interface MySubClass : MyClass
-(void) show;
@end


#import "MySubClass.h"
@implementation MySubClass
- (void)show
{
    _claseInt = 100;
    [self report];
}
@end
```
> main.m

``` objc
#import <Foundation/Foundation.h>
#import "MyClass.h"
#import "MySubClass.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        MyClass *c = [[MyClass alloc] init];
        c.name = @"xu";
        [c report];

        MySubClass *sc = [[MySubClass alloc] init];
        sc.name = @"xu";
//        [sc report];
        [sc show];
    }
    return 0;
}
```
> 输出

``` objc
name = xu, value = 23
name = xu, value = 23
```

## 多态
> 父类`Printer.h`  `Printer.m`

``` objc
#import <Foundation/Foundation.h>
@interface Printer : NSObject
- (void) print;
@end


#import "Printer.h"
@implementation Printer
- (void)print
{
    NSLog(@"我是一个打印机");
}
@end
```
> 子类`ColorPrinter.h`  `ColorPrinter.m`

``` objc
#import "Printer.h"
@interface ColorPrinter : Printer
@end


#import "ColorPrinter.h"
@implementation ColorPrinter
- (void)print
{
    [super print]; // 子类中调用父类的方法
    NSLog(@"我是一个彩色打印机");
}
@end
```
> main.m

``` objc
#import <Foundation/Foundation.h>
#import "ColorPrinter.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        ColorPrinter *cp = [[ColorPrinter alloc] init];
        [cp print];

        // 父类可以引用子类型
        Printer * p = [[ColorPrinter alloc] init];
        [p print];
    }
    return 0;
}
```
> 输出

``` objc
我是一个打印机
我是一个彩色打印机
我是一个打印机
我是一个彩色打印机
```
