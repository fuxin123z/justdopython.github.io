---
layout: post
category: python
title: Python 世界的黑客帝国 
tagline: by 太阳雪
tags:
  - python
---
![标题图片](http://justdopython.com/assets/images/2020/10/matrix/00.jpg)
相比于子弹时间和火爆场景，我更喜欢《黑客帝国》故事背景的假设 —— 人们熟悉的世界是虚构的，是机器给人大脑输入的幻象，而幻象是不完美的，存在一些不符合自然规律的地方，这些地方或多或少的展示了幻象世界的破绽和真实世界的样子，如果你看过《黑客帝国》动画版《超越极限》和《世界纪录》，将会有更深刻的感受

我们熟悉的、赖以生存的 Python 世界，其实也是个虚拟的，这个虚拟世界展示给我们无比绚烂的场景和功能的同时，也存在一些超乎常理和认知的地方，今天就带你一起探寻一些那些超自然点，以及它背后的真实世界
<!--more-->

## 神奇的海象操作符

海象操作符 `:=` 是 Python3.8 引入的一个新特性，意为节省一次临时变量的赋值操作，例如：

```python
a = [1,2,3,4,5]
n = len(a)
if n > 4:
    print(n)
```

意思是，如果列表 a 的长度大于 4，则打印 a 的长度，为了避免对列表长度的两次求解，利用变量 n 存储 a 的长度，合情合理

如果用 海象操作符（`:=`），会是这样：

```python
a = [1,2,3,4,5]
if n := len(n) > 4:
    print(n)
```

可以看到，省去了临时变量 n 的定义，通过海象操作符，一举两得

不得不说，Python 为能让我们提高效率，真是挖空心思，刚刚发布的 [正式版 Python3.9](https://mp.weixin.qq.com/s/xKARVrLAbDyWyBN-Kv-X9w)，也是为提升效率做了多处改善

### 海象的表演

不过，看下面的代码

```python
>>> a = "wtf_walrus"
>>> a
'wtf_walrus'

>>> a := "wtf_walrus"  # 报错！
  File "<stdin>", line 1
    a := 'wtf_walrus'
      ^
SyntaxError: invalid syntax

>>> (a := "wtf_walrus") # 奇迹发生，竟然通过了！
'wtf_walrus'
>>> a
'wtf_walrus'
```

再来一段

```python
>>> a = 6, 9  # 元组赋值
>>> a  # 结果正常
(6, 9)

>>> (a := 6, 9)  # 海象赋值，表达式结果正常
(6, 9)
>>> a  # 临时变量竟然不同
6

>>> a, b = 6, 9 # 解包赋值
>>> a, b
(6, 9)
>>> (a, b = 16, 19) # Oh no！
  File "<stdin>", line 1
    (a, b = 6, 9)
          ^
SyntaxError: invalid syntax

>>> (a, b := 16, 19) # 这里竟然打印出三员元组！
(6, 16, 19)

>>> a # 问题是 a 竟然没变
6

>>> b
16
```

### 解密海象

- **非括号表达式的海象赋值操作**
海象操作符（`:=`）适用于一个表达式内部的作用域，没有括号，相当于全局作业域，是会受到编译器限制的

- **括号里的赋值操作**
相应的，赋值操作符（`=`）不能放在括号里，因为它需要在全局作用域中执行，而非在一个表达式内

- **海象操作符的本质**
海象操作符的语法形式为 `Name := expr`，`Name` 为正常的标识符，`expr` 为正常的表达式，因此可迭代的 `装包` 和 `解包` 表现的结果会和期望不同
  - `(a := 6, 9)` 实际上会被解析为 `((a := 6), 9)`，最终，a 的值为 6，验证一下：

    ```python
    >>> (a := 6, 9) == ((a := 6), 9)
    True
    >>> x = (a := 696, 9)
    >>> x
    (696, 9)
    >>> x[0] is a # 引用了相同的值
    True
    ```

  - 同样的，`(a, b := 16, 19`) 相当于 `(a, (b := 16), 19`，原来如此

## 不安分的字符串

先建立一个感知认识

```python
>>> a = "some_string"
>>> id(a)
140420665652016
>>> id("some" + "_" + "string") # 不同方式创建的字符串实质是一样的.
140420665652016
```

奇特的事情即将发生

```python
>>> a = "wtf"
>>> b = "wtf"
>>> a is b
True

>>> a = "wtf!"
>>> b = "wtf!"
>>> a is b  # 什么鬼！
False
```

如果将这段代码写入脚本文件，用 Python 运行，结果却是对的：

```python
a = "wtf!"
b = "wtf!"
print(a is b)  # 将打印出 True
```

还有更神奇的，在 Python3.7 之前的版本中，会有下面的现象:

```python
>>> 'a' * 20 is 'aaaaaaaaaaaaaaaaaaaa'
True
>>> 'a' * 21 is 'aaaaaaaaaaaaaaaaaaaaa'
False
```

20 个字符 `a` 组合起来等于 20个 `a` 的字符串，而 21 个就不相等

![](http://justdopython.com/assets/images/2020/10/matrix/01.jpg)

### 揭秘字符串

计算机世界里，任何奇特的现象都有其必然原因

- 这些字符串行为，是由于 Cpython 在编译优化时，某些情况下会对不可变的对象做存储，新建时之间建立引用，而不是创建新的，这种技术被称作 **字符串驻留(string interning)**，这样做可以节省内存和提高效率

- 上面代码中，字符串被隐式驻留了，什么情况下才会被驻留呢？
  - 所有长度为 0 和 1 的字符串都会被驻留
  - 字符串在编译时被驻留，运算中不会（`"wtf"` 会驻留，`"".join("w", "t", "f")` 则不会）
  - 只有包含了字母、数值和下划线的字符串才会被驻留，这就是为什么 `"wtf!"` 不会被驻留的原因（其中还有字符 `!`）

- 如果 a 和 b 的赋值 "wtf!" 语句在同一行，Python 解释器会创建一个对象，然后让两个变量指向这个对象。如果在不同行，解释器就不知道已经有了 `"wtf!"` 对象，所以会创建新的（原因是 `"wtf!"` 不会被驻留）

- 像 IPython 这样的交互环境中，语句是单行执行的，而脚本文件中，代码是被同时编译的，具有相同的编译环境，所以就能理解，代码文件中不同行的不被驻留字符串引用同一个对象的现象

- 常量折叠（constant folding）是 Python 的一个优化技术：窥孔优化(peephole optimization)，如 `a = "a"*20`，这样的语句会在编译时展开，以减少运行时的运行消耗，为了不至于让 pyc 文件过大，将展开字符限制在 20 个以内，不然想想这个 `"a"*10**100` 语句将产生多大的 pyc 文件

- 注意 Python3.7 以后的版本中 常量折叠 的问题得到了改善，不过还不清楚具体原因（矩阵变的更复杂了）

## 小心链式操作

来一段骚操作

```python
>>> (False == False) in [False] # 合乎常理
False
>>> False == (False in [False]) # 也没问题
False
>>> False == False in [False] # 现在感觉如何?
True

>>> True is False == False
False
>>> False is False is False
True

>>> 1 > 0 < 1
True
>>> (1 > 0) < 1
False
>>> 1 > (0 < 1)
False
```

不知到你看到这段代码的感受，反正我看第一次到时，怀疑我学的 Python 是假冒的~

### 到底发生了什么

按照 Python 官方文档，表达式章节，值比较小节的描述（https://docs.python.org/2/reference/expressions.html#not-in）：

> 通常情况下，如果 a、b、c、...、y、z 是表达式，op1、op2、...、opN 是比较运算符，那么 `a op1 b op2 c ... y opN z` 等价于 `a op1 b and b op2 c and ... y opN z`，除了每个表达式只被计算一次的特性

基于以上认知，我们重新审视一下上面看起来让人迷惑的语句：

- `False is False is False` 等价于 `(False is False) and (False is False)`
- `True is False == False` 等价于 `True is False and False == False`，现在可以看出，第一部分 `True is False` 的求值为 `False`， 所以整个表达式的值为 `False`
- `1 > 0 < 1` 等价于 `1 > 0 and 0 < 1`，所以表达式求值为 `True`
- 表达式 `(1 > 0) < 1` 等价于 `True < 1`，另外 `int(True)` 的值为 1，且 `True + 1` 的值为 2，那么 `1 < 1` 就是 `False` 了

## 到底 is(是) 也不 is(是)

我直接被下面的代码惊到了

```python
>>> a = 256
>>> b = 256
>>> a is b
True

>>> a = 257
>>> b = 257
>>> a is b
False
```

再来一个

```python
>>> a = []
>>> b = []
>>> a is b
False

>>> a = tuple()
>>> b = tuple()
>>> a is b
True
```

同样是数字，同样是对象，待遇咋就不一样尼……

我们逐一理解下

### is 和 == 的区别

- `is` 操作符用于检查两个变量引用的是否同一个对象实例
- `==` 操作符用于检查两个变量引用对象的值是否相等
- 所以 `is` 用于引用比较，`==` 用于值比较，下面的代码能更清楚的说明这一点:

  ```python
  >>> class A: pass
  >>> A() is A()  # 由于两个对象实例在不同的内存空间里，所以表达式值为 False
  False
  ```

### 256 是既存对象，而 257 不是

这个小标题让人很无语，还确实对象和对象不一样

在 Python 里 从 -5 到 256 范围的数值，是预先初始化好的，如果值为这个范围内的数字，会直接建立引用，否则就会创建

这就解释了为啥 同样的 257，内存对象不同的现象了

为什么要这样做？官方的解释为，这个范围的数值比较常用（https://docs.python.org/3/c-api/long.html）

### 不可变的空元组

和 -5 到 256 数值预先创建一样，对于不可变的对象，Python 解释器也做了预先创建，例如 对空的 Tuple 对象

这就能解释为什么 空列表对象之间引用不同，而空元组之间的引用确实相同的现象了

## 被吞噬的 Javascript

先看看过程

```python
some_dict = {}
some_dict[5.5] = "Ruby"
some_dict[5.0] = "JavaScript"
some_dict[5] = "Python"

print(some_dict[5.5])  # Ruby
print(some_dict[5.0])  # Python  Javascript 去哪了？
```

### 背后的原因

- Python 字典对象的索引，是通过键值是否相等和比较键的哈希值来进行查找的
- 具有相同值的不可变对象的哈希值是相同的

  ```python
  >>> 5 == 5.0
  True
  >>> hash(5) == hash(5.0)
  True
  ```

- 于是我们就能理解，当执行 `some_dict[5] = "Python"` 时，会覆盖掉前面定义的 `some_dict[5.0] = "Javascript"`，因为 5 和 5.0 具有相同的哈希值

> 需要注意的是：有可能不同的值具有相同的哈希值，这种现象被称作 **哈希冲突**

关于字典对象使用哈希值作为索引运算的更深层次的原因，有兴趣的同学可以参考 StackOverflow 上的回答，解释的很精彩，网址是：`https://stackoverflow.com/questions/32209155/why-can-a-floating-point-dictionary-key-overwrite-an-integer-key-with-the-same-v/32211042`

## 总结

限于篇幅（精力）原因，今天就介绍这几个 Python 宇宙中的异常现象，更多的异常现象，收录在 satwikkansal 的 wtfpython 中（https://github.com/satwikkansal/wtfpython）。

任何华丽美好的背后都是各种智慧、技巧、妥协、辛苦的支撑，不是有那么一句话嘛：如果你觉得轻松自如，比如有人在负重前行。而这个人就是我们喜爱的 Python 及其 编译器，要更好的理解一个东西，需要了解它背后的概念原理和理念，期望通过这篇短文对你有所启发

> 本文代码测试版本为 Python3.8.2，实践中遇到问题，可留言或在交流群讨论

## 参考

- <https://github.com/satwikkansal/wtfpython>
- <https://docs.python.org/2/reference/expressions.html#not-in>
- <https://docs.python.org/3/c-api/long.html>
- <https://github.com/leisurelicht/wtfpython-cn>

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/matrix>
