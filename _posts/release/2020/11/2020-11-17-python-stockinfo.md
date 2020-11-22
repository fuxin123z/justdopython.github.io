---
layout: post
title: 价值十万的代码之二---手把手教你获取数据篇
category: python
tagline: by 闲欢
tags: 
  - python
  - 股票
  - 数据分析
---

上篇文章 [一份代码帮我赚了10万](https://mp.weixin.qq.com/s/Xscy84JwgEeaBs3fE-XnDQ/) 中，小酱承诺如果大家点赞数超过30个，我会继续分享如何利用个股研报数据来进行分析。小酱是个信守承诺的小伙子，既然答应了大家，就一定会做到的。

我们要利用个股研报数据，肯定是会结合个股行情数据的，所以首先要获取股票数据，本篇我跟大家分享一下我是如何获取个股行情数据的。

<!--more-->

### 选定目标

现在获取股票行情数据的渠道有好多，比较正规的途径就是各种量化平台的 API 接口，主要分两类：

1. 有条件免费或者可以在平台上使用数据的量化平台，例如聚宽（https://www.joinquant.com/）、Tushare平台（http://tushare.org/）。
2. 大型财经平台的量化平台，例如同花顺的  MindGO（http://quant.10jqka.com.cn/platform/html/home.html）、东方财富的 Choice 数据量化（http://quantapi.eastmoney.com/）。

第一种渠道，如果你在他们平台上去用 Python 写交易策略模型进行回测很方便，平台上是使用的 Jupyter Notebook 来编辑程序，但是如果想获取行情数据到本地，自己自由支配就需要通过他们提供的 API 接口来获取数据，而 API 接口通常对数据量或者访问频次有限制，导致我们很难随心所欲地获取数据。

第二种渠道，也可以在平台上进行回测，想要获取数据到本地基本上是需要交费成为会员才可以。

为了图免费方便，大多数人选择第一种方式，在他们平台上去写各种策略模型或者程序实现自己的逻辑，对模型进行回测。

对于我个人来说，我选择了第三种方式，不依靠免费平台的数据，也不花钱去购买数据，而是靠个人能力获取所有数据到本地存储。因为我不喜欢依赖别人的平台，万一哪天突然垮掉了或者收费了呢？在有选择的前提下，我更不愿意花费巨额资金去购买，虽然研究这个一方面也是为了赚钱，但是能省点是点，不是吗？

大家应该也猜到了我所谓的“个人能力”是啥，无非就是靠技术手段去获取，虽然麻烦点，但是很香啊！

我的主要目标网站就是国内比较大的媒体网站的财经版块，有 搜狐财经（https://q.stock.sohu.com/）、新浪财经（http://vip.stock.finance.sina.com.cn/mkt/）、网易财经（http://quotes.money.163.com/stock）和东方财富网。从这些财经版块的页面去找到个股行情数据，然后将其爬取到本地。

这里面我自己长期固定的目标是网易财经，因为到目前为止，获取数据比较稳定，并且个股的信息比较丰富。下面我就分享一下我获取个股每日行情数据的方法。


### 分析目标页面

我们获取数据的第一步是找到目标页面，既然是获取股票数据，我们肯定是要找到网易财经的股票页面：http://quotes.money.163.com/stock。

然后在这个页面的左侧导航栏中找到“涨跌排行”栏目，点击选择“沪深A股”，如下图所示：

![网易财经股票页面](http://www.justdopython.com/assets/images/2020/11/stockinfo/0.png)

我们就来到了最新的行情数据页面，网址如下：
> http://quotes.money.163.com/old/#query=EQA&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=
0

如果当前时间是交易时间，那么这个页面显示的是实时行情，如果当前时间是非交易时间，那么这个页面显示的是最近交易日的收盘行情。我们来看看这个页面：

![网易财经沪深行情](http://www.justdopython.com/assets/images/2020/11/stockinfo/1.png)

如果单纯看这个网页的网址，或许你会想是不是我替换一下 count 和 page 这两个参数就可以获取数据了。但是实际上替换 count 管用，可以改变页面每页的记录数，而 page 参数，无论你填什么值，页面都不会有变化。所以我们先放弃这个点，去看看页面的请求，看能不能发现“天机”。

逐条扫描请求，我们会发现有一个请求是这样的：

![请求链接](http://www.justdopython.com/assets/images/2020/11/stockinfo/2.png)

看起来这个返回结果是我们所需要的行情数据。找到它之后，接下来我们再来看看请求参数：


```
host：请求域名
page：请求页码
query：未知
fields：获取股票数据的列
sort：股票数据排序方式
order：排序顺序
count：每页显示数目
type：请求类型
```

对于我们来说，我们只需要关心 page、fields、count 这几个参数就行，其他的就按照页面的来，每次请求带上一样的值就好。而对于 fields 这个参数，我觉得好不容易爬一次数据，肯定数据列越全越好，所以全部都要吧，小孩才做选择呢！我们点击页面下面的翻页页码，可以观察到 page 参数是变化的，因此我们可以根据 page 的变化来获取每一页的数据，从而获取到所有股票行情数据。


### 代码实现

第一步，肯定是发送请求，获取返回数据：

```python

def get_data(self, url):
        response = requests.get(url, headers=self.ua_header, verify=False)
        content = response.content.decode('unicode_escape')
        return content
        
```

接着，我会对请求到的数据做一些自定义的特殊处理，因为返回的数据信息当中可能会包含有“:”、“""”、“{}”之类的符号，从而影响到后续的数据 json 解析，所以我必须想办法先干掉他们：

```python

def deal_json_invaild(self, data):
        data = data.replace("\n", "\\n").replace("\r", "\\r").replace("\n\r", "\\n\\r") \
            .replace("\r\n", "\\r\\n") \
            .replace("\t", "\\t")
        data = data.replace('":"', '&&GSRGSR&&')\
            .replace('":', "%%GSRGSR%%") \
            .replace('","', "$$GSRGSR$$")\
            .replace(',"', "~~GSRGSR~~") \
            .replace('{"', "@@GSRGSR@@") \
            .replace('"}', "**GSRGSR**")
        # print(data)

        data = data.replace('"', r'\"') \
            .replace('&&GSRGSR&&', '":"')\
            .replace('%%GSRGSR%%', '":')\
            .replace('$$GSRGSR$$', '","')\
            .replace("~~GSRGSR~~", ',"')\
            .replace('@@GSRGSR@@', '{"')\
            .replace('**GSRGSR**', '"}')
        # print(data)
        return data

```

注意，这里面是我平时跑程序时会经常遇到的一些特殊字符的总结（血淋淋的教训换来的），你以后可能会遇到其他的特殊字符，往这里面添加规则就行。

再接下来，我们就要进入解析数据的环节了，解析比较简单，直接转换成 json 就行：

```python

def parse_data(self, data):
        result_obj = json.loads(data)

        obj = {}
        obj['pagecount'] = result_obj['pagecount']
        obj['time'] = result_obj['time']
        obj['total'] = result_obj['total']
        list_str = result_obj['list']
        stock_list = []
        if list_str:
            data_list = list(list_str)
            for s in data_list:
                # print(s)
                stock = {}
                stock['query_code'] = s['CODE']
                stock['code'] = s['SYMBOL']
                stock['name'] = s['SNAME']
                if 'PRICE' in s.keys():
                    stock['close_price'] = self.trans_float(s['PRICE'])
                else:
                    stock['close_price'] = 0.00
                if 'HIGH' in s.keys():
                    stock['top_price'] = self.trans_float(s['HIGH'])
                else:
                    stock['top_price'] = 0.00
                if 'LOW' in s.keys():
                    stock['low_price'] = self.trans_float(s['LOW'])
                else:
                    stock['low_price'] = 0.00
                if 'OPEN' in s.keys():
                    stock['open_price'] = self.trans_float(s['OPEN'])
                else:
                    stock['open_price'] = 0.00
                if 'YESTCLOSE' in s.keys():
                    stock['last_price'] = self.trans_float(s['YESTCLOSE'])
                else:
                    stock['last_price'] = 0.00
                if 'UPDOWN' in s.keys():
                    stock['add_point'] = self.trans_float(s['UPDOWN'])
                else:
                    stock['add_point'] = 0.00
                if 'PERCENT' in s.keys():
                    stock['add_percent'] = self.trans_float(s['PERCENT'])
                else:
                    stock['add_percent'] = 0.00
                if 'HS' in s.keys():
                    stock['exchange_rate'] = self.trans_float(s['HS'])
                else:
                    stock['exchange_rate'] = 0.00
                if 'VOLUME' in s.keys():
                    stock['volumn'] = self.trans_float(s['VOLUME'])
                else:
                    stock['volumn'] = 0.00
                if 'TURNOVER' in s.keys():
                    stock['turnover'] = self.trans_float(s['TURNOVER'])
                else:
                    stock['turnover'] = 0.00
                if 'TCAP' in s.keys():
                    stock['market_value'] = self.trans_float(s['TCAP'])
                else:
                    stock['market_value'] = 0.00
                if 'MCAP' in s.keys():
                    stock['flow_market_value'] = self.trans_float(s['MCAP'])
                else:
                    stock['flow_market_value'] = 0.00
                stock_list.append(stock)

        obj['stock'] = stock_list

        return obj

```

至于这里面每一项的含义，大家可以参照页面的列去一一对应。

解析完数据后，我们就要将数据持久化，我这里选择 mysql 存储数据，便于后续分析使用：

```python

def insert_db(self, obj_list, day):
        try:
            if len(obj_list):
                insert_attrs = ['day', 'query_code', 'code', 'name', 'close_price', 'top_price', 'low_price', 'open_price', 'last_price', 'add_point', 'add_percent', 'exchange_rate', 'volumn', 'turnover', 'market_value', 'flow_market_value']
                insert_tuple = []
                for obj in obj_list:
                    insert_tuple.append((day,
                                         obj['query_code'],
                                         obj['code'],
                                         obj['name'],
                                         obj['close_price'],
                                         obj['top_price'],
                                         obj['low_price'],
                                         obj['open_price'],
                                         obj['last_price'],
                                         obj['add_point'],
                                         obj['add_percent'],
                                         obj['exchange_rate'],
                                         obj['volumn'],
                                         obj['turnover'],
                                         obj['market_value'],
                                         obj['flow_market_value']))
                values_sql = ['%s' for v in insert_attrs]
                attrs_sql = '('+','.join(insert_attrs)+')'
                values_sql = ' values('+','.join(values_sql)+')'
                sql = 'insert into %s' % 'stock_info'
                sql = sql + attrs_sql + values_sql
                try:
                    print(sql)
                    for i in range(0, len(insert_tuple), 20000):
                        self.cur.executemany(sql, tuple(insert_tuple[i:i+20000]))
                        self.conn.commit()
                except pymysql.Error as e:
                    self.conn.rollback()
                    error = 'insertMany executemany failed! ERROR (%s): %s' % (e.args[0], e.args[1])
                    print(error)
        except Exception:
            #输出异常信息
            traceback.print_exc()

```

送佛送到西，顺便附上建表语句吧：

```

CREATE TABLE `stock_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `query_code` varchar(20) DEFAULT '',
  `code` varchar(10) DEFAULT NULL COMMENT '股票代码',
  `name` varchar(64) DEFAULT NULL COMMENT '名称',
  `close_price` double DEFAULT NULL COMMENT '收盘价',
  `top_price` double DEFAULT NULL COMMENT '最高价',
  `low_price` double DEFAULT NULL COMMENT '最低价',
  `open_price` double DEFAULT NULL COMMENT '开盘价',
  `last_price` double DEFAULT NULL COMMENT '前收盘价',
  `add_point` double DEFAULT NULL COMMENT '涨跌额',
  `add_percent` double DEFAULT NULL COMMENT '涨跌幅',
  `exchange_rate` double DEFAULT NULL COMMENT '换手率',
  `volumn` double DEFAULT NULL COMMENT '成交量',
  `turnover` double DEFAULT NULL COMMENT '成交金额',
  `amplitude` double DEFAULT NULL COMMENT '振幅',
  `market_value` double DEFAULT NULL COMMENT '总市值',
  `flow_market_value` double DEFAULT NULL COMMENT '流通市值',
  `flag` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `day` (`day`,`query_code`),
  KEY `code_name` (`code`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3953 DEFAULT CHARSET=utf8;

```

运行程序，你就能在数据库中看到行情数据了。如果不想每天手动运行的话，可以写个定时，每天在收盘后自动运行，当然丢服务器上更好了。这样每天获取当天最新的行情数据，日积月累，你就可以获取到从今以后的股票行情数据了。


### 总结

本文以网易财经为例，手把手分享怎样获取股票行情数据，希望对大家有帮助。但是大家记住一点，获取数据只是自己分析研究使用，千万不要违反我们的职业道德哦。

看到这里，大家可能会想：这只是获取一天的行情数据，并没有历史数据，如果我今天要使用历史数据分析，那不是扑街啦？

这个想法是对的，大家不要着急，本文的数据只是后续步骤的前提，先给我点个`在看`，我会继续分享如何获取所有股票的历史行情数据。



> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/stockinfo)
