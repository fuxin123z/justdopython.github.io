---
layout: post
title: 我半夜爬了严选的女性文胸数据，发现了惊天秘密
category: python
tagline: by 闲欢
tags: 
  - python
  - 爬虫
  - 数据分析
---

刚刚过去的七夕，相信大家看到最多的是朋友圈秀恩爱（晒花），路上随处可见的也是某某女性手捧鲜花，各种大小花店一抢而空，只剩下满店狼藉。鲜花固然代表着美丽，代表着各种美好的含义，但是也不能教师节送花，母亲节送花，情人节也送花呀！作为情侣以及准情侣之间的礼物，能不能花点心思，送点不一样的，比如内衣……

有的男性朋友会跳出来骂了：说得好听，你知道送花多难吗？这种隐秘的数据，又不好直接开口问，又不能直接丈量，万一送错了不得把美好的事情搞砸了？

钢铁直男的想法总是这么赤果果，其实想知道妹子喜欢什么颜色的内衣，尺码是怎样的，不一定需要直接询问，可以有各种方法可以获取到，这里就不展开这个话题了。

为了探究妹子们的平常对内衣的普遍选择，我连夜爬取了网易严选关键词为“文胸”的商品评论数据，从中挑选了几个代表性的属性来做分析。

<!--more-->

### 爬取数据

巧妇难为无米之炊，为了分析数据，我们首先要获取数据，在本次行动中，我们需要获取的是文胸的评论数据，我们从结果出发，一步步来细化我们的需求和步骤。

首先，我们在网易严选的搜索框输入关键词“文胸”，出来文胸的产品列表界面：

![搜索结果](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/1.jpg)

我们随便点开一个商品，点击“评论”，就可以看到如下信息：

![评论信息](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/2.jpg)

我们分析请求列表，就可以很容易地发现评论数据是他通过 https://you.163.com/xhr/comment/listByItemByTag.json 这个请求来获取的。然后我们逐个地排除请求的参数，最终发现 itemId 和 page 两个参数是必须的，其他的参数都可以不传。

itemId 是指产品的ID，page 不用说了，就是指的请求的页码。所以我们要获取评论数据的前提是获取到对应的产品ID。

在详情页的请求中是可以获取到产品ID的，但是我们想获取搜索结果的产品ID列表就必须去搜索结果页寻找。

![产品列表](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/3.jpg)

同样的，我们在搜索界面的请求分析中，找到了 http://you.163.com/xhr/search/search.json 这个请求，逐个分析请求参数后发现，我们只需要 keyword 和 page 两个参数即可。

有了这个分析的前提，我们就可以着手写代码来获取数据了。代码如下：

```python

# 获取产品列表
def search_keyword(keyword):
    uri = 'https://you.163.com/xhr/search/search.json'
    query = {
        "keyword": keyword,
        "page": 1
    }
    try:
        res = requests.get(uri, params=query).json()
        result = res['data']['directly']['searcherResult']['result']
        product_id = []
        for r in result:
            product_id.append(r['id'])
        return product_id
    except:
        raise

# 获取评论
def details(product_id):
    url = 'https://you.163.com/xhr/comment/listByItemByTag.json'
    try:
        C_list = []
        for i in range(1, 100):
            query = {
                "itemId": product_id,
                "page": i,
            }
            res = requests.get(url, params=query).json()
            if not res['data']['commentList']:
                break
            print("爬取第 %s 页评论" % i)
            commentList = res['data']['commentList']
            C_list.extend(commentList)
            time.sleep(1)

        return C_list
    except:
        raise


product_id = search_keyword('文胸')
r_list = []
for p in product_id:
    r_list.extend(details(p))

with open('./comments.txt', 'w') as f:
    for r in r_list:
        try:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        except:
            print('出错啦')
```

这里我只抓取了第一页的产品来分析每个产品的前100页的评论数据。我将获取到的评论数据放在文件中存储。预览如下：

![存储数据](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/4.jpg)


### 分析数据

抓取完数据后，我们就可以进入探索环节了，我想从颜色、尺码、评论三个角度去看看有没有什么惊奇地发现。

我们来看看数据结构的特点：

```
{
  "skuInfo": [
    "颜色:灰紫色套头套装",
    "尺码:L（80BC-85AB）"
  ],
  "frontUserName": "葡****字",
  "frontUserAvatar": "http://yanxuan.nosdn.127.net/2a4479567d935ca3a88d7ea0e425ebc8",
  "content": "好穿！很舒服",
  "createTime": 1593738737271,
  "picList": [],
  "commentReplyVO": null,
  "memberLevel": 4,
  "appendCommentVO": null,
  "star": 5,
  "itemId": 3989517
}
```

这是一条评论数据，我们可以看到颜色和尺码都放在 skuInfo 里面，评论是放在 content 字段里面。同时，我们多翻一些数据就可以发现，这个颜色和尺码并不是统一的，不同的产品可能有不同的格式。

经过总结，对于颜色，我可以根据特点去除噪音，获取到统一的格式。而对于尺码，我只能将其分为两类：一类是以S、M、L、XL、XXL这种标识的比较通用的尺码，另一类是类似于75B这种比较准确的尺码。

我将颜色和尺码都做成柱状图来展示，而评论就用词云来展示。最终的效果图如下：

![颜色分布](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/5.jpg)

![尺寸分布](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/6.jpg)

![尺寸分布](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/7.jpg)

![评论词云](http://www.justdopython.com/assets/images/2020/08/yanxuanbra/8.jpg)

这个颜色有点出乎我的意料，我预想的最受欢迎的颜色应该是黑色，结果浅肤色排在了第一，黑色排在了第二，不过相差不大。如果数据量再多一些的话，可能黑色会反超，成为第一。

而对于尺寸来说，我们看到精确的尺寸分布图，前三都是B，紧接着是A和C，这个意味着什么大家自己去判断，这里我就不展开了。而通用的尺码里面，M码是最多的，L码比M码稍少，但是相差不明显。

而对于评论的词云，毫无意外地显示，舒服是第一位的，质量也比较重要。


### 总结

网易严选面向的群体应该是35岁以下的新时代后浪们，而且主打的是物美价廉和性价比。所以这些数据也是这个群体的购买喜好的提现。至于分析的结果，那就是仁者见仁智者见智了，哈哈！


示例代码 (https://github.com/JustDoPython/python-examples/tree/master/xianhuan/yanxuanbra)
