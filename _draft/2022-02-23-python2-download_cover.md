---
layout: post
title: 偷偷摸鱼，撸一个下载 B 站小姐姐封面偷偷看
category: python
tagline: by 某某白米饭
tags: 
  - python
  - B 站
---

这几天字节跳动又又又人猝死了，所以身为打工人，该摸鱼的时候还得摸鱼。小编在摸鱼期间写了一个下载 B 站封面的小脚本，封面一般是一个视频的灵魂所在，所以摸鱼看小姐姐。不过现在的 B 站好像没有以前那样大尺度了。
<!--more-->

![](https://files.mdnice.com/user/15960/775f4511-9ab9-47dc-a10e-0d50771ce9cc.png)


### 摸鱼开始

所用到的模块有 requests，pathlib，shutil，json。这几个模块都是老熟人了，不过多的介绍了。

打开 up 主的 B 站空间 `https://space.bilibili.com/320491072`，并且把 F12 控制面板打开。在网络面板就可以用搜索快速找到请求视频的 url 地址（`https://api.bilibili.com/x/space/arc/search`），它的返回值里面包含了分页的信息：page['count'] 总条数，page['ps'] 每页条数。

![](https://files.mdnice.com/user/15960/dadee4df-a9e2-4d06-8272-f0aa4addc021.png)

```python
import requests
import pathlib
import shutil
import json

base_url = 'https://api.bilibili.com/x/space/arc/search?mid=632887&ps=30&tid=0&pn={0}&keyword=&order=pubdate&jsonp=jsonp'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

def get_total_page():
    response = requests.get(base_url.format(1), headers=headers)
    j = response.content
    data = json.loads(j)
    page = data['data']['page']
    return int(page['count'] / page['ps']) + 1
```

先请求一次得到总页数。

pic 的地址具体包含在 `vlist` 下面。

![](https://files.mdnice.com/user/15960/8a02b700-a4e2-4a27-ae2d-9b52400ea6b8.png)

```python
def get_image_urls():
    total_page = get_total_page()+1
    
    for i in range(1, total_page):
        url = base_url.format(i)
        response = requests.get(url, headers=headers)
        j = response.content
        data = json.loads(j)
        for i in data['data']['list']['vlist']:
            yield {'name': i['title'], 'url': i["pic"]}
```

最后就是处理文件名中的特殊符号，我们用字符串的 replace 方法处理。

```python
def remove_unvalid_chars(s):
    for c in r'''"'<>/\|:*?''':
        s = s.replace(c, '')
    return s
```

最后一个方法将所有的函数都串联起来，并且创建文件夹和将图片写入文件。

```python
def download_images():
    save_folder = r'~/Desktop/images'
    folder = pathlib.Path(save_folder).expanduser()
    if not folder.exists():
        folder.mkdir()
    for i in get_image_urls():
        response = requests.get(i['url'], stream=True)
        filename = remove_unvalid_chars(i["name"])+'.jpg'
        with open(folder/filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg下载完成')
```

![](https://files.mdnice.com/user/15960/80dfbe68-e8c5-420a-98b0-bb7104458bc4.png)


### 总结

工作么，能摸鱼就摸鱼。大把年华，别加班，谨防猝死。
