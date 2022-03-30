---
layout: post
category: python
title: 视频剪辑神器 FFmpeg
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/FFmpeg/logo.png)

全民副业时代，好像大家都在做短视频。

今天就给大家介绍一款视频剪辑神器-FFmpeg。

FFmpeg 的用途之广泛，功能之强大远超你想象，很多商业软件都在使用。也正是有由于其功能大而全，单篇文章很难接受的全面，本文主要就一些视频音频的处理做下介绍，但也足够我们日常使用了。

### 安装

大家可以直接在官方下载对应的版本来安装，很简单，就不再赘述了。

### 基本概念

容器：视频文件本身就是一个容器，像 MP4、AVI 等不同的格式就代表不同的容器。

编码格式：数据要经过编码才能形成固定的格式，软件才能读取，这也就是我们常见的文件了，像 H.262 H.264 H.265 都是常用的视频编码格式。 

音频格式就是 MP3 咯。

### 简单实用

FFmpeg 的命令格式非常复杂，但基本可以简化成如下格式。

```
ffmpeg [a] [b] -i [c] [d] [e]
```

其中 a、b、c、d、e 分别代表全局参数、输入文件参数、输入文件、输出文件参数、输出文件。

是不是对照起来还挺对称的呢。

其中很多时候很多参数又都是可以省略的，比如 a b d 都可以省略。

于是，最简单的一个转换格式的命令就是下面这个样子了。

```
ffmpeg -i in.mp4 out.avi
```

有木有很简单，而且转换速度非常快。

### 常用命令

1、提取音频

```
ffmpeg -i input.flv -vn -codec copy out.mp3
```

其中 copy 表示直接复制原，不经过重新编码解码，这样子比较快。

2、截取视频

```
ffmpeg -y -ss 5 -t 5 -i 1.mp4 -c:v copy -c:a copy cut.mp4

ffmpeg -y -ss 5 -t0 10 -i 1.mp4 -c:v copy -c:a copy cut.mp4
```

-ss 表示直接从第 0 秒开始截取，-t 表示持续多久，-to 表示结束时间。

因此，上面的两条命令都是表示将 1.mp4 从第 5 秒开始，截取 5 秒的片段。

3、单张图片转视频

```
ffmpeg -y -loop 1 -i bg.png -c:v libx264 -t 15 -pix_fmt yuv420p -vf scale=1080:1440 out.mp4
```

4、多张图片转视频

```
ffmpeg -f image2 -i %d.png -vcodec libx264 output2.mp4
```

其中 %d.png 表示 1.png 2.png ...

此方法需要先将图片重命名。

5、截图

```
ffmpeg -y -i input.mp4 -ss 00:00:00 -t 00:00:01 output_%3d.jpg
```

6、转变分辨率

```
ffmpeg -i input.mp4 -vf scale=480:-1 output.mp4
```

将 input.mp4 转换为 480p。

### 总结

今天给大家分享了一些 FFmpeg 的简单实例，希望对你有所帮助，小伙伴们在使用 FFmpeg 的过程中还有哪些实用的操作也可以一起分享一下哦～