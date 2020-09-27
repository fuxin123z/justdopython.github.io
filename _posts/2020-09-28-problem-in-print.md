# Python少有人走过的坑

毫无疑问，`print`函数是我们日常最常用的函数，无论是格式化输出还是打印中间变量进行调试，几乎没有`print`接不了的活儿。

但是上一次阿酱就差点被`print`给坑了。

## 坑从何来

最初是想要为自己的一个命令行小工具增加一个进度显示功能，于是用了`threading`模块来实现多线程，一个线程用于执行实际的逻辑，另一个线程用于打印当前进度。

![01](http://www.justdopython.com/assets/images/2020/09/problem_in_print/01.gif)

根据我们~~多年~~使用命令行的经验，一般打印进度都是在行内打印，而Python的`print`则会默认在结尾打印一个换行符，这就十分不美了。

不过好在，`print`也提供了接口来改变打印的末尾字符，通过指定`print`的`end`参数，即可改变`print`的打印结果。

所以我就哼哧哼哧地开干了，把打印进度的`print("#")`调用改为`print("#", end="")`。

类似这样：

```python
import time
import threading

def print_sharp():
    while True:
        time.sleep(0.5)
        print("#", end="")


t1 = threading.Thread(target=print_sharp)
t1.setDaemon(True)
t1.start()

time.sleep(5)

```

哪成想，这么一改却出了大问题：进度没法实时打印了。

![02](http://www.justdopython.com/assets/images/2020/09/problem_in_print/02.jpg)

也就是说，本来应该在程序执行期间，挨个打印出来的`#`号不再是听话的、可爱的`#`号了，而是在整个程序执行完成之后一次性输出到控制台中。

它长大了，**也变丑了**。

![03](http://www.justdopython.com/assets/images/2020/09/problem_in_print/03.gif)

那我要你有何用？

![04](http://www.justdopython.com/assets/images/2020/09/problem_in_print/04.jpg)

## 啥问题呢？

一开始阿酱以为是多线程出了问题，傻乎乎地到处找资料来“佐证”自己的各种猜测——事后想来实在太傻了，以至于现在说起还是会哈哈哈

![05](http://www.justdopython.com/assets/images/2020/09/problem_in_print/05.jpg)

这件事给我们的教训就是：**千万不要自以为是，而应踏踏实实地解决问题，虚心对待每个细节**。

实际上，之所以我们看不到实时的输出，就是因为我们改变了`print`的结尾字符。

为了尽量减少I/O操作，Python存在一个这样的机制：尽量将输出字符缓存起来，当遇到字符串结束、换行符或强制刷新缓冲区时，才会一次性将缓冲区的内容输出到相应的流中。

——而我们改掉的地方，就是把`print`默认的换行符去掉了，所以原本每一个`print`都会触发一次缓冲区刷新，变成了现在一直触发不了缓冲区刷新，直到程序结束触发一次。

好嘛，知道了啥问题，我们又吭哧吭哧找资料，听说`sys.stdout.flush`可以强制触发标准输出缓冲区的刷新，于是在`print`后面，紧跟着又加上了`sys.stdout.flush()`。

诶？还真好了？

![06](http://www.justdopython.com/assets/images/2020/09/problem_in_print/06.gif)

这些可都是知识点，快记下来记下来，要考的

![07](http://www.justdopython.com/assets/images/2020/09/problem_in_print/07.jpg)

让我们查看`print`的官方文档，其原型为：

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

根据其下的描述，Python中`print`的输出是否进行缓冲，取决于两个参数：`file`和`flush`。

`file`的类型有的需要缓冲，比如`sys.stdout`；而有的则不需要缓冲，比如`sys.stderr`。

对于`flush`参数，当其值为`False`（默认）时，是否缓冲依赖`file`；而当其值为`True`时，则会强制刷新缓冲区。

我们把示例调用中的`print`调用修改一下：

```python
import sys
import time
import threading


def print_sharp():
    while True:
        time.sleep(0.5)
        print("#", end="", flush=True)


t1 = threading.Thread(target=print_sharp)
t1.setDaemon(True)
t1.start()

time.sleep(5)

```

![08](http://www.justdopython.com/assets/images/2020/09/problem_in_print/08.gif)

同样可以实现进度的实时打印。

此外，还有一种方法，在调用程序时增加一个`-u`选项，也可以实现缓冲区的实时刷新：

```shell
$ python -u no_flush.py
```

![09](http://www.justdopython.com/assets/images/2020/09/problem_in_print/09.gif)

当然这种方法就不太推荐了，毕竟不能对程序的使用者作任何预设。

## 总结

本文是阿酱的一次踩坑实录，记录了Python中一个很少有人会遇到的奇葩问题。

总的来说，要想成为一个真正的Python程序员，只是单纯掌握基本语法和一些奇技淫巧是远远不够的，还是需要对Python本身有一定的了解。

毕竟，剑客如果不熟悉自己的剑，又该如何行走江湖呢？

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-09-28-problem-in-print>