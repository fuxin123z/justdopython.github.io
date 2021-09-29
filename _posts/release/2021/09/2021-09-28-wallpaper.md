---
layout: post
category: python
title: 神器 ｜ 一键下载海量高清无码壁纸
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/09/wallpaper/000.jpg)

电脑默认的壁纸简直不是太难看，今天给大家介绍一个拥有海量壁纸的网站，即使你一天换一张也取之不尽用之不竭，网址如下：

<!--more-->

```
https://unsplash.com/
```

## 分析网站

这个网站基本上会定时更新自己的图库，都是高清无码的哦，质量只是不用说，做电脑壁纸实在是不二之选。

作为技术人当然不能一张一张去手动下载啦，这操作不符合我们技术人的身份气质，于是我研究了下网站的结构，发现当下拉页面时，网页会不断请求服务器获取新的图片信息，简单分析完网络请求之后发现了天机。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/09/wallpaper/001.png)

返回的信息是一个列表，每个列表中的有一个 urls 的字段，这个字段中包含很多个链接，一看就是根据图片清晰度做的区分，我们直接打开 full 链接看看是否是我们要找的图片。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/09/wallpaper/002.png)

至此，我们已经摸清了网站的图片加载流程，简言之就是通过调整 api 请求中的 page 参数来获取不同页码的请求结果，然后将图片 url 从请求结果中解析出来并下载到本地即可。

## 下载图片

首先需要一个下载图片的函数，该函数接受一个图片的路径和名称，然后将图片下载到当前目录。

```python
import urllib.request

# 下载图片
def download_img(img_url, file_name):
    print(F'downloading {file_name}, img_url = {img_url}')
    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            with open(file_name, "wb") as f:
                f.write(response.read())  # 将内容写入图片
            return 'ok'
    except:
        return "fail"
```

然后就是处理结果集的函数了，该函数负责解析出图片路径，然后调用下载函数直接下载。

```python
# 处理结果集
def deal_result(result, page):
    index = page * 12 # 每页有 12 张图片，所以这里需要转换下
    for i in range(len(result)):
        img_url = result[i]['urls']['full']
        index += 1
        download_img(img_url, str(index) + '.png')
```

接下来就是网络请求函数，非常简单，直接将请求结果返回即可。

```python
import requests as req

# 发送请求
def send_get(url, params):
    time.sleep(2)
    response = req.get(url, headers=None, params=params)
    return response.text
```

最后通过不断循环自增 page 来模拟翻页，并在入口函数中调用其即可。

```python
# 循环翻页
def loop():
    for i in range(3):
        url = 'https://unsplash.com/napi/photos?per_page=12&page=' + str(i)
        print(F'page = {i}, url = {url}')
        response = json.loads(send_get(url, None))
        deal_result(response, i)

if __name__ == '__main__':
    loop()
```

先来看看程序日志。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/09/wallpaper/003.png)

打开资源管理器看下运行结果。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/09/wallpaper/004.png)

至此，大功告成。

## 总结

今天派森酱给大家介绍了一个拥有海量高清无码图片的抓取方法，40 行代码即可轻松实现一键下载海量高清图片，美滋滋，再也不担心没有好看的图片做壁纸了。小伙伴们平时都是怎么找壁纸的呢，欢迎在评论区分享你的独家秘密哦～
