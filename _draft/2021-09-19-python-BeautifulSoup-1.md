---
layout: post
category: python
title: 巨细！小姐姐告诉你关于 BeautifulSoup 的一切(上)！
tagline: by 潮汐
tags:
  - Python技巧
  - 编程
---


![](https://files.mdnice.com/user/6478/d22ad820-00a2-44fb-b39e-5a89e50840c0.png)


现在的朋友们都很聪明，只要会爬虫都知道 BeautifulSoup，但是随着知识点越来越多，很多伙伴可能只知道如何使用这个爬虫工具，并不知道 BeatifulSoup 的详尽用法，今天的文章就带大家了解 BeautifulSoup 的基础详细用法。

**BeautifulSoup 是什么？？？**


BeautifulSoup 是一个可以从 HTML 或 XML 文件中提取数据的 Python 扩展库。BeautifulSoup 通过合适的转换器实现文档导航、查找、修改文档等。它可以很好的处理不规范标记并生成剖析树（Parse Tree）；它提供的导航功能（Navigating），可以简单又快速地搜索剖析树以及修改剖析树。BeautifulSoup 技术通常用来分析网页结构，抓取相应的 Web 文档，对于不规则的 HTML 文档，它提供了一定的补全功能，从而节省了开发者的时间和精力。今天的文章就一起学习 BeatifulSoup 的详细用法吧~
 
<!--more-->

###  环境部署

#### 安装 BeautifulSoup

BeautifulSoup 主要通过 pip 指令进行安装，在命令提示符 CMD 环境下或者在 PyCharm 的命令行窗口进行安装都可，即调用 `pip install bs4` 命令进行安装，bs4 即 BeautifulSoup4。

由于我本地环境已经安装了，显示如下：

![](https://files.mdnice.com/user/6478/999267bd-6fc4-496b-bf71-7b1a32062dc7.png)

没安装的小伙伴可以去直接输入命令尝试安装，如果已安装就可以直接上手实践。

当 BeautifulSoup 扩展包安装成功后，就可以在命令行输入`from bs4 import BeautifulSoup` 语句导入该扩展包，测试安装是否成功，如果没有异常报错即安装成功，如下所示:

![](https://files.mdnice.com/user/6478/5c0b54ae-3c4d-463b-bae9-966d5e5509c1.png)

### BeautifulSoup 解析 HTML 获取网页信息

#### BeautifulSoup 解析 HTML

BeautifulSoup 解析 HTML 的原理是创建一个 BeautifulSoup 对象，然后调用 BeautifulSoup 包的 prettify() 函数格式化输出网页信息。

实例如下：

```python
from bs4 import BeautifulSoup

html = """
<html>
	<head>
		<title>Hello Python</title>
	</head>
	<body>
    <p>BeatifulSoup 技术详解</p>
	</body>
</html>
"""
# 结果会按照标准的缩进格式的结构输出
soup = BeautifulSoup(html)
print(soup.prettify())
```

使用 BeautifulSoup 解析网页输出结果如下：

![](https://files.mdnice.com/user/6478/1ac387de-7ee7-4972-8160-890871c71477.png)

BeatifulSoup 解析会把 HTMl 网页的所有标签信息和内容按照 HTML 标签的缩进全部输出。

用 BeautifulSoup 解析 HTML 文档时，它会将 HTML 文档类似 DOM 文档树一样处理，使用 `prettify()` 函数输出结果时会自动补齐标签，这是 BeautifulSoup 的一个优点，即使 BeautifulSoup 得到了一个损坏的标签，它也产生一个转换 DOM 树，并尽可能和原文档内容含义一致，这种措施通常能够帮助更正确地搜集数据。

**实例如下：** 将一个网址输入后直接用 `prettify()` 函数获取

```python
from bs4 import BeautifulSoup

html = 'https://www.baidu.com/'
# 结果会按照标准的缩进格式的结构输出
soup = BeautifulSoup(html)
print(soup.prettify())
```

输出内容如下：
```html
<html>
 <body>
  <p>
   https://www.baidu.com/
  </p>
 </body>
</html>
```
输出的内容自动补齐了标签，并按照 HTML 格式输出。

#### BeautifulSoup 获取网页标签信息

上面的知识讲解如何用 BeautifulSoup 解析了网页，在解析完网页之后，如果想获取某个标签的内容信息，怎么实现呢？比如获取以下超文本的 `标题`,接下来将教大家如何使用 BeautifulSoup 技术获取网页标签信息。
获取网页`标题`代码如下：

```python
from bs4 import BeautifulSoup

# 获取标题
def get_title():
    #创建本地文件soup对象
    soup = BeautifulSoup(open('test.html','rb'), "html.parser")

    #获取标题
    title = soup.title
    print('标题:', title)

if __name__ == '__main__':
    get_title()
```
输出内容如下:

![](https://files.mdnice.com/user/6478/d556276c-dee9-4d20-85dc-d798559bfc44.png)

同样的获取其他标签的内容也一样，如 HTML 的头部 a 标签

```python
# 获取a标签内容
def get_a():
    #创建本地文件soup对象
    soup = BeautifulSoup(open('test.html','rb'), "html.parser")

    #获取a标签内容
    a = soup.a
    print('a标签的内容是:', a)
```

输出内容如下：

```
a标签的内容是: <a href="https://www.baidu.com">ddd</a>
```

### 定位标签并获取内容

前面的内容简单介绍了 BeautifulSoup 获取title、a等标签，但是如何定位标签并获取到相应标签的内容呢，这里就需要使用 BeatifulSoup 的 `find_all()`函数，详细使用方式如下：

```python
def get_all():
    soup = BeautifulSoup(open('test.html', 'rb'), "html.parser")
    # 从文档中找到<a>的所有标签链接
    for a in soup.find_all('a'):
        print(a)
    # 获取<a>的超链接
    for link in soup.find_all('a'):
        print(link.get('href'))

if __name__ == '__main__':
    get_all()
```
输出内容如下：

```
<a href="https://www.baidu.com">ddd</a>
https://www.baidu.com
ddd
```
以上是关于 BeautifulSoup 如何定位标签并获取内容的方式。

### 总结

本文主要讲解关于 BeautifulSoup 知识点的最基础部分，下文将讲解关于 BeautifulSoup 的核心用法，咱们下期见~

### 参考

[BeautifulSoup 官网](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)
[https://blog.csdn.net/Eastmount](https://blog.csdn.net/Eastmount/article/details/109497225)







