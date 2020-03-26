---
layout: post
category: python
title: 教你用 Python 下载手机小视频
tagline: by 極光
tags:
  - python100
---

上次给大家介绍了 `mitmproxy` 这个抓包工具，并且演示了如何用这个工具改变你电脑上网的请求以及请求返回信息，是不是觉得还有点意思。今天再为大家介绍下使用这个工具如何监控手机上网，并且通过抓包，把我们想要的数据下载下来。

<!--more-->

### 启动 mitmproxy

首先我们通过执行命令 `mitmweb` 启动 `mitmproxy`，让它处理监听状态，服务会监听本机 8080 端口，启动后如下：

```
$ mitmweb
Web server listening at http://127.0.0.1:8081/
Proxy server listening at http://*:8080
```

### 手机网络配置

1. 保证手机和电脑在同一局域网内，并查看电脑的局域网 IP 地址是多少以备用，查看方式可以用命令查看，如 Windows 系统用 `ipconfig` 命令，Mac 或 Linux 则用命令 `ifconfig`，看到如下图所示，找到本机在局域网的 IP 地址。

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-00.png)

不同操作系统，可能展示结果不同，在这里我们可以看到红框里我本机的 IP 地址为 192.168.0.108。

2. 配置手机代理地址，比如以下用 iphone 手机进行配置，打开设置 -> 无线局域网 -> 点现在连接的网络 -> 点最下面点 HTTP 代理配置，选择手动后，配置代理地址为我们电脑的 IP地址和 mitmproxy 的监听端口，配置如下图所示：

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-02.png)

3. 现在我们就可以让手机通过电脑上网了，不过目前手机 App 都是通过 HTTPS 加密请求，所以我们需要在手机上安装个 mitmproxy 的 HTTPS 证书。接下来我们打开手机浏览器，输入网址：mitm.it，打开如下图所示页面，选择对应手机的操作系统，下载证书并安装。

![下载页](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-01.png)

在这里我点 Apple 的图标下载证书，下载后等待安装：

![待安装](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-03.png)

![点安装](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-05.png)

单击上面的安装，可能会出现信任的提示，只要选择信任证书就可以了，下面是安装好的界面如下图：

![安装成功](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-06.png)

好了，配置完成下面我们点开个手机 APP 看到电脑 mitmweb 的页面上，已经出现请求内容了。

![安装成功](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-07.png)


### 编写下载脚本

好了，现在经过分析拦截的请求，我们开始用 Python 编写代码，通过解析视频的 url 将视频下载到本地。在这里我们先来打印下数据，新建文件  `xiaoshipin.py`，然后编写如下代码，实现将已编码的 json 字符串解码为 python 对象：

```py
# xiaoshipin.py

import json

def response(flow):
    url='https://api.amemv.com/aweme/v1/aweme/post/'
    #筛选出以上面url为开头的url
    if flow.request.url.startswith(url):
        text=flow.response.text
        #将已编码的json字符串解码为python对象
        data=json.loads(text)
        print(data)
```

编辑完后保存，然后执行命令：`mitmweb -s xiaoshipin.py`，带上这段脚本来运行我们的代理服务，刷新几个视频，会看到如下图所示内容：

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-08.png)

其中就包含了我们需要的下载地址信息，接下来我们只需提取视频的 url ,并且缓存视频到本地就 OK 了。

下面我们就来修改上面的 `xiaoshipin.py` 的代码，完善下视频下载的功能。

```py
#xiaoshipin.py

#引入包
import json,os
import requests

# 只拦截并处理返回请求
def response(flow):
    # 请求的 url
    url='https://api.amemv.com/aweme/v1/aweme/post/'
    #筛选出以上面url为开头的url
    if flow.request.url.startswith(url):
        text=flow.response.text
        #将已编码的json字符串解码为python对象
        data=json.loads(text)
        # 刚分析看到每一个视频的所有信息
        # 都在aweme_list中
        video_url=data['aweme_list']
        # 设置下载路径
        path='/Users/xx/shipin'
        # 如果文件夹不存在，则新建
        if not os.path.exists(path):
            os.mkdir(path)

        # 循环所有视频 url
        for each in video_url:
            #视频描述
            desc=each['desc']
            url=each['video']['play_addr']['url_list'][0]
            # 设置视频名称
            filename=path+'/'+desc+'.mp4'
            # 用 request 请求视频流
            req=requests.get(url=url,verify=False)
            # 保存视频文件
            with open(filename,'ab') as f:
                f.write(req.content)
                f.flush()
                print(filename,'下载完毕')
```

上面我已经把相关代码注释好了，现在我们保存编辑好的代码，然后再次执行命令：`mitmweb -s xiaoshipin.py`，启动监听服务。然后打开手机再次下视频，就会看到视频是不是已经都存到本地了。

![](http://www.justdopython.com/assets/images/2020/python/python-mitm/python-mitmproxy-mobile-09.png)


## 总结

本文为大家介绍了如何通过 `mitmproxy` 工具下载手机上浏览的小视频，当然除了视频他还可以下载音乐啊图片啊什么的，只要你能通过拦截工具分析你想要的内容在哪个请求中，然后对这个请求返回内容进行搜索分析，然后再用今天这个工具，再通过简单的 Python 编码实现自动处理完成就可以了。


## 参考

官网：https://mitmproxy.org
