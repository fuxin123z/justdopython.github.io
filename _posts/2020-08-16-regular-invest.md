---
layout: post
category: python
title: 定投到底好不好 —— python 告诉你答案
tagline: by 太阳雪
tags:
  - python
  - matplotlib
  - 定投
---
最近股市火热，有很多人跃跃欲试，面对琢磨不透的市场，除了随波逐流，勇当韭菜的命运外，还有没有其他选择呢？今天就用 Python，从定投的视角上重新认识下股市。
<!--more-->

## 定投

很多人都听说过定投的概念，定投就是定期定额买入一个标的（股票、基金或者其他有增长空间的投资物），并且长期持有，最终会获得很好的收益，是很好的投资策略

关于长期，股神巴菲特说：
> 如果你没打算将一只股票持有十年，甚至都不用考虑持有十分钟

言下之意长期就是十年或者永远。

为什么要定投？一般认为，定投可以拉低购买的成本价，使收益扩大

不过也可能抬高成本价

真正原因是，市场中的 **熊市比牛市长很多很多**，定投相当于在长期的熊市里积聚力量，最终在牛市中展现出投资的价值

真是这样的吗？

下面我们就研究下国内市场上的一些股票基金，看看结果如何

## 获取数据

我们以网易财经 <http://quotes.money.163.com/old/#HS> 作为数据来源

通过指定股票或者基金代码获取数据

由于网易财经股票和基金 url 和 展示页不同，所以需要分别处理，以获取基金数据为例：

```python
def fund(code):
    url = 'http://quotes.money.163.com/fund/jzzs_%s_%d.html?start=2001-01-01&end=2020-12-31&sort=TDATE&order=asc'
    data = pd.DataFrame()
    for i in range(0, 100):
        html = getHtml(url % (code, i))
        page = dataFund(html)
        if page is not None:
            data = data.append(page, ignore_index=True)
        else:
            break
        print("page ", i)
        time.sleep(1)
    filename = 'fund_%s.xlsx' % code
    data.to_excel(filename, index=False)
    print("数据文件:", filename)

def getHtml(url)):
    while(True):
        rp = rq.get(url)
        rp.encoding = 'utf-8'
        if rp.text.find("对不起!您所访问的页面出现错误") > -1:
            print("获取过于频繁，等待 5 秒再试")
            time.sleep(5)
            continue
        else:
            break
    return rp.text

def dataFund(html):
    table = Bs(html, 'html.parser').table
    if table is None:
        print(html)
        return None
    rows = table.find_all('tr', recursive=True)
    data = []
    columns = [th.text for th in rows[0].find_all('th')]
    for i in range(1, len(rows)):
        data.append(rows[i].text.split('\n')[1:-1])
    if len(data) > 0:
        pdata = pd.DataFrame(np.array(data), columns=columns)
        return pdata
    else:
        return None
```

- 方法 `fund` 为基金数据获取总方法，接受基金代码作为参数
- 通过特定的 url，可查询到 2001 年到 2020 年间的数据，数据开始时间晚于 2001 年的，会以实际开始时间来获取
- 数据是分页展示的，预设最大为 100 页，循环每一页获取数据
- 将获取的数据追加到 `data` 中，`data` 为 pandas 的 DataFrame
- 最后将数据存入以类型和代码命名的 Excel 文件中
- 方法 `getHtml` 接受 url 作为参数，返回 html 字符串
- `rq` 是 requests 的别名，通过 get 方法，获取页面的 html 字符串
- 判断是否被拒绝访问，如果被拒绝，等待 5 秒再试
- 方式 `dataFund` 接受 html 字符串作为参数，从中抓取基金数据
- 因为页面只有一个 table，所以先拿到 table，然后提取所有行
- 从第一行中获取列名
- 然后获取其他行的数据，存入 data 列表
- 如果获取到了数据，将数据转换为 DataFrame 对象返回，否则返回 `None`

例如获取代码为 `150124` 的基金：

```python
fund('150124')
```

最后在当前目录中，生成 `fund_150124.xlsx` 文件

相应的股票对应的方法是 `stock`，例如获取代码为 `601600` 的股票数据：

```python
fund('601600')
```

生成的数据文件则为: `stock_601600.xlsx`

## 整理数据

股票数据和基金数据列有所不同，需要在分析前将数据处理为统一的形式

另外，定投而言，只需保留`日期`和`价格`，这样也有助于减少数据量

代码如下：

```python
def dataFormat(code, type_='fund', cycleDays=5, begin='2001-01-01'):
    rawdf = pd.read_excel('%s_%s.xlsx' % (type_, code))
    buydf = rawdf[rawdf.index % cycleDays==0] ## 选出定投时机
    # 选择对应的列
    if type_ == 'fund':
        buydf = buydf[['公布日期','单位净值']]
    else:
        buydf = buydf[['日期','收盘价']]
    buydf.columns = ["日期","单价"]

    buydf = buydf[buydf['日期']>=begin]
    return buydf
```

- 方法 `dataFormat` 为数据整理方法
- 参数 `code` 为股票或者基金代码，`type_` 用来指定分析的是股票还是基金
- 参数 `cycleDays` 表示定投时间间隔，默认为 5 天，即一个星期(扣除周末)
- 参数 `begin` 为开始定投日期，默认为 2001-01-01，这也是获取数据最早的日期
- 根据 `code` 和 `type_` 用 pandas 读取数据文件，存入原始数据 `rawdf` 中
- 再从 `rawdf` 中过滤出购买定投的数据，即从开始日期起，把每隔定投时间间隔的数据筛选出来，出入 `buydf`
- 然后根据 `type_` 参数抽取需要的列，即 `日期` 和 `价格`，由于股票数据和基金数据的列名不同，需要更新为统一的列，`日期` 和 `单价`
- 最后再筛选出开始日期及以后的数据，作为定投数据

## 呈现

开始之前，需要先搞清楚怎么计算定投的价值

首先在每个定投点上，需要定投固定的金额，这个金额除以当前价格，会得到购买份数

持续下去，到将来某个点上，价值是多少呢？应该是 **此前所有购买份数之和乘以这个点上的价格**

对比每个点上定投的金额合计与这个点上的价值，就能知道此点上是盈是亏，用图表来展示更加直观

代码如下：

```python
def show(buydf, amount=1000):
    buydf.insert(2,'定投金额', np.array(len(buydf)*[amount]))  ## 增加定投列
    buydf.insert(3,'数量', buydf['单价'].apply(lambda x: amount/x))  # 计算出价值
    buydf.insert(4,'累计本金', buydf['定投金额'].cumsum())  ## 计算定投累计
    buydf.insert(5,'累计数量', buydf['数量'].cumsum())  ## 计算价值累计
    buydf.insert(6,'当前价值', buydf['累计数量']*buydf['单价']) ## 计算实际单价

    ## 净值趋势
    tend = pd.DataFrame(columns=['单价'],index=buydf['日期'].to_list(),data={'单价':buydf['单价'].to_list()})

    tend.plot.line(title="净值走势", linewidth=1.5, yticks=[])
    plt.show()

    ## 选取投资比较
    data = pd.DataFrame(columns=['累计本金','当前价值'],
        index=buydf['日期'].to_list(),
        data={'累计本金': buydf['累计本金'].to_list(),
              '当前价值': buydf['当前价值'].to_list()})

    data.plot.line(title="定投效果", linewidth=1.5, yticks=[])
    plt.show()
```

- 方法 `show` 数据展示方法，接受两个参数，`buydf` 为需要定投的数据，`amount` 为定投金额
- 向 `buydf` 中插入辅助计算的列，并利用 pandas 的集合运算计算出 `数量`、`累计本金`、`累计数量` 和 `当前价值`，其中 DataFrame 的 `cumsum` 方法会计算每行的累计值
- 再提取 `单价` 用于展示价格走势
- 最后提取 `累计本金` 和 `当前价值` 作为投资效果展示

> 价格走势和投资效果最好展示在一个图表上，试试有什么办法可以做到，欢迎在学习群里交流

以基金建信央视50B (150124) 为例，从2015年5月26日开始到现在的定投：

```python
show(dataFormat('150124', begin='2015-05-26'))
```

图表如下：

![价格走势](http://www.justdopython.com/assets/images/2020/08/regular_invest/01.jpg)

![定投效果](http://www.justdopython.com/assets/images/2020/08/regular_invest/02.jpg)

> **注意**：基金为随意挑选，并不具备投资参考价值

## 结论

对多个不同的基金、股票做定投分析，发现以下结论：

- 更早的投资，获取收益的可能性较大
- 熊市越久，最后获得的收益越好
- 无论是熊市还是牛市买入，长期来看对最终结果影响不大
- 最重要的是：即使在最高点买入，在价格收复之前，价值便会超过成本，太神奇了！

最终可以得到一个与众不同的观点，定投策略几乎可以稳赚，只要坚持的时间够久

与大多数人认知不同的是，熊市是最终收益的基础，进一步证实了:

> 市场中的熊市比牛市长很多很多，定投相当于在长期的熊市里积聚力量，最终在牛市中展现出投资的价值

你怎么看的，跑下代码试试看

## 总结

习得一个技能，不仅仅可以提高效率，更重要的是它可能改变我们的思考方式，将之前视而不见的东西，看的更清楚，理解的更透彻了，就像带上了眼镜，面对的是相同的世界，却看的更清晰了。

## 参考

- [https://www.liaoxuefeng.com/wiki/1016959663602400/1017785454949568](https://www.liaoxuefeng.com/wiki/1016959663602400/1017785454949568)
- [https://blog.csdn.net/ajian6/article/details/93615594](https://blog.csdn.net/ajian6/article/details/93615594)
- [https://www.pythonf.cn/read/71](https://www.pythonf.cn/read/71)
- <https://zhuanlan.zhihu.com/p/33450843>
- <https://ri.firesbox.com/#/cn/>

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/regular_invest>
