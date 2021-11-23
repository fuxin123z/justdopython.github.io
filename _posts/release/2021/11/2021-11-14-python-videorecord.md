---
layout: post
title: 用Python来做一个屏幕录制工具
category: python
tagline: by 闲欢
tags: 
  - python
  - 录屏
---


![封面](http://www.justdopython.com/assets/images/2021/11/videorecord/0.jpg)


女朋友是一个软件测试人员，在工作中经常会遇到需要录屏记录自己操作，方便后续开发同学定位。因为录屏软件动不动就开始收费，所以她经常更换录屏软件。闲暇之余，我就觉得手痒，感觉可以用万能的 Python 来解决她的烦恼。

![](http://www.justdopython.com/assets/images/2021/11/videorecord/1.gif)


<!--more-->

#### 思路

我上网搜寻了一下相关知识，录制视频基本上都用的图像处理库 PIL 的 ImageGrab 模块。这个模块可以用于将当前屏幕的内容或者剪贴板上的内容拷贝到 PIL 图像内存。

既然这个模块可以获取当前屏幕上的内容，那么我一直不间断地获取，然后把这些获取的内容拼起来，那不就是视频了吗？


#### 实现

##### 录制

整体思路是 PIL 模块中的 ImageGrab 不停的获得当前屏幕，利用 opencv 写入视频流。

```python
def video_record(sttime):
    global name
    # 当前的时间（当文件名）
    name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 获取当前屏幕
    screen = ImageGrab.grab()
    # 获取当前屏幕的大小
    width, high = screen.size
    # MPEG-4编码,文件后缀可为.avi .asf .mov等
    fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D')
    # （文件名，编码器，帧率，视频宽高）
    video = VideoWriter('%s.avi' % name, fourcc, 15, (width, high))
    print(str(sttime) + '秒后开始录制----')
    time.sleep(int(sttime))
    print('开始录制!')
    global start_time
    start_time = time.time()
    while True:
        if flag:
            print("录制结束！")
            global final_time
            final_time = time.time()
            # 释放
            video.release()
            break
        # 图片为RGB模式
        im = ImageGrab.grab()
        # 转为opencv的BGR模式
        imm = cvtColor(np.array(im), COLOR_RGB2BGR)
        # 写入
        video.write(imm)

```

录制视频的主要代码只需几行即可，但是我们需要对录制操作进行控制，例如开始录制、结束录制等。以及获取屏幕内容之后，需要对内容进行转码，然后写入视频流。

##### 监听键盘事件

录制视频我们是使用的一个 while 循环来获取屏幕信息，开始之后会一直进行。但是我们需要监听键盘事件，来终止这个循环，从而终止录制视频。这个监听事件就显得很重要了，这里采用的是 pynput 这个强大的三方库，可以全局监听键盘、鼠标事件。

我们设定的是用户在按下键盘的 ESC 按键后，终止 while 循环，从而终止视频录制。

```python
# 监听按键
def on_press(key):
    global flag
    if key == keyboard.Key.esc:
        flag = True
        # 返回False，键盘监听结束！
        return False

```

##### 主体控制

因为我们需要不断地获取屏幕内容，所以我们最好启动一个线程来干这个事情。

```python
th = threading.Thread(target=video_record, args=sstime)
    th.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

```

##### 视频信息

录制视频结束之后，我们也可以获取视频的一些相关信息，例如时长、帧率、分辨率等。

```python
# 视频信息
def video_info():
    # 记得文件名加格式不要错！
    video = VideoCapture('%s.avi' % name)
    fps = video.get(CAP_PROP_FPS)
    count = video.get(CAP_PROP_FRAME_COUNT)
    size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
    print('帧率=%.1f' % fps)
    print('帧数=%.1f' % count)
    print('分辨率', size)
    print('视频时间=%.3f秒' % (int(count) / fps))
    print('录制时间=%.3f秒' % (final_time - start_time))
    print('推荐帧率=%.2f' % (fps * ((int(count) / fps) / (final_time - start_time))))
```

##### 效果

最后，我启两个程序，第一个程序启动录制之后，我再来操作第二个程序，这样大家就可以看到这个程序的运行过程：

![](http://www.justdopython.com/assets/images/2021/11/videorecord/2.avi)


#### 总结

这里的程序只是一个初版，刚刚实现了录制屏幕的想法。后续还需要对其进行改进，支持 GUI 界面操作，支持框选特定区域录制等等。


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/videorecord)