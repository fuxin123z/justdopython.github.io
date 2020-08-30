---
layout: post
category: python
title: 你只知道with，那with该with who呢？
tagline: by 轩辕御龙
tags:
  - python
---

# 你只知道with，那with该with who呢？

在长期的编程实践中，我们必然已经有过使用下面这段代码的经验：

```python
with open("test.txt", "r", encoding="utf-8") as f:
    s = f.readlines()
```

有的人知道这么写的原因；但也有很多人不知道，只是单纯地“别人都这么写，我也应该这么写”。

同时，很多知道原因的人也只是知其然而不知其所以然：with语句可以替我们自动关闭打开的文件对象。但是这是通过什么机制办到的呢？

<!--more-->

## 1. with和异常处理

我们知道，如果不使用with语句的话，正常地读写一个文件应该经过这些过程：打开文件、操作文件、关闭文件。表达为Python代码如下：

```python
f = open("test.txt", "r", encoding="utf-8")
s = f.readlines()
f.close()
```

在正常情况下，这样写看起来也没啥问题。

接下来我们就人为制造一点“意外”：把打开文件对象时指定的模式由“r”改为“w”。

```python
f = open("test.txt", "w", encoding="utf-8")
s = f.readlines()
f.close()
```

此时，当程序执行到第2行读取文件内容时，就会抛出错误：

```shell
Traceback (most recent call last):
  File "test_with.py", line 2, in <module>
    s = f.readlines()
io.UnsupportedOperation: not readable
```

然后……一个可怕的情况就发生了。

Python产生未处理的异常从而退出了，导致第2行之后的代码尚未执行，因此**`f.close()`**也就再也没有机会执行。一个孤魂野鬼般打开的文件对象就这样一个人漂泊在内存的汪洋大海中，没有人知道他是谁、他从哪儿来、他要去哪儿。

就这样，每当抛出一次异常，就会产生这么一个流浪对象。久而久之，内存的汪洋大海也就顺理成章被改造成了流浪者的乐土，其他人想来压根儿没门儿。

追根究底，我们发现导致这个问题的关键在于“打开-操作-关闭”文件这个流水操作中，存在抛出异常的可能。

所以我们想到了使用Python为我们提供的大杀器，来对付这些异常：try-catch。

用异常处理改造一下前面的代码：

```python
try:
    f = open("test.txt", "a", encoding="utf-8")
    s = f.readlines()
except:
    print("出现异常")
finally:
    f.close()
```

这样一来，通过附加的`finally`语句，无论文件操作是否抛出异常，都能够保证打开的文件被关闭。从而避免了不断占用资源导致资源泄露的问题。

实际上，with语句正是为我们提供了一种`try-catch-finally`的封装。

编程时，看似只是随随便便的一个with，其实已经暗地里确保了类似于上面代码的异常处理机制。

## 2. 上下文管理器

with要生效，需要作用于一个上下文管理器——

打住，到底什么是上下文管理器呢？

长话短说，就是实现了`__enter__`和`__exit__`方法的对象。

在进入一个运行时上下文前，会先加载这两个方法以备使用。进入这个运行时上下文时，调用`__enter__`方法；退出该上下文前，则会调用`__exit__`方法。

这里的“运行时上下文”，可以简单地理解为一个提供了某些特殊配置的代码作用域。

当我们使用`with open("test.txt", "r", encoding="utf-8") as f`这句代码时，Python首先对`open("test.txt", "r", encoding="utf-8")`求值，得到一个上下文管理器。

这里有一点特殊的是，Python中文件对象本身就是一个上下文管理器，因此我们可以使用`open`函数作为求值的表达式。

随后调用`__enter__`方法，返回的对象绑定到我们指定的标识符`f`上。文件对象的`__enter__`返回文件对象自身，因此这句代码就是将打开的“test.txt”文件对象绑定到了标识符`f`上。

紧跟着执行with语句块中的内容。

最后调用`__exit__`，退出with语句块。

根据上面的内容，我们也可以自行构造一个上下文管理器（注意，两个特征方法的参数要与协议一致）：

```python
class testContextManager:
    def __enter__(self):
        print("进入运行时上下文，调用__enter__方法")

    def __exit__(self, exc_type, exc_value, traceback):
        print("退出运行时上下文，调用__exit__方法")


with testContextManager() as o:
    pass
```

输出结果：

```shell
进入运行时上下文，调用__enter__方法
退出运行时上下文，调用__exit__方法
```

with语句之所以能够替代繁琐的异常处理语句，正是由于上下文管理器遵循协议实现了`__enter__`和`__exit__`方法，而with语句又确保了发生异常时能够执行完`__exit__`方法，再退出相关运行时上下文。

在这个方法中，我们就可以完成一些必要的清理工作。

## 总结

本文我们讲解了with语句的内部逻辑，尝试实现了一个自定义的上下文管理器。相信大家对于with的作用方式有了更深刻的领会。

with语句不仅仅可以用于读写文件，还可以用于锁的自动获取和释放、全局状态的保存和恢复等。更多的实用方式留待大家探索。

## 参考

[官方文档：8.5. `with` 语句](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement)

[官方文档：3.3.9. with 语句上下文管理器](https://docs.python.org/zh-cn/3/reference/datamodel.html#with-statement-context-managers)

[官方文档：上下文管理器类型](https://docs.python.org/zh-cn/3/library/stdtypes.html#typecontextmanager)

示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-08-24-python-with-statement>