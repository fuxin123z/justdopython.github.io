---
layout: post
category: python
title: 老板让很快处理数百图片，我该辞职吗
tagline: by 太阳雪
tags:
  - python
  - 图片缩放
  - 加水印
---
工作种常常会遇到一些棘手的问题，干好了名利双收，干不好就可能失去工作机会，特别是在疫情严重的现在，裁员压力很大:(
<!--more-->

## 从天而降

小派同学，刚进公司不久，接到了一个任务，需要在立即将数百张图片进行缩放处理，并且加上水印，以便在网页上展示，处理后的图片像这样：

![目标](http://www.justdopython.com/assets/images/2020/08/resize/03.jpg)

正常处理一张照片，从打开、调整大小、加上文字，另存，需要将近一分钟，几百张图片，手工操作，简直是 Mission Impossible，这可如何是好，放弃呢还是硬着头皮扛下来……

对于有 Python 技能的我们来说，这都不是事

## 神器入场

图片处理，Pillow 首屈一指，它源自于 PIL(Python Imaging Library)，是 Python 平台事实上的图像处理标准库，功能非常强大，而且接口简单。

为了支持 Python 3.x，在 PIL 的基础上创建了兼容的版本，Pillow，并且加入了许多新特性，因此今天我们的主角是 Pillow，非常适合当前的任务场景

通过 pip 安装：

```shell
$ pip install pgmagick
```

> 注意：
> Pillow 和 PIL 不能同时存在，如果已经安装过 PIL 请先卸载或者创建虚拟环境，再安装 Pillow
> 创建虚拟环境，可参考 [《Python 虚拟环境 看这一篇就够了》](https://mp.weixin.qq.com/s/NJLjflbn3ru9iftVFJQC1g)

## 庖丁解牛

有了处理神器 pgmagick，现在来分析下任务

- 图片是为了在 Web 上展示的，所以体积不能太大，另外要保持一定的清晰度
- 要处理的图像文件格式有多种， png、jpg（jpeg）等，所以需要同时支持多种格式
- 对于处理后的图片需要添加水印，所以需要用到 pillow 的绘制功能

### 缩放

直接上代码：

```python
from PIL import Image

def resize(img, size):
    nsize = scale(img.size, size)
    return img.resize(nsize, Image.ANTIALIAS)

def scale(size, lsize):
    nsize = (size[0], size[1])
    if nsize[0] > lsize[0]:
        nsize = (lsize[0], int(lsize[0]*nsize[1]/nsize[0]))
    if nsize[1] > lsize[1]:
        nsize = (int(lsize[1]*nsize[0]/nsize[1]), lsize[1])
    return nsize
```

- 定义 `resize` 方法，接受一个图片对象，和调整后的大小（turtle 类型）
- 利用 Pillow Image 对象的 `resize` 方法进行缩放，第二个参数 `Image.ANTIALIAS` 作用是抗锯齿，会让调整后的图像更清晰
- 返回处理好的图片对象，以便后续操作
- `scale` 方法用来计算调整后的图像规格，利用等比缩放原理，原始图像规格为 (x,y)，调整后的为 (x',y')， 就会有：x/y = x'/y'，所以给定三个值，就可以计算出第四个值

### 水印

图片加水印有两种方式：

一种是在图片上加上可见的文字或者图标，适合在网上展示，用于声明图片版权等

另一种是在图像中，加入不可见数据，用户图片的版权保护和防伪，也可以图像签名

因为图片是为了在网上展示，所以用第一种加水印方式

原理是：创建一个和原图大小一致的透明图片，将水印文字写到图片的右下角，然后将水印图片和原图进行叠加，成为加完水印的图片

上代码：

```python
def waterMark(image, text, font=None):
    font = font if font else ImageFont.truetype(r"C:\Windows\Fonts\STHUPO.TTF", 24)
    mode = image.mode
    if mode != 'RGBA':
        rgba_image = image.convert('RGBA')
    else:
        rgba_image = image

    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = (rgba_image.size[0] - text_size_x - 10, rgba_image.size[1] - text_size_y - 10)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 100))

    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    if mode != image_with_text.mode:
        image_with_text = image_with_text.convert(mode)

    return image_with_text
```

- `waterMark` 是为图片加水印的方法，参数分别是图像对象，水印文字，和字体
- 字体可以选择系统中，字体文件夹中的字体文件，如果有汉字，需要选汉字字体文件，这里默认使用`华文琥珀`字体
- 如果原始图像不是 `RGBA` 模式，将转换为 `RGBA` 模式，即增加透明通道，以便水印图片叠加
- 按照原始图片大小，创建一个透明通道值为 `0`，即全透明的图片，作为水印图层
- 获取图层上的绘制接口 `image_draw`, 然后计算将要绘制水印文字的大小，绘制文字大小取决于字体、字号和文本长度
- 计算出水印块在原始图片中右下角的坐标，且最小离边距为 10 个像素
- 使用绘制接口，指定绘制坐标、颜色和透明度，将水印绘制在水印图层上
- 最后使用 pillow Image 类方法 `alpha_composite` 将原始图像和水印图层合并
- 判断原始图片模式是否于转换后的相同，如果不同转换为原始图像模式

### 集成

有了缩放和水印功能，现在可以集成了

因为要处理多个图片，需要有编写一个方法，指定图片目录，获取目录中的图片，做为处理的输入

上代码：

```python
def process(imgPath, destPath=None, size=(800,600), text=""):
    destPath = destPath if destPath else os.path.join(imgPath,'out','')
    if not os.path.isdir(destPath):
        os.makedirs(destPath)

    files = [x for x in os.listdir(imgPath) if os.path.isfile(imgPath + x)]
    for f in files:
        fext = os.path.splitext(f)[1]   # 扩展名
        if fext in ['.png', '.jpg', '.bmp', '.jpeg']:
            img = Image.open(os.path.join(imgPath, f))
            img = resize(img, size)
            img = waterMark(img, text)
            img.save(os.path.join(destPath,f))
```

- `process` 是整体处理方法，参数分别是图片目录路径，目标路径（处理完成后的存放位置），标准大小，以及水印文字
- 如果没有提供目标路径，默认为图片目录中的 `out` 目录
- 如果目标位置不存在，则创建
- 利用 `os.listdir` 获取目录中的文件名和目录名，过滤掉非文件对象，汇总到集合 `files` 中
- 遍历 `files`，获取扩展名，过滤掉非图片文件
- 对图片进行处理，打开，调整尺寸，添加水印，最后保存到目标目录中

最后在是调用：

```python
if __name__ == "__main__":
    process("D:\\images\\", text="@python技术")
```

## 精彩呈现

测试了 208 张桌面背景图片，分辨率大体为 `1920 X 1080`，运行环境是 Win10，CUP i5-10210U，内存 16GB，运行时间在 20秒左右

![运行时长](http://www.justdopython.com/assets/images/2020/08/resize/04.jpg)

> 注意：不同环境中，运行时间会有所不同

这是待处理文件：

![处理前](http://www.justdopython.com/assets/images/2020/08/resize/01.jpg)

这是处理后的结果：
![结果](http://www.justdopython.com/assets/images/2020/08/resize/02.jpg)

再看下水印效果:

![水印](http://www.justdopython.com/assets/images/2020/08/resize/05.jpg)

好了，交工，感受到嘉奖的味道了吗？

## 总结

工作中常常会遇到一些棘手的问题，与其说是阻碍或者挑战，倒不如说是一个机会，正式这样一个个机会，成就了未来强大的我们。
理想很丰满，现实很骨感，只有拥有足够的技能和综合能力，才能抓住这些机会，祝愿明天的你更强大！

## 参考

- [https://www.liaoxuefeng.com/wiki/1016959663602400/1017785454949568](https://www.liaoxuefeng.com/wiki/1016959663602400/1017785454949568)
- [https://blog.csdn.net/ajian6/article/details/93615594](https://blog.csdn.net/ajian6/article/details/93615594)
- [https://www.pythonf.cn/read/71](https://www.pythonf.cn/read/71)
- [https://zhuanlan.zhihu.com/p/33450843](https://zhuanlan.zhihu.com/p/33450843)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/resize>
