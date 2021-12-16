---
layout: post
category: python
title: 用 python 助力斗图，做本群最靓的仔
tagline: by 某某白米饭
tags:
  - 爬虫
---

![封面](https://files.mdnice.com/user/15960/b3638a6d-e90f-4d35-840b-f1825c3c968a.png)

在平常的群聊中有时候就会碰到那种杠精，一言不合就开始阴阳怪气的说话然后发各种表情包，然而你的微信表情总是就那么一点点，还不够个性化，去网上百度么又太麻烦了。这篇文章就根据关键字在表情啦网站下载表情到本地，让杠精远离你。

本文用 python 爬虫抓取“发表情”网站（https://fabiaoqing.com/）的表情包。

<!--more-->

### 分析思路

打开网站，搜索【装逼】关键字的表情包，并且打开 F12 控制面板，可以看到每个表情包都被包含在 div 元素里面，并且在翻页的时候可以从 url 地址上可以看出第一页的最后数字是 1，第二页是 2，第三页是 3。这就好办了，只要改变数字就可以了。

![](https://files.mdnice.com/user/15960/af38ede0-db5b-4e6c-97cd-0ef349bbe6da.png)

下面开始码代码，首先定义一个 header 请求头，然后就用 request.get() 抓取页面，并且在输出页面 html 的时候使用 utf-8 的编码格式。

```python
import os
import requests,re


def get_html(search_key, page):
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Host': 'www.fabiaoqing.com'
        }

    key_url = 'https://fabiaoqing.com/search/bqb/keyword/{}/type/bq/page/{}.html'.format(search_key, page)

    resp = requests.get(key_url, headers=header)
    resp.encoding='utf-8'
    return resp.text
```

继续查看网页源码，表情图片就藏在 div 层下的 img 表情中，用正则表达式解析提取 img 的 src 属性。当没有提取到表情包的 src 时，表示这页已经是最后一页了。

![](https://files.mdnice.com/user/15960/7a92fcc4-1149-4c38-bfc2-b88904fe0652.png)

```python
def get_src(html):
    srcs = re.findall('<img class="ui image bqppsearch lazy" data-original="(.*?)" title="(.*?)"',html,re.S)
    return srcs
```

最后用 urlretrieve 下载表情包。

```python
def downlaod(srcs, path):
    
    from urllib.request import urlretrieve
    for item in srcs:
        print(item[2])
        urlretrieve(item[0], path + '\\' + item[2].replace('\n', '') + '.png')

```

![](https://files.mdnice.com/user/15960/b3638a6d-e90f-4d35-840b-f1825c3c968a.png)

### 总结

用简单的 python 爬虫，抓取了源源不断的表情包来斗图，小伙伴们也可以把 python 用在其他的日常中。
