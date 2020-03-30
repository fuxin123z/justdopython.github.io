---
layout: post
category: python
title: 用 Python 画哆啦 a 梦
tagline: by 豆豆
tags: 
  - python100
---

相信大家童年都看过哆啦 A 梦，他的口袋简直是无所不能，里面装满了各种神奇的道具。曾经的我也幻想如果自己也有一个这样的口袋多好。今天我们就用 Python 来画一个哆啦A梦，怀念下我们的童年。

<!--more-->

先来看看我们最终实现的效果图。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/001.png)

## 头部轮廓和围巾

首先，我们先画下多啦 A 梦头部外轮廓，头部轮廓主要是一个多半圆，围巾就是一个小的长方形。

```python
# 头部
def head():
    t.up()
    t.circle(150, 45)
    t.down()
    t.fillcolor(head_color)
    t.begin_fill()
    t.circle(150, 270)
    t.end_fill()


# 围巾
def scarf():
    t.fillcolor(scarf_color)
    t.begin_fill()
    t.seth(0)
    t.fd(216)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.fd(220)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.end_fill()
```

来看下效果如何，呃呃呃，怎么感觉有点像大马路上的石墩儿呢，除了颜色有点像之外。

不急不急，我们再画一下脸部细节。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/002.png)

## 脸部

### 眼睛

俗话说眼睛是心灵的窗户，我们先把眼睛画上。

```python
def face():
    t.fd(186)
    t.lt(45)
    t.fillcolor(color_white)
    t.begin_fill()
    t.circle(120, 100)
    t.seth(180)
    t.fd(120)
    t.seth(215)
    t.circle(120, 100)
    t.end_fill()

def draw_eyes():
    t.fillcolor(color_white)
    t.begin_fill()
    a = 2.5
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a -= 0.05
        else:
            a += 0.05
        t.lt(3)
        t.fd(a)
    t.end_fill()

def eyes():
    go_to(0, 227)
    t.seth(90)
    draw_eyes()
    go_to(0, 227)
    t.seth(270)
    draw_eyes()
```

画眼睛不能直接画一个正圆，那样看起来会比较奇怪，要画一个椭圆才行，来看下效果。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/003.png)

眼睛画上去之后明显感觉精神多了，也有点多啦 A 梦的模样了。可是看起来还是有点不太对，是的，眼睛还没有画瞳孔。

简单起见，直接补两个黑色的圆圈圈即可。

```python
def fill_eyes():
    # 填充眼睛
    go_to(-15, 220)
    t.pensize(12)
    t.color('black')
    for i in range(30):
        t.forward(2)
        t.right(12)
    go_to(15, 220)
    for i in range(30):
        t.forward(2)
        t.left(12)
    t.pensize(1)
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/004.png)

不错不错，越来越有样了。下面我们把鼻子和嘴巴加上。

### 鼻子 & 嘴巴

鼻子也不难，在眼睛下面画个小圈圈就行，嘴巴就类似一个到倒 T 字。

```python
# 鼻子
def nose():
    go_to(-13, 166)
    t.seth(315)
    t.fillcolor(nose_color)
    t.begin_fill()
    t.circle(20)
    t.end_fill()


# 嘴巴
def mouth():
    go_to(0, 156)
    t.seth(270)
    t.fd(100)
    pos = t.pos()
    t.seth(0)
    t.circle(110, 60)
    go_to(pos[0], pos[1])
    t.seth(180)
    t.circle(-110, 60)
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/005.png)

离成功就剩下最后一步了，把胡须和铃铛画上就大功告成了。

### 胡须 & 铃铛

胡须就类似画猫的胡须就好，铃铛表复杂些，大圆套小圆，还有装饰。

```python
# 胡须
def mustache():
    h = 70
    go_to(30, 140)
    t.seth(15)
    t.fd(h)

    go_to(30, 130)
    t.seth(0)
    t.fd(h)

    go_to(30, 120)
    t.seth(-15)
    t.fd(h)

    go_to(-30, 140)
    t.seth(150)
    t.fd(h)

    go_to(-30, 130)
    t.seth(180)
    t.fd(h)

    go_to(-30, 120)
    t.seth(195)
    t.fd(h)

# 铃铛
def bell():
    # 大圆
    go_to(0, 33)
    t.pensize(1)
    t.fillcolor("#FCE341")
    t.begin_fill()
    t.circle(25)
    t.end_fill()

    # 横条纹
    go_to(-15, 22)
    t.seth(0)
    t.forward(42)
    go_to(-18, 17)
    t.seth(0)
    t.forward(47)

    # 小圆
    go_to(5, 0)
    t.pensize(1)
    t.color("black", '#79675D')
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    t.seth(270)
    t.pensize(1)
    t.forward(15)
```

最后我们写一个入口函数，将这些画身体不同部位的函数给封装起来。代码如下；

```python
if __name__ == '__main__':
    head()
    scarf()
    face()
    eyes()
    fill_eyes()
    nose()
    mouth()
    mustache()
    bell()
    go_to()
    t.hideturtle()
    t.done()
```

最终效果如下：

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/03/2020-03-20-duo-la-a-meng/001.png)

是不是觉得很简单，块去后台获取源码 run 起来吧。有兴趣的读者还可以把身体给加上去。

## 总结

本文我们使用 Python 的 turtle 库画了一下哆啦 A 梦，不知道和大家记忆中的哆啦 A 梦是否一样呢。

其实 turtle 使用不难，主要是要理清乌龟的位置以及朝向，然后就是其运动模式，直线运动，还是曲线运动以及怎调换运动方向。其中乌龟的坐标计算比较麻烦，尤其是做曲线运动的时候，大家可以结合 pos() 函数来获取查看乌龟的坐标，有助于你理清画图思路。

大家多加练习，肯定都可以画出自己想画的，有趣且好玩的图像。

## 代码地址

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/doudou/2020-03-27-duo-la-a-meng