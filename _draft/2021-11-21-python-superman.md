---
layout: post
category: python
title: 你相信：生命是可以延长的吗？
tagline: by 李晓飞
tags:
  - Python
  - 工具
  - 效率
---
![封面](http://www.justdopython.com/assets/images/2021/11/superman/00.jpg)

到今天，笔者使用 Python 有四五年了，在生活和工作上都有使用，写了不少应用和项目。

我一直认为 Python 是一个能提高工作效率的工具，直到最近，才发现：

> Python 是一个能延长生命的神器！

是怎么回事呢？

<!--more-->

## 一年顶千年

作家李笑来，最近在微博上，发状态，说：在一个月的时间里，翻译了十本书！

之后他在 [github](https://github.com/xiaolai/apple-computer-literacy/tree/main/deepl-aided-semi-automatic-book-translatiion '工具源码') 上公开了实现的方法。

更让人惊奇的是他说的这句话：

> 一本书中文译文大约 39 万字的书，差不多用 **1.5** 小时就可以处理完毕（包括基本的格式编辑）

![处理过程](http://www.justdopython.com/assets/images/2021/11/superman/01.gif)

这是什么概念？

正常情况下，翻译一本外语书，经过翻译，校对，排版，需要差不多 6 个人，工作一年的时间，而现在，这个过程不到 2 小时，如果加上一些微调，大概需要一天时间。

也就是一个人 1 天 顶过去 6个人一年，这算下来，保守估计，一年就比过去的 一千年 还多！

这哪是提高了效率呀，简直就是延长了生命，将大量的时间可以节省下来去做其他事情。

## 无比简单

你可能会想，提升这么高效率一定很难吧。

那就看一下[源码](https://github.com/xiaolai/apple-computer-literacy/blob/main/deepl-aided-semi-automatic-book-translatiion/deepl-automatic-html-translation.ipynb '翻译工具源码')，是用 Python 写的，加文字说明还不到 600 行。

用了什么高超技术了吗？

看遍全文，用到的只有：[requests](https://docs.python-requests.org/en/latest/ 'requests') 和 [正则表达式](https://www.runoob.com/python/python-reg-expressions.html '正则表达式')。

可以说，只要 Python 入门了，都可以看得懂。

做很厉害的事情，并不需要特别复杂的技术。

## 处理过程

具体如何做的呢？通过李笑来的描述，首先从亚马逊上，购买需要翻译的电子书，然后用 PC 版 [Kindle app](https://www.amazon.cn/gp/browse.html%3Fnode=2331640071&ref=kcp_fd_hz 'Kindle app') 打开并下载，在转化为 [epub](https://zh.wikipedia.org/wiki/EPUB 'epub') 格式的电子书。

![电子书](http://www.justdopython.com/assets/images/2021/11/superman/02.jpg)

再用 [Calibre](https://calibre-ebook.com/ 'Calibre') 电子书转化工具，将 epub 格式的电子书转化为 html 格式。

处理完原始资料，利用 Python 的 `open` 方法，打开 `html`格式的原始文件，简单处理格式后，逐行使用 `requests` 发送到 [Deep L](https://www.deepl.com/zh/translator 'Deep L') 进行翻译。

将翻译结果收集起来，和原始内容相间排放，最后保存成 `html` 文件，用 [VS code](https://code.visualstudio.com/ 'VS code') 编辑器，进行编排和校对。

## 无独有偶

读过《[黑客与画家](https://book.douban.com/subject/6021440/ '黑客与画家')》的读者，一定对其作者 [保罗·格雷厄姆 (Paul Graham)](https://zh.wikipedia.org/wiki/%E4%BF%9D%E7%BD%97%C2%B7%E6%A0%BC%E9%9B%B7%E5%8E%84%E5%A7%86 '保罗·格雷厄姆 (Paul Graham)') 印象深刻，他从一个程序员成长为导师，而且创作不断，影响了很多人。

有位 保罗·格雷厄姆 的粉丝，将 保罗·格雷厄姆 发布的文集，利用爬虫和电子书转化工具，整理成了一本[电子书](https://github.com/evmn/Paul-Graham 'Paul-Graham 文集')，方便他随时查看，不受网络限制。

虽然，这个应用只是方便自己（也可能方便他人），但使用的工具一样简单。

通过 `requests` 将博客上的文章抓取到，经过整理，通过上面提到的电子书转化工具 Calibre，转化为 kindle 电子书。

为了方便检索，还做了一下索引和检索，不过都是通过 Python 脚本搞得定的。

有兴趣的读者可以查看[源码](https://github.com/evmn/Paul-Graham/blob/master/calibre.recipe '电子书源码')

## 我的实践

前段时间，完成了一个数据项目，从网上获取了大量的网页数据，其中关于提取文章核心的部分写过[一篇介绍](https://mp.weixin.qq.com/s/cl5keeugJADz5-1iyLlXZg)，有兴趣的读者可以看看。

其中有个环节，需要将获取到的页面组织成一个静态网页：

首页按照最高分类划分，然后是二级分类，最后是列表，点击列表可以查看具体页面。

处理方法是，创建页面模板（需要处理分页），然后读取各层分类，合成数据，替换到模板上，最后保存成 html 文件。

![处理结果](http://www.justdopython.com/assets/images/2021/11/superman/03.png)

六十多万条数据，处理完毕需要 2 小时。

如果不用 Python，人工处理的话，几乎是不可能完成的工作。

## 总结

回想当初学 Python 的时候，觉得需要掌握更高级的用法和技能，才能更好的用 Python，成为更专业的人。

而现在的感受是，编程，其实是任何人都可以提升效率的工具，人人都可以是超人。

如果说刚开始，编程是专业人士，科学家们的玩具，那么现在，编程的门槛低到，任何人都可以掌握并使用。

对于大多数人来说，编程更大的意义在于通过提升效率，提升效率就意味着：

> **延长生命**

那么在学习 Python 的过程中，应该多将精力放在应用，解决实际问题，和思考之上，让 Python 真正变成我们的效率武器。

欢迎你在留言区写下自己的想法与思考。

比心！
