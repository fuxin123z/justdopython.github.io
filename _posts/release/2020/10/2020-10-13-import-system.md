---
layout: post
category: python
title: 学了半天，`import`到底在干啥？
tagline: by 轩辕御龙
tags:
  - python
---

# 学了半天，`import`到底在干啥？

Python凭什么就那么好用呢？

毫无疑问，大量现成又好用的内置/第三方库功不可没。

那我们是怎么使用它们的呢？

噢，对了~是用的`import xxx`这个语句。

<!--more-->

之所以会有此一问，也是之前有一次使用PyCharm进行开发时（又）踩了个坑……

![01](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/01.jpg)

## 废话少说，先讲问题

像下面这样一个项目结构：

```none
Projetc_example
|-- A
   |-- alpha.py
   |-- beta.py
|-- B
    |-- theta.py
|-- main
    |-- main.py
```

假设要在`main.py`中导入`theta.py`：

```python
# main/main.py
from B import theta

```

显然会导致我们所不希望的问题，即Python不知道要到哪里去找这个名为B的模块（包是一种特殊的模块）：

```shell
Traceback (most recent call last):
  File "main/main.py", line 1, in <module>
    from B import theta
ModuleNotFoundError: No module named 'B'
```

可是这就奇了怪了，为啥同样的代码，在PyCharm里运行就是好的了呢？

![02](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/02.jpg)

## `import`的查找路径

于是我们不辞艰辛，上下求索，原来在Python中，import语句实际上封装了一系列过程。

### 1. 查找是否已导入同名模块

首先，Python会按照`import xxx`中指定的包名，到`sys.modules`中查找当前环境中是否已经存在相应的包——不要奇怪为什么都没有导入`sys`这个模块就有`sys.modules`了。

`sys`是Python内置模块，也就是亲儿子，导入只是意思一下，让我们这样的外人在导入的环境中也可以使用相关接口而已，实际上相应的数据对Python而言从始至终都是透明的。

![03](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/03.jpg)

我们可以导入`sys`查看一下这个对象的具体内容（节省篇幅，做省略处理）：

```shell
>>> import sys
>>> sys.modules
{'sys': <module 'sys' (built-in)>, 'builtins': <module 'builtins' (built-in)>, ...'re': <module 're' from 'E:\\Anaconda\\Anaconda\\lib\\re.py'>, ...}
```

这些就都是Python一开始就已经加载好的模块，也就是安装好Python之后，只要一运行环境中就已经就绪的模块——只是作为外人的我们还不能直接拿过来用，得跟Python报备一声：“欸，我要拿您儿子来用了嗨~”

很容易可以发现，`sys.modules`中列出来的已加载模块中存在明显的不同，前面的很多模块显得很干净，而后面的很多模块都带有`from yyy'`的字样，并且这个`yyy`看起来还像是一个路径。

这就关系到我们接下来要讲的步骤了。

### 2. 在特定路径下查找对应模块

前面我们讲到了，当我们导入某个模块时，Python先会去查询`sys.modules`，看其中是否存在同名模块，查到了那当然皆大欢喜，Python直接把这个模块给我们用就好了，毕竟儿子那么多，借出去赚点外快也是好事儿不是？

可问题在于：那要是没找到呢？

这显然是一个很现实的问题。毕竟资源是有限的，Python**不可能**把你*可能*用到的所有模块全都一股脑给加载起来，否则这样男上加男加男加男……谁也顶不住啊不是（大雾

![04](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/04.jpeg)

于是乎就有人给Python出了个主意：那你等到要用的时候，再去找他说他是你儿子呗

Python：妙哇~

![05](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/05.jpg)

有了这个思路，Python就指定了几家特定的酒楼，说：“凡是去消费的各位，都可以给我当儿子。”

就这样，一些本来不是Python亲儿子的人，出于各种原因聚集到了这几家酒楼，以雇佣兵的身份随时准备临时称为Python的儿子。

这可就比周文王开局就收100个义子优雅多了，养家糊口的压力也就没那么大了（Python：什么？我的亲儿子都不止100个？你说什么？听不见啊——

![06](http://www.justdopython.com/assets/images/2020/10/2020-10-13-import-system/06.png)

回到正经的画风来——

实际上，在Python中，`sys.path`维护的就是这样一个py交易的结果~~（诶？好像莫名发现了什么）~~，其中保存的内容就是这几家“指定酒楼”，也就是当Python遇到不认识的~~儿子~~模块时，就会去实地查找的路径。

我们也可以打印出来看看具体内容：

```shell
>>> sys.path
['', 'E:\\Anaconda\\Anaconda\\python37.zip', 'E:\\Anaconda\\Anaconda\\DLLs', 'E:\\Anaconda\\Anaconda\\lib', 'E:\\Anaconda\\Anaconda', 'E:\\Anaconda\\Anaconda\\lib\\site-packages', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32\\lib', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\Pythonwin']
```

大体上就是安装环境时配置的一些包所在路径，其中第一个元素代表当前所执行脚本所在的路径。

也正是因此，我们可以在同一个目录下，大大方方地调用其他模块。

### 3. 将模块与名字绑定

找到相应的非亲生模块还没完，加载了包还得为它分配一个指定的名字，我们才能在脚本中使用这个模块。

当然多数时候我们感知不到这个过程，因为我们就是一个`import`走天下：

```python
import sys
import os
import requests
```

这个时候我们指定的模块名，实际上也是指定的稍后用来调用相应模块的对象名称。

换个更明显的：

```python
import requests as req
```

如果这个时候只使用了第二种方式来导入`requests`这个模块，那么很显然在之后的程序流程中，我们都不能使用`requests`这个名字来调用它而应当使用`req`。

这就是Python导入过程中的名称绑定，本质上与正常的赋值没有太大区别，加载好了一个对象之后，然后为这个对象赋一个指定的变量名。

当然即使是已经加载好的模块，我们也可以利用这个名称绑定的机制为它们取别名，比如：

```shell
>>> import sys
>>> import sys as sy
>>> sys.path
['', 'E:\\Anaconda\\Anaconda\\python37.zip', 'E:\\Anaconda\\Anaconda\\DLLs', 'E:\\Anaconda\\Anaconda\\lib', 'E:\\Anaconda\\Anaconda', 'E:\\Anaconda\\Anaconda\\lib\\site-packages', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32\\lib', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\Pythonwin']
>>> sy.path
['', 'E:\\Anaconda\\Anaconda\\python37.zip', 'E:\\Anaconda\\Anaconda\\DLLs', 'E:\\Anaconda\\Anaconda\\lib', 'E:\\Anaconda\\Anaconda', 'E:\\Anaconda\\Anaconda\\lib\\site-packages', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\win32\\lib', 'E:\\Anaconda\\Anaconda\\lib\\site-packages\\Pythonwin']
>>> sys == sy
True
```

## 问题解决

好了，上面就是对Python导入机制的大致介绍，但是说了半天，我们的问题还没有解决：在项目中如何简洁地跨模块导入其他模块？

在使用PyCharm的时候倒是一切顺遂，因为PyCharm会自动将项目的根目录加入到导入的搜索路径，也就是说像下面这样的项目结构，在任意模块中都可以很自然地通过`import A`导入模块A，用`import B`导入模块B。

```none
Projetc_example
|-- A
   |-- alpha.py
   |-- beta.py
|-- B
    |-- theta.py
|-- main
    |-- main.py
```

但是在非IDE环境中呢？或者说就是原生的Python环境中呢？

很自然地我们就会想到：那就手动把项目根目录加入到`sys.path`中去嘛。说起来也跟PyCharm做的事没差呀

可以，贫道看你很有悟性，不如跟我去学修仙吧

所以我们就通过`sys`和`os`两个模块七搞八搞（这两个模块以前有过介绍，不再赘述）——

噔噔噔噔——好使了

```python
# Peoject_example/A/alpha.py
print("name: " + __name__)
print("file: " + __file__)

def al():
    print("Importing alpha succeeded.")
```

`main.py`中则加入一个逻辑，在`sys.path`中增加一个项目根目录：

```python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import A.alpha


A.alpha.al()

# name: A.alpha
# file: *\Project_example\A\alpha.py
# Importing alpha succeeded.
```

大功告成，风紧扯呼~

## 总结

本文借由一个易现问题引出对Python导入机制的介绍，实际上限于篇幅，导入机制只是做了一个概览，具体的内容还要更加复杂。本文讲到的这三步则适用于比较常见的情形，了解了这三步也足以应付很多问题了。更多内容还是留待大家自行探索，当然后续也可能会有文章进一步讲解——谁知道呢哈哈~~（又挖坑了）~~

## 参考资料

[Python官方文档-导入系统](https://docs.python.org/zh-cn/3/reference/import.html)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-10-13-import-system

