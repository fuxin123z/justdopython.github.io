---
layout: post
category: python
title: 当我print时，Python做了什么
tagline: by 轩辕御龙
tags:
  - python
---

# 当我print时，Python做了什么

写了这么久的程序，不知道大家有没有思考过，Python到底在干嘛呢？

或者换句话说，当我们执行Python代码的时候，是怎么实现的呢？

<!--more-->

众所周知，Python是一门解释型的语言

——所谓“解释型”，当然是区别于以C语言为代表的编译型语言。编译型语言需要将整个程序文件全部转换为可以直接由机器执行的二进制文件；而解释型语言则是由相应的解释器一行一行“解释”并执行代码描述的行为。

正是因此，对于新接触的人来说，Python这样的解释性语言很多时候需要执行到相应的语句，才会发现一些显然的错误。

话说回来，Python的解释器是怎么样来“解释”Python代码的呢？

实际上，类似于Java的执行机制，Python也拥有自己的虚拟机。而这个虚拟机实际上执行的也是一种“字节码”。

在Python程序的执行中依然存在一个“编译”的过程：将Python代码编译为字节码。

并且，Python也提供了一个名为`dis`模块，用于查看、分析Python的字节码。

## 1. `dis`模块

举例来说，`dis`模块中有一个同名函数`dis`，可以用于将当前命名空间中的对象反汇编为字节码。

```python
import dis

def add(add_1, add_2):
    sum_value = add_1 + add_2

dis.dis(add)
```

执行结果为：

```shell
  4           0 LOAD_FAST                0 (add_1)
              2 LOAD_FAST                1 (add_2)
              4 BINARY_ADD
              6 STORE_FAST               2 (sum_value)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
```

其中，开头的数字“4”表示字节码的内容对应于脚本中第4行的内容。

随后的一列数字则表示对应指令所在的地址。纵向观察可以发现一个规律：下一条指令的地址总比上一条指令的地址大2。这是巧合吗？

显然不是的。官方文档《[dis --- Python 字节码反汇编器](https://docs.python.org/zh-cn/3/library/dis.html)》中记录的更改显示，从Python 3.6版本开始，”每条指令使用2个字节“。所以每条指令的地址会在上一条指令地址的基础上加2。

再往后，是一列表示指令含义的单词组合，实际上就是人类可读的对应指令名称。顾名思义，`LOAD_FAST`就是加载某个内容/对象到某处，”FAST“很可能意味着这是一个便捷快速的命令实现。

最右边，则是对应于当前命令的操作数，即操作对象。数字同样是一个类似于地址的表示，括号中的字符串则表示相应对象在Python代码中的具体名称。

这样我们就可以大概地阅读生成的字节码了：

首先Python将函数`add`的第一个参数`add_1`加载到某处，紧跟着将第二个参数`add_2`加载到第一个参数之后。然后调用了一个名为`BINARY_ADD`的指令，即对之前加载的两个参数做加法。再然后则是将加法所得的和`sum_value`存储在了另一个位置。最后，加载了一个常量`None`并返回。

其实读完上面这个执行过程，我们很容易想到一种常用的数据结构——栈。

像下面这样：

![01](http://www.justdopython.com/assets/images/2020/08/dis/01.gif)

当然这并不是本文的重点——真要探讨Python的实现机制，还得另外写几篇长文才能说得一二。

使用`dis.dis`函数除了可以查看当前脚本中各个对象对应的字节码，还可以直接传入一段代码对应的字符串进行反汇编：

```python
# test_dis.py
import dis


s = """
def add(add_1, add_2):
    sum_value = add_1 + add_2

print("Hello World!")

import sys
"""

dis.dis(s)
```

汇编结果：

```shell
  2           0 LOAD_CONST               0 (<code object add at 0x0000019FF66DFDB0, file "<dis>", line 2>)
              2 LOAD_CONST               1 ('add')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (add)

  5           8 LOAD_NAME                1 (print)
             10 LOAD_CONST               2 ('Hello World!')
             12 CALL_FUNCTION            1
             14 POP_TOP

  7          16 LOAD_CONST               3 (0)
             18 LOAD_CONST               4 (None)
             20 IMPORT_NAME              2 (sys)
             22 STORE_NAME               2 (sys)
             24 LOAD_CONST               4 (None)
             26 RETURN_VALUE
```

## 2. `compile`函数

除了在程序中直接给出要反汇编的程序形成的字符串，我们还可以通过使用内置函数`compile`来形成相应脚本的编译对象，再使用`dis.dis`查看其字节码内容。

```python
# test_compile.py
import dis

with open("test_dis.py", "r", encoding="utf-8") as f:
    s = f.read()

compile_obj = compile(s, "test_dis.py","exec")

dis.dis(compile_obj)
```

字节码输出结果：

```shell
  1           0 LOAD_CONST               0 (0)
              2 LOAD_CONST               1 (None)
              4 IMPORT_NAME              0 (dis)
              6 STORE_NAME               0 (dis)

 11           8 LOAD_CONST               2 ('\ndef add(add_1, add_2):\n    sum_value = add_1 + add_2\n\nprint("Hello World!")\n\nimport sys\n')
             10 STORE_NAME               1 (s)

 13          12 LOAD_NAME                0 (dis)
             14 LOAD_METHOD              0 (dis)
             16 LOAD_NAME                1 (s)
             18 CALL_METHOD              1
             20 POP_TOP
             22 LOAD_CONST               1 (None)
             24 RETURN_VALUE
```

## 总结

`dis`模块为我们提供了一个观察Python内部机制的手段，恰当地使用`dis`模块，并结合其他方法，可以快速有效弄懂一些Python令人迷惑的地方。

希望大家善于利用这样一些有用的工具。

## 参考

[dis --- Python 字节码反汇编器](https://docs.python.org/zh-cn/3/library/dis.html)

[谈谈 Python 程序的运行原理](https://www.cnblogs.com/restran/p/4903056.html)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-08-24-python-dis-bytecode>