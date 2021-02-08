---
layout: post
category: python
title: 派森酱带你用 Python 实现中间人攻击
tagline: by 豆豆
tags: 
  - python100
---

![封面](http://www.justdopython.com/assets/images/2021/02/mitmproxy/000.jpg)

中间人攻击，顾名思义，就是客户端和服务端的通信被第三者拦截了，这样通信双方的通信内容就会被窃听。你可能会认为，没关系啊，窃听就窃听呗，反正又没什么重要的信息，那如果我告诉你，攻击者不但可以窃听你们的通信内容，甚至可以修改你们的通信内容，你还会这么认为么。

想象一下，当你和你的女朋友正聊的火热时，你们的聊天记录就好像被挂在了公屏上了一样，攻击者一览无余，甚至当你给你的女票发送了一句「我爱你」之后，攻击者篡改了你发送的内容，修改为「我恨你」。想象后果严重不严重。

与信息被窃听带来的危害相比，攻击者篡改通信内容所带来的危害则更甚。今天派森酱就带你来玩一玩中间人攻击。

## 工具安装

熟话说工欲善其事，必先利其器。好的工具可以让我们事半功倍，今天的主角就是 mitmproxy，这是一款出色的代理工具，使用起来也非常简单方便，使用 pip 安装即可。

```python
pip3 install mitmproxy
```

安装好之后，我们就可以使用 mitmproxy、mitmdump 或者 mitmweb 这三个命令来愉快的玩耍了。

其中 mitmproxy 是命令行的方式来交互的，不太好用，所以很少用，暂时忽略即可；mitmdump 是 mitmproxy 的命令行接口，关键的是，该命令可以使用 Python 对请求做数据做处理，比如数据的解析，过滤，存储等；而 mitmweb 则是 web 交互交互模式。

## mitmweb

直接在命令行是输入 `mitmweb` 按回车即可。

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/001.png)

此时，我们可以看到 mitmweb 在 8080 监听，而 8081 则是 web 交互界面的端口，打开地址 http://127.0.0.1:8081/ 即可看到。

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/002.png)

设置好电脑的代理服务器地址和端口，代理地址是本地，端口就是 8080，然后用浏览器访问必应首页 `https://cn.bing.com/`，mitmweb 监控页面就会收到一系列请求了，针对每隔具体的请求，还可以看到详细的请求和返回数据，

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/003.png)

## mitmdump

相比于 mitmweb，mitmdump 的功能更强大，我们可以使用 python 脚本来处理相应的请求。

先建一个 `script.py` 的脚本。

```python
def request(flow):
    print('request url is %s' % flow.request.url)
```

接着执行 `mitmdump -s script.py` 命令，可看到 mitmproxy 仍然是在 8080 端口开启监听。

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/004.png)

然后我们开始访问必应首页，可以看到控制台输出如下。

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/005.png)

细心的你可能发现了，第二张图的命令比第一张图多了一个 `-q` 的参数，这是为了防止 mitmproxy 的日志输出对结果造成干扰。我们的脚本程序已经跑通了，接下来就是如何对数据做处理了。

今天我们来做点好玩的，不管用户访问什么网站，我们都将其指向必应首页。

```python
def request(flow):
    flow.request.url = 'http://cn.bing.com'
```

一行代码搞定，启动 mitmproxy 来看下效果，我们试着访问下百度搜索。

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/006.gif)

另外，假设你正在 bing 搜索「如何自学 Python」，我们将返回的答案修改为「自学 Python，请关注“Python 技术”公众号」。

```python
def response(flow):
    text = flow.response.get_text()
    for str in ['自学 Python', '自学Python', '自学 python', '自学python']:
        text = text.replace(str, '自学 Python，请关注「Python 技术」公众号')
    flow.response.set_text(text)
```

![](http://www.justdopython.com/assets/images/2021/02/mitmproxy/007.gif)

启动 mitmproxy，然后用 bing 搜索相应的关键字，我们可以看到 bing 返回的结果已经被修改为我们程序中内定的文案了。

是不是很流弊呀，这就是 mitmproxy 的强大之处，我们可以用 Python 脚本对请求做任何处理，只有你想不到，没有做不到。

## 总结

今天我们用 mitmproxy 实现了中间人攻击，只是作为实验达到学习知识的目的。现实中的中间人人攻击远比这个要复杂的多，会涉及到 DNS 欺骗，网络劫持等多种手段，大家平时上网还需多留心。

> 代码地址：https://github.com/JustDoPython/python-examples/tree/master/doudou/2021-02-08-mitmproxy

