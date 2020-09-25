---
layout: post
title: 还在为多张Excel汇总统计发愁？Python 秒处理真香！
category: python
tagline: by 闲欢
tags: 
  - python
  - 数据分析
  - 表格处理
---


为什么越来越多的非程序员白领都开始学习 Python ？他们可能并不是想要学习 Python 去爬取一些网站从而获得酷酷的成就感，而是工作中遇到好多数据分析处理的问题，用 Python 就可以简单高效地解决。本文就通过一个实际的例子来给大家展示一下 Python 是如何应用于实际工作中高效解决复杂问题的。

<!--more-->

### 背景

小明就职于一家户外运动专营公司，他们公司旗下有好多个品牌，并且涉及到很多细分的行业。小明在这家公司任数据分析师，平时都是通过 Excel 来做数据分析的。今天老板丢给他一个任务：下班前筛选出集团公司旗下最近一年销售额前五名的品牌以及销售额。

对于 Excel 大佬来说，这不就是分分钟的事吗？小明并没有放在眼里，直到市场部的同事将原始的数据文件发给他，他才意识到事情并没有那么简单：

![表格文件（数据来源于网络）](http://www.justdopython.com/assets/images/2020/09/pandasexcel/1.jpg)

这并不是想象中的排序取前五就行了。这总共有90个文件，按常规的思路来看，他要么将所有文件的内容复制到一张表中进行分类汇总，要么将每张表格进行分类汇总，然后再最最终结果进行分类汇总。

想想这工作量，再想想截止时间，小明挠了挠头，感觉到要渐渐头秃。

### 思路分析

这种体力活，写程序解决是最轻松的啦。小明这时候想到了他的程序员好朋友小段，于是他把这个问题抛给了小段。

小段缕了下他那所剩无几的头发，说：so easy，只需要找潘大师即可。

小明说：你搞不定吗？还要找其他人！

小段苦笑说：不不不，潘大师是 Python 里面一个处理数据的库，叫 Pandas ，俗称 潘大师。

小明说：我不管什么大师不大师，就说需要多久搞定。

小段说：给我几分钟写程序，再跑几秒钟就好了！

小明发过去了膜拜大佬的表情。

小段略微思考了下，整理了一下程序思路：

- 计算每张表每一行的销售额，用“访客数 * 转化率 * 客单价”就行。
- 将每张表格根据品牌汇总销售额。
- 将所有表格的结果汇总成一张总表
- 在总表中根据品牌汇总销售额并排序


### 编码

第零步，读取 Excel :

```
import pandas as pd

df = pd.read_excel("./tables/" + name)
```

第一步，计算每张表格内的销售额：

```
df['销售额'] = df['访客数'] * df['转化率'] * df['客单价']

```

第二步，将每张表格根据品牌汇总销售额：

```
df_sum = df.groupby('品牌')['销售额'].sum().reset_index()
```

第三步，将所有表格的结果汇总成一张总表：

```
result = pd.DataFrame()
result = pd.concat([result, df_sum])
```

第四步，在总表中根据品牌汇总销售额并排序：

```
final = result.groupby('品牌')['销售额'].sum().reset_index().sort_values('销售额', ascending=False)
```

最后，我们来看看完整的程序：

```
import pandas as pd
import os

result = pd.DataFrame()

for name in os.listdir("./tables"):
    try:
        df = pd.read_excel("./tables/" + name)
        df['销售额'] = df['访客数'] * df['转化率'] * df['客单价']
        df_sum = df.groupby('品牌')['销售额'].sum().reset_index()
        result = pd.concat([result, df_sum])
    except:
        print(name)
        pass

final = result.groupby('品牌')['销售额'].sum().reset_index().sort_values('销售额', ascending=False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(final.head())
```

最后的结果是这样的：

```
       品牌           销售额
15   品牌-5 1078060923.62
8   品牌-17 1064495314.96
4   品牌-13 1038560274.21
3   品牌-12 1026115153.00
13   品牌-3 1006908609.07
```

可以看到最终的前五已经出来了，整个程序运行起来还是很快的。

几分钟之后，小段就把结果给小明发过去了，小明感动得内牛满面，直呼改天请吃饭，拜师学艺！


### 总结

本文主要是想通过一个实际的案例来向大家展示潘大师（Pandas）的魅力，特别是应用于这种表格处理，可以说是太方便了。写过程序的可能都有点熟悉的感觉，这种处理方式有点类似于 SQL 查询语句。潘大师不仅能使我们的程序处理起来变得更简单高效，对于需要经常处理表格的非程序员也是非常友好的，上手起来也比较简单。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xianhuan/pandasexcel>
