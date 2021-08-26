---
layout: post
category: python
title: 无损提取视频中的小姐姐图片
tagline: by 某某白米饭
tags:
  - python
---

人类都是视觉动物，不管是男生还是女生看到漂亮的小姐姐、小哥哥甚至是马赛克视频，就想截图保存下来。可是截图会对画质会产生损耗，截取的画面不规整，像素不高等问题。
<!--more-->
![](http://www.justdopython.com/assets/images/2021/08/lsp/0.png)

用 Python 写一个逐帧无损保存视频画面的小脚本大致可以分为三个步骤：

1. 在 cmd 中使用 you-get 下载视频
2. OpenCV 读取并处理视频
3. 将视频画面保存为图片

### 安装模块

1. you-get 模块用于下载视频，它需要 ffmpeg 模块配合使用。

```python
pip3 install you-get
```

2. windows 的 ffmpeg 的下载地址是 [https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z]，解压后将 bin 文件加入环境变量。

![](http://www.justdopython.com/assets/images/2021/08/lsp/1.png)

3. python-OpenCV 模块用来读取视频帧，并保存成图片。

```python
pip3 install opencv-python
```

### you-get

you-get 是一个开源的视频下载软件，支持 80+ 网站视频的下载。只需要一行代码就可以了。

在 cmd 中运行下面的命令下载视频：

```python
you-get -o 下载后保存文件的目录 视频的 url 地址
```

![](http://www.justdopython.com/assets/images/2021/08/lsp/2.png)

如果报 **'you-get' 不是内部或外部命令，也不是可运行的程序** 问题，可以运行 

```python
pip show you-get
```

将 Location 的值的 site-packages 改成 Scripts 加入到环境变量，如：c:\users\xxx\appdata\roaming\python\python39\site-packages 改成c:\users\xxx\appdata\roaming\python\python39\Scripts。

### OpenCV
 
磨刀不误砍柴工， 在开发之前先来认识一下 OpenCV。它的全称是 Open Source Computer Vision Library，是一个可以跨平台的计算机视觉库 ，OpenCV-Python 是 OpenCV 的 Python API。它集合了 C++ 和 Python 的最优特征，用于支持 Python 解决计算机视觉的问题。OpenCV 可以用于人机互动、图像分割、人脸识别等等领域。

![](http://www.justdopython.com/assets/images/2021/08/lsp/3.png)

在处理视频按帧保存图片的时候需要用到以下几个函数：

1. `cap = cv2.VideoCapture("视频地址")`：参数是视频的地址表示读取一个视频文件。
2. `cap = cv2.VideoCapture(0)`：参数是 0 表示打开电脑上的摄像头。
3. `cap.isOpened()`：返回 true 和 false 表示是否成功。
4. `success, frame = cap.read()`: 这个函数就是 OpenCV 读取视频的下一帧，第一个返回值表示是否读取成功，第二个返回值就是返回读取到的视频帧。 
5. `cv2.imencode()`：将上面的视频帧按照图片编码后缓存到内存中，调用 `tofile()` 函数保存成文件。 

话不多说，用上面的函数写一个截取视频画面的 Python 程序.

```python
import cv2
import os

image_base_path = "D:\\video\\images\\";

def get_images(video_path):
    frame_times = -1;
    fileName = video_path.split("\\")[-1:][0].split('.')[0]
    image_out_path = image_base_path + fileName
    if not os.path.exists(image_out_path):
        os.makedirs(image_out_path) 

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        frame_times = frame_times + 1
        success, frame = cap.read()
        if not success:
            break;

        cv2.imencode('.jpg', frame)[1].tofile(image_out_path + "\\" + str(frame_times) + ".jpg")

if __name__ == '__main__':
    get_images('D:\\vedio\\只予你的晴天【三杞】.mp4')
```

![](http://www.justdopython.com/assets/images/2021/08/lsp/4.png)

### 总结

本文简单的介绍了you-get 的使用和如何使用 OpenCV 读取视频并保存图片。大家喜欢的话就多多点赞支持一下。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/lsp>
