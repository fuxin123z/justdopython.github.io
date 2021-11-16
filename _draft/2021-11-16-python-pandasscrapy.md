---
layout: post
title: Pandas爬虫，一行代码迅速爬网页！
category: python
tagline: by 闲欢
tags: 
  - python
  - 爬虫
  - pandas
---



![封面](http://www.justdopython.com/assets/images/2021/11/pandasscrapy/0.jpg)

提到爬取网页数据，大家最先想到的常规方式是通过 requests 请求网页数据，然后使用 lxml 解析定位网页节点，从而获取所需数据。

但是对于一些简单的网页表格数据抓取来讲，我们没有必要去研究页面的结构，然后解析页面，甚至通过晦涩难懂的正则表达式去解析数据。

今天我就给大家介绍一个神器 —— 潘大师（Pandas），可以一行代码即刻获取网页中的表格数据。

<!--more-->

#### 介绍

Pandas 自带了一个 read_html() 的方法，通过这个方法可以直接获取网页中的所有表格数据。

当然，这个获取方式也是有前提条件的，它要求网页中的表格是我们常见的标准格式：

```python
<table class="..." id="...">
    <thead>
    <tr>
    <th>...</th>
    </tr>
    </thead>
    <tbody>
        <tr>
            <td>...</td>
        </tr>
        <tr>...</tr>
        <tr>...</tr>
        <tr>...</tr>
        <tr>...</tr>
        ...
        <tr>...</tr>
        <tr>...</tr>
        <tr>...</tr>
        <tr>...</tr>        
    </tbody>
</table>

```

当你使用 F12 定位页面表格时，如果出现的是这种标准的 HTML 表格，那么我们就可以直接使用 read_html() 这个方法快速地获取页面的表格信息。

#### 实例

下面我们以福布斯 500 强的新闻网页（https://www.fortunechina.com/fortune500/c/2018-07/19/content_311046.htm）为例，这个页面整个是一个新闻网页，在后面穿插一个福布斯排名的表格：

![](http://www.justdopython.com/assets/images/2021/11/pandasscrapy/1.jpg)

我们来看看这个简洁而暴力的代码实现：

```pyhton
data = pd.read_html('https://www.fortunechina.com/fortune500/c/2018-07/19/content_311046.htm',header=0,encoding='utf-8')
print(data)

```

打印出来的内容如下：

```python
[      排名 上年排名                              公司名称(中英文)  营业收入(百万美元) 利润(百万美元)  国家
0      1    1                           沃尔玛（WALMART)    500343.0     9862  美国
1      2    2                     国家电网公司（STATE GRID)    348903.1   9533.4  中国
2      3    3              中国石油化工集团公司（SINOPEC GROUP)    326953.0   1537.8  中国
3      4    4  中国石油天然气集团公司（CHINA NATIONAL PETROLEUM)    326007.6   -690.5  中国
4      5    7          荷兰皇家壳牌石油公司（ROYAL DUTCH SHELL)    311870.0    12977  荷兰
..   ...  ...                                    ...         ...      ...  ..
495  496   --      河南能源化工集团（HENAN ENERGY & CHEMICAL)     23699.4    -68.6  中国
496  497  430   大同煤矿集团有限责任公司（DATONG COAL MINE GROUP)     23697.5     66.8  中国
497  498  452                   BAE系统公司（BAE SYSTEMS)     23591.6   1099.6  英国
498  499   --                    青岛海尔（QINGDAO HAIER)     23563.2   1024.7  中国
499  500  419                        爱立信公司（ERICSSON)     23556.3  -4119.8  瑞典
[500 rows x 6 columns]]

```

惊不惊喜，意不意外？就是这么简单，接下来对这个表格数据需要怎么处理直接从 data 里面取就行。

细心的你可能发现这个输出有个问题，好像外面包了一层中括号。

对，你没看错！其实我们的 data 是一个列表，这也就意味着如果网页中有多个表格的话，我们也可以通过这一行代码全部获取。

我们再来看一个实例。

这次我选取的网页是 https://www.boxofficemojo.com/ 。这个网页有好几个表格：

![](http://www.justdopython.com/assets/images/2021/11/pandasscrapy/2.jpg)

同样地，我们来看我们的代码：

```python

data = pd.read_html('https://www.boxofficemojo.com/',header=0,encoding='utf-8')
print(data)

```

输出是这样子的：

```python
[                      Eternals  $4,211,822
0     Clifford the Big Red Dog  $2,300,172
1                         Dune    $826,144
2               No Time to Die    $662,296
3  Venom: Let There Be Carnage    $375,377,                       Eternals  $6,243,758
0     Clifford the Big Red Dog  $3,280,603
1                         Dune  $1,225,876
2               No Time to Die    $993,982
3  Venom: Let There Be Carnage    $692,789,                       Eternals  $7,839,828
0     Clifford the Big Red Dog  $4,315,807
1                         Dune  $1,646,511
2               No Time to Die  $1,395,424
3  Venom: Let There Be Carnage  $1,042,997,                       Eternals $11,868,839
0     Clifford the Big Red Dog  $7,536,674
1                         Dune  $2,422,023
2               No Time to Die  $2,012,687
3  Venom: Let There Be Carnage  $1,847,858,                       Eternals  $7,141,461
0     Clifford the Big Red Dog  $4,775,010
1                         Dune  $1,474,474
2               No Time to Die  $1,125,239
3  Venom: Let There Be Carnage  $1,029,300,    1                     Eternals  $26.9M  false  false.1
0  2     Clifford the Big Red Dog  $16.6M   True    False
1  3                         Dune   $5.5M  False    False
2  4               No Time to Die   $4.5M  False    False
3  5  Venom: Let There Be Carnage   $3.9M  False    False,      Untitled Elvis Presley Project     Wide   Jun 3, 2022  →  Jun 24, 2022
0         Untitled Star Trek Sequel     Wide   Jun 9, 2023  →  Dec 22, 2023
1  Transformers: Rise of the Beasts     Wide  Jun 24, 2022  →   Jun 9, 2023
2                    The Contractor  Limited  Dec 10, 2021  →  Mar 18, 2022
3                National Champions     Wide           New  →  Dec 10, 2021,    1 Shang-Chi and the Legend of the Ten Rings  $224.4M  -
0  2               Venom: Let There Be Carnage  $202.6M  -
1  3                               Black Widow  $183.7M  -
2  4                         F9: The Fast Saga  $173.0M  -
3  5                     A Quiet Place Part II  $160.1M  -,    1 The Battle at Lake Changjin  $882.0M  -
0  2                     Hi, Mom  $822.0M  -
1  3           F9: The Fast Saga  $721.1M  -
2  4              No Time to Die  $708.4M  -
3  5       Detective Chinatown 3  $686.3M  -]

```

如果我们分别打印出这三个个表格：

```python
data = pd.read_html('https://www.boxofficemojo.com/',header=0,encoding='utf-8')
print(data[0])
print(data[1])
print(data[2])

```

输出就将这三个表格的数据分开了：

```python
                      Eternals  $4,211,822
0     Clifford the Big Red Dog  $2,300,172
1                         Dune    $826,144
2               No Time to Die    $662,296
3  Venom: Let There Be Carnage    $375,377
                      Eternals  $6,243,758
0     Clifford the Big Red Dog  $3,280,603
1                         Dune  $1,225,876
2               No Time to Die    $993,982
3  Venom: Let There Be Carnage    $692,789
                      Eternals  $7,839,828
0     Clifford the Big Red Dog  $4,315,807
1                         Dune  $1,646,511
2               No Time to Die  $1,395,424
3  Venom: Let There Be Carnage  $1,042,997

```

上面就是 pandas 这个方法的简单使用了。其实 read_html() 这个函数有很多参数可供调整，比如匹配方式、标题所在行、网页属性识别表格等等，具体说明可以参看pandas的官方文档说明： https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html


#### 总结

本文介绍的爬虫方式很简单，但是当你只想获取一个网页中的表格数据时，确实最有用最省时省力的方式。以后遇到这种需求，别再傻傻地去做解析了，直接一行代码解决！









