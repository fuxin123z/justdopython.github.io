---
layout: post
category: python
title: 第16天：初识 Python 多线程 
tagline: by 程序员野客
tags: 
  - python100
---

我们知道，多线程与单线程相比，可以提高 CPU 利用率，加快程序的响应速度。

<!--more-->

单线程是按顺序执行的，比如用单线程执行如下操作：

```
6秒读取文件1
9秒处理文件1
5秒读取文件2
8秒处理文件2
```

总共用时 28 秒，如果开启两条线程来执行上面的操作（假设处理器为多核 CPU），如下所示：

```
6秒读取文件1 + 5秒读取文件2
9秒处理文件1 + 8秒处理文件2
```

只需 15 秒就可完成。

## 1 GIL

### 1.1 什么是 GIL ？

GIL 全称 Global Interpreter Lock（全局解释器锁），是 Python 解释器 CPython 中引入的一个概念，下面看一下官方解释：


In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing
Python bytecodes at once. This lock is necessary mainly because CPython’s memory management is not thread-safe.
(However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)


从上面解释中，我们了解到：GIL 是一个防止解释器多线程并发执行机器码的一个全局互斥锁，其存在主要是因为在代码执行过程中，CPython 的内存管理不是线程安全的。

什么是 CPython 呢？我们从 Python 官方网站下载安装 Python 后，获得的官方解释器就是 CPython ，因其是 C 开发的，故名为 CPython ，是使用最广泛的 Python 解释器。然而因为 CPython 是大部分环境下的默认解释器，有些人会认为 CPython 就是 Python ，从而误以为 GIL 是 Python 的特性，在这里我们要明确一个概念：GIL 不是 Python 特性，Python 可以完全不依赖 GIL 。除了 CPython 解释器，还有：PyPy、Psyco、JPython 等解释器，像 JPython 解释器就没有 GIL。

### 1.2 GIL 带来哪些影响？

通过上面的介绍我们了解到 GIL 是一个全局互斥锁，很明显 GIL 的存在会对多线程的效率有很大影响，甚至在 CPython 下，Python 的多线程几乎等于单线程。到底实际效果如何呢？我们通过下面的示例来看一下：

```
# 单线程
from threading import Thread
import os,time

def task():
    ret = 0
    for i in range(100000000):
        ret *= i
if __name__ == '__main__':
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(5):
        task()
    stop = time.time()
    print('单程耗时 %s' % (stop - start))
    
# 测试结果：
'''
本机为 4 核 CPU
单线程耗时 23.19068455696106
'''
```

```
# 多线程
from threading import Thread
import os,time

def task():
    ret = 0
    for i in range(100000000):
        ret *= i
if __name__ == '__main__':
    arr = []
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(5):
        p = Thread(target=task)
        arr.append(p)
        p.start()
    for p in arr:
        p.join()
    stop = time.time()
    print('多线程耗时 %s' % (stop - start))
    
# 测试结果：
'''
本机为 4 核 CPU
多线程耗时 25.024707317352295
'''
```

通过实际测试结果，我们发现在 CPython 环境下，多线程比单线程花费的时间还要多。

### 1.3 如何解决 GIL 带来的影响？

现在，我们已经了解了在 CPython 环境下，Python 多线程几乎发挥不出多核 CPU 的优势？GIL 是 CPython 的设计缺陷，简直如 bug 一般的存在；那如何解决 GIL 带来的影响呢？有没有现成的解决方案呢？我们来具体看一下：

1）multiprocess 代替 thread

multiprocess 库的出现很大程度上是为了弥补 thread 库因为 GIL 而低效的缺陷；它完整的复制了一套 thread 所提供的接口方便迁移，唯一的不同就是它使用了多进程而不是多线程，每个进程有自己的独立的 GIL ，因此不会出现进程之间的 GIL 争抢。

2）使用其他解释器

上面我们说了 GIL 是 CPython 解释器中引入的，那么，我们使用没有 GIL 的解释器不就可以了，如：之前提到的 JPython ，还有 IronPython ；然而这两个解释器使用 Java/C# 实现，也就失去了利用社区众多 C 语言模块有用特性的机会，导致这种方式还是比较小众。

3）等待官方解决

对于 CPython 的 GIL 问题，Python 社区也一直在不断努力的去尝试改进 GIL 。

## 2 任务类型

### 2.1 计算密集型任务

计算密集型任务的特点是要进行大量的计算，消耗 CPU 资源，比如：计算圆周率、对视频进行解码 ... 全靠 CPU 的运算能力。上面单线程与多线程对比的例子就是计算密集型任务，我们看下通过使用 Python 多进程的耗时情况：

```
# 计算密集型任务-多进程
from multiprocessing import Process
import os,time

def task():
    ret = 0
    for i in range(100000000):
        ret *= i
if __name__ == '__main__':
    arr = []
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(5):
        p = Process(target=task)
        arr.append(p)
        p.start()
    for p in arr:
        p.join()
    stop = time.time()
    print('计算密集型任务，多进程耗时 %s' % (stop - start))
    
# 输出结果
'''
本机为 4 核 CPU
计算密集型任务，多进程耗时 14.087027311325073
'''
```

### 2.2 I/O 密集型任务

涉及到网络、磁盘 I/O 的任务都是 I/O 密集型任务，这类任务的特点是 CPU 消耗很少，任务的大部分时间都在等待 I/O 操作完成（因为 I/O 的速度远远低于 CPU 和内存的速度）。通过下面例子看一下耗时情况：

```
# I/O 密集型任务-多进程
from multiprocessing import Process
import os,time

def task():
    f = open('tmp.txt','w')
if __name__ == '__main__':
    arr = []
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(500):
        p = Process(target=task)
        arr.append(p)
        p.start()
    for p in arr:
        p.join()
    stop = time.time()
    print('I/O 密集型任务，多进程耗时 %s' % (stop - start))
	
# 输出结果
'''	
本机为 4 核 CPU
I/O 密集型任务，多进程耗时 21.05265736579895
'''
```

```
# I/O 密集型任务-多线程
from threading import Thread
import os,time

def task():
    f = open('tmp.txt','w')
if __name__ == '__main__':
    arr = []
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(500):
        p = Thread(target=task)
        arr.append(p)
        p.start()
    for p in arr:
        p.join()
    stop = time.time()
    print('I/O 密集型任务，多进程耗时 %s' % (stop - start))
	
# 输出结果
'''
本机为 4 核 CPU
I/O 密集型任务，多线程耗时 0.24960064888000488
'''
```

```
# I/O 密集型任务-单线程
from threading import Thread
import os,time

def task():
    f = open('tmp.txt','w')
if __name__ == '__main__':
    arr = []
    print('本机为',os.cpu_count(),'核 CPU')
    start = time.time()
    for i in range(500):
        task()
    stop = time.time()
    print('I/O 密集型任务，多进程耗时 %s' % (stop - start))
	
# 输出结果
'''
本机为 4 核 CPU
I/O 密集型任务，单线程耗时 0.2964005470275879
'''
```

通过上面的测试结果我们发现：对于计算密集型任务，多进程耗时更短；对于 I/O 密集型任务，多线程耗时更短（单线程耗时与多线程耗时接近）。

对于一个运行的程序来说，随着 CPU 的增加执行效率必然会有所提高，因此大多数时候，一个程序不会是纯计算或纯 I/O ，所以我们只能相对的去看一个程序是计算密集型还是 I/O 密集型。

## 总结

本节给大家介绍了 Python 多线程，让大家对 Python 多线程现状有了一定了解，能够根据任务类型选择更加高效的处理方式。

参考：

[https://www.cnblogs.com/SuKiWX/p/8804974.html](https://www.cnblogs.com/SuKiWX/p/8804974.html)

