---
layout: post
category: python
title: 用 Python 获取股市交易数据
tagline: by 極光
tags:
  - python100
---

最近受全球大环境影响，美股犹如坐上过山车，感觉每天都在见证历史时刻。而我们的大盘最近也不消停，不过这也给大家抄底制造了机会，但机会都是给有准备的人，想要抓住机会就得懂得分析数据，想要分析数据还得先拿到交易数据，今天就来说说用 Python 如何获取股市交易数据。

<!--more-->

## TuShare 工具

Tushare 是一个免费、开源的 Python 财经数据接口包。主要实现对股票等金融数据从数据采集、清洗加工到数据存储的过程，能够为金融分析人员提供快速、整洁、和多样的便于分析的数据，为他们在数据获取方面极大地减轻工作量，使他们更加专注于策略和模型的研究与实现上。

## 安装

Tushare 的运行需要 `pandas` 模块支持，所以需要先安装它，然后再安装 `tushare`：

```sh
$ pip3 install pandas
 …… 忽略日志

$ pip3 install tushare
 …… 忽略日志
```

安装完成后，会看到 `Successfully installed` 提示即为安装成功。下面我们简单看下它都提供了哪些功能。

## 功能说明

### 1、获取历史数据

get_hist_data()：获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线，以及5分钟、15分钟、30分钟和60分钟k线数据。我们通过下面引入包，然后执行这个方法就可以获取上证指数的历史交易数据。

```py
# 引入包
import tushare as tu

# 获取上证指数历史三年的数据
tu.get_hist_data('000001')

# 当然我们也可以只获取一段时间范围内的数据
tu.get_hist_data('000001',start='2020-01-05',end='2020-02-05')

```

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-01.png)

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-02.png)


参数说明：
- code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
- start：开始日期，格式YYYY-MM-DD
- end：结束日期，格式YYYY-MM-DD
- ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
- retry_count：当网络异常后重试次数，默认为3
- pause:重试时停顿秒数，默认为0

返回值说明：
- date：日期
- open：开盘价
- high：最高价
- close：收盘价
- low：最低价
- volume：成交量
- price_change：价格变动
- p_change：涨跌幅
- ma5：5日均价
- ma10：10日均价
- ma20:20日均价
- v_ma5:5日均量
- v_ma10:10日均量
- v_ma20:20日均量
- turnover:换手率[注：指数无此项]

### 2、获取时实行情

get_today_all()：一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日）。

```py
# 引入包
import tushare as tu

# 获取所有股票当前行情
tu.get_today_all()

```

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-03.png)

返回值说明：
- code：代码
- name:名称
- changepercent:涨跌幅
- trade:现价
- open:开盘价
- high:最高价
- low:最低价
- settlement:昨日收盘价
- volume:成交量
- turnoverratio:换手率
- amount:成交金额
- per:市盈率
- pb:市净率
- mktcap:总市值
- nmc:流通市值

### 3、获取实时交易数据

get_realtime_quotes(): 可获取实时分笔数据，可以实时取得股票当前报价和成交信息，实时监测交易量和价格的变化。

```py
# 引入包
import tushare as tu

# 获取茅台和格力两支股票的实时数据
data = tu.get_realtime_quotes(['600519','000651'])

# 也可以设置只显示某些值
data[['code','name','price','bid','ask','volume','amount','time']]

#或者获取上证指数 深圳成指 沪深300指数 上证50 中小板 创业板
tu.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])

```

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-05.png)

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-06.png)

返回值说明：
- 0：name，股票名字
- 1：open，今日开盘价
- 2：pre_close，昨日收盘价
- 3：price，当前价格
- 4：high，今日最高价
- 5：low，今日最低价
- 6：bid，竞买价，即“买一”报价
- 7：ask，竞卖价，即“卖一”报价
- 8：volume，成交量 maybe you need do volume/100
- 9：amount，成交金额（元 CNY）
- 10：b1_v，委买一（笔数 bid volume）
- 11：b1_p，委买一（价格 bid price）
- 12：b2_v，“买二”
- 13：b2_p，“买二”
- 14：b3_v，“买三”
- 15：b3_p，“买三”
- 16：b4_v，“买四”
- 17：b4_p，“买四”
- 18：b5_v，“买五”
- 19：b5_p，“买五”
- 20：a1_v，委卖一（笔数 ask volume）
- 21：a1_p，委卖一（价格 ask price）
- …… 忽略部分
- 30：date，日期；
- 31：time，时间；

### 4、大盘指数行情列表

get_index()：获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。

```py
# 引入包
import tushare as tu

# 获取大盘行情
data = tu.get_index()

```

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-07.png)

返回值说明：
- code:指数代码
- name:指数名称
- change:涨跌幅
- open:开盘点位
- preclose:昨日收盘点位
- close:收盘点位
- high:最高点位
- low:最低点位
- volume:成交量(手)
- amount:成交金额（亿元）

### 5、大单交易数据

get_sina_dd()：获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。

```py
# 引入包
import tushare as tu

# 获取茅台当前日期的大单交易数据，默认400手
tu.get_sina_dd('600519', date='2020-03-27')

# 获取交易100手以上的数据
tu.get_sina_dd('600519', date='2020-03-27', vol=100)

```

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-tushare-08.png)

参数说明：
- code：股票代码，即6位数字代码
- date：日期，格式YYYY-MM-DD
- vol：手数，默认为400手，输入数值型参数
- retry_count：int, 默认3,如遇网络等问题重复执行的次数
- pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

返回值说明：
- code：代码
- name：名称
- time：时间
- price：当前价格
- volume：成交手
- preprice ：上一笔价格
- type：买卖类型【买盘、卖盘、中性盘】

## 总结

本文为大家简单介绍了 `Tushare` 工具的一小部分功能，通过这些通过我们就能获取到大量的分析数据，当然它还有很多强大的接口功能，如果感兴趣以后再介绍，或者你可以直接访问它的官网了解更多。

## 参考

Tushare 官网：http://tushare.waditu.com/

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/jiguang/tushare>
