---
layout: post
category: python
title: 一行代码下载各大网站视频
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/you-get/logo.png)

都什么年代了还在下载视频？

非也非也，你永远不知道有些人就是喜欢收藏视频，比如我和正在读文章的你。

今天派森酱就教你一招，一键下载各大视频网站视频。小破站、腾讯、爱奇艺、油管...

### 工具准备

所用到的工具就是 `you-get` 这个库，话不多说，肯定得先安装一下。

不用担心，安装也非常简单。

```python
pip3 install you-get
```

没错，就是这么简单，接下来就是见证奇迹的时刻了。

### 小试牛刀

先来试试小破站的视频吧。

应该没有人不喜欢在小破站看小姐姐跳舞吧。中国联通的这个极乐净土有接近两百万的播放。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/001.png)

把地址栏中的的地址复制下来，接着打开命令行终端输入以下命令。

```python
$ you-get https://www.bilibili.com/video/BV1fV411H7Vt
```

稍等片刻就会下载完成啦。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/002.png)

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/002.png)

其中 xml 文件是视频的字幕。

来，在本地体验下小破站高清视频吧。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/004.png)
有了这个工具，妈妈再也不用担心我没有「学习资源」啦。

### 高级设置

事实上，这个工具不但可以下载小破站的视频，其他各大网站视频基本都可以下载。甚至国外的油管视频也不在话下，前提是你的网络是通畅的。

如果不加参数的话是默认下载到当前目录，如果你想指定下载目录的话只需要加上 `-o` 参数即可，指定文件名用 `-0` 参数。

```python
$ you-get -o ~/Videos -O 极乐净土.flv 'https://www.bilibili.com/video/BV1fV411H7Vt'
```

> 路径参数是小写字母 o，文件名称是数字 0

指定路径和文件名称在使用脚本批量下载视频、原视频标题和系统字符不匹配时特别好用。

一般视频网站都会为每个视频提供不同的清晰度版本，我们可以通过 `-i` 参数查看视频具体的信息。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/005.png)

默认下载的是最高清版本，如需指定其他版本，通过 `--format` 参数指定。

```
$ you-get --format=dash-flv720 'https://www.bilibili.com/video/BV1fV411H7Vt'
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/Lantern-Festival/006.png)

事实上，该工具不仅可以下载视频，甚至还可以下载图片。

```
$ you-get https://cdn.pixabay.com/photo/2021/11/14/18/36/telework-6795505_960_720.jpg
```

### 总结

今天给大家分享了一个超级神的工具，以后遇到喜欢的视频再也不怕官方下架啦。

除了视频和图片，你还想到用它来下载什么呀，可以在评论区和小伙伴么一起交流下哦～