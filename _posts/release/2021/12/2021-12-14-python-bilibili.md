---
layout: post
category: python
title: 不熬夜、不修仙，B 站快速升级脚本
tagline: by 某某白米饭
tags:
  - 技术
---

![封面](https://files.mdnice.com/user/15960/aac8c608-7db6-480f-be82-3250c98090ed.jpg)

在 B 站上看了进击的金厂长的投稿的视频如：B 界等级修仙传，B 界等级修魔传等，觉得 B 站升级对小编这种白嫖党 + 懒癌党太不友好了，就码了这篇 B 站升级脚本。
<!--more-->
### 获取个人信息

用自己的账号登录到 B 站并打开个人页面，按 F12 控制面板。可以找到一个 `https://api.bilibili.com/x/space/myinfo?jsonp=jsonp&callback=__jp0` 的地址，从相应的返回值来看，这就是个人资料的请求地址。并且把请求头中的 cookie 复制到代码中，让我们可以正常用代码登录 B 站。

![](https://files.mdnice.com/user/15960/c19a0325-5ecf-4f22-82eb-e5c4305ef3f2.png)

这里的 cookie 是一串字符串，在 requests.get() 请求的时候肯定是要转换为字典类型的。其中一个 bili_jct 比较关键，在后续操作中将被用到。

```python
def convert_cookies_to_dict(cookies):
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies
```

下面代码就用上面转换成字典的 cookie 获取 B 站的个人资料。

```python
def getInfo(cookie):
    url = "http://api.bilibili.com/x/space/myinfo"

    
    resp = requests.get(url, cookies=cookie).text
    myinfo = json.loads(resp)

    data = myinfo['data']
    mid = data['mid']
    name = data['name']
    level_exp = data['level_exp']
    current_level = level_exp['current_exp']
    current_exp = level_exp['current_exp']
    next_exp = level_exp['next_exp']
    sub_exp = int(next_exp) - int(current_exp)
    days = int(int(sub_exp)/70)
    coin = data['coins']
    print("{}，你的等级是{}，当前经验是{}，下一级经验是{}，还需要{}天升级，有{}个硬币".format(name, current_level,current_exp,next_exp,days,coin))
```

### 观看视频

因为小编实在是不想解析页面，就在网上找了一个 B 站的 `http://api.bilibili.cn/recommend` 接口来获取视频地址。返回值是一个 json 串，这里面有 aid 和 bvid。

```python
def getVideo(cookie):
    url = "http://api.bilibili.cn/recommend"

    resp = requests.get(url, cookies=cookie).text
    data = json.loads(resp)
    
    list_length = len(data['list'])
    result = []
    for i in range(list_length):
        bvid = data['list'][i]['bvid']
        aid = data['list'][i]['aid']
        result.append({'bvid': bvid, 'aid': aid})
    return result
```

获取到 aid 和 bvid 后，打开播放视频页面会有发送心跳链接到服务器，这个应该可以看做是看过视频的。

![](https://files.mdnice.com/user/15960/8e9b13c5-04ee-48f9-a340-7dfb46a69640.png)

```python
def view(bvid, aid, bili_jct, playedTime):
    url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/"+bvid,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }
    data = {
        'aid': aid,
        'bvid': bvid,
        'played_time': playedTime,
        'csrf': bili_jct
    }
    resp = requests.post(url, data = data ,headers=header).text
    json_data = json.loads(resp)
    code = json_data['code']
    time.sleep()
    if code == 0:
        print('视频观看成功，bvid 号为：' + bvid)
    else:
        print('视频观看失败，bvid 号为：' + bvid)
```

### 投币

投币比较简单，只有 4 个参数，但是每天就只能投 5 个币，得 50 经验。

![](https://files.mdnice.com/user/15960/c7402819-ed30-4cdd-8a4e-18ab4e175235.png)

```python
def coin(bvid, aid, csrf):
    
    url = "https://api.bilibili.com/x/web-interface/coin/add"
    data = {
        'aid': aid,
        'multiply': 1,
        'select_like': 1,
        'cross_domain': 'true',
        'csrf': csrf
    }
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/"+bvid,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }

    resp = requests.post(url, headers=header, data=data).text
    data = json.loads(resp)
    code = data['code']
    if code == 0:
        print("投币成功")
    else:
        print('投币失败')
```


### 分享视频

在分享到动态的时候，可以看到有一个 share 的地址，然后小编就用这个试了好几次都没有成功，只能求助万能的 github。

![](https://files.mdnice.com/user/15960/eb13eed2-46e3-4047-ba00-42908056c16f.png)

上面这个地址没成功，都是分享失败，下面的截图是 github 的，分享成功。

![](https://files.mdnice.com/user/15960/950cf114-f51e-47bc-8190-ac60065482f7.png)

```python
def share( bvid, csrf):
    url = 'https://api.bilibili.com/x/web-interface/share/add'
    data = {
        'csrf': csrf,
        'bvid': bvid
    }
    header = {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        "Connection": "keep-alive",
        "origin": "https://t.bilibili.com",
        "referer": 'https://t.bilibili.com',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }
    resp = requests.post(url, data=data, headers=header).text
    json_data = json.loads(resp)
    code = json_data['code']
    if code == 0:
        print('视频分享成功')
    else:
        print('视频分享失败')
```

### 总结

python 小脚本总能在想不到的地方有意外的惊喜。人生苦短，认为本文还可以的朋友点个赞和再看。
