---
layout: post
title: 用协程的方式下载英雄联盟的高清皮肤
category: python
tagline: by 某某白米饭
tags: 
  - python
  - 英雄联盟
---


![封面](https://files.mdnice.com/user/15960/b312ae28-e016-4de7-9ed0-d2d008ec9e53.jpeg)
小伙伴们大多数都有玩过英雄联盟吧？大多都喜欢各个英雄的各种皮肤，今天和小编一起将所有英雄的皮肤下载下来，当做桌面、手机壁纸吧。

<!--more-->

### 分析

打开 LOL 的英雄资料页：（https://lol.qq .com/data/info-heros.shtml），并且打开 F12 控制面板的网络界面。可以看到有一个 hero_list.js，里面就可以获取到各个英雄的 Id。

![](https://files.mdnice.com/user/15960/ae0b8803-4567-411a-a521-84feb945b924.png)

然后进入英雄界面，在网络面板中就有一个以英雄 Id 所关联的 js。

![](https://files.mdnice.com/user/15960/83312141-5682-4fa9-a366-0c6ad24e9048.png)

可以得到英雄的各个资料，heroName、heroTitle、name 以及 mainImg。

### 代码

下面是用到的各个模块。

```python
from gevent import monkey; monkey.patch_all()
import requests
import gevent
import os
import re
```

代码比较简单，就是用 requests 的 get() 方法读取页面和下载图片，这里使用了 gevent 协程非阻塞式下载图片。将 gevent 协程设置为非阻塞的需要给它打个补丁，这里选用的是 monkey 第三方模块。一个协程设置了 10 个英雄下载页面。


```python
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

root_path = 'D:\LOL'

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)   

def crawling():
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    resp = requests.get(url=url, headers=header)
    heros = resp.json()['hero']
    index = 0
    task_list = []
    for hero in heros:
        index = index + 1

        heroId = hero['heroId']
        hero_url = f'https://game.gtimg.cn/images/lol/act/img/js/hero/{heroId}.js'
        hero_resp = requests.get(url=hero_url, headers=header)
        skins = hero_resp.json()['skins']

        task = gevent.spawn(get_pic, skins)
        task_list.append(task)
        if len(task_list) == 10 or len(skins) == index:
            gevent.joinall(task_list)
            task_list = []
    
def get_pic(skins):
    for skin in skins:

        dir_name = skin['heroName'] + '_' + skin['heroTitle']
        pic_name = ''.join(skin['name'].split(skin['heroTitle'])).strip();
        url = skin['mainImg']
        
        if not url:
            continue 

        invalid_chars='[\\\/:*?"<>|]'
        pic_name = re.sub(invalid_chars,'', pic_name)
        download(dir_name, pic_name, url)

def download(dir_name, pic_name, url):
    print(f'{pic_name} 下载完成, {url}')
    dir_path = f'{root_path}\{dir_name}'
    mkdir(dir_path)
    
    resp = requests.get(url, headers=header)
    with open(f'{dir_path}\{pic_name}.png', 'wb') as f:
        f.write(resp.content)
    print(f'{pic_name} 下载完成')

if __name__ == '__main__':
    mkdir(root_path)
    crawling()
```

![](https://files.mdnice.com/user/15960/792c4ef2-78c9-40ff-b639-4755cf9d5c0e.png)

### 总结

本文介绍了如何用 requests 和非阻塞的协程下载英雄联盟的皮肤。喜欢皮肤的小伙伴们可以每天换一张了。
