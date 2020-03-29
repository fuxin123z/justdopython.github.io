---
layout: post
category: python
title: 指数基金定投到底能不能赚钱？Python 来告诉你答案
tagline: by 豆豆
tags: 
  - python100
---

受疫情严重影响，全球股市都在不断下跌，就连一贯成熟、增长稳定的美股也在接二连三的不断向下熔断，仅这个月已经熔断五次了，要知道美股历史上的第一次熔断发生在 1997 年。很多人都被跌的一夜回到解放前了。

相比股市的大幅下跌，跟踪大盘指数的基金要相对平缓很多，虽然也在跌，但没有股市那么大幅度。就连巴菲特也曾经劝导我们，对于个人投资者而言，最好的投资方式就是定投指数基金。

所谓定投指数基金，就是在固定日期买入固定金额的基金。与买卖股票相比，定投指数基金省时省力，不用时刻盯盘，只需每周或者每月买入一次即可，年轻人应该多花些时间在自己的工作上，不断的提升自己的能力才是最好的投资。

那么，今天我们就用数据来验证下，定投指数基金到底能不能赚钱，又能赚多少钱呢。

<!--more-->

#### 抓取基金网站数据

国内过很多网站都可以查到基金的历史净值，本文以天天基金网为例，基金取的是「沪深 300 ETF」，代码为 510300。

首先我们打开 510300 的净值查询页面（http://fundf10.eastmoney.com/jjjz_510300.html），可以看到该基金的成立日期为 2012-05-04，到现在差不多有 8 年的历史了，该基金跟踪的是沪深 300 指数，可以说是相当有代表性的指数基金了。

![](001)

然后我们将查询日期设置为 2012-05-04 到 2020-03-01，打开 chrome 的开发者面板，切换到 Network 下，点击「查询」查看网络请求。我们会发现如下的一个请求，确认下其响应的数据确实是我们需要的基金净值数据。

![](002)

请求的 URL 如下：

```
http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183024641278834999003_1585311648931&fundCode=510300&pageIndex=1&pageSize=20&startDate=2012-05-04&endDate=2020-03-01&_=1585383229681
```

仔细观察这个请求的 URL 我们发现，fundCode 就是我们所要查询的基金代码，pageIndex 是当前页码，pageSize 是每页数量，startDate 是开始时间，endDate 是结束时间。callback 可以说对我们没什么用。

正常的逻辑是按页码来获取指定时间段的数据，简单起见，我们这里一次性将所有的数据全部获取过来，只需要将 pageSize 改成 3000 即可，因为从成立到现在还没有 8 年时间，再去除非交易日，3000 足够了。

于是，我们的爬虫程序可以这么写。老规矩，先引入本篇文章所需要的全部模块。

```python
import json
import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib import font_manager
```

获取基金历史净值数据函数如下：

```python
import requests

startDate = '2012-05-04'
endDate = '2020-03-01'
foundCode = '510300'
pageSize = 3000
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Referer': f'http://fundf10.eastmoney.com/jjjz_{foundCode}.html'
}
url = f'http://api.fund.eastmoney.com/f10/lsjz?&fundCode={foundCode}&pageIndex=1&pageSize={pageSize}&startDate={startDate}&endDate={endDate}&_=1585302987423'
response = requests.get(url, headers=header)

def write_file(content):
    filename = f'found_{foundCode}.txt'
    with open(filename, 'a') as f:
        f.write(content + '\n')

write_file(response.text)
```

至此，我们已经获取到了所需的基础数据，顺便将获取到的数据写入到了 found_510300.txt 文件中，方便后续操作。

#### 计算定投收益

有了历史净值数据，我们就要开始计算收益了。

来看下我们获取到的数据格式，其中对我们有用的就是 LSJZList 中的净值日期（FSRQ）和单位净值（DWJZ）了。因此，我们要先把数据整理成我们需要的格式，以日期为 key，净值为 value 放入到 dict 中即可。

```python
foundCode = '510300'
file = f'./found_{foundCode}.txt'
found_date_price = {}
found_price_x = []
found_price_y = []

with open(file) as f:
    line = f.readline()
    result = json.loads(line)
    for found in result['Data']['LSJZList'][::-1]:
        found_date_price[found['FSRQ']] = found['DWJZ']
        found_price_x.append(found['FSRQ'])
        found_price_y.append(found['DWJZ'])
```

这里我们采用两种计算方式，一种是周定投，一种是月定投。对应的函数分别是 `calculate_found_profit_by_week(start_date, end_date, weekday)` 和 `calculate_found_profit_by_month(start_date, end_date)`，其中两个函数共有的参数 start_date 和 end_date 分别表示起始日期，按周来计算收益的函数参数 weekday 则表示定投日，weekday 为 0 表示周一定投，1 表示周二定投...

两个函数的返回值是一样的，分别是定投次数，最终持有份额，买入总金额，实际收益。

我们的定投规则如下，每逢 weekday 或者每月 1 号定投，如果当天不是交易日则顺延至后一个交易日，同时周定投每次买入 500 元，月定投每次买入 2000 元。

calculate_found_profit_by_week 函数：

```python
# 买入规则：从 start_date 日期开始，每逢 weekday 买入，如果 weekday 不是交易日，则顺延至最近的交易日
# 每次买入 500 元，之后转化为相应的份额
def calculate_found_profit_by_week(start_date, end_date, weekday):
    total_stock = 0
    total_amount = 0
    nums = 0
    day = start_date + datetime.timedelta(days=-1)
    while day < end_date:
        day = day + datetime.timedelta(days=1)
        if day.weekday() != weekday:
            continue
        while found_date_price.get(day.strftime('%Y-%m-%d'), None) is None and day < end_date:
            day += datetime.timedelta(days=1)
        if day == end_date:
            break
        nums += 1
        total_stock += round(fixed_investment_amount_per_week / float(found_date_price[day.strftime('%Y-%m-%d')]), 2)
        total_amount += fixed_investment_amount_per_week

    # 计算盈利
    while found_date_price.get(end_date.strftime('%Y-%m-%d'), None) is None:
        end_date += datetime.timedelta(days=-1)
    
    total_profit = round(total_stock, 2) * float(found_date_price[end_date.strftime('%Y-%m-%d')]) - total_amount

    return nums, round(total_stock, 2), total_amount, round(total_profit)
```

calculate_found_profit_by_month 函数：

```python
def get_first_day_of_next_month(date):
    first_day = datetime.datetime(date.year, date.month, 1)
    days_num = calendar.monthrange(first_day.year, first_day.month)[1]  # 获取一个月有多少天
    return first_day + datetime.timedelta(days=days_num)

# 买入规则：从 start_date 日期开始，每月 1 号买入，如果 1 号不是交易日，则顺延至最近的交易日
# 每次买入 2000 元，之后转化为相应的份额
def calculate_found_profit_by_month(start_date, end_date):
    total_stock = 0
    total_amount = 0
    nums = 0
    first_day = datetime.datetime(start_date.year, start_date.month, 1)
    day = first_day + datetime.timedelta(days=-1)  # 将日期设置为 start_date 上个月最后一天
    while day < end_date:
        day = get_first_day_of_next_month(day)
        while found_date_price.get(day.strftime('%Y-%m-%d'), None) is None and day < end_date:
            day = day + datetime.timedelta(days=1)
        if day == end_date:
            break
        nums += 1
        total_stock += round(fixed_investment_amount_per_month / float(found_date_price[day.strftime('%Y-%m-%d')]), 2)
        total_amount += fixed_investment_amount_per_month

    # 计算盈利
    while found_date_price.get(end_date.strftime('%Y-%m-%d'), None) is None:
        end_date += datetime.timedelta(days=-1)

    total_profit = round(total_stock, 2) * float(found_date_price[end_date.strftime('%Y-%m-%d')]) - total_amount

    return nums, round(total_stock, 2), total_amount, round(total_profit)
```

#### 数据分析

有了净值数据，也有了定投规则和收益计算的具体实现，我们来看看我们的收益如何。

首先我们将该基金的所有净值数据生成一张折线图，来看看该基金的走势如何。

```python
def show_found(found_price):
    found_price_y = list(map(float, found_price))
    x = [i for i in range(0, len(found_price))]

    plt.figure(figsize=(10, 6))

    plt.plot(x, found_price_y, linewidth=1, color='r')

    plt.xlabel('时间', fontproperties=my_font)
    plt.ylabel('单位净值', fontproperties=my_font)
    plt.title(f"{foundCode} 基金走势", fontproperties=my_font)
    plt.xticks(x[::90], found_price_x[::90], rotation=45)

    plt.show()
```

![](003)

从图中我们可以看出，该基金在 2015 年又一个很高的顶点，原因大家都知道的，2015 年是大牛市。之后在 2017 年底又有一个小的峰值，随后在 2018 年跌入最低点。

首先我们来分析下，定投频率对投资结果的影响，我们分别统计下，周一，周二，周三，周四，周五以及月定投的收益。

计算收益函数如下：

```python
total_amount = [] # 总投资金额
total_profit = [] # 总收益金额

for i in range(5):
    result = calculate_found_profit_by_week(start_date, end_date, i)
    total_amount.append(result[2])
    total_profit.append(result[3])

result_month = calculate_found_profit_by_month(start_date, end_date)
total_amount.append(result_month[2])
total_profit.append(result_month[3])
```
得出投资金额和收益之后，我们生成柱状图来综合对比下。

```python
def show_pic():
    labels = ['周一', '周二', '周三', '周四', '周五', '月定投']
    index = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots()
    rect1 = ax.bar(index - width / 2, total_profit, color='red', width=width, label='投资收益')
    rect2 = ax.bar(index + width / 2, total_amount, color='springgreen', width=width, label='投资金额')

    plt.title("投入金额 & 收益柱状图", fontproperties=my_font)
    plt.xticks(fontproperties=my_font)
    ax.set_xticks(ticks=index)
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 220000)
    auto_text(rect1)
    auto_text(rect2)

    plt.show()
```

![](004)

由图示我么可以看出，周定投投入的金额基本一致，而月定投金额略少于周定投金额。在看收益率，周五定投收益率最高为 56263 元，而周一最少为 56263；而月定投为 56784 元。综合对比来看，单单来看周定投的话，周五定投收益最高。如果月定投也加入比较对象之内，那么月定投投资金额最低，收益率最高。

最后我们再来看看，入市时间对定投收益的影响。这次我们采用月定投的方式来计算收益。

都知道 2015 年是大牛市，那么我们就悬着在股市最高点入场，将开始时间设置为 2015-06-10，当天上证指数在 5000+，今天 2700+，最终计算出来的收益如下：

```python
start_date = datetime.datetime.fromisoformat('2015-06-10')
end_date = datetime.datetime.fromisoformat('2020-03-01')
result = calculate_found_profit_by_month(start_date, end_date)
print(result)

# 输出结果
(57, 31715.69, 114000, 10684)
```

共计定投 57 次，投入金额 114000 元，共计收益 10684，相比 2010-01-01 入场少了接近 4W 元，但至少收益率还是正的。而且这还是在股市从大牛市跌到大熊市，几近腰斩呃情况下取得的成绩。

## 总结

今天我们以沪深 300 ETF 的数据来分析了指数基金定投的收益。可以得出如下结论：

周五定投收益最高，周一最低。而周定投和月定投来比，月定投的收益率更高一些。

于此同时我们还发现，2010-01-01 上证指数在 2900 点附近，如今在 2700 点附近，指数不涨反降低，但我们的收益却不断增长。即使选择在股市最高点入市，把时间拉长，指数定投也不会亏钱。

当然，本文只做了 510300 这一只基金的数据分析，数据可能不够全面，读者可以从后台获取程序源码后，分析更多的基金数据，以及不通时间段的收益情况。

**注意：股市千变万化，是不可完全预测的，要敬畏市场。本文仅作为学习讨论，不作为任何投资建议。**

## 代码地址

> 示例代码：https://github.com/JustDoPython/python-100-day/