---
layout: post
category: python
title: 大学大比拼
tagline: by 太阳雪
tags:
  - python100
---
![标题图片]( http://justdopython.github.io/assets/images/2020/07/university/00.png)
高考刚刚结束，成绩陆续公布，接下来就要填报志愿了，如何挑选一个合适的大学几乎是每个考生面临的问题，多年前，为填报志愿通宵翻阅招生指南的情形还历历在目，今天我们从中国大学综合排名以及其他指标为视角，对大学进行分析对比，也许能对目标大学有更好的认识
<!--more-->

先看下部分结果图

![指标对比](http://www.justdopython.com/assets/images/2020/07/university/02.png)

![排名走势](http://www.justdopython.com/assets/images/2020/07/university/01.png)

下面将以构建过程为顺序，进行说明，如果只想要结果，翻到文后，查看并回复关键字，获取代码运行即可

## 数据采集

数据分析的第一步是数据采集，搜索查找后，发现 `最好大学网` 上有公布的中国大学数据，从 2015 年至今，从十个不同维度对学校进行记录，用来分析对比再好不过

爬取时会有些障碍点：

- 2015 年数据，分了将 10 个指标分为 3 大类，每一类用单独的网页来呈现，而后的几年只用一个页面呈现了所有指标数据
- 有些年份数据中，双标题中包含了`换行符`或者`回车符`，需要识别并处理
- 还有些标题并非单纯文字，包含了 Html 标记，获取到后需要单独处理，从中取到文字部分

这是数据抓取的部分核心代码：

```python
from bs4 import BeautifulSoup as Bs
import pandas as pd
import numpy as np

def dataProcessing(html, num):
    rows = Bs(html, 'html.parser').table.find_all('tr', limit=num, recursive=True)

    thf = []
    for th in rows[0].find_all('th', limit=10):
        if th.text.find('\r\n') == -1 and th.text.find('\n') == -1:
            thf.append(th.contents)
    for i in [op.contents for op in rows[0].find_all('option', recursive=True)]:
        thf.append(i)
    thf = ["".join(th) for th in thf]

    universityList = []
    for tr in rows[1:]:
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        contents = [td.contents for td in tds]
        if len(contents[0]) > 1:
            contents[0] = [contents[0][0]]
        contents[1] = contents[1][0].contents
        universityList.append(["".join(attr) for attr in contents])

    return pd.DataFrame(np.array(universityList), columns=thf)
```

- `dataProcessing` 方法接收一个字符串，和一个数值，字符串为目标页面的 Html 文本，数值表示需要获取的大学数量，分析数据后，2020 年记录的大学最全，共有 549 个
- 先将 html 字符串 转换为 BeautifulSoup 对象，再从 table 对象中筛选出 tr 即列表行来
- 第一行为标题，除了 2015 年，其他年份处理方式一样，先获取简单标题，之后，从指标选择框中获取指标标题，存放在 `thf` 中
- 接下来处理记录，从中提取每一列数据，存放在 `universityList` 中
- 最后将记录数据转换为 numpy.array 结构，用标题做列，将数据创建成 pandas 的 DataFrame 结构并返回

转换为 DataFrame 结构主要是为了方便存储为 Excel，调用 `DataFrame.to_excel` 方法，指定文件名，就能将数据保存到 Excel 文件

> 特别提醒：
> **数据分析中，原始数据至关重要**，无论做什么分析，请确保原始数据不被修改，这也是为什么不直接对获取的 DataFrame 进行处理，而是先存储为 Excel 的原因

## 数据整理

原始数据常常需要清理后才能被使用，因为可能一些问题，直接分析，可能出错，或者影响分析结果

对数据检查后发现，存在以下问题：

- 存在空缺值，比如就业率，有些学校的没有被统计
- 存在指标空缺或不一致，比如 2015、2016 年度，没有留学生比例指标
- 存在非数值字符，比如科研质量指标有些数字前有 `>`
- 不同指标采用的数值范围不同，比如社会声誉范围从 0 到 百万，而科研质量数值范围仅在 0 ~ 2 之间
- 原始数据的指标名称较长，比如 `生源质量（新生高考成绩得分）`，太长的名称不利于图表展示，需要对指标名称进行处理

针对上述问题，做了个配置，定义不同指标的处理方式，另外可以在处理逻辑中减少对具体的业务问题的依赖，使代码更简单：

```python
## 读取文件 选择特定的列，队列进行归一化，之后对整个数值进行归一化
config = {
    '学校名称': {'name': '学校'},
    '省市': {'name': '省市'},
    '排名': {'name': '排名', 'fun': lambda x: 500-int(x) if x is not np.nan else int(x)},
    '总分': {'name': '总分'},
    '生源质量（新生高考成绩得分）':{'name': '生源质量', 'norm': True},
    '培养成果（本科毕业生就业率）':{'name': '就业', 'alias': '培养结果（毕业生就业率）', 'norm': True, 'fun': lambda x: float(x[:-1])/100 if x is not np.nan else float(x)},
    '社会声誉（社会捐赠收入·千元）':{'name': '声誉', 'norm': True},
    '科研规模（论文数量·篇）':{'name': '科研规模', 'norm': True},
    '科研质量（论文质量·FWCI）':{'name': '科研质量', 'norm': True, 'fun': lambda x: float(x) if str(x).find(">")==-1 else float(x[1:]) },
    '顶尖成果（高被引论文·篇）':{'name': '顶尖成果', 'norm': True},
    '顶尖人才（高被引学者·人）':{'name': '顶尖人才', 'norm': True},
    '科技服务（企业科研经费·千元）':{'name': '科技服务', 'norm': True},
    '成果转化（技术转让收入·千元）':{'name': '成果转化', 'norm': True},
    '学生国际化（留学生比例）':{'name': '学生国际化', 'norm': True, 'fun': lambda x: float(x) if str(x).find("%")==-1 else float(x[:-1])}
}
```

- 配置是一个 Dirt 对象，Key 为原始数据的列名，值也是一个 Dirt 对象，用于说明应该如何处理原始数据
- `name` 表示需要将原始列名换成的列名
- `norm` 表示是否要对该列做归一化处理（后面会解释）
- `alias` 表示列的别名，在原始数据中，存在不同年份同一指标使用不同列名的现象，为此而设立
- `fun` 表示一个对原始值进行处理的方法，比如取消百分号，大于号或者做数据反转等，采用 lambda 表达式，使用定义好的方法名也可以

这里着重说明下归一化

**归一化的基本含义是将原始的数值，转换为从 0 ~ 1 之间的某个数值**，为什么要这么做呢？是为了让不同指标可对比，想象一下，如果不处理，数值在 1 ~ 10 的指标就没法和数值在 1000 ~ 10000 的指标进行对比

归一化的主要方式一般有 3 种，**线性转换、对数函数转换** 和 **反余切函数转换**

这里采用线性转换，公式是：

![线性转换](http://www.justdopython.com/assets/images/2020/07/university/03.png)

用 pandas 实现代码为：

```python
 dft = (dft - dft.min())/(dft.max() - dft.min())
```

`dft` 为一个指标的数值集合

处理完成数据后，将处理结果存入 Excel 文件（注意不要覆盖原始数据文件），之所以将数据存入文件，是为了后续查询时，不必每次都将原始数据处理一遍

## 数据分析及可视化

数据分析首先需要明确目标，我们就以展示不同大学在多个指标上的能力对比，以及某个指标在各年份的走势为目标

### 分析

因为数据整理中，对各个指标做了归一化处理，所有指标之间具备了可比性

结合业务对数据进行研究，得到以下结论：

- 目前各个学校，很重视就业率，采用各种方式会将就业率提高，数据中的体现是，无论学校好坏，就业率都在 90% 以上
- 中国大学，除了专门的外国语学校，外国留学生很少，数据中，学生国际化指标普遍较低，鉴于本分析是针对国内考生的，此指标意义不大
- 成果转换，表示的是年度技术转让收入，目前各个学校都是以培养实用型人才为目标，纯理论科研水平和意识较低，成果转换普遍较低

基于以上结论，在指标对比分析中，去除掉 就业率、学生国际化 和 成果转换 三个指标

### 可视化

**多项指标对比**，使用雷达图比较合适，可以直观的展示出一个学校的能力范围，另外，雷达图能同时对多个学校进行对比，代码如下：

```python
def indicatorChart(schools, indicators=['生源质量','声誉','科研规模',
'科研质量','顶尖成果','顶尖人才','科技服务',], year=2019):
    """
    指定学校，年份，以及需要对比的指标，显示出雷达图
    """
    year = str(year) + '年'
    result = pd.DataFrame(index=schools,columns=indicators)
    df = data[year][indicators]
    for school in schools:
        if school in df.index:
            result.loc[school] = df.loc[school]

    labels=result.columns.values #特征值
    kinds = list(result.index) #成员变量
    result = pd.concat([result, result[[labels[0]]]], axis=1) # 由于在雷达图中，要保证数据闭合，这里就再添加第一列，并转换为np.ndarray
    centers = np.array(result.iloc[:,:])
    n = len(labels)
    angle = np.linspace(0, 2 * np.pi, n, endpoint=False)# 设置雷达图的角度,用于平分切开一个圆面
    angle = np.concatenate((angle, [angle[0]]))#为了使雷达图一圈封闭起来,需要下面的步骤
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True) # 参数polar, 以极坐标的形式绘制图

    for i in range(len(kinds)):
        ax.plot(angle, centers[i], linewidth=1.5, label=kinds[i])
        plt.fill(angle,centers[i] , 'r', alpha=0.05)

    ax.set_thetagrids(angle * 180 / np.pi, labels)
    plt.title(year + ' 指标对比')
    plt.legend()
    plt.show()
```

- `pd` 为 pandas，`np` 为 numpy
- 代码中的 data 是以年份为 key 的，值为对应年份结构为 DataFrame 的数据，方便按年获取相应数据
- 极坐标实际上就是二维坐标系的变形，即将两个 y 轴合并一起，所以要在数据最末列添加上数据的第一列
- 雷达图是用 matplotlib 极坐标图表绘制的
- 其他代码基本是绘制雷达图固定的，只要计算出 labels、kinds、centers就好了

**指标走势**，采用折线图，对指定的学校，展示出某个指标的走势，之间利用 pandas 的 plot 工具来绘制就可以，需要特别处理的是，将年份作为列，学校作为索引，对应的值为某个指标的值：

```python
def trendChart(schools, indicator='总分'):
    """
    给定学校(数组)，得到这些学校5年的趋势图
    """
    ret = pd.DataFrame(index=[str(x)+"年" for x in range(2015,2020)],columns=schools)

    for year in data:
        df = data[year][indicator]
        for school in schools:
            if school in df.index:
                ret.loc[year, school] = df[school]
            else:
                ret.loc[year, school] = np.nan

    ret.plot.line(title="%s 走势" % indicator, linewidth=1.5, yticks=[])
    plt.show()
```

代码相对简单，不做赘述

> 注意：上面两个图表方法中，都对不存的学校做了处理，否则执行中可能会提示找不到对应的列或者索引

## 使用

代码分为三部分，`dataCapture.py` 数据抓取、`dataProcess.py` 数据整理  和 `dataShow.py` 可视化

每个部分都是独立的，他们之间通过数据的 Excel 文件关联，数据抓取产生原始数据文件，数据整理产生整理后的数据文件，可视化读取整理后的数据文件做展示

如果从头开始，依次执行代码文件，注意执行命令的当前路径需要在代码目录下

如果只想展示结果，待分析数据我已处理好，只需执行 `dataShow.py` 就行，更换不同的学校名称以及指标，就可以得到不同的结果：

```python
# 显示不同大学指标对比雷达图
indicatorChart(['清华大学', '北京大学','上海交通大学', '浙江大学', '复旦大学'])

# 显示不同学校总体排名走势图
trendChart(['北京理工大学', '西北工业大学', '东华大学', '福州大学', '中国矿业大学'], '排名')
```

## 总结

今天我们从数据分析的角度对中国的大学做了简单对比，学习数据分析过程的同时，可以对要选择学校的朋友，通过不同角度的参考。当然分析过程比较简略，数据展示过于粗糙，如果你有兴趣，可以尝试将展示结果 Web 化，做成一个 Web 应用，以及可以增加更多的分析方式，提升技能的同时，还可以帮助更多的人。

特别感谢滴滴出行数据科学家 Rose 的大力支持和帮助

## 参考

- [http://zuihaodaxue.com/index.html](http://zuihaodaxue.com/index.html)
- [https://blog.csdn.net/weixin_43941364/java/article/details/105949701](https://blog.csdn.net/weixin_43941364/java/article/details/105949701)
- [https://blog.csdn.net/weixin_30702413/article/details/95034435](https://blog.csdn.net/weixin_30702413/article/details/95034435)
- [https://blog.csdn.net/weixin_41895381/article/details/92794464](https://blog.csdn.net/weixin_41895381/article/details/92794464)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/university>
