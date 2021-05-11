---
layout: post
category: python
title: 将什么值得买优惠信息部署到腾讯云函数并推送到QQ
tagline: by 某某白米饭
tags: 
  - python100
---

什么值得买是一家分享电商优惠信息的网站，它的每个优惠信息都带有这个优惠商品是否值得的数值和的评论，这对消费者来说增加了一些信任度。小编也经常找一些生活用品，但经常也会错过大额的优惠内容。今天我们就把优惠信息推送到QQ。
<!--more-->
服务器选择腾讯云函数，可以定时的运行脚本任务，免费，是爬虫脚本的好助手。

推送到 QQ 选择 qmsg 酱，因为它的操作很简单，登录后1分钟就会学会，使用 http 的方式推送内容到 QQ。

### 抓取网站

在网站的爆料人界面开始抓取与解析，把爆料人 ID 作为参数改变抓取页面的内容。

![](http://www.justdopython.com/assets/images/2021/04/smzdm/1.png)

这个网页比较简单，只要找到 class 为 pandect-content-stuff 的 div 下的 A 标签超链接和 class 为 pandect-content-time 的 span 的内容。

![](http://www.justdopython.com/assets/images/2021/04/smzdm/2.png)

```python
import requests
from bs4 import BeautifulSoup
import time

userAgent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        }

def parse_html(event, context):
    now = time.time()
    authorIds = ['1222805984']
    for author in authorIds:
        url = 'https://zhiyou.smzdm.com/member/' + author + '/baoliao/'


        html_content = requests.get(url, headers = userAgent).content

        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        infos = soup.find_all(name='div',attrs={'class': 'pandect-content-stuff'})


        for info in infos:
            a = info.find(name='div', attrs={'class': 'pandect-content-title'}).a
            t = info.find(name='span', attrs={'class': 'pandect-content-time'}).text

            # 只推送 5分钟之内的爆料
            content_time = time.mktime(time.strptime('2021-' + t + ':00', "%Y-%m-%d %H:%M:%S"))
            if((now - content_time) < 5 * 60):
                content = a.text.strip() + '\r\n' + a['href']
                push_qmsg(content)


def push_qmsg(msg):
    key = 'xxx'
    url = 'https://qmsg.zendee.cn/send/' + key
    msg = {'msg':  msg}
    requests.post(url, params=msg)
```

### 使用腾讯云函数

#### 准备云函数目录

将第三方 BeautifulSoup 模块的 bs 文件夹和脚本文件放在同一个目录，

```python
# 将 BeautifulSoup4 添加到 smzdm 文件夹下，将 bs 文件夹复制到和 py 脚本是同一级目录
pip install BeautifulSoup4 -t smzdm/
```

![](http://www.justdopython.com/assets/images/2021/04/smzdm/3.png)

#### 使用

在 `https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default` 页面选择自定义创建，并将 函数代码和触发器配置面板写出下图的样子。

![](http://www.justdopython.com/assets/images/2021/04/smzdm/4.png)


点击完成按钮后打开函数代码界面，并测试部署的是否正确。测试成功表示部署已经成功，可以 5 分钟抓取一次优惠信息了。

![](http://www.justdopython.com/assets/images/2021/04/smzdm/5.png)

### 总结

用什么值得买的爬虫帮助大家免费的使用腾讯云函数，省下了花费在爬虫服务器金钱和心力。如果这篇文章对小伙伴有用，请多多点个赞和再看。


> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/smzdm/smzdm.py>
