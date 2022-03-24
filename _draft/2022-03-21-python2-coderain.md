---
layout: post
title: 用 Python 实现炫酷黑客帝国特效！
category: python
tagline: by 闲欢
tags: 
  - python
  - pygame
---


![封面](http://www.justdopython.com/assets/images/2022/03/coderain/0.jpg)

时隔18年，还以为经典的《黑客帝国》已经完结了，没想到又拍了三部曲的续作—第四部《黑客帝国：矩阵重启》！

看《黑客帝国》，大家可能比较有印象的是好像每部影片都有代码雨效果：

![](http://www.justdopython.com/assets/images/2022/03/coderain/1.jpg)

今天就用 Python 来实现这部经典影片中的代码雨，来致敬《黑客帝国》！

<!--more-->


### 实现思路

其实原理很简单，就是我们按一定的时间间隔，对屏幕中的文字进行重绘即可。重点就是如何对文字定位。

所谓定位，在坐标轴上，我们可以用横纵坐标来定位一个点。那么在一个平面上，原理是类似的，我们用行和列来定位雨点。

代码雨的效果其实就是不断地计算行和列，来定位雨点，然后定时刷新屏幕就可以。

### 实现代码

基于以上思路，我们通过 pygame 来实现这个效果：

```python
import random
import pygame

FONT_PX = 15
pygame.init()
winSur = pygame.display.set_mode((640, 480))
font = pygame.font.SysFont("fangsong", 20)
bg_suface = pygame.Surface((640, 480), flags=pygame.SRCALPHA)
pygame.Surface.convert(bg_suface)
bg_suface.fill(pygame.Color(0, 0, 0, 13))
winSur.fill((0, 0, 0))

# 相关参数
texts = [font.render(str(i), True, (0, 255, 0)) for i in range(10)]
colums = int(640 / FONT_PX)
drops = [0 for i in range(colums)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.time.delay(33)
    winSur.blit(bg_suface, (0, 0))

    for i in range(len(drops)):
        text = random.choice(texts)
        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))
        drops[i] += 1
        if drops[i] * 10 > 480 or random.random() > 0.95:
            drops[i] = 0

    pygame.display.flip()

```

运行这个程序，效果如下：


![](http://www.justdopython.com/assets/images/2022/03/coderain/2.gif)

这里实现的随机数字，你也可以将数字换成字母、文字或者其他字符。

### 总结

实现原理很简单，代码也不多，感兴趣的可以尝试将数字换成其他字符，或者横向下雨试试！

