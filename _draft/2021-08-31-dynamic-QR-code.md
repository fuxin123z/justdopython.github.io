---
layout: post
category: python
title: 刺激！用 Python 帮小姐姐做了一个专属的动态二维码
tagline: by 豆豆
tags: 
  - python100
---

![封面](http://www.justdopython.com/assets/images/2021/08/dynamic-QR-code/000.png)

随着微信不断的渗入到我们生活的方方面面，二维码也越来越常见。但大家常见的都是黑白的静态二维码，那我们可不可以做一些彩色的、动态的等比较酷炫的二维码呢。

比如用小姐姐的头像做背景、或者用一些非常可爱的动图做背景，于是我搜到了 MyQR 这个库。

今天咱们就帮小姐姐做一个她专属的动态的超酷炫二维码。

<!--more-->

## 模块安装

今天我们用到的库是 MyQR，这是 Python 中非常流行的制作二维码的库，通过一个简单的函数就可以生成各种各样的二维码，真可谓是神器。

安装过程也非常简单，直接通过 pip 进行安装即可。

```python
pip install MyQR
```

## 上手实操

俗话说掌握一项技能最快的方式就是实战，我们就先用 MyQR 制作几个简单的二维码吧。

想要生成二维码，最常用的方法是调用 MyQR 库中的 myqr 模块的 run 函数。该函数有以下几个参数。

+ words：二维码内容
+ picture：二维码背景图 .jpg，.png，.bmp，.gif，默认为黑白色
+ colorized：二维码背景颜色，默认 False，即黑白色
+ save_name：二维码名称，默认为 qrcode.png
+ save_dir：二维码路径，默认为程序当前路径

下面先生成一个最简单的二维码。

```python
from MyQR import myqr

words = 'Python'
myqr.run(
    words
)
```

效果如下：

![](http://www.justdopython.com/assets/images/2021/08/dynamic-QR-code/001.png)

黑白的有点不是很美观，加上背景图试试看。

```python
from MyQR import myqr

words = 'Python'
myqr.run(
    words,
    picture = './bg.png',
    colorized = True
)
```

效果如下：

![](http://www.justdopython.com/assets/images/2021/08/dynamic-QR-code/002.png)


最后咱们来生成动态的的酷炫二维码。

首先要准备好我们的动图素材，我从网络上找了一个大土豆和章鱼小丸子的超可爱动图。

![](http://www.justdopython.com/assets/images/2021/08/dynamic-QR-code/003.gif)


其实这一步和上一步很像，只是把静态图换成动态的就好了，代码如下：

```python
from MyQR import myqr

words = 'Python'
myqr.run(
    words,
    picture = './bg.png',
    colorized = True
)
```

效果如下：

![](http://www.justdopython.com/assets/images/2021/08/dynamic-QR-code/004.gif)

理所当然，生成的二维码也是 gif 格式的，长按二维码是可以识别的哦。

## 总结

今天带大家制作了一些比较有趣的二维码，大家可以发散下脑洞，看看还能做出什么更好玩更有趣的东西，欢迎在评论区互相探讨哦。