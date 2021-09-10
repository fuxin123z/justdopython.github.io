---
layout: post
category: python
title: 中秋不发女朋友，发追女神的方法
tagline: by 某某白米饭
tags:
  - Python技巧
---

大家都知道微博在国内的影响力是非常巨大，许多人都在使用微博。微信早就已经变成了一个工作工具，领导、同事、亲戚等等关系人都往里面加为好友。有一些牢骚、喃喃自语就不适合发在朋友圈。

利用情感分析 API 对女神微博内容进行心情分析。好心情就发出约会邀请，差心情就带她出去吃大餐。

<!--more-->
### 抓取微博

### 安装第三方库

（1）这里我们不自己造轮子，使用 github 上拥有 4.3K 星星的 微博爬虫 weibo-spider 模块。weibo-spider 可以爬去用户信息和微博信息，可以下载用户发图片和视频。

```python
python3 -m pip install weibo-spider
```

![](http://www.justdopython.com/assets/images/2021/09/weibo/0.png)

（2）baidu-aip 是百度情感倾向分析模块，可以判断文字是消极的还是积极的。

```python
python -m pip install baidu-aip
```

### 抓取内容

1. 指定一个文件夹如：D:\\weibo，在这个文件夹中运行下面的 cmd 命令。会在当前文件生成一个 config.json 的配置文件。

```python
python3 -m weibo_spider
```

![](http://www.justdopython.com/assets/images/2021/09/weibo/1.png)

修改 config.json 配置文件中的 `user_id_list`、 `since_date`、 以及 `cookie`

1. user_id_list 这里添加女神的微博 id，是微博链接 `https://m.weibo.cn/profile/3733371872` 中最后的数字。

![](http://www.justdopython.com/assets/images/2021/09/weibo/2.png)

2. since_date 可以配置日期，就是从那个日期开始抓取到现在，如果要抓取女神的所有微博内容，可以配置一个很久以前的日期，如果只需要抓前几天的数据，可以配置一个数字，表示抓取今天开始倒退天数的微博内容。

3. cookie 如下图，访问 `https://weibo.cn/`

![](http://www.justdopython.com/assets/images/2021/09/weibo/3.png)

配置好文件之后，再次在命令行运行 `python3 -m weibo_spider` 命令。

![](http://www.justdopython.com/assets/images/2021/09/weibo/4.png)

微博内容就在 本地 CSV 文件中了。

![](http://www.justdopython.com/assets/images/2021/09/weibo/5.png)

### 分析情感

登录百度之后将页面打到 `https://ai.baidu.com/tech/nlp_apply/sentiment_classify` ,创建一个应用就可以得到 appid, ak 和 sk 了。

![](http://www.justdopython.com/assets/images/2021/09/weibo/6.png)

解析情感分析注意点：
1. 微博内容有各种非法字符，需要屏蔽掉，只剩下标点符号和汉字。
```python
hanzi = re.compile('[\u4e00-\u9fa5 0-9?？。.,，]')
```
2. 情感分析 API 的接口最多只能分析 1024kb 的文本。
3. API 返回值是 json 对象：
```json
{
    "text":"文本",
    "items":[
        {
            "sentiment":2,    //表示情感极性分类结果
            "confidence":0.40, //表示分类的置信度
            "positive_prob":0.73, //表示心情好的概率
            "negative_prob":0.27  //表示心情差的概率
        }
    ]
}
```

解析代码走起来：

```python
from aip import AipNlp
import csv
import time
import re

APP_ID = 'APP_ID'
API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


file = open("D:\\weibo\\weibo\\宫崎骏漫画全集\\3733371872.csv", "r", encoding="utf-8", errors='ignore')
reader = csv.reader(file)
result = {'good':0,'bed':-1}
hanzi = re.compile('[\u4e00-\u9fa5 0-9?？。.,，]')
for item in reader:
    time.sleep(1)
    a = "".join(hanzi.findall(item[1]))
    if len(a.encode()) > 1024:
        continue
  
    sent = client.sentimentClassify(a)

    items = sent['items'][0]
    if items["positive_prob"] > items["negative_prob"]:
        result['good'] = result['good'] + 1
    else:
        result['bed'] = result['bed'] + 1
    
print('微博内容总共：{} 条，好心情：{}，差心情：{}'.format(result['good'] + result['bed'], result['good'], result['bed']))
if(result['good'] > result['bed']):
    print('最近女神心情好，建议发出约会要求')
else:
    print('最近女神心情非常差，建议吃大餐')
```

示例结果：

![](http://www.justdopython.com/assets/images/2021/09/weibo/7.png)

### 总结

将脚本作为定时任务运行，不放过女神任何的心情动态， 当女神心情差的时候，咱就买点礼物、带她去吃一顿等等操作，给她一个依靠。当女神心情好的时候，那就发起约会申请撒。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/weibo.py>
