---
layout: post
title: 用 Python 下载好快的 coser 小姐姐
category: python
tagline: by 某某白米饭
tags: 
  - python
  - coser
---

![封面](https://files.mdnice.com/user/15960/a5660322-d46c-4baa-851b-1a69ae054f6f.png)

米哈游不仅有原神，还有 coser 小姐姐和 coser 女装大佬，上班的时候用 python 爬虫偷偷下载，加班的时候摸摸鱼，谨防猝死。
<!--more-->

### 防爬虫

打开米哈游的 coser 界面 `https://bbs.mihoyo.com/dby/topicDetail/547`，并且在打开 F12 控制面板的时候，刷新页面。意外的是居然有 js 的防爬虫机制，表现为如下图：

![](https://files.mdnice.com/user/15960/0dfcc72a-64c4-4d0e-a47c-f7ad810cc128.png)

js 代码是

```js
(function anonymous(
) {
debugger
})
```

点击下面的倒数第二个按钮，破解掉它。

![](https://files.mdnice.com/user/15960/55467a3c-067d-4e3b-ab8f-0e96970cb396.png)


### 列表页

想要快速找到返回页面内容的 url 地址，可以在网络面板中使用 Ctrl+F 查找，然后对呀返回值一条条查看是否是需要的那条，这里找到了一条 `getTopicPostList` 地址的 url。

![](https://files.mdnice.com/user/15960/961015fe-2886-4302-a1ae-7ea0f8d9ce01.png)


这个页面是没有翻页的，对比第二页的 `getTopicPostList` 请求地址，比第一个多了 `last_id` 参数，最终的参数为：

* game_id: 5，可能就是那个右边的大别墅的意思
* gids: 5，连大别墅在内一个是 5 个
* last_id: 18114983，最后一个的 id
* list_type: 0，未知
* page_size: 20，每页条数
* topic_id: 547，板块 id

```python
import requests
import time

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Origin": "https://bbs.mihoyo.com",
        "Referer": "https://bbs.mihoyo.com/",
        "Host": "bbs-api.mihoyo.com"
    }

def request_get(url, ret_type):
    res = requests.get(url=url, headers=headers, timeout=5)
    res.encoding = "utf-8"
    if ret_type == "text":
        return res.text
    elif ret_type == "image":
        return res.content
    elif ret_type == "json":
        return res.json()

def main(last_id):
    url = f"https://bbs-api.mihoyo.com/post/wapi/getForumPostList??game_id=5&gids=5&last_id={last_id}&list_type=0&page_size=20&topic_id=547"
    res_json = request_get(url, "json")
    if res_json["retcode"] == 0:
        for item in res_json["data"]["list"]:
            detail(item["post"]["post_id"])
```

### 详细页

详细的 url 地址也是返回的 json 串，而且只需要传递 `post_id` 参数就好了，比较简单。图片的 url 地址就在 ["data"]["post"]["image_list"] 下，在返回的图片中有违规的图片，需要提前处理下。

```python
def detail(post_id):
    url = f"https://bbs-api.mihoyo.com/post/wapi/getPostFull?gids=5&post_id={post_id}&read=1"
    res_json = request_get(url, "json")
    if res_json["retcode"] == 0:
        image_list = res_json["data"]["post"]["image_list"]
        for img in image_list:
            img_url = img["url"]
            if (img_url.find("weigui")) < 0:
                save_image(img_url)
```

### 保存图片

保存图片就是普通的 `with open` 函数和文件的 `write` 函数。

```python
def save_image(image_src):
    r = requests.get(image_src)
    content = r.content
    name = image_src.split('/')[-1]
    with open('D://mhy//' + name, "wb") as f:
        f.write(content)
```

![](https://files.mdnice.com/user/15960/ee4ebeff-2b5c-4c0b-84b3-cb9a23dc0909.png)


### 总结

这篇文章的技术就使用了 requests 和 json 以及一点点的控制面板反爬虫。小伙伴们学会了吗？
