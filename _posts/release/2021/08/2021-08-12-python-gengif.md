---
layout: post
title: 卧槽！几行代码，干掉一个网站！
category: python
tagline: by 闲欢
tags: 
  - python
---


![封面](http://www.justdopython.com/assets/images/2021/08/gengif/0.jpg)

最近项目做得差不多了，上班的时候可以经常摸鱼。估计大家跟我差不多，摸鱼最多的时候是微信聊天。

最近在一个小群聊天时，快被气死了。一个哥们老是发过来一堆 gif 动图来怼我。可惜我库存不足，图到用时方恨少。我问他哪来这么多动图，他也是一副“不告诉你”的那种傲娇的姿态。

![就不告诉你](http://www.justdopython.com/assets/images/2021/08/gengif/1.jpg)

这就激起我的斗志了。不用说我也知道，无非就是用哪个软件或者哪个网站生成的。谁还不会了？

我打开浏览器搜索，输入关键词“gif生成”，下面出来一堆结果。

![搜索](http://www.justdopython.com/assets/images/2021/08/gengif/2.jpg)

点了几个进去看，实在是坑，要么需要注册，又是搜集一堆信息，要么就是到处是广告。

最讨厌注册个人信息和带广告的页面了。作为一个有追求的程序员，我萌生了自己写一个生成器的想法。

<!--more-->

### 思路

首先来看看这个 GIF 动画的构成。大家都知道，无非就是几张图片合成。那么要写一个这样的生成器，很有可能需要用到 Python 的 图像相关的包或者模块。

我搜索了一下相关资料，发现 PIL 这个包可以用来生成 GIF 动画。找到模块就很容易了，接着找到生成的方法和所需的参数就可以了。

### 实现

实现其实很简单，至少比我想象中的要简单得多。加起来也只有几行代码。我们来看看代码：

```
imgFolderPath = "C:\\Users\\xxx\\Downloads\\imgs"
fileList = os.listdir(imgFolderPath)
firstImgPath = os.path.join(imgFolderPath, fileList[0])
im = Image.open(firstImgPath)
images = []
for img in fileList[1:]:
    imgPath = os.path.join(imgFolderPath, img)
    images.append(Image.open(imgPath))
im.save('C:\\Users\\xxx\\Downloads\\imgs\\result.gif', save_all=True, append_images=images, loop=0, duration=500)

```

下面我们来解析一下这段代码：

> 获取需要生成 GIF 的图片。
> 获取第一张图片（这里我选择第一张图片作为 GIF 的首图）。
> 遍历图片，将图片添加到 images 对象存储。
> 生成动图。这里有几个参数，其中 loop 表示循环次数，duration 表示图片播放间隔，单位是毫秒。

我们来看一下生成的效果：

![美女动图](http://www.justdopython.com/assets/images/2021/08/gengif/3.jpg)

效果还可以吧？不过这里需要提醒一点，最好保持图片的大小一致，不然生成出来有可能出现奇怪的动图，你试试就知道了。

工具有了，图片哪里来呢？

像我这么懒的人，肯定不会去某网站一张张下载的。还记得之前的文章[后浪青年的聊天，需要 Python 助威](https://mp.weixin.qq.com/s?__biz=MzU1NDk2MzQyNg==&mid=2247485439&idx=1&sn=7fbfdb7ad8372eecf2821a6bb6b8680d&chksm=fbdadf72ccad5664e11920b12dc6d780e28c3fd9fcfe98c6a7494741be9fb32ce9f7a3bebcb9&token=1824218766&lang=zh_CN#rd)吗？运行一下，聊天斗图的素材源源不断地送进你的文件夹！


### 总结

工欲善其事，必先利其器。虽然代码只有短短几行，但是可以使你免于约束，自由自在地斗图。

今天就到这里，我还要赶着去给我对象定制一套专属动图，作为节日的礼物呢！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/gengif)