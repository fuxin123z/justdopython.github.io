---
layout: post
title: 价值十万代码之三-获取全部历史数据
category: python
tagline: by 闲欢
tags: 
  - python
  - 股票
  - 数据分析
---

上篇文章 [价值十万的代码之二---手把手教你获取数据篇](https://mp.weixin.qq.com/s/vlZkNb22GiNjUS2lUCkOdA) 中，小酱手把手教大家如何获取股票行情的实时数据，大家自己亲自动手实现了吗？首先感谢大家一贯的支持和鼓励，给我了持续分享的动力。本篇将接着上一篇的内容，为大家讲解一下如何获取所有个股的历史数据。

<!--more-->

### 选定目标

上篇我们是通过网易财经的行情页来获取股票的实时行情数据的，那么我们最好还是在网易财经获取历史数据，避免不同平台一些股票标识不一样，导致数据需要进行转换。

在网易财经上左翻右翻，左看右看，终于被我找到了我们的目标。我们首先进入股票实时行情页面（上一篇我们的目标页面）：

![股票行情页](http://www.justdopython.com/assets/images/2020/11/stockhisinfo/0.png)

点击某只股票名称，进入股票详情页面：

![股票详情页](http://www.justdopython.com/assets/images/2020/11/stockhisinfo/1.png)

我们可以看到这里面是按照季度来展现股票的历史交易数据的。细心的你肯定发现了旁边的“下载数据”的链接按钮，是不是突然有点兴奋了，仿佛点击这个按钮就可以获取到数据了，希望就在眼前。我们点击这个按钮看看：

![股票详情页](http://www.justdopython.com/assets/images/2020/11/stockhisinfo/2.png)

哇！我看到了起始日期和截止日期，选择开始日期和截止日期，就可以下载一只股票的所有历史交易数据，so easy~ 

![下载数据](http://www.justdopython.com/assets/images/2020/11/stockhisinfo/3.png)

我仿佛看到了各位脸上兴奋的笑容，只需要模拟这个下载操作，我就可以获取一只股票的数据了，所有的 A 股数据也只需要获取几千次而已。

没错，这个思路确实很正确，我之前也是这么操作的。不过好景不长，从今年的某个时间起，我的程序通过这种操作获取不到数据了，每次获取到的只有一行标题，当时我就有点迷茫了，这么好的一个渠道失去了，意味着我又需要重新寻找获取数据的方法。当然了，如果你不嫌麻烦并且时间充裕，可以一只只股票点击来，然后点击下载数据，也可以将所有数据下载到本地，只是机械操作比较多而已。

既然“下载数据”这个入口已经不适合程序操作了，那我们回到股票详情页面，这个页面是按照季度来查询历史交易数据的，那我们把这个页面的数据解析出来，不就获取了这只股票一个季度的数据了吗？然后写个循环，逐个季度获取，不就完事了吗？


### 分析目标页面

我们选择2020年三季度，然后点击“查询”按钮，查看“天迈科技”2020年三季度的历史交易数据：

![季度数据](http://www.justdopython.com/assets/images/2020/11/stockinfo/4.png)

我们可以看到第一个请求 URL，就很像是这个页面的请求，再看看返回预览是这个页面的数据，看来这个大概率是我们的目标请求了。

我们再接着看这个请求的返回，显示是一个 html 页面的代码，想要知道这个 HTML 页面中是否包含我们的目标数据（主要是为了区分这页面是及时返回数据，还是页面加载后通过 ajax 请求再来获取数据），我们只需要将这个页面代码复制到文本编辑器，然后用交易数据的表格中的一个数据项搜索页面代码，如果能搜索到，说明页面的数据都在这个页面代码中，如果获取不到，我们再去研究页面代码，找到加载数据的请求。通过搜索，我们发现可以搜到，说明是及时加载的，也给我们提供了方便，不用再去研究延时加载了。

既然这样，我们就可以直接通过解析这个 HTML 页面内容来解析出我们需要的股票数据了。


### 代码实现

通过上面的分析，我们知道，我们获取一只股票的历史交易数据，需要逐个季度的请求解析，然后拼凑在一起。所以，我们的第一步是获取目前 A 股所有的股票，还记得我们上篇文章的输出吗？全部的 A 股股票就在那里。我们当时是存入 MySQL 数据库的，现在可以获取出来为我所用了：

```python

def query_lcode(self, day):
        query_sql = "select code,name from stock_info where day='%s'" % day

        try:
            lcode = self.cur.execute_sql(query_sql)
            return lcode
        except Exception:
            #输出异常信息
            traceback.print_exc()

```

接着，我们以获取一只股票的一个季度的数据为例，来说说怎么解析这个页面获取数据。

第一步，我们获取页面 HTML 内容：

```python

def get_data(self, code, year, season):
        url = 'http://quotes.money.163.com/trade/lsjysj_%s.html?year=%s&season=%d' % (code, year, season)
        ua_header = {"Connection": "keep-alive",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
                     "Host": "quotes.money.163.com",
                     "Cookie": "vjuids=2453fea.1759e01b4ef.0.c69c7922974aa; _ntes_nnid=99f0981d725ac03af6da5eec0508354e,1604673713410; _ntes_nuid=99f0981d725ac03af6da5eec0508354e; _ntes_stock_recent_=1300033; _ntes_stock_recent_=1300033; _ntes_stock_recent_=1300033; ne_analysis_trace_id=1604846790608; s_n_f_l_n3=20f075946bacfe111604846790626; _antanalysis_s_id=1604933714338; vjlast=1604673713.1605015317.11; pgr_n_f_l_n3=20f075946bacfe1116050154486829637; vinfo_n_f_l_n3=20f075946bacfe11.1.0.1604846790623.0.1605015456187",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Accept-Encoding": "gzip, deflate",
                     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7",
                     "Cache-Control": "no-cache",
                     "Pragma": "no-cache",
                     "Referer": "http://quotes.money.163.com/trade/lsjysj_%s.html" % code,
                     "Upgrade-Insecure-Requests": "1",
                     }
        response = requests.get(url, headers=ua_header, verify=False)
        content = response.content.decode("utf-8")

        return content

```

第二步，我们来解析数据：

```python

def parse_data(self, code, name, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find("table", class_="table_bg001 border_box limit_sale").prettify()
        tb_soup = BeautifulSoup(table, 'html.parser')
        tr_list = tb_soup.find_all('tr')
        stock_list = []
        if len(tr_list):
            del tr_list[0]
            for tr in tr_list:
                items = tr.text.split('\n\n')
                if len(items):
                    del items[0]
                    stock = {}
                    stock['day'] = items[0].replace('\n ', '').replace(' ', '')
                    stock['code'] = code
                    stock['name'] = name
                    stock['open_price'] = self.trans_float(items[1].replace('\n ', '').replace(' ', ''))
                    stock['top_price'] = self.trans_float(items[2].replace('\n ', '').replace(' ', ''))
                    stock['low_price'] = self.trans_float(items[3].replace('\n ', '').replace(' ', ''))
                    stock['close_price'] = self.trans_float(items[4].replace('\n ', '').replace(' ', ''))
                    # stock['last_price'] = self.trans_float(items[7])
                    stock['add_point'] = self.trans_float(items[5].replace('\n ', '').replace(' ', ''))
                    stock['add_percent'] = self.trans_float(items[6].replace('\n ', '').replace(' ', ''))
                    stock['volumn'] = self.trans_float(items[7].replace('\n ', '').replace(' ', '').replace(',', ''))
                    stock['turnover'] = self.trans_float(items[8].replace('\n ', '').replace(' ', '').replace(',', ''))
                    stock['amplitude'] = self.trans_float(items[9].replace('\n ', '').replace(' ', ''))
                    stock['exchange_rate'] = self.trans_float(items[10].replace('\n \n', '').replace(' ', ''))
                    # stock['market_value'] = self.trans_float(items[13])
                    # stock['flow_market_value'] = self.trans_float(items[14])

                    stock_list.append(stock)

        return stock_list

```

这里我先用 bs4 来解析 HTML 页面，定位到数据表格，然后再解析表格的内容就可以获取每一个日期的数据项了。但是这里相对于我们上一篇的实时行情数据，会少几项，例如前一个交易日的收盘价，市场成交额等，不过这几项数据是可以通过所有的历史数据计算出来的，所以即使以后要用我们也有办法。

解析完数据之后，我们就可以存储到数据库了：

```python

def insertdb(self, data_list):
        attrs = ['day', 'code', 'name', 'open_price', 'top_price', 'low_price', 'close_price', 'add_point',
                 'add_percent', 'volumn', 'turnover', 'amplitude', 'exchange_rate']
        insert_tuple = []
        for obj in data_list:
            insert_tuple.append((obj['day'], obj['code'], obj['name'], obj['open_price'], obj['top_price'], obj['low_price'], obj['close_price'], obj['add_point'], obj['add_percent'], obj['volumn'], obj['turnover'], obj['amplitude'], obj['exchange_rate']))
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
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

```

这个没什么好说的，就是一个数据库批量插入操作而已。

到这里，我们就把一只股票的一个季度的数据获取到了。那么如何获取所有股票的历史数据呢？相信聪明的你已经有了答案了。一种办法是获取股票的详细信息，然后解析出上市日期，然后从上市日期所在年度季度开始，逐个季度获取数据。另一种办法是从 A 股开市时间开始，沪市的开市日期是1990-12-20，深市的开市日期是1991-01-03，创业板的开市日期是2009-10-30，科创板的开市日期是2019-07-22。四个板块的股票分别从这几个日期开始获取，不管这只股票是什么时候上市的，都可以获取全这只股票的历史数据。


### 总结

本文教大家如何从网易财经的个股历史交易数据页面获取到全市场个股的历史交易数据，大家可以根据文中的方法自己去实践一下。

到此为止，获取股票的数据这个环节我就介绍完了，接下来就是如何利用手中的数据去分析出有价值的东西。如果大家感兴趣，还望先给我点个`在看`，我会继续履行前面许下的承诺，结合研报数据和股票数据去分析，从而辅助股票交易的决策分析。



> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/stockhisinfo)
