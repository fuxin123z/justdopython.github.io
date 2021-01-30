---
layout: post
category: python
title: 吐血整理的Python 面试题，请务必收藏！
tagline: by 潮汐
tags:
  - python
---

年关将至，给年后准备跳槽的准备一份面试指南，希望大家在涨薪和成神的路上多一点指引！

<!--more-->
### python2和python3区别？
- Python3 使用 print 必须要以小括号包裹打印内容，比如 print('hi')

- Python2 既可以使用带小括号的方式，也可以使用一个空格来分隔打印内容，比如 print 'hi'

- python2 range(1,10)返回列表，python3中返回迭代器，节约内存

- python2 中使用 ascii 编码，python中使用 utf-8 编码

- python2 中 unicode 表示字符串序列，str 表示字节序列

- python3 中 str 表示字符串序列，byte 表示字节序列

- python2 中为正常显示中文，引入 coding 声明，python3 中不需要

- python2 中是 raw_input()函数，python3 中是input()函数

### Python代码中_args, *_kwargs 含义及用法？

**args：** arguments 的缩写，表示位置参数

**kwargs：** keyword arguments 的缩写，表示关键字参数

### 请列出 5 个 python 标准库？
- os：提供了不少与操作系统相关联的函数
- sys:   通常用于命令行参数
- re:   正则匹配
- math: 数学运算
- datetime:处理日期时间

### Python的可变数据类型和不可变数据类型分别有？

可变数据类型：列表、字典、集合

不可变数据类型：数字、字符串、元组

### Python中魔法方法和其用途？

`__init__`：对象初始化方法

`__new__`：创建对象时候执行的方法，单列模式会用到

`__str__`:当使用print输出对象的时候，只要自己定义了__str__(self)方法，那么就会打印从在这个方法中return的数据

`__del__`：删除对象执行的方法

### Python 中os和sys模块的作用分别是？

os模块：负责程序与操作系统的交互，提供了访问操作系统底层的接口。
sys模块：负责程序与python解释器的交互，提供了一系列的函数和变量，用于操控python的运行时环境。

### 简述Python引用计数机制？

python垃圾回收主要以引用计数为主，标记-清除和分代清除为辅的机制，其中标记-清除和分代回收主要是为了处理循环引用的难题。


### Python赋值、浅拷贝和深拷贝的区别？

Python 有 3 种赋值方式：直接赋值、浅拷贝、深拷贝；

直接赋值：就是对象的引用。（相当于给原来的对象起个别名），比如有个人叫张三，外号叫小张，对象的引用就是类似，虽然换个名字，但是两个名字指的是同一个人。

浅拷贝，拷贝的是父对象，不会拷贝到内部的子对象。（单从`浅`字就可以看出拷贝的东西不深，可以理解为只拷贝一层）
{
1、完全切片方法；2、工厂函数，如 list()；3、copy 模块的 copy()函数
}


深拷贝，包含对象里面的自对象的拷贝（可以理解为克隆，全拷贝过去但是两者没有任何关系了，各自是各自的）；
所以原始对象的改变不会造成深拷贝里任何子元素的改变
{
copy 模块的 `deep.deepcopy()`函数
}


### 请阐述在Python中split()，sub()，subn()的功能分别是什么？

**split()：** 使用正则表达式模式将给定字符串“拆分”到列表中。

**sub()：** 查找正则表达式模式匹配的所有子字符串，然后用不同的字符串替换它们

**subn()：** 它类似于sub()，并且还返回新字符串。

### 举例 sort 和 sorted方法的区别？

使用 sort()方法对 list 排序会修改 list 本身,不会返回新 list，sort()不能对 dict 字典进行排序；

sorted 方法对可迭代的序列排序生成新的序列，对 dict 排序默认会按照 dict 的 key 值进行排序，最后返回的结果是一个对 key 值排序好的list；

sorted 对 tuple， dict 依然有效，而 sort 不行；

### 解释 Python 中的可变类型和不可变类型？

1.Python中的可变类型有list,dict；不可变类型有string，number,tuple.

2.当进行修改操作时，可变类型传递的是内存中的地址，也就是说，直接修改内存中的值，并没有开辟新的内存。

3.不可变类型被改变时，并没有改变原内存地址中的值，而是开辟一块新的内存，将原地址中的值复制过去，对这块新开辟的内存中的值进行操作。

### Python中类方法、类实例方法、静态方法有何区别？

**类方法:** 是类对象的方法，在定义时需要在上方使用 `@classmethod` 进行装饰,形参为`cls`，表示类对象，类对象和实例对象都可调用

**类实例方法:** 是类实例化对象的方法,只能由实例对象调用，形参为`self`,指代对象本身;

**静态方法:** 是一个任意函数，在其上方使用 `@staticmethod` 进行装饰，实例对象和类对象都可以调用。但是方法体中不能使用类或实例的任何属性和方法。

### Python 中编写函数的原则？
Python 中编写函数的原则有**4**个，分别有：

 - 函数设计要尽量短小，嵌套层次不宜过深。避免过长函数，嵌套最好能控制在3层之内

- 函数申明应该合理，简单，易于使用。除函数名能够够正确反映其大体功能外，参数的设计也应该简洁明了，参数个数不宜太多

- 函数参数设计应该考虑向下兼容。可以通过加入默认参数来避免退化

- 一个函数只做一件事，就要尽量保证抽象层级的一致性，所有语句尽量在一个粒度上。若在一个函数中处理多件事，不利于代码的重用；

### 请阐述同步，异步，阻塞，非阻塞的概念？
- **同步：** 多个任务之间有先后顺序执行，一个执行完下个才能执行。

- **异步：** 多个任务之间没有先后顺序，可以同时执行，有时候一个任务可能要在必要的时候获取另一个同时执行的任务的结果，这个就叫回调！

- **阻塞：** 如果卡住了调用者，调用者不能继续往下执行，就是说调用者阻塞了。

- **非阻塞：** 如果不会卡住，可以继续执行，就是说非阻塞的。

同步异步相对于多任务而言，阻塞非阻塞相对于代码执行而言。

### 合并两个列表并去除重复元素？
```
list1 = ['b','c','c','a','f','r','y','e','e']
list2 = ['t','y','x','y','z','e','f']
def merge_list(*args):
    s = set()
    for i in args:
        s = s.union(i)
    print(s)
    return s

merge_list(list1,list2)
```

### 如何查询和替换一个文本中的字符串?
```
tempstr = "hello python,you,me,world"
print(tempstr.replace("hello","python"))

#还可以使用正则,有个sub()
tempstr = "hello python,you,me,world"
import re
rex = r'(hello|Use)'
print(re.sub(rex,"HELLO",tempstr))
```

### 总结

关于 Python 的面试问题还有很多很多，今天小编暂且总结到这里，希望对大家有所帮助。

### 参考
[https://github.com/DasyDong/interview/blob/master/notes/python_interview.md](https://github.com/DasyDong/interview/blob/master/notes/python_interview.md)
