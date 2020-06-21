---
layout: post
title: 用 Python 画动态时钟
category: python
tagline: by 闲欢
tags: 
  - python
---

![封面](http://www.justdopython.com/assets/images/2020/06/drawclock/fm.jpg)

时钟是我们日常生活中最常见的也是必不可少的东西，你有没有想过用 Python 来画一个实时动态的时钟呢？下面我们来看看如何使用简单的代码实现一个动态时钟吧！
<!--more-->


## 海龟绘图介绍

Turtle 库是 Python 语言中一个很流行的绘制图像的函数库，虽然不知道为什么叫海龟这么奇怪的名字，但是可以根据这个名字联想到我们在操控一直海龟在 x 和 y 轴的二元坐标系上爬行，爬过的轨迹就是我们绘制的线条。从这个角度看，作者也是一个很有意思的人。

操纵海龟绘图有着许多的命令，这些命令可以划分为三种：一种为运动命令，一种为画笔控制命令，还有一种是全局控制命令。

### 画笔运动命令

![画笔运动命令](http://www.justdopython.com/assets/images/2020/06/drawclock/moveorder.jpg)

### 画笔控制命令

![画笔控制命令](http://www.justdopython.com/assets/images/2020/06/drawclock/ctrorder.jpg)

### 全局控制命令

![全局控制命令](http://www.justdopython.com/assets/images/2020/06/drawclock/globalorder.jpg)

### 其他命令

![其他命令](http://www.justdopython.com/assets/images/2020/06/drawclock/otherorder.jpg)


## 整体思路

了解了海龟绘图的命令后，我们下面来整理一下我们的绘图思路。

我们知道，一个时钟是由表盘和时针组成。

表盘是由刻度组成，一共有60个刻度，对应着一个圆的60个点，每隔4个刻度都会有一个刻度是条短线，每逢5的倍数刻度都会标有小时数（1-12）。

指针有三根，分别为秒针、分针和时针，三根指针长度由短及长。秒针走一圈，分针走一个刻度，分针走一圈，时针走一个刻度。

另外，我们还可以在表盘中显示星期和日期。

这样，我们这个时钟的元素就清晰了，包括表盘（60个刻度以及小时数）、指针（三根）、星期和日期。

## 代码实现

### 代码

确定了思路之后，我们开始运用海龟绘图的命令来绘制图像。整体代码如下：

```python
import turtle
from datetime import *

# 抬起画笔，向前运动一段距离放下
def skip(step):
    turtle.penup()
    turtle.forward(step)
    turtle.pendown()

def mkHand(name, length):
    # 注册Turtle形状，建立表针Turtle
    turtle.reset()
    # 先反向运动一段距离，终点作为绘制指针的起点
    skip(-length * 0.1)
    # 开始记录多边形的顶点。当前的乌龟位置是多边形的第一个顶点。
    turtle.begin_poly()
    turtle.forward(length * 1.1)
    # 停止记录多边形的顶点。当前的乌龟位置是多边形的最后一个顶点。将与第一个顶点相连。
    turtle.end_poly()
    # 返回最后记录的多边形。
    handForm = turtle.get_poly()
    turtle.register_shape(name, handForm)

def init():
    global secHand, minHand, houHand, printer
    # 重置Turtle指向北
    turtle.mode("logo")
    # 建立三个表针Turtle并初始化
    mkHand("secHand", 135)
    mkHand("minHand", 125)
    mkHand("houHand", 90)
    secHand = turtle.Turtle()
    secHand.shape("secHand")
    minHand = turtle.Turtle()
    minHand.shape("minHand")
    houHand = turtle.Turtle()
    houHand.shape("houHand")

    for hand in secHand, minHand, houHand:
        hand.shapesize(1, 1, 3)
        hand.speed(0)

    # 建立输出文字Turtle
    printer = turtle.Turtle()
    # 隐藏画笔的turtle形状
    printer.hideturtle()
    printer.penup()

# 绘制表盘
def setupClock(radius):
    # 建立表的外框
    turtle.reset()
    turtle.pensize(7)
    for i in range(60):
        # 向前移动半径值
        skip(radius)
        if i % 5 == 0:
            # 画长刻度线
            turtle.forward(20)
            # 回到中心点
            skip(-radius - 20)

            # 移动到刻度线终点
            skip(radius + 20)
            # 下面是写表盘刻度值,为了不与划线重叠，所以对于特殊位置做了处理
            if i == 0:
                turtle.write(int(12), align="center", font=("Courier", 14, "bold"))
            elif i == 30:
                skip(25)
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
                skip(-25)
            elif (i == 25 or i == 35):
                skip(20)
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
                skip(-20)
            else:
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
            
            # 回到中心点
            skip(-radius - 20)
        else:
            # 画圆点
            turtle.dot(5)
            skip(-radius)
        # 顺时针移动6°
        turtle.right(6)

def week(t):
    week = ["星期一", "星期二", "星期三",
            "星期四", "星期五", "星期六", "星期日"]
    return week[t.weekday()]

def date(t):
    y = t.year
    m = t.month
    d = t.day
    return "%s %d%d" % (y, m, d)

def tick():
    # 绘制表针的动态显示
    t = datetime.today()
    second = t.second + t.microsecond * 0.000001
    minute = t.minute + second / 60.0
    hour = t.hour + minute / 60.0
    secHand.setheading(6 * second)
    minHand.setheading(6 * minute)
    houHand.setheading(30 * hour)

    turtle.tracer(False)
    printer.forward(65)
    printer.write(week(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.back(130)
    printer.write(date(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.home()
    turtle.tracer(True)

    # 100ms后继续调用tick
    turtle.ontimer(tick, 100)

def main():
    # 打开/关闭龟动画，并为更新图纸设置延迟。
    turtle.tracer(False)
    init()
    setupClock(160)
    turtle.tracer(True)
    tick()
    turtle.mainloop()

if __name__ == "__main__":
    main()
```

### 代码讲解

这里我们讲解一下代码里面的几个方法。

- skip() 方法是一个公用方法，用于抬起画笔，向前移动一段距离，然后放下画笔。

- mkHand() 方法是画指针的方法，思路是从表盘的中心点出发，先反向运动一段距离，终点作为绘制指针的起点，然后再向中心点画线作为指针。

- setupClock() 方法是绘制表盘，绘制表盘主要注意每到第5个刻度需要绘制短线以及标注小时数。

- tick() 方法是实现我们动态时钟的关键方法，它在初始化时钟的基础上，一方面是显示表盘中的星期和日期信息，另一方面通过定时刷新指针位置来达到实时显示的效果。

- init() 方法是初始化时钟信息，包括指针和表盘上的星期、日期信息。

最后，我们在 main() 方法中调用了 Tkinter 的 mainloop 函数来启动事件循环，它必须是乌龟图形程序中的最后一个语句。


## 运行结果

![动态时钟](http://www.justdopython.com/assets/images/2020/06/drawclock/clock.jpg)

直接运行程序，你会看到一个弹出窗口，上面就是我们绘制的动态时钟了，指针是在走动的哦！



## 总结

本文通过使用海龟绘图实现了一个动态刷新的时钟，代码本身并不复杂，重要的是实现的思路。如果你觉得有意思，赶紧点在看分享给身边的小伙伴吧！


> 示例代码 (https://github.com/JustDoPython/python-examples/tree/master/xianhuan/drawclock)

