---
layout: post
category: python
title: 你的代码长啥样？
tagline: by 轩辕御龙
tags:
	
---

# 你的代码长啥样？

我们以前在文章《[第17天：Python 之引用](https://mp.weixin.qq.com/s/WyXVOitod4PmxeIn993H7Q)》中详细地讨论过Python中关于“引用”的话题，可能有的同学还有印象。

前几天陈老师（微博[@爱可可-爱生活](https://weibo.com/fly51fly?topnav=1&wvr=6&topsug=1&is_hot=1)）在B站上传了一个名为《[十分钟！彻底弄懂Python深拷贝与浅拷贝机制](https://www.bilibili.com/video/BV1jT4y1G7AN)》的视频，建议感兴趣的同学可以看看（写下这句话的时间是4月7号，完成这篇文章的时间是4月29号……所以“前几天”这个说法emmm……只能请大家睁一只眼闭一只眼了哈哈）。

本酱观看之后颇有一些忐忑，因为自觉之前讨论Python引用的文章还是不太到位，所以过后打算写文重新阐述一下。

但是今天促使我写这篇文章的却是另有其物——毕竟反省是不可能反省的，除非有读者要求。

<!--more-->

废话少说，我们先来上张图：

![01](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/01.png)

嚯，有点东西啊？

对照一下很容易发现，右侧的图像大略对应于左侧代码的图示。

有的读者可能会说：“嗨，这有什么了不起的，调试器不也可以列出程序运行中的各个变量及其相应值嘛；只不过多了图形表示而已。”

非也非也。看到图中的箭头了吗？那就是我们逝去的青春啊——咳咳，那就是我们讨论过的引用啊。

正所谓，“工欲善其事，必先利其器”，我们老是讨论引用啊、对象啊之类的东西，但是很多同学实际上并不是很理解它们到底是个神马玩意儿，“噢，你说引用就引用呗，谁还不能死记硬背嘛”——毕竟对很多同学来说这东西着实有些过于抽象了。但现在我们有了这样一个用来理解引用和变量之间关系的利器——[pythontutor.com](http://pythontutor.com/)，生动形象，十分到位，那谁还要自行车啊。

接下来我们快来捋捋这东西到底该怎么用吧。

## 快速上手

打开Python Tutor工具的主页，映入眼帘的是这样一个页面：

![02](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/02.png)

可以看到，这个工具不仅支持Python，同时也支持C、C++、JavaScript和Ruby等常见的编程语言。

在图中框出的两处链接中，凭个人喜好选择一个点击进入即可。

然后我们就来到了如下图所示的一个页面：

![03](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/03.png)

其中，正上方下拉菜单可以选择使用的语言类型，可以看到常见的C、C++、Java、Python和JavaScript等语言均在其列，如下图所示：

![04](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/04.png)

在页面正中的代码框中输入如下代码：

```python
list_a = [1,2,3]
list_b = list_a
list_c = list_a.copy()
```

然后点击下方左侧的按钮“Visualize Execution”，即可使用该工具执行输入的代码。

![05](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/05.gif)

点击“Next”按钮，即可按逻辑顺序逐行执行Python代码。

但我们关注的还是右边的可视化图像——不严谨地说，这部分图像就是对应代码的可视化表述。在系统中数据存在什么样的关系，也都一一体现在右侧这个方寸大小的图像当中。

可以看到，变量`list_a`和`list_b`都指向同一个列表对象，而`list_c`则指向一个新的列表对象；其中`list_c`所指向的列表又是由`list_a`复制来的。

通过观察这一段示例代码，我们很容易领会到这样的视角：在Python中，变量之间的直接赋值实际上仅仅是传递了变量的“引用”，而这所谓的“引用”实际上只不过是一种指向关系，通过变量保存的引用可以找到对应的对象，诸如列表、字典，甚至是数字——仅此而已。

经过直接赋值和调用`copy`方法再赋值，除了`list_c`是指向了一个新的列表对象，`list_a`和`list_b`之间并没有实质上的区别：对其中任意一个的修改都会相应地影响另一个变量所指向的值。而`list_c`则是独立的，不会受前两者的影响，反过来也不会对前两者造成影响：

![06](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/06.gif)

## 实时执行

> 由于临时网络原因，写作本节时无法正常访问相应页面，因此本节截图均来自于陈老师制作的视频《[十分钟！彻底弄懂Python深拷贝与浅拷贝机制](https://www.bilibili.com/video/BV1jT4y1G7AN)》，相应著作权归属陈老师。如果有机会会重新制并替换相应截图。

注意到，在按钮“Visualize Execution”右侧还有另一个按钮，“Live Programming Mode”。让我们好奇地点进去——老实说本酱其实是并不好奇的，因为我已经试过这是干嘛的了——姑且当我是好奇的吧。

点击链接之后进入了这样一个页面：

![10](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/10.png)

实际上这种实时执行的模式与常规模式唯一的区别就是：只要你完成了代码输入，不需要进行任何其他的多余操作，工具就会自动执行这个代码并绘制出相应图示。这其中涉及到代码的自动保存。其使用过程如图所示：

![11](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/11.gif)

如果非要进行类比的话，常规模式就像是规规矩矩的使用Python脚本编程，堂皇正大，但是失之灵巧；而实时执行模式则类似于Python交互式环境或者是jupyter环境，虽然有时候不大靠谱，但却很适合快速开发，快速测试。

## 学习雷锋

Python Tutor这个工具还有一个非常有趣的特性：协作。或者说按照工具官方的说法，叫做“获取实时帮助”。

在工具主页面的左上方，时常会看到这样的内容：

![12](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/12.png)

点击左侧上方的“Get live help”就可以向正在使用Python Tutor的用户发出实时求助（本着尽量不给别人添麻烦的思想，该按钮本酱并未测试）；而右侧列出来的内容中，每一个列表项都对应着一位向你或他发出求助的用户。

如果你对自己还比较有自信，那么你就可以大方点击列表项中的“click to help”链接，跳转到求助者的页面。不过需要提醒的是，由于该工具面向的用户不限于国人，因此你遇到的用户几乎都是英语用户，如果想要提供帮助还是需要基础的英语理解能力。

协助页面如下图所示：

![13](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/13.png)

而通过协助他人解决一些看似简单的问题，你收获的不只是对Python更深入的理解，更重要的是会获得一种心理上的满足感，以及你的努力能够帮助到他人的宽慰：

![14](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/14.png)

![15](http://www.justdopython.com/assets/images/2020/04/2020-04-07-visualize-your-code/15.png)

目前来看，协助过程中的交互界面还比较简陋，并且也不支持账号系统，也就是无法进行实际意义上的社交活动，也不能保存帮助他人的记录，更遑论解锁“十世善人”成就、开放正义值排行榜这些骚操作了。

但是，做好事不留名，不就是雷锋精神的真实写照吗？“事了拂衣去，深藏身与名”，如此洒脱，又何尝不是失落的侠义精神在今天这个互联网时代换发的老树新枝呢？

学习雷锋，还等什么学雷锋纪念日呢？

哪怕你的编程水平还不足以指点他人，那又何妨在这里求助于人呢？想必这样的互动，也会带来远胜个人闭门造车的效果吧。

## 总结

本文主要介绍了一款十分优秀的代码可视化工具——[Python Tutor](http://pythontutor.com/)。使用这个工具探索自己遇到过的问题、产生的疑惑，相信会给你带来不一样的体验。

在远程协作上，无论是求助还是给予帮助，都能给双方带来有价值的收获。又为什么不试一试呢？

## 参考资料

《[十分钟！彻底弄懂Python深拷贝与浅拷贝机制](https://www.bilibili.com/video/BV1jT4y1G7AN)》（微博[@爱可可-爱生活](https://weibo.com/fly51fly?topnav=1&wvr=6&topsug=1&is_hot=1)）

[Python Tutor主页](http://pythontutor.com/)

[第17天：Python 之引用](https://mp.weixin.qq.com/s/WyXVOitod4PmxeIn993H7Q)