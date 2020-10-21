---
layout: post     
title:  用 Python 制作商品历史价格查询   
category: 用 Python 制作商品历史价格查询
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---
一年一度的双十一就快到了，各种砍价、盖楼、挖现金的口令将在未来一个月内充斥朋友圈、微信群中。玩过多次双十一活动的小编表示一顿操作猛如虎，一看结果2毛5。浪费时间不说而且未必得到真正的优惠，双十一电商的“明降暗升”已经是默认的潜规则了。打破这种规则很简单，可以用 Python 写一个定时监控商品价格的小工具。

<!--more-->
![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_0.png)

### 思路

1. 第一步抓取商品的价格存入 Python 自带的 SQLite 数据库
2. 每天定时抓取商品价格
3. 使用 pyecharts 模块绘制价格折线图，让低价一目了然

### 抓取京东价格

从商品详情的页面中打开 F12 控制面板，找到包含 p.3 的链接，在旁边的 preview 面板中可以看到当前商品价格

![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_1.png)

```python
def get_jd_price(skuId):

    sku_detail_url = 'http://item.jd.com/{}.html'
    sku_price_url = 'https://p.3.cn/prices/get?type=1&skuid=J_{}'

    r = requests.get(sku_detail_url.format(skuId)).content

    soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
    sku_name_div = soup.find('div', class_="sku-name")

    if not sku_name_div:
        print('您输入的商品ID有误！')
        return
    else:
        sku_name = sku_name_div.text.strip()

    r = requests.get(sku_price_url.format(skuId))
    price = json.loads(r.text)[0]['p']

    data = {
        'sku_id': skuId,
        'sku_name': sku_name,
        'price': price
    }
    return data
```

把抓取的价格存入 sqlite 数据库，使用 PyCharm 的 Database 功能创建一个 sqlite 数据库

![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_2.png)

![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_3.png)

最终将数据插入到数据库

```python
# 新增
def insert(data):
    conn = sqlite3.connect('price.db')
    c = conn.cursor()
    sql = 'INSERT INTO price (sku_id,sku_name,price) VALUES ("{}", "{}", "{}")'.format(data.get("sku_id"), data.get("sku_name"), data.get('price') )
    c.execute(sql)
    conn.commit()
    conn.close()

# 查询
def select(sku_id):
    conn = sqlite3.connect('price.db')
    c = conn.cursor()
    sql = 'select sku_id, sku_name, price, time from price where sku_id = "{}" order by time asc'.format(sku_id)
    cursor = c.execute(sql)

    datas = []
    for row in cursor:
        data = {
            'sku_id': row[0],
            'sku_name': row[1],
            'price': row[2],
            'time': row[3]
        }
        datas.append(data)
    conn.close()

    return datas
```

示例结果

![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_4.png)

### 计划任务

使用轻量级的 schedule 模块每天早上 10 点抓取京东价格这一步骤

安装 schedule 模块

```python
pip install schedule
```

```python
def run_price_job(skuId):

    # 使用不占主线程的方式启动 计划任务
    def run_continuously(interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
    
    # 每天10点运行，get_jd_price：任务方法，skuId：任务方法的参数
    schedule.every().day.at("10:00").do(get_jd_price, skuId=skuId)
    run_continuously()
```

### 查看历史价格

使用 pytharts 模块绘制折线图，直观的查看每一天的价格差异

```python

datas = select(skuId)

def line(datas):
    x_data = []
    y_data = []
    for data in datas:
        x_data.append(data.get('time'))
        y_data.append(data.get('price'))

    (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(datas[0].get('sku_name'), y_data, is_connect_nones=True)
        .render("商品历史价格.html")
    )

```

![](http://www.justdopython.com/assets/images/2020/10/jd_price/j_5.png)

### 总结

本文抓取了京东商城的价格，小伙伴们也可以修个脚本抓取淘宝的价格。使用 Python 解决生活中的小小痛点，让钱包不再干瘪。

> 示例代码：[用 Python 制作商品历史价格查询](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/jd_price)