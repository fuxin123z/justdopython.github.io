---
layout: post
title: 用 Python 写摸鱼监控进程，用这个！
category: python
tagline: by 闲欢
tags: 
  - python
  - 监控
  - 摸鱼
---


![封面](http://www.justdopython.com/assets/images/2022/02/monitor/0.jpg)


继打游戏、看视频等摸鱼行为被监控后，现在打工人离职的倾向也会被监控。  

有网友爆料称知乎正在低调裁员，视频相关部门几乎要裁掉一半。而在知乎裁员的讨论区，有网友表示企业安装了行为感知系统，该系统可以提前获知员工跳槽念头。 

而知乎在否认了裁员计划的同时，也声明从未安装使用过网上所说的行为感知系统，今后也不会启用类似软件工具。 

因为此事，深信服被推上风口浪尖，舆论关注度越来越高。

一时间，“打工人太难了”“毫无隐私可言”的讨论层出不穷。

今天就带大家领略一下怎么写几行 Python 代码，就能监控电脑。

<!--more-->

### 监控键盘

如果公司偷偷在我们的电脑上运行了一个后台进程，来监控我们的键盘事件，最简单的 python 写法大致是这样的：

```python
from pynput import keyboard

def on_press(key):
    print(f'{key} :pushed')


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as lsn:
    lsn.join()

```

随意敲击键盘，你就会从控制台看到这样的输出：

![](http://www.justdopython.com/assets/images/2022/02/monitor/1.png)

代码内容就是两个方法，一个是监听按键事件，另一个是监听退出事件——敲击 `ESC` 按键后释放就退出了。


### 监控鼠标

如果还要监听鼠标事件，那么上这段代码就行了：

```python
from pynput import mouse

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('left was pressed!')
    elif button == mouse.Button.right:
        print('right was pressed!')
        return False
    else:
        print('mid was pressed!')


# 定义鼠标监听线程
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

```

这段代码主要是监听鼠标的左右键点击操作，运行之后操作鼠标，就可以看到控制台打印如下结果：

![](http://www.justdopython.com/assets/images/2022/02/monitor/2.png)

细心的你一定会发现，每次点击事件，都打印了两次。这是因为按下和松开都会触发鼠标事件。


### 记录监控日志

键盘事件和鼠标事件都有了，是时候将二者结合起来，把用户的操作记录到日志了。这里我们用 loguru 来记录日志，这个 python 模块我们之前的文章也讲过。

整个代码如下：

```python
from pynput import keyboard, mouse
from loguru import logger
from threading import Thread

# 定义日志文件
logger.add('moyu.log')


def on_press(key):
    logger.debug(f'{key} :pushed')


def on_release(key):
    if key == keyboard.Key.esc:
        return False


# 定义键盘监听线程
def press_thread():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as lsn:
        lsn.join()


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        logger.debug('left was pressed!')
    elif button == mouse.Button.right:
        logger.debug('right was pressed!')
    else:
        return False


# 定义鼠标监听线程
def click_thread():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == '__main__':
    # 起两个线程分别监控键盘和鼠标
    t1 = Thread(target=press_thread())
    t2 = Thread(target=click_thread())
    t1.start()
    t2.start()

```

运行之后，你就可以在同级目录下的日志文件中，看到这样的内容了：

![](http://www.justdopython.com/assets/images/2022/02/monitor/3.png)


### 总结

本文主要通过 `pynput` 这个 python 模块讲解一下怎么记录键盘和鼠标的操作。这几行简单的代码对于监控输入密码之类的简单操作可以使用，但是对于聊天记录之类的复杂语句，你还需要针对日志用 NLTK 语言处理，才能复原你的聊天记录。

学会了这个，你最想做的事情是什么？欢迎评论区留言！













