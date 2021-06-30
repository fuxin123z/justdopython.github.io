---
layout: post
category: python
title: 反了！居然让我教她自动化测试
tagline: by 極光
tags:
  - 
---


一个做测试的居然让我教她怎么做自动化测试，真是反了……行吧，正好懂一些 `Selenium`，今天就来跟大家一起了解下 `Python` 如何使用 `Selenium` 进行自动化测试。

<!--more-->

## 简单介绍

`Selenium` 大家应该都很熟悉了吧，简单说它就是个基于浏览器的 Web 自动化测试工具，基本上是自动化测试人员首选工具。因为相比其他工具，它有很多的优势：

- 支持多种语言，比如 Python、Java、C或C#、ruby 等都支持；
- 支持多种浏览器, 比如 IE、FireFox、Safari、Opera、Chrome 这些主流浏览器基本都支持；
- 支持多种操作系统，比如 Windows、Mac、Linux 这个款主流操作系统。

其实单就上面这些优势就足以证明它的强大了，再加上它还支持分布式部署自动化测试程序，在多台不同的机器上同时执行。

是不是感觉很厉害？然而这么强大的工具它居然还是免费的，并且代码已经开源，这简直不敢想象。

说的这么厉害，那它要如何使用呢？

## 环境安装

首先你得先装好了 `Python`，然后通过 `pip install selenium` 命令进行安装就可以了（参见 `https://pypi.org/project/selenium/`）。

安装完 `selenium` 后，还需要再下载 `webdriver` ，不同的浏览器需要下载不同的驱动，以下是常见浏览器驱动的下载地址：

|浏览器 | 下载地址|
|------|-------|
|Chrome| https://sites.google.com/a/chromium.org/chromedriver/downloads|
|Edge |https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/|
|Firefox|https://github.com/mozilla/geckodriver/releases|
|Safari |	https://webkit.org/blog/6900/webdriver-support-in-safari-10/ |

我平时都是用 `Chrome` 浏览器，所以我下载了 `chromedriver` ，但有一点需要注意，你下载的 `chromedriver` 版本要和你安装的浏览器版本一致，不然使用中可能会出现各种问题。

![](http://www.justdopython.com/assets/images/2021/06/selenium/1.png)

## 简单开始

好了，现在我们就从最最简单的启动浏览器，然后打开一个网页开始。

- Chrome 浏览器
```
// 导入 webdriver
from selenium import webdriver

// executable_path 用于指定driver存放路径
browser = webdriver.Chrome(executable_path='/Users/xx/python/chromedriver')
// 打开百度页面
browser.get('https://wwww.baidu.com/')

```

写好后保存为 `test1.py` Python 文件，然后执行命令 `python test1.py`，然后就可以看到如下效果：

![](http://www.justdopython.com/assets/images/2021/06/selenium/2.png)

程序通过 `selenium` 调用 `chromedriver` 驱动 `Chrome` 浏览器启动，并让浏览器打开百度的首页，大概就是这么个过程。

除了使用 `Chrome` 浏览器，我们也可以使用其他的，比如 `Firefox`、`EDGE` 等。

- Firefox 浏览器
```
// 导入 webdriver
from selenium import webdriver

// executable_path 用于指定driver存放路径
browser = webdriver.Firefox(executable_path='/Users/xx/python/firefoxdriver')
// 打开百度页面
browser.get('https://wwww.baidu.com/')

```

- EDGE 浏览器
```
// 导入 webdriver
from selenium import webdriver

// executable_path 用于指定driver存放路径
browser = webdriver.Edge(executable_path='/Users/xx/python/edgedriver')
// 打开百度页面
browser.get('https://wwww.baidu.com/')

```


好了，通过对比上面代码相信你也能看出来，其实用哪个浏览器其实区别都不是很大，这里就不再一一截图了，接下来我就使用 `Chrome` 来介绍和演示效果了。

## 简单使用

当然启动浏览器，并打开页面我们只是走出了第一步，也就是写了个 `Hello World`，下面我们再慢慢介绍如何使用，再来看个简单例子：

```
// 导入 webdriver
from selenium import webdriver

// executable_path 用于指定driver存放路径
browser = webdriver.Chrome(executable_path='/Users/xx/python/chromedriver')
// 打开百度页面
browser.get('https://wwww.baidu.com/')
// 在搜索框内输入 `python selenium` 并点搜索返回结果
browser.find_element_by_id("kw").send_keys("python selenium")

```

好了，我们再保存下然后执行命令 `python test1.py`，然后看下效果：

![](http://www.justdopython.com/assets/images/2021/06/selenium/3.png)

没错，这次是打开百度首页后，又在搜索框输入 `python selenium` 字符串，并且点击 `百度一下` 按钮搜索出了结果。

但它是怎么获取到搜索框，这里我们用的是 `find_element_by_id()` 方法，也就是通过 `HTML` 标签元素的 `id` 找到了这个输入框。

那除了通过这个方法，还有别的方法能找到搜索框吗？


## 总结

好了，今天我们简单介绍了下 `selenium` 是什么，以及在 `Python` 中如何安装配置使用 `selenium`。如果你也对这个工具感兴趣，可以继续关注了解更多。OK，今天就聊这些，如果你喜欢记得点 `在看`。
