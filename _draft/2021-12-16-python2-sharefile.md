---
layout: post
title: 一行Python代码实现文件共享
category: python
tagline: by 闲欢
tags: 
  - python
---



![](http://www.justdopython.com/assets/images/2021/12/sharefile/0.jpg)

有时候，我们想要在局域网内共享一些文件，一般的实现方式是配置共享目录或者搭建一个文件服务器。但是无论哪种方式都是挺麻烦的。

但是现在不用担心了，今天教你一个快捷简便的方法。只要你电脑装了 python，就可以轻松实现。

### 共享文件

首先，请确保电脑上安装了 Python ，并且设置了全局变量。

接下来，你需要打开命令行终端，转到你需要共享的文件夹下：

![](http://www.justdopython.com/assets/images/2021/12/sharefile/1.jpg)

然后敲下我们的一行神命令：

> python -m http.server 9090

这行代码的意思就是把电脑的文件通过 http 协议共享出去，`9090`是端口，你可以任意指定没有被占用的端口。

如果你的界面是这样子的，证明共享成功了：

![](http://www.justdopython.com/assets/images/2021/12/sharefile/2.jpg)


### 访问文件

对于本机来说，如果你想测试一下是否共享成功，你可以打开浏览器，在地址栏输入：

> http://localhost:9090

访问后的界面：

![](http://www.justdopython.com/assets/images/2021/12/sharefile/3.jpg)

当然，你也可以找到本机的 ip地址，然后将 `localhost` 替换成 ip地址:

> http://192.168.1.4:9090/

效果和上面是一样的。

对于连接上同一网络的局域网内其他机器来说，他们只需要在浏览器上访问带有你的 ip地址的链接就可以访问到文件夹，即：

> http://192.168.1.4:9090/

看到的效果跟上面也是一样的。点击文件就可以下载了。

![](http://www.justdopython.com/assets/images/2021/12/sharefile/4.gif)

### 总结

关于一行 python 代码、实现文件共享服务器介绍完了，是不是 so easy ？下次如果有这种场景的时候，是不是可以装X一下了？


