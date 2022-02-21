---
layout: post
title: 一行代码，生成和读取二维码！
category: python
tagline: by 闲欢
tags: 
  - python
  - 二维码
---


![封面](http://www.justdopython.com/assets/images/2022/02/qrcode/0.jpg)


二维码是用某种特定的几何图形按一定规律在平面（二维方向上）分布的、黑白相间的、记录数据符号信息的图形。

二维码被称为快速响应码，可能看起来很简单，但它们能够存储大量数据。无论扫描二维码时包含多少数据，用户都可以立即访问信息。

近些年二维码也是迅速普及，目前已经成为了我们生活中的一部分，它有许多应用场景：

- 信息获取（名片、地图、WIFI密码、资料）
- 网站跳转（跳转到微博、手机网站、网站）
- 广告推送（用户扫码，直接浏览商家推送的视频、音频广告）
- 手机电商（用户扫码、手机直接购物下单）
- 防伪溯源（用户扫码、即可查看生产地；同时后台可以获取最终消费地)
- 优惠促销（用户扫码，下载电子优惠券，抽奖）
- 会员管理（用户手机上获取电子会员信息、VIP服务）
- 手机支付（扫描商品二维码，通过银行或第三方支付提供的手机端通道完成支付）
- 账号登录（扫描二维码进行各个网站或软件的登录）
 
Python 处理二维码也非常简单，今天我们就来看看怎样使用一行代码生成或者读取二维码。

<!--more-->

### 生成二维码

Python 有一个处理二维码的模块叫`qrcode`，我们要生成二维码，需要安装这个库：

> pip install qrcode

生成二维码就是调用这个模块的 `make` 函数：

```python
import qrcode

img = qrcode.make('https://www.zhihu.com/people/wu-huan-bu-san')
img.save('./pic.jpg')

```

运行这段代码，就可以得到下面的二维码：

![](http://www.justdopython.com/assets/images/2022/02/qrcode/1.jpg)

大家可以扫码试试看，说不定有惊喜哦！

你肯定会说：骗子！这不是一行代码啊！

好吧，这两行可以合并的嘛：

```python
qrcode.make('https://www.zhihu.com/people/wu-huan-bu-san').save('./pic.jpg')
```

### 读取二维码

读取二维码就是将二维码背后隐藏的信息解析出来，这时候就不是用 `qrcode` 这个模块了，而是用 OpenCV 这个模块。相信公众号的读者肯定对这个库比较熟悉，经常出现在我们的文章中。

先安装这个库：

> pip install opencv-python

接着，我们以上面生成的二维码为例，来看看读取的代码：

```python
import cv2

d = cv2.QRCodeDetector()
val, _, _ = d.detectAndDecode(cv2.imread("pic.jpg"))
print("the secret is: ", val)

```

运行这段代码，打印信息是：

> the secret is: https://www.zhihu.com/people/wu-huan-bu-san

这正是我们生成二维码的内容。

这里怎么转换成一行代码就不需要我赘述了吧！


### 总结

二维码的操作代码够简单吧！相信看过这篇文章的你肯定能记住，下次遇到二维码操作的时候只需5秒就可以出结果！当然，还有其他一些操作，大家可以阅读模块的接口去尝试。




