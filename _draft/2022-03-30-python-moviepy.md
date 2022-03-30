---
layout: post
category: python
title: 全民副业时代，自动化剪视频更香
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/moviepy/logo.png)

最近的短视频特别火，尤其是微信推出了视频号之后，更是火的一塌糊涂。

今天就给大家介绍一款自动化剪视频神器-moviepy.

有了这款神器，再也不用担心剪视频慢了。

### 安装

```python
pip3 install moviepy
```
### 简单使用

1、视频裁剪

只需一行代码即可实现视频裁剪。

```python
from moviepy.editor import *

video =CompositeVideoClip([VideoFileClip("input.mp4").subclip(30,40)])
video.write_videofile("output.mp4")
```

2、更改分辨率

```python
from moviepy.editor import *

clip1 = VideoFileClip("1.mp4").resize((1080, 720))
```

在本例中我们将输入的视频更改为 1080p。

3、提取音频

```python
from moviepy.editor import *

audio = VideoFileClip('input.mp4').audio
audio.write_audiofile('output.mp3')
```

4、视频拼接

```python
from moviepy.editor import *

clip1 = VideoFileClip("1.mp4")
clip2 = VideoFileClip("2.mp4").subclip(30, 40)
clip3 = VideoFileClip("3.mp4")

final_clip = concatenate_videoclips([clip1, clip2, clip3])
final_clip.write_videofile("output.mp4")
```

这种拼接方式就是简单的将视频首位相连，再来看下更高级的视频拼接。

5、视频拼接

```python
from moviepy.editor import *

clip1 = VideoFileClip("1.mp4")
clip2 = VideoFileClip("2.mp4").set_start(4).crossfadein(1)
clip3 = VideoFileClip("3.mp4").set_start(9).crossfadein(1)

clip = CompositeVideoClip([clip1, clip2, clip3])
```

其中每个视频片段都是 5 秒钟，我们让 clip2 在第四秒开始播放，淡入 1 秒，clip3 在第 9 秒 开始播放，淡入 1 秒。

整体效果看起来过度就不会那么唐突，有一个淡入的过程。

注意，要有淡入效果的话，两个视频片段一定要有交叉才行。

### 汇总应用

熟悉了几个基本应用之后，我们就可以开始放大招了。

利用爬虫从网络爬去无版权的音乐和视频素材，然后结合音乐的长度将不同的素材拼接为整体视频，之后再去各大视频网站投稿赚取收益，岂不是美滋滋。

### 总结

今天给大家分享了一个款自动化剪辑视频的库，脑子活的小伙伴大可以根据本文提供的思路去搞一下，这年头有一份睡后收入它不香嘛。