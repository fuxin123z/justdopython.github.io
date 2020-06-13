---
layout: post
category: python
title: 30 行代码利用 Python 在命令行看图片
tagline: by 豆豆
tags: 
  - python100
---

每次看黑客类的电影时都惊叹于黑客的技术之高超，黑客的手在键盘上飞快的敲击，屏幕上各种字符狂闪不止，接着系统就被黑掉了。

我们都知道黑客在命令行发送的各种命令都是英文字母或者数字，那么我们是否可以直接在命令行查看图片呢？

答案是可以的，今天派森酱就带你在终端查看图片。

<!--more-->

先来看看我们最终实现的效果。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/05/image_to_chars/001.gif)

## 安装

我们今天要用到 pillow 库，直接使用 pip 安装即可。

```python
$ pip install pillow
```

使用之前需要先将相应模块引入我们的程序。

```python
from PIL import Image
from PIL import ImageFilter
```

## Hello World

PIL（Python Imaging Library）是 Python 平台上一个非常好用的图像处理库，功能强大且 API 简单易用，但仅支持到 Python 2.7，所以有人就在 PIL 的基础上创建了新的版本 pillow，可以支持到 Python 3.x。

来看看模糊效果，只需三四行代码。

```python
im = Image.open('/tmp/qq.jpg')
im2 = im.filter(ImageFilter.BLUR)  # 应用模糊滤镜:
im2.save('/tmp/qq_2.jpg', 'jpeg')
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/05/image_to_chars/002.png)

图像缩放，几行代码轻松搞定。

```python
im = Image.open('/tmp/qq.jpg')
w, h = im.size
im.thumbnail((w // 2, h // 2))  # 缩放到 50%
im.save('/tmp/qq_thumbnail.jpg', 'jpeg')
```

## 字符画

众所周知，终端只可以显示字符，那如果可以把图片转化为字符的画，岂不是可以在终端正常显示了，事实上还真可以这么做。其原理就是将图片不同位置的像素点用不同的字符来代替，从而将由像素组成的图片转变成由字符组成的字符画。

但是像素是有颜色的，我们如何将不同颜色的像素编码为对应的字符呢？

这就要涉及到灰度图的概念了。

> 灰度图，又称灰阶图，把白色与黑色之间按对数关系分为若干等级，称为灰度，共分为 256 阶，0 到 255，0 为黑色，255 为白。用灰度表示的图像称作灰度图。

事实上任何颜色都有红、绿、蓝三原色组成，假如某个像素点的颜色为 RGB(R，G，B)，那么，我们可以通过固定公式将其转换为指定灰度即可。

> GRAY ＝ 0.2126 * R + 0.7152 * G + 0.0722 * B

拿到像素点的灰度值之后，我们将其对应到指定字符即可，为了最大限度的还原原图像，灰度值较高的像素点我们使用视觉上较深的字符表示（如$），灰度值较低的像素点我们使用视觉上较浅的字符（如：0）表示。

所以，字符的种类与数量越多，能表现的颜色也就越多，字符画的层次感也就会更好。最理想情况是将灰度值和字符一一对应，然而事实上字符数量是远远少于灰度值值域的，所以就会有多个灰度值对应到同一个字符上的情况。

比如我们只用 0 到 9 十个阿拉伯数字来作为我们的字符集，那么一个字符对应的灰度值区间大小就是 25.6（区间大小 = 256 / 字符集长度）。

灰度值区间和字符对应关系：

```
[0, 25.6) -- 0
[25.6, 51.2) -- 1
[51.2, 76.8) -- 2
...
[204.8, 230.4) -- 8
[230.4, 256) -- 9
```

### RGB 转换字符

有了以上的理论基础，我们将 RGB 转换为字符的函数定义如下：

```python
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
def get_char_by_rgb(r, g, b):
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = 256.0 / length
    return ascii_char[int(gray / unit)]
```

### 处理图像

完成了上面的转换函数后，我们就要开始对处理图像了。

首先我们需要调整下图片的大小，以免图片太大或者太小，然后我们遍历图片的每个像素点获取到 RGB 值，然后根据函数 `get_char_by_rgb(r, g, b)` 获取到对应的字符，最后将所有的字符拼拼接起来输出到终端即可。

注意，我们通过函数 `getpixel(x,y)` 获取坐标 `(x,y)` 的像素的 RGB 值，该函数的返回值为一个元组，比如 (1,2,3) 或者 (1,2,3,0) 最后一位的 0 是 alpha 值。alpha 的值为 0 是表示该位置空白。

所以，我们需要修改下 `get_char_by_rgb(r, g, b)` 函数，添加 alpha 参数。

```python
def get_char_by_rgb(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = 256.0 / length
    return ascii_char[int(gray / unit)]
```

遍历图片获取像素点，然后转换为相应的字符。

```python
def process_image(image_path, file_path='out.txt'):
    img = Image.open(image_path)
    img = img.resize((WIDTH, HEIGHT))
    width, height = img.size
    txt = ""
    for x in range(height):
        for y in range(width):
            txt += get_char_by_rgb(*img.getpixel((y, x)))
        txt += '\n'

    with open(file_path, 'w') as f:
        f.write(txt)
    print(txt)
```

最后编写入口函数，就大功告成啦。

```python
if __name__ == '__main__':
    image_path, file_path = '/tmp/qq.jpg', '/tmp/qq.txt'
    process_image(image_path, file_path)
```

至此，我们完成了从原始图像到字符画的转换。

## 总结

今天我们实现了将图片转换字符画，以便在终端查看图片，可能在不通的终端会显示不通的效果，大家可酌情调整宽高比例。

## 代码地址

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/doudou/2020-05-17-character-drawing