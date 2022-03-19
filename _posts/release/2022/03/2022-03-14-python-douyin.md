---
layout: post
category: python
title: 抖音放爬虫？不存在的，看我如何绕过抖音的防爬虫机制一键下载无水印视频
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/douyin/logo.png)

不得不说抖音真的是一款神器，它会让你不知不觉的沉迷其中，曾经的我无数次都是抱着向同行学习的初衷下载的抖音，无奈最终都以沉迷抖音的各种视频中无法自拔而告终，人间真实。

不过有一说一，抖音上还是有一些很不错的视频的，比如一些科普、科技 UP 主，他们分享的知识都挺不错的，我就想把他们吓到本地保存起来方便后续继续学习。

不过，大家都知道通过抖音 App 的保存视频到本地是会在视频的末尾加上抖音的水印和音频的，及其不友好。

于是，我就想能不能通过抓包的方式来抓取视频的无水印路径，然后在下载呢，说赶紧干。

一通设置之后，美滋滋的打开抖音准备拦截请求，神奇的一幕发生了。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/douyin/001.png)

刚开始我以为是我哪里设置不对，再三确认之后发现没有错，测试了下发现其他的 App 都能正常连网，芭比 Q 了，大概率是抖音做了防爬机制，说实话我也是第一次遇到这种情况，可能抖音官方觉得市面上爬取视频的人太多了，就出了这一招。

研究了半天还是绕不过抖音的防爬机制，咋整，不能半途而废呀，这不是我们技术人的风格，是吧。

好巧不巧，就在准备放弃时，突然想起来好像有小程序可以去抖音水印，抖音的包抓不了，小程序的包应该可以吧，可以吧，吧。

打开某去水印小程序，将抖音的口令复制进去，开始抓包，果不其然，一切都在预料之中。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/douyin/002.png)

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/douyin/003.png)

简单分析下这个请求，`token` 就是唯一用户标识，基本上可以认为长久有效，`val` 则是抖音的口令。

事已至此，就很简单啦。

```python
def get_douyin_video(content):
    api = 'https://api.qingdou.vip/miniApp/watermark/index'
    params = {
        'val': content,
        '_platform': 'miniapp',
        'token': ''
    }
    data = json.loads(req.send_post(api, params, None))
    return data['result']['url']
```

### 总结

做技术的都知道，任何问题都以通过添加一个中间层来解决，这不就是很好的例子么。当然程序还有很多可以优化的点，比如可以做成微信/钉钉机器人，将口令推送给机器人，然后直接解析出原视频地址。

关于无水印下载抖音视频，你还有什么好的方案呀，可以给大家分享分享哦～