---
layout: post
title: 微信公众号里的视频下载
category: python
tagline: by 某某白米饭
tags: 
  - python
---

微信公众号可以发视频了，但是这个视频似乎没有直接能下载到本地的功能，小编就写一个 Python 小脚本将视频下载到本地。
<!--more-->
### 分析

将公众号文章在默认的浏览器中打开

![](https://files.mdnice.com/user/15960/f3d37cf0-a3dd-431b-9ba9-55cbe28156bc.png)

浏览器中的 url 才是我们最需要的

![](https://files.mdnice.com/user/15960/5e044080-7205-4e32-a751-2323742307f6.png)

在 F12 控制面板的网络面板找到视频的播放地址，这个地址隐藏的有点深。找到一个 `https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz=MzU0NjAxMzAyMQ==&mid=2247546485&idx=1&vid=wxv_2319653037964951553&uin=&key=&pass_ticket=&wxtoken=777&devicetype=&clientversion=&__biz=MzU0NjAxMzAyMQ%3D%3D&appmsg_token=&x5=0&f=json` 的 url 返回值中带有 `.mp4` 的 url。

![](https://files.mdnice.com/user/15960/30d59bff-a318-486a-b200-5fb039b68900.png)

下面是他的返回值。

![](https://files.mdnice.com/user/15960/2e1a3938-cc2d-4820-9b14-d99c6ed78dd7.png)

这时就简单了，我们只要分析 `https://mp.weixin.qq.com/mp/videoplayer` url 就可以了。可以看到这里的 mid、vid、_biz 是需要改变的，这些内容在文章中就能找到。

分析完了链接，下面就开始写代码：

```python
import requests,re

url = 'https://mp.weixin.qq.com/s/C6P5RwIejmUrnovom3lZFg'

result = requests.get(url).text
biz = re.search(r'__biz=(.*?)&amp;',result)[1]
mid = re.search(r'mid=(.*?)&amp;',result)[1]
vid = re.search(r'wxv_(.*?)\"',result)[0].replace('\"', '')

video_url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz={biz}&mid={mid}&idx=1&vid={vid}&uin=&key=&pass_ticket=&wxtoken=777&devicetype=&clientversion=&__biz={biz}&appmsg_token=&x5=0&f=json'

url_info = requests.get(video_url).json()['url_info'][0]['url']

resp = requests.get(url_info, stream=True)

with open('day10', 'wb') as f:
    f.write(resp.content)

print('视频下载完成')
```

### 总结

公众号的视频下载还是挺简单的。大家学会了吗？

