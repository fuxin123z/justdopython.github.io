---
layout: post
category: python
title: 用 Python 帮小伙伴找到头上一片绿的证据！
tagline: by 某某白米饭
tags:
  - Python技巧
  - 编程
---

这周末有个小伙伴找到派森酱，说他女票这几天整天都在上网，也不知道浏览什么内容，只要这个小伙伴凑上去瞧瞧就只看见了桌面，查看浏览器历史记录也被删除的一干二净。小伙伴有时候觉得自己头上已经是一片绿，想让派森酱弄个 python 程序找点实锤线索。
<!--more-->
![](http://www.justdopython.com/assets/images/2021/08/history/0.png)

小编就花了一点时间写了一个读取浏览器历史的小脚本，并教他如何隐藏小脚本并且使用 windows 自带的任务调度 3 分钟一次自动运行。



### browserhistory

browserhistory 是一个可以很方便的获取浏览器历史记录的第三方模块，支持 safari、chrome、firefox 浏览器。

```python
pip install browserhistory
```

### 使用

先来看看 Chrome 浏览器的历史记录存防止磁盘的哪个地方， 在浏览器地址栏输入 `chrome://version`，如下图可以找到 Chrome 将个人资料存放的地址。

![](http://www.justdopython.com/assets/images/2021/08/history/1.png)

其中 history 文件就是历史记录，它是一个 sqlite 数据库文件，可以使用 DB Browser for SQLite (https://sqlitebrowser.org/dl/) 工具打开并查询数据。

![](http://www.justdopython.com/assets/images/2021/08/history/2.png)

下面三行代码调用 browserhistory 模块获取历史，并保存在了 CSV 文件中。

```python
import browserhistory as bh

dict_obj = bh.get_browserhistory()
bh.write_browserhistory_csv()
```

![](http://www.justdopython.com/assets/images/2021/08/history/3.png)

### 统计

用 Excel 看浏览的网站数据并不是很直观，可以使用 pycharts 模块生成饼图查看点击次数最高的前十次网站。

```python
import csv
from urllib import parse
from pyecharts import options as opts
from pyecharts.charts import Pie

hostname_dic = {}
with open("chrome_history.csv", encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile)
    birth_header = next(csv_reader)
    for row in csv_reader:
        hostname = parse.urlparse(row[0]).hostname
        hostname_dic[hostname] = hostname_dic.get(hostname, 0) + 1
sorted(hostname_dic.items(),key = lambda x:x[1],reverse = True)


c = (
    Pie()
    .add(
        "",
        [
            list(z)
            for z in zip(
                list(hostname_dic)[0:10],
                list(hostname_dic.values())[0:10],
            )
        ],
        center=["40%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="历史记录"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("pie_scroll_legend.html")
)
        
print(hostname_dic)
```

![这个是小编的历史记录](![](http://www.justdopython.com/assets/images/2021/08/history/4.png)

最后的最后这个小伙伴的女票一时忘记删除历史记录，让这个小脚本跑成功了，小伙伴也发现自己绿了。


### 总结

python 在 windows 上是可以干许多事情的，比如监控屏幕发送到 QQ、微信等等，所以小伙伴们千万别三心二意哦。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/history>
