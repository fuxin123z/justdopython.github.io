---
layout: post
category: python
title: 视频号的视频也不是那么难下载嘛
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/channel/logo.png)
昨天有小伙伴留言问：有办法下载视频号的视频吗？

作为一个充分宠粉的博主，必须安排，史上最便捷下载视频号视频方案来了。

正文开始之前，我在网上搜索了下如何下载视频号的视频，搜到最多的答案就是「如何下载微信视频号的视频？教你3种方法，1分钟轻松搞定！」

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/channel/001.png)

点开链接一看，里面的内容全都一样，复制黏贴大法果然好使。

文中提供了三种方法发，分别是安卓手机修改后缀、PC 微信查看源代码、以及使用下载工具。

第一种方法只适用于安卓手机，而且还要在手机的文件系统中找来找去，过于麻烦。

第二种只限定特定的微信版本，现在最新版本的微信已经不支持查看源代码了。

第三种需要安装工具，据我所知这个工具只能在 windows 上使用，对 Mac 用户不够友好，而且这个工具会不会窃取用户隐私还是另外一回事呢，**不要随便下载安装未知来源的软件**。

以上，所有方案均不可行。

其实，从网上下载资源大家都会的，无论是文本、图片还是视频，其底层原理都是二进制流，从网络读取之后写到本地硬盘就好了。

但前提是必须知道从哪里读取对吧，而视频号的视频之所以难下载就是因为其链接很难找，视频号不像公众号一样可以在浏览器访问，这就直接限制了一大部分只会 F12 的小伙伴。

难道除了 F12 就没有其他办法获取到视频的请求数据了吗，肯定不可能，微信在厉害，也要和服务器进行数据交互，视频不可能存储在本地。

于是，我在电脑端配置好网络代理，开启 mitmweb 抓包工具，之后开始用 PC 端的微信客户端刷视频，好家伙，这一下子跳出来上百个请求，经过我的仔细观察和验证，终于发现了下面这个链接。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/channel/002.png)

在浏览器中打开一看，果不其然，就是我刚才刷到的视频。

嘿嘿嘿，也不是很难嘛。

既然拿到了播放链接那下载就是小意思啦，可以在浏览器打开链接下载，也可以通过程序来下载，任君挑选。

讲到这里，这个方案顶多算是一个可行的方案，其一抓包工具大家都有，其二该方案透明不会有隐私泄露风险。

那如果说每次都要从上百个链接中找到视频链接，在手动去下载的话岂不是很麻烦么。

聪明的你肯定想到了解决方案，mitmproxy 不仅支持 web 端，更是支持 python 脚步的呀，写个脚本帮我们下载就好了。

于是，你会得到类似下面的这种代码。

```python
channel.py

def response(flow):
    url = flow.request.url
    content_type = flow.response.headers.get('Content-Type', default=None)
    logger.info(content_type)
    if "finder.video.qq.com" in url:
        content_type = flow.response.headers.get('Content-Type', default=None)
        if content_type is not None and content_type == 'video/mp4':
            logger.info(url)
            file_name = './urls.txt'
            with open(file_name, mode='a', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
                f.close()
```
```
mitmdump -q -p 8080 -s channel.py
```

至此，你只需要不停的刷视频，脚本就会自动把视频链接存储好，之后通过程序批量下载就好啦。

### 总结

今天给小伙伴们分享了如何下载视频号视频的方法，比较遗憾的是，还未发现如何批量下载某个用户下的所有视频。

关于下载视频号视频，小伙伴们有什么更好的方案或者想法呢，可以在评论区畅所欲言哦～