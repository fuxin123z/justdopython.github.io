---
layout: post
title: 嘿嘿！几行代码秒出美女素描图！
category: python
tagline: by 闲欢
tags: 
  - python
  - OpenCV
---



![封面](http://www.justdopython.com/assets/images/2021/12/pencilimg/0.jpg)


今天上班时，我正在敲代码。女朋友突然发了一张图片给我：

![](http://www.justdopython.com/assets/images/2021/12/pencilimg/1.jpg)

“老公，我也想要一个这样的头像...”
后面跟着一个可怜的表情。

无奈，不管怎样我只好应承下来。

下班回到家中，我准备把这个任务完成了。其实完全可以找个美颜的 APP ，上传图片，点几下就好了。但是作为她心目中的技术大神，我肯定不能这么干，不然干嘛要让我来做这件事情（要深刻理解女生的目的）。

我略加思索，感觉这件事情用 Python 来实现并不困难。

<!--more-->

### 实现步骤

实现需要用到的工具是 OpenCV 库，用 OpenCV 库里面的图片处理接口就能满足需求。

##### 安装 OpenCV 库

安装方法还是我们的老一套：

> pip install opencv-python

#### 读取图片

我从手机相册中找了一张照片，发送到微信，然后保存到电脑上。

![](http://www.justdopython.com/assets/images/2021/12/pencilimg/2.jpg)

我们代码的第一步就是要读取这张图片。

```python
import cv2
img = cv2.imread("mv5.jpg")

```

#### 转换成灰度图片

我们读取的是 RGB 格式的图片。接着，我们将这张图片转换为灰度图片。

```python
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

```

转换之后，图片是这样子的：

![](http://www.justdopython.com/assets/images/2021/12/pencilimg/3.jpg)

#### 反转灰度图像

接下来，我们要将灰度图像反转，以便于增强图像的细节。

```python
inverted_image = 255 - gray_image

```

反转之后，我们得到的图片是这样的：

![](http://www.justdopython.com/assets/images/2021/12/pencilimg/4.jpg)

看起来是不是有点恐怖？

#### 创建铅笔图

最后，我们将反转的图像进行模糊处理，然后再将模糊的图像倒置，最后将灰度图像除以倒置的模糊图像，就可以创建铅笔草图了。

```python
blurred = cv2.GaussianBlur(inverted_img, (21, 21), 0)
inverted_blurred = 255 - blurred
pencil_sketch = cv2.divide(gray_img, inverted_blurred, scale=256.0)
```

我们使用 OpenCV 显示一下：

```python
cv2.imshow("original", img)
cv2.imshow("pencil", pencil_sketch)
cv2.waitKey(0)

```

最后输出的图像是这样子的：

![](http://www.justdopython.com/assets/images/2021/12/pencilimg/5.jpg)


### 总结

别看我写了这么几个步骤，实际上代码也就几行而已。下次妹子问你能不能给她做素描图像，千万别甩一句：用美图秀秀啊！不然你会失去一个妹子的！










