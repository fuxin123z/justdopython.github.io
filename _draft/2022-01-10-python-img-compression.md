---
layout: post
category: python
title: 什么！竟然有人把图片从 1M 优化到 1024kb
tagline: by 豆豆
tags: 
  - python100
---
![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/logo.png)

前两天刷知乎热搜看到一篇帖子，某省会城市健康码连续两次崩溃，相关公司在之前的报道中还声称：用两天两夜，将 1M 图片优化到 100kb。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/001.png)

报道中提到：“为了确保系统运行更高效，他们将一张图片从 1MB 压缩到 500 KB，再从 500KB 优化到 100kb。”

同时还声称，这样的工作看似简单，缺蕴涵着高技术含量，工程师连续两天两夜守在电脑前，终于攻下难关。

关于健康码崩溃的事网上众说纷纭，但消息肯定有真有假，就坐等官方发布最终消息就好了。不信谣不传谣。

今天咱们就单纯来讨论下图像压缩这件事。

关于图像压缩，工作中肯定是少不了的，尤其是涉及到图片传输和存储的时候，比如微信、微博、知乎等都需要考虑如此大批量的图片如何存储的问题。

都知道，咱 Python 是有很多图像库的，那想搞一下图像压缩还不是手到擒来，

## PIL

PIL 是 Python Image Library 的简称，其功能非常强大，短短三行代码即可实现图像的压缩。

咱们先来看下原图。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/002.png)

```python
from PIL import Image

im = Image.open("girl.jpg")
im.save("girl-out2.jpg", quality=10) # quality 是压缩比率
```

来看下压缩之后的。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/003.png)

从以上压缩结果来看，quality 设置为 10 时从 2.5MB 压缩到了 400KB，整体效果还是不错的。但整体来看图片是有一定的失真的，尤其是突然降图片放大之后，失真更明显，不信你看。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/004.png)

经过多次实验，发现将 quality 设置为 20 效果最佳。此时图像最终大小压缩到了 500KB，而且图片也不会失真。

事实上，PIL 提供了很多方法对图片进行缩放，下面咱们再试试另外一种办法。

```python
from PIL import Image

im = Image.open("girl.jpg")
w, h = im.size
im.thumbnail((w // 2, h // 2))
im.save("girl-out.jpg")
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/005.png)

在上面的代码中，我们先获得了图片的原始尺寸，然后直接将图片缩放至原来的百分之五十。最终图片大小为 343KB，而且图片看起来也不会失真。

由此可见，`thumbnail()` 的效果要比设定 quality 的效果要好一些。

当然，PIL 还提供了 resize() 函数来对图片进行缩放，小伙伴们可以自行尝试下哦。

## OpenCV

OpenCV 也是一个比较好用的操作图像的库，四行代码实现图片缩放。

```python
import cv2 as cv

img = cv.imread("girl.jpg")
resize_img = cv.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv.INTER_NEAREST)
cv.imwrite('girl-out3.jpg', resize_img)
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/img-compression/006.png)

在以上的代码中，我们先将原始图片读入进来，之后所缩放至原图的四分之一。从结果来看，效果还算可以。大小合适，图像没有明显的失真。

## 总结

今天给大家介绍了两款高质量图像处理库，从结果来看，二者的压缩效果是差不多的。事实上，这两个库不仅适用于图像压缩，还有很多高级玩法，这个就要靠小伙伴们自行解锁了。

除了本文所说的两个图像操作库，你还知道哪些方便好用的图像库么，可以在评论区和大家分享一下呀～