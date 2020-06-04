---
layout: post
title: 打造网红地摊
category: python
tagline: by 闲欢
tags: 
  - python
---

最近，火遍全国的词语非“地摊”莫属了。总理在两会记者会上，强调了地摊经济对于恢复经济社会秩序，满足群众生活需要的过程中发挥的积极作用。这个意义在于不仅官方承认了地摊经济的合法性，而且官方是鼓励发展地摊经济的。作为后浪青年的我们，时代的弄潮儿，怎么也要参与一把是不是？
<!--more-->


## 如何开始

说干就干，既然我们要摆地摊，那么我们怎么开始呢？

万事开头难，好的开始就等于成功了一半。作为一个技术人员，对于每一件事情我都是非常认真的，要么不做，要么做最好。所以我要打造一个网红地摊，要做到这点，我不能跟一般人那样，找些小物品，随便找个摊位，然后一边刷抖音一边接客，我要把摆摊这件事上升到产品层面，打造一款爆品出来。

这样想来就简单了，做产品无非就是找到产品定位以及明确目标用户。下面我们分别从这两方面来具体分析。

![烟火风口](http://www.justdopython.com/assets/images/2020/06/hotsell/hotwind.jpeg)


## 目标产品

说到摆地摊，我们绕不过的坎是阿里巴巴的1688网站，淘宝和拼多多的好多商家批发的货源都是阿里巴巴，包括现在的大部分路边小摊都是从这个网站进货的。所以毫无疑问，我们的产品也是从这里面来。

那么我们怎么找到我们的目标产品呢？一个简单粗暴的方法是找到阿里巴巴上畅销的货品，毕竟这是全国大多数人的选择。

一般人可能就是找到热门的分类，然后在热门分类下按照销量排序。但，我不是一般人，作为程序员，我只相信我的程序。

所以我找到了阿里巴巴的“热销市场”，网址是：https://re.1688.com/ 。我们打开网址，映入眼帘的页面是这样的：

![主页](http://www.justdopython.com/assets/images/2020/06/hotsell/main.png)

接着我们点击搜索框，我们可以看到“大家都在搜”这个小模块，里面列出来最近比较热搜的商品，如下图所示：

![热搜](http://www.justdopython.com/assets/images/2020/06/hotsell/hotsearch.png)

我看到数据线是最热的，于是我搜索一下“数据线”，看到下面的搜索结果：

![搜索结果](http://www.justdopython.com/assets/images/2020/06/hotsell/searchresult.png)

好了，到这里一般人都做得到。剩下的怎么办？怎么找到销量最好的？怎么找到靠谱的店家？

该我的绝技登场了——爬虫。我要把这个页面的商品爬下来，并且获取关键数据，然后进行分析。

我们先找到目标请求，为了找到目标请求，我先点击了底下分页的第二页，看看会出现什么请求：

![请求分析](http://www.justdopython.com/assets/images/2020/06/hotsell/targetrequest.png)

我们可以看到第一个请求就是我们需要的请求，接着我们直接修改 `beginpage` 参数，就可以请求目标分页的数据。下面我们直接上代码：

```python
import requests
import time
import random
import openpyxl


# 分页获取商品
def get_premium_offer_list(keyword, page):
    offer_list = []
    for i in range(1, int(page) + 1):
        time.sleep(random.randint(0, 10))
        olist = get_page_offer(keyword, i)
        offer_list.extend(olist)
    return offer_list

# 获取一页商品
def get_page_offer(keyword, pageNo):
    url = "https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=%d&keywords=%s" % (pageNo, keyword)
    res = requests.get(url)
    result = res.json()
    offerResult = result['data']['content']['offerResult']
    result = []
    for offer in offerResult:
        obj = {}
        # print(offer['attr']['id'])
        obj['id'] = str(offer['attr']['id'])
        # print(offer['title'])
        obj['title'] = str(offer['title']).replace('<font color=red>', '').replace('</font>', '')
        # print(offer['attr']['company']['shopRepurchaseRate'])
        obj['shopRepurchaseRate'] = str(offer['attr']['company']['shopRepurchaseRate'])
        # print(offer['attr']['tradeQuantity']['number'])
        obj['tradeNum'] = int(offer['attr']['tradeQuantity']['number'])
        obj['url'] = str(offer['eurl'])
        result.append(obj)

    return result

# 写Excel
def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        id = value[i].get('id', '')
        title = value[i].get('title', '')
        shopRepurchaseRate = value[i].get('shopRepurchaseRate', '')
        tradeNum = value[i].get('tradeNum', '')
        url = value[i].get('url', '')
        cell = [id, title, shopRepurchaseRate, tradeNum, url]
        sheet.cell(row=1, column=1, value='ID')
        sheet.cell(row=1, column=2, value='标题')
        sheet.cell(row=1, column=3, value='回购率')
        sheet.cell(row=1, column=4, value='成交量')
        sheet.cell(row=1, column=5, value='链接')
        for j in range(0, len(cell)):
            sheet.cell(row=i+2, column=j+1, value=str(cell[j]))
    workbook.save(path)
    print("xlsx格式表格写入数据成功！")


def main(keyword, page):
    offer_list = get_premium_offer_list(keyword, page)
    print(offer_list)
    write_excel_xlsx('./data.xlsx', '数据', offer_list)

if __name__ == '__main__':
    main("数据线", 10)
```

在程序里面我设置了关键词和总爬取页数两个参数。最后我们输出的 Excel 文件看起来是这个样子的：

![Excel](http://www.justdopython.com/assets/images/2020/05/doutu/excel.jpg)

这里我找到了回购率和成交量两个指标来分析商家的靠谱程度以及商品的热销程度。当然你也可以从中找到其他你关心的指标。

拿到这个表格后，我们只需要对指标进行排序，就可以找到前排商品了，然后复制链接到浏览器就可以查看商品详情了。


## 目标用户

解决了目标产品，接下来我们就要找到目标用户，一般来说，地摊的目标客户大体应该是上下班的人流以及社区的闲逛人员。

针对这两类人群，我们要除了要找到他们的需求商品外，我们还需要他们在哪里。

针对上下班人群，我们的摆摊地点可以是地铁站出入口或者公交站旁边，或者是写字楼的出入口。哪个地铁站的出入口或者公交站人流量最大？哪个写字楼的上班白领最多？我想这两者应该是有联系的。一般热门写字楼旁边的地铁站肯定是上班族人流量最大的。

要找到上班族多的写字楼，就得靠各位去想办法获取数据了。这里有一个不成熟的想法就是去爬招聘网站的数据，然后获取到公司的办公地址，出现较多的写字楼地址应该就是有好多公司办公的。

针对社区闲逛人员，要找到人流量大的社区，可以直接去爬取房屋中介网站，找到小区的总户数这个数据，以及结合小区的新旧程度来综合判断。一般大型老社区的人流量应该是比较大的。


## 干吗

找到了目标人群，找到了热销产品，接下来的问题是：干吗？分析得头头是道，不干咋知道效果！我干了，你随意！记得到时候扶我回去啊！


## 总结

本文主要传授如何打造网红地摊（纸上谈兵的嘴炮选手），其实主要是想告诉大家，作为一个会 Python 的人，要将 Python 运用到我们的生活中的各个方面，让 Python 成为我们的得力助手，这样才是业余选手的正道（专业选手请绕道行驶）。

> 示例代码 (https://github.com/JustDoPython/python-examples/tree/master/xianhuan/hotsell)

