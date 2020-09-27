---
layout: post
category: python
title: 工具需用好，阅读源码没烦恼
tagline: by 轩辕御龙
tags:
  - python
---

# 工具需用好，阅读源码没烦恼

每当我们接手一个新项目时，面对庞杂的模块、繁复的代码，想必心情是非常绝望的，“这都特么啥呀？”

~~如果你也有这样的烦恼，那~~你就应该看这篇文章。

<!--more-->

我们阅读源码的一大烦恼在于，项目代码中存在着各种各样的调用，而我们的大脑却没办法像计算机一样完好地维护一个动态的调用链；时常发生的情况就是一头扎进了源码中，然后——

“我是谁？我在哪儿？我为什么要在这儿？”

显然，作为一个地道的程序员，这个时候应该想到借助工具了。

再根据软件界第一定律“99%的工作都是别人做过的”，于是我们大可以拿来主义一把，琢磨琢磨是不是已经有人做了这样的工具。

说到这里可能很多同学已经想到了一个被局部称为“世界第一编辑器”的软件——Source Insight。（然后看了看正版价格就灰溜溜滚回了Google）

然后还有强大的Understand，付费环节还比较繁琐，暂时pass。

直到我们在V2EX看见有同学推荐了一款名为Sourcetrail的开源软件。

## 下载安装

打开软件官方网站，可以看到一个很简洁的页面，直截了当地告诉你它是哪条道上的四年级*老大哥*：Sourcetrail就是为你阅读陌生源码赋能的。同时还免费、开源、跨平台……háo嘛，今年几大红火要素都占齐活儿了，不捞一把都说不过去。

![01](http://www.justdopython.com/assets/images/2020/09/sourcetrail/01.png)

接下来就是download，在GitHub的release页面选择自己系统对应的发布版本下载安装：

![02](http://www.justdopython.com/assets/images/2020/09/sourcetrail/02.png)

具体的安装步骤与其他应用相比大同小异，就不再赘述了，否则这篇文章也太水了点

![03](http://www.justdopython.com/assets/images/2020/09/sourcetrail/03.jpg)

## 软件介绍

安装好后，运行程序，会出现这样的界面：

![04](http://www.justdopython.com/assets/images/2020/09/sourcetrail/04.png)

我们选择“**New Project**”，在随后的界面中填写好项目名称和项目路径：

![05](http://www.justdopython.com/assets/images/2020/09/sourcetrail/05.png)

填好后点击下方的`Add Source Group`按钮，用以添加代码。

——在Sourcetrail中允许我们在同一个项目中添加多个来源的代码，甚至允许各个代码分组的语言互不相同，这些代码分组即为各个`Source Group`。

由于我们只需要查看一个代码库的内容，因此我们也只需要添加一个`Source Group`即可，如下图依次点击：

![06](http://www.justdopython.com/assets/images/2020/09/sourcetrail/06.png)

在继续输入新的信息前，打开你的命令行工具（Windows系统：Win+R，输入cmd然后回车；Linux下不赘述），输入`where python`（Windows）或`which python3`(Linux)，即可看到当前环境的Python安装路径，记下这个路径，我们需要用它来解析Python代码。

然后在新的界面中，需要填写Python环境的字段填入刚刚我们查到的Python所在目录（即去除最后一个斜杠及之后的内容）。

其他的需要注意的就是“要建立索引的文件/目录”，这个字段就是添加我们真正要阅读的Python源码路径。字段左下角有一个“**+**”号，点击即可增加一个源码路径：

![07](http://www.justdopython.com/assets/images/2020/09/sourcetrail/07.png)

原本是想把Python之父龟叔多年前写的爬虫程序作为示例的，奈何网络不给力，迟迟拉取不下源码，于是另外找了一份开源项目“[北京实时公交](https://github.com/wong2/beijing_bus)”替换之。

点击右下角“Create”，再点击“Start”：

![08](http://www.justdopython.com/assets/images/2020/09/sourcetrail/08.png)

解析就开始了：

![09](http://www.justdopython.com/assets/images/2020/09/sourcetrail/09.png)

再点击“OK”：

![10](http://www.justdopython.com/assets/images/2020/09/sourcetrail/10.png)

得到下图的解析结果：

![11](http://www.justdopython.com/assets/images/2020/09/sourcetrail/11.png)

可以看到，Sourcetrail将解析结果按“文件”、“模块”等大致分了类。

我们点击最关心的“函数（Function）”来体验一下：

![12](http://www.justdopython.com/assets/images/2020/09/sourcetrail/12.gif)

在左边，Sourcetrail为我们生成了形象的调用图；在右边，Sourcetrail列出了当前焦点函数的代码及其相应调用。

无论在左边操作还是在右边操作，都会带来界面的同步变化。

从此我们再也不必苦哈哈地在A4纸上写下繁琐的调用关系了哈哈哈哈，翻身农奴把歌唱

![13](http://www.justdopython.com/assets/images/2020/09/sourcetrail/13.png)

## 总结

本文介绍了一个可以把源码调用关系可视化的工具，可以极大便利我们阅读他人代码的工作。实际上这类工具还有很多，比如Source Insight和Understand。

只要是能够提升我们学习/开发效率的，我们都应该乐于尝试。后续我们还会推荐一些这类实用的工具，希望可以帮助大家升职加薪[手动滑稽]。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-09-28-sourcetrail-introduction>