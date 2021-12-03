---
layout: post
category: python
title: 再见 Pycharm，这款开箱即用的轻量级神器你值得拥有
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/logo.png)

如果你问我最好用的 IDE 是什么，那我肯定会毫不犹豫的告诉你 Pycharm。毕竟 jetbrains 出品必属精品。

但对于很多初学者来讲，Pycharm 显得略笨重，很多功能点也不够简单易上手，对电脑的配置要求也会稍微高一些。导致很多人被 IDE 折磨的抓狂，今天派森酱就给大家介绍一款简单、易上手、面向初学者的的轻量级 IDE - Thonny。

## 安装

Thonny 是由爱沙尼亚的 Tartu 大学开发，非常适合初学者的一款轻量级 IDE。

该 IDE 目前支持三大主流操作系统，可以从官网直接下载安装。

```pyhton
https://thonny.org/
```

打开上面的网址之后，选择对应的操作系统直接下载即可。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/001.png)

当你安装完毕满心欢喜的启动应用之后，你会发现居然还可以选择语言，其实对于编程类的 IDE 还是英文看起来会比较舒服，但这次我想试一下中文，看看支持程度到底怎么样。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/002.png)

## 初体验

打开软件之后，你会发现界面是如此的简洁，这对于初学者是极其友好的，不会被过多的分散精力，把主要精力放在代码上即可。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/003.png)

默认界面分为上下两个部分，上面是代码区，下面是终端区。

嗯，先整个 Hello World 试一下。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/004.png)

可以看到，在终端 Hello World 已经被正确的输出来了，至此，环境是跑通了。

不知道你注意到没有，从始至终我们都没有安装过 Python，也没有配置过 Python 解释器，事实上 Thonny 是自带了 Python 解释器了，真正做到了开箱即用。

当然，你也可以配置自己的解释器，在菜单栏点击“运行” -> “选择解释器”来更改默认的解释器。

## 视图

我们所写的程序中通常都会定义非常多的变量，如果可以清楚的看到程序运行过程中变量的值那简直不要太爽。

你可以通过菜单栏的「视图」来勾选不同的选项来显示和关闭不同的视图窗口，通常情况下可以把变量和堆勾选上，这对于调试程序非常有帮助。尤其是对于初学者来讲，可以非常直观的看到变量的值。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/005.png)

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/006.png)

所见即所得，这点 Thonny 的体验超好。

## 调试

对于很多初学者来讲，函数之间的调用是很难理解的，尤其是涉及到递归函数时。但这块 Thonny 做的非常好。

打开你想调试的程序，甚至都不需要设置断点，直接以 debug 模式运行即可，工具会自动的按照程序步骤来运行，而且涉及到函数时，会自动弹出一个新的窗口来显示运行情况，就连运行过程中变量的值都会在新窗口一并显示，而这一点也不会影响旧窗口。

尤其是涉及到多层函数嵌套，尤其是递归函数，每调用一次嵌套函数就会打开一个新的窗口来显示，这对于初学者来说简直是莫大的福利啊。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/007.png)

## 堆栈

要想理解 Python 的内存模型就离不开堆栈，而 Thonny 做到了将堆栈可视化。

在代码区输入以下代码。

```python
a = [1, 2, 3, 4]
b = a
b.append(5)

print(a)
print(b)
```

运行之后你会在变量视图发现变量 a 和 b 居然都指向了同一块内存地址，这也就解释了为啥改变 b 之后 a 的值也一起跟着改变了。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/008.png)

## 错误提示

在错误提示这块 Thonny 同样有代码高亮提示，当你的代码有很明显的语法错误时，Thonny 会将整行代码高亮来提示你此行代码有错误。

与此同时，Thonny 还会给出明确的整改建议。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/thonny/009.png)

## 总结

今天给大家介绍了 Thonny 的基本使用，这是一款面向初学者的轻量级 IDE，可以让初学者更好更快的入门上手 Python，而不致于在环境上浪费过多的时间。

关于 Thonny 的使用大家还有什么技巧可以在评论区交流哦～