---
layout: post
category: python
title: 当 IDEA 支持了 M1 芯片，太强悍！！
tagline: by 極光
tags:
  - 
---


几个月前苹果发布了第一款自研芯片 Apple Silicon（M1），这款芯片与 intel 的芯片完全不兼容，导致很多软件不能运行在这款芯片上，即使能运行也是通过软件将指令集做了转义，执行效率也大打折扣。而做为我们平时开发的重要工具 IDEA 也一样，虽然能通过软件兼容运行在新的芯片上，但用着用着经常会无故闪崩，而且运行效率也不太满意。就在前段时间 IDEA 终于了支持 Apple Silicon（M1） 的版本，赶紧下载了尝尝鲜。

<!--more-->

## 开始下载

首先我们要到 jetbrains 的官网 （https://www.jetbrains.com/zh-cn/idea/download/#section=mac）去下载，默认下载是 intel 版本的，点击这个下拉框可以看到 Apple Silicon 版本下载。

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/0.jpg)

好了，下载完成后安装就不用说了，跟以前一样。在这里为了比较两个版本的区别，我特意做了个比较，用实际数据看看这两个版本的效果差距有多大。

## intel 版本

现在我们先看下 intel 版本，在这里主要表现的是 CPU 的差距，所以我只对 CPU 运行占用做了截图。

一般在 Mac OS 系统下， IDEA 同时打开多个项目，如果此时退出 IDEA，那在下次打开 IDEA 时会自动打开退出前的所有项目。

所以在这里我就选了三个项目同时打开来做这个测试，这样三个项目同时进行初始化工作，能明显看出 CPU 消耗的多少。

首先来个执行前 CPU 的使用率截图：

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/5.jpg)

可以看到目前 CPU 大概闲置 91%，下面来启动 IDEA，然后我截了个还在初始化中的图：

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/6.jpg)

可以看到目前 CPU 闲置还剩39%， 其实最少时闲置有30%，也就最高时 CPU 使用率能达到70%左右，但只有很短的时间，截图手速慢了没截到。

好了，下面这张就是 IDEA 初始化结束后的 CPU 占用率波动以及初始化运行时长的截图，看好这个图下面我们再看 Apple Silicon 的表现。

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/7.jpg)

## Apple Silicon 版本

现在来看 Apple Silicon 版本怎么样，运行之前还是先来一张当前的 CPU 占用率截图，可以看出闲置率大概93%的样子。

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/1.jpg)

下面我运行 IDEA，打开三个项目进行初始化，然后截一张初始化运行中的图。

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/2.jpg)

可以看到，截图时 CPU 占用率能达到70%，但并不是最高的时候，最高时占用率应该能达到80%以上，这说明 Apple Silicon 版对于 CPU 的利用率明显更高。

最后我再放一张运行完成的截图，大家看了不要惊讶，没错这就是 M1 的真正实力，跟上面 intel 版本的相比，Apple Silicon 版本在执行初始化时可以用干净利落来形容，只用了之前 1/3 到 1/4 的时间，就完成了所有的初始化。

![](http://www.justdopython.com/assets/images/2021/01/m1_idea/3.jpg)

虽然只是几张截图，但已经足够表明它的强悍，其实在实际使用中，能明显感觉 Apple Silicon 版本比原来快了很多，而且很稳定再也不会闪崩，开发效率提升明显。

## 总结

总的来说，这只是个简单的测试，并不是专业测评，可能并没有太多的说服力，如果你在意这样，就当我只是说了下自己的使用感受吧。OK，今天就聊这些，如果你喜欢记得点 `在看`。
