---
layout: post
category: python
title: 用 Python 将 html 转为 pdf、word
tagline: by 某某白米饭
tags: 
  - python
---

在日常中有时需将 html 文件转换为 pdf、word 文件。网上免费的大多数不支持多个文件转换的情况，而且在转换几个后就开始收费了。

![](http://www.justdopython.com/assets/images/2021/02/convertHtml/-1.png)

### 转 pdf

转 pdf 中使用 pdfkit 库，它可以让 web 网页直接转为 pdf 文件，多个 url 可以合并成一个文件。

#### 安装 pdfkit 库

```
pip3 install pdfkit
```

#### 安装 wkhtmltopdf 文件

pdfkit 是基于 wkhtmltopdf 的 python 封装库，所以需要安装 wkhtmltopdf 软件。

下载地址：https://wkhtmltopdf.org/downloads.html

![](http://www.justdopython.com/assets/images/2021/02/convertHtml/0.png)

在windows 系统中，需要将 wkhtmltopdf.exe 文件路径配置在系统环境变量中。

#### url 生成 pdf

这里使用 baidu 首页和 bing 首页作为示例

```python
import pdfkit

# 第一个参数可以是列表，放入多个域名，第二个参数是生成的 PDF 名称
pdfkit.from_url(['www.baidu.com','www.bing.com'],'search.pdf')
```
![](http://www.justdopython.com/assets/images/2021/02/convertHtml/1.png)

#### 本地 html 文件生成 pdf

提前将需要转换的 html 存储到本地，也可以使用 python 爬虫代码抓取 html 文件到本地。

```python
import pdfkit

pdfkit.from_file('/Users/xx/Desktop/html/baidu.html', 'search.pdf')
```

### 转 word

使用 pypandoc 库将 html 转换为 word 文件，pypandoc 是一个支持多种文件格式转换的 Python 库，它用到了 pandoc 软件，所以需要在电脑上安装 pandoc 软件

#### 安装 pypandoc 库

```
pip install pypandoc
```

#### 安装 pandoc 软件

pypandoc 是基于 pandoc 软件的库，所以要安装一下 pandoc (https://github.com/jgm/pandoc/releases/tag/2.11.4)，pandoc 支持多种类型转换。下图是 pandoc 的转换类型。

![](http://www.justdopython.com/assets/images/2021/02/convertHtml/2.png)

#### 使用

将 html 文件提前存储在本地，也可以用爬虫将需要转换的 html 文件在代码中抓取后使用。pypandoc 无法对 word 进行排版，所以需要小伙伴们进行 2 次排版。

```python
import pypandoc

# convert_file('原文件','目标格式','目标文件')
output = pypandoc.convert_file('/Users/xx/Desktop/html/baidu.html', 'docx', outputfile="baidu.doc")

```

![](http://www.justdopython.com/assets/images/2021/02/convertHtml/3.png)

### 总结

利用好 Python 第三方库类，可以为小伙伴写出各种个性化定制的小程序

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/convertHtml>