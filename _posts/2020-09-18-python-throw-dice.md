---
layout: post
category: python
title: 做硬核老爸，我用 Python
tagline: by 太阳雪
tags:
  - python
  - pygame
---
前几天，给儿子买了个飞行棋，甚是喜欢，每天都要和我来两盘，昨天准备大战一场时，发现骰子弄丢了，没有骰子就没法玩了，正想要用橡皮做一个，突然想到了个更好的办法，经过一顿折腾，终于搞定了，结果……
<!--more-->

## 构思

骰子是个立方体，有六个面，每个面上，标有不同地点，从 1 个 到 6 个，代表 1 到 6 六个数字，玩的时候，将骰子一掷，等它停下，朝上的面是几点，就表示摇到了几。

不同的游戏中，对摇到的点数有不同的玩法，例如飞行棋中，摇到 5 或者 6，可以起飞一架飞机

![飞行棋](http://justdopython.com/assets/images/2020/09/dice/01.jpg)

现在我需要用程序来模拟这个过程，实际上就是产生 1 到 6 直接的随机数，直接用 `random.randint(1, 6)` 就可以搞定，不过我不想就这样简单完成，一是对于小孩子来说，直接给出数字不够直观，二是，能有机会给儿子炫技一把，何乐不为？

于是构思如下：

- 找一些骰子的素材，需要有每个数字向上的图片
- 为了制造骰子的转动效果，还需要一些处于转动中间状态的图片
- 随机产生 0 到 5 之间的数字，0 代表点数 1，1 代表点数 2，依次类推，5 代表点数 6，为什么不直接生成 1 到 6 呢？后面有解答
- 掷骰子过程有两种状态，即 显示点数 和 转动，那么就需要有触发机制，考虑到小孩子对鼠标操作不灵活，选用空格键来控制，按一下就相当于掷一次

## 实现

构思好后，赶紧实现

### 素材

先从网上找了些骰子的素材，最终选择了以微信掷骰子表情图为元素的一系列 gif 图片，通过图片解析工具，从 gif 图片中提取出每个帧，其中包括了点数朝上的图片，和转动中间的图片，这样图片素材就搞定了

> 实践时如果不方便获得图片素材，可从本文示例代码中获得

接下来，就是编程部分了，之前在 [模拟疫情扩散的示例](https://mp.weixin.qq.com/s/BJ0GdZ5ipGNCIAaDh0C01A) 中，用到过 **pygame** python 游戏引擎库，这次还用它

### 骰子

首先，写一个 骰子类，用来定义骰子的各种资源，以及管理骰子的状态，代码如下：

```python
import random
import pygame

class Dice:
    def __init__(self):
        self.diceRect = pygame.Rect(200, 225, 100, 100)
        self.diceSpin = [
            pygame.image.load("asset/rolling/4.png"),
            pygame.image.load("asset/rolling/3.png"),
            pygame.image.load("asset/rolling/2.png"),
            pygame.image.load("asset/rolling/1.png")
        ]
        self.diceStop = [
            pygame.image.load("asset/dice/1.png"),
            pygame.image.load("asset/dice/2.png"),
            pygame.image.load("asset/dice/3.png"),
            pygame.image.load("asset/dice/4.png"),
            pygame.image.load("asset/dice/5.png"),
            pygame.image.load("asset/dice/6.png")
        ]

        self.StopStatus = random.randint(0, 5)
        self.SpinStatus = 0

    def move(self):
        self.SpinStatus += 1
        if self.SpinStatus == len(self.diceSpin):
            self.SpinStatus = 0
```

- 初始化方法中，用 `pygame.Rect` 方法设定了一个矩形区域，即游戏窗口坐标为(200, 225)，高度和宽度都为 100，这个矩形区域是为了在游戏窗口中绘制骰子用的
- diceSpin 存储了骰子转动过程中的图片素材，注意需要用 `pygame.image.load` 方法加载图片资源
- diceStop 存储了骰子点数的图片素材
- StopStatus 记录骰子停止状态的点数值，在 0 ~ 5 之间，初始化为一个随机数
- SpinStatus 记录转动过程中当前帧的图片索引，默认为 0
- move 方法相当于一个转动控制器，每调用一次会改变一次转动中图片的索引，骰子转动过程中会反复被调用

### 引擎

接下来，编写一个游戏引擎类，用于驱动游戏过程，代码如下：

```python
import random
import sys
import pygame

class Game:
    def __init__(self, width=500, height=600):
        pygame.init()
        size = width, height
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

        self.rollTimes = 0  # 掷骰子过程的帧数记录
        self.Dice = Dice()
        self.start = False  # 状态标识
        self.rollCount = random.randint(3, 10)  # 初始投掷帧数

    def roll(self):
        self.screen.blit(self.Dice.diceSpin[self.Dice.SpinStatus], self.Dice.diceRect)
        self.Dice.move()
        self.rollTimes += 1
        if self.rollTimes > self.rollCount:
            self.start = False
            self.rollCount = random.randint(3, 10)
            self.Dice.StopStatus = random.randint(0, 5)
            self.rollTimes = 0

    def stop(self):
        self.screen.blit(self.Dice.diceStop[self.Dice.StopStatus], self.Dice.diceRect)

    def run(self):
        while True:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if ((event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE) \
                or event.type == pygame.MOUSEBUTTONDOWN) \
                and self.start == False:
                    self.start = True

            if self.start:
                self.roll()
            else:
                self.stop()
            pygame.display.update()
```

- 初始化方法中，做了游戏窗口的初始化，并设定了窗口大小，然后对过程中的控制类变量做了初始化
- roll 方法为抛掷，抛掷过程中会被反复调用，先设置一个转动中图片，然后，调用骰子的 `move` 方法，得到一个新的转动状态
- roll 方法中，接下来是一个控制器，如果达到了设定的转动次数，就停止，并得到随机的点数
- stop 方法，在停止转动时调用，将转动停止时的点数图片绘制到窗口上，这里 `StopStatus` 范围是 0 ~ 5，刚好对应 `diceStop` 列表的索引，这就是随机数范围是 0~5 的原因
- run 方法是引擎的启动入口，它启动了一个事件循环
- 循环中，检查一遍事件记录，如果接收到了退出事件，则结束循环
- 如果接收到了按下空格键或者鼠标键，且投掷状态为停止时，将投掷状态设置为开始
- 检查完事件记录，判断投掷状态，如果是开始状态，调用 `roll` 方法，否则调用 `stop` 方法
- 最后每次循环都需要调用 `pygame.display.update()` 刷新一次窗口

这里需要说明下 `clock.tick`，它的作用是让循环每秒执行多少次，抽象来说可以理解为动画的帧，即每秒多少帧。

相对于 `clock.tick`，我们更熟悉 `time.sleep`，后者表示等待多久再执行，那么 `clock.tick(10)` 的效果就相当于 `time.sleep(0.1)`，即每秒执行 10 次，就等于每次等待十分之一秒

### 运行

```python
if __name__ == '__main__':
    Game().run()
```

> 注意： 将目录切换到代码目录下运行，否则可能提示找不到图片文件

运行效果如下，像那么回事吧

![掷骰子效果](http://justdopython.com/assets/images/2020/09/dice/01.gif)

折腾完后，我迫不及待地去儿子跟前炫耀，结果，他已经睡着了，身旁散落着一些飞行棋子儿……

## 总结

无论在生活或者工作中，编程技能越来越重要了，编程已然成为了思考和创造的工具了，习得一项编程技能，不仅能帮助自己，也许可以省一笔少儿编程的花费，在提高孩子逻辑思维能力的同时，还能增进与孩子的感情，不得不说，当儿子使用我编写的骰子玩飞行棋时，更开心了

做硬核家长，我用 Python

## 参考

- <https://www.mscto.com/smartprogram/299581.html>
- <https://baike.baidu.com/item/%E9%AA%B0%E5%AD%90/1823190>
- <https://www.yiibai.com/python/time_sleep.html>

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/dice>
