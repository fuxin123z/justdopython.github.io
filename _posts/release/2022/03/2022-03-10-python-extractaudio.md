---
layout: post
title: 几行代码迅速提取音频，YYDS！
category: python
tagline: by 闲欢
tags: 
  - python
  - 音频提取
---


![封面](http://www.justdopython.com/assets/images/2022/03/extractaudio/0.png)

前几天，有个小妹妹问我：哪里可以找到 BBC 英语的音频？

她只有视频文件，但是她想在路上听音频学英语。

我当时就去网盘资源里面搜索，废了好大功夫才找到她要的资源。

今天，突发奇想：为什么不用程序将视频中的音频给提取出来呢？

于是，查阅了相关资料，发现其实这事用 Python 实现非常简单，几行代码，眨眼功夫就可以搞定！

<!--more-->

### FFmpeg 简介

FFmpeg 是一个自由软件，可以运行音频和视频多种格式的录影、转换、流功能，包含了 libavcodec ——这是一个用于多个项目中音频和视频的解码器库，以及 libavformat ——一个音频与视频格式转换库。

在 Python 中，有一个库跟 FFmpeg 对应，叫 `ffmpy`，利用这个库，我们就可以很轻松地从视频中提取音频了。

安装这个库的方式也很简单：

> pip install ffmpy -i https://pypi.douban.com/simple


### 代码实现

我们只需要传入三个参数——视频地址、音频结果存放地址和音频的格式后缀，就可以调用 FFmpeg 提取音频了。

```python
def run_ffmpeg(video_path: str, audio_path: str, format: str):
    ff = FFmpeg(inputs={video_path: None},
                outputs={audio_path: '-f {} -vn'.format(format)})
    ff.run()
    return audio_path

```

然后，再写个接收参数的函数：

```python
def extract(video_path: str, tmp_dir: str, ext: str):
    file_name = '.'.join(os.path.basename(video_path).split('.')[0:-1])
    return run_ffmpeg(video_path, os.path.join(tmp_dir, '{}.{}'.format(uuid.uuid4(), ext)), ext)

```

最后，我们来测试一下：

```python
if __name__ == '__main__':
    print(extract('C:/个人/video/test/bbc.mp4', 'C:/个人/video/test', 'wav'))

```

运行这个代码，就会在你的视频目录生成一个文件名为 uuid 的 wav 格式音频文件。

你也可以选择输出 mp3 格式的音频。

其实，这个提取过程就等价于在命令行敲了一行命令：

```python
 ffmpeg -i C:/个人/video/test/bbc.mp4 -f wav -vn C:/个人/video/test\77350be1-b2ae-4fc8-af80-da4eda463fa9.wav
```

### 总结

整个音频提取过程的核心代码其实就几行，最终执行的是一个命令行的命令，可以说是相当简单了。这段代码可以作为一个工具类收藏着，需要用的时候可以迅速拿出来使用。今天的技能你学会了吗？
