---
layout: post
category: python
title: 第72天：Python newspaper 框架
tagline: by 程序员野客
tags: 
  - python100
---

## 1 简介

newspaper 框架是一个主要用来提取新闻内容及分析的 Python 爬虫框架，更确切的说，newspaper 是一个 Python 库，但这个库由第三方开发。

<!--more-->

newspaper 主要具有如下几个特点：

* 比较简洁

* 速度较快

* 支持多线程

* 支持多语言

GitHub 链接：https://github.com/codelucas/newspaper

安装方法：`pip3 install newspaper3k`

## 2 基本使用

### 2.1 获取新闻

我们以环球网为例，如下所示：

```
import newspaper

hq_paper = newspaper.build("https://tech.huanqiu.com/", language="zh", memoize_articles=False)
```

默认情况下，newspaper 缓存所有以前提取的文章，并删除它已经提取的任何文章，使用 memoize_articles 参数选择退出此功能。

### 2.2 获取文章 URL

```
>>> import newspaper

>>> hq_paper = newspaper.build("https://tech.huanqiu.com/", language="zh", memoize_articles=False)
>>> for article in hq_paper.articles:
>>>     print(article.url)

http://world.huanqiu.com/gallery/9CaKrnQhXvy
http://mil.huanqiu.com/gallery/7RFBDCOiXNC
http://world.huanqiu.com/gallery/9CaKrnQhXvz
http://world.huanqiu.com/gallery/9CaKrnQhXvw
...
```

### 2.3 获取类别

```
>>> import newspaper

>>> hq_paper = newspaper.build("https://tech.huanqiu.com/", language="zh", memoize_articles=False)
>>> for category in hq_paper.category_urls():
>>>     print(category)

http://www.huanqiu.com
http://tech.huanqiu.com
http://smart.huanqiu.com
https://tech.huanqiu.com/
```

### 2.4 获取品牌和描述

```
>>> import newspaper

>>> hq_paper = newspaper.build("https://tech.huanqiu.com/", language="zh", memoize_articles=False)
>>> print(hq_paper.brand)
>>> print(hq_paper.description)

huanqiu
环球网科技，不一样的IT视角！以“成为全球科技界的一面镜子”为出发点，向关注国际科技类资讯的网民，提供国际科技资讯的传播与服务。
```

### 2.5 下载解析

我们选取其中一篇文章为例，如下所示：

```
>>> import newspaper

>>> hq_paper = newspaper.build("https://tech.huanqiu.com/", language="zh", memoize_articles=False)
>>> article = hq_paper.articles[4]
# 下载
>>> article.download()
# 解析
article.parse()
# 获取文章标题
>>> print("title=", article.title)
# 获取文章日期
>>> print("publish_date=", article.publish_date)
# 获取文章作者
>>> print("author=", article.authors)
# 获取文章顶部图片地址
>>> print("top_iamge=", article.top_image)
# 获取文章视频链接
>>> print("movies=", article.movies)
# 获取文章摘要
>>> print("summary=", article.summary)
# 获取文章正文
>>> print("text=", article.text)

title= “美丽山”的美丽传奇
publish_date= 2019-11-15 00:00:00
...
```

### 2.6 Article 类使用

```
import newspaper
from newspaper import Article

def newspaper_url(url):
    web_paper = newspaper.build(url, language="zh", memoize_articles=False)
    for article in web_paper.articles:
        newspaper_info(article.url)

def newspaper_info(url):
    article = Article(url, language='zh')
    article.download()
    article.parse()
    print("title=", article.title)
    print("author=", article.authors)
    print("publish_date=", article.publish_date)
    print("top_iamge=", article.top_image)
    print("movies=", article.movies)
    print("text=", article.text)
    print("summary=", article.summary)

if __name__ == "__main__":
        newspaper_url("https://tech.huanqiu.com/")
```

## 总结

本文为大家介绍了 Python 爬虫框架 newspaper，让大家能够对 newspaper 有个基本了解以及能够上手使用。

> 示例代码：[Python-100-days-day072](https://github.com/JustDoPython/python-100-day/tree/master/day-072)

参考：

[https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html#performing-nlp-on-an-article](https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html#performing-nlp-on-an-article)

