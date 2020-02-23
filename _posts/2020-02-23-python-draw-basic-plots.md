---
layout: post
category: Python
title:  趣玩Python之绘制基本图形
tagline: by 萌较瘦
tags: 
  - LeetCode面试题系列
---

Python中的类库极其丰富，数据科学中经常会用到可视化技术。今天我们来一起学习一下Python中基本图形的绘制方法，本文我们将主要基于`turtle`(小乌龟)库来画图~

<!--more-->

为了方便后面进行**交互性演示**，这里我建议大家安装好`Anaconda`，传送门是 https://www.anaconda.com/distribution/>，请根据自己电脑的操作系统(Windows/Mac/Linux)自行下载和安装，记得要选 `Python3.7`的版本，因为Python 2.7官方不打算维护了。

![Anaconda-download](http://www.justdopython.com/assets/images/2020/python/Anaconda-download.png)

后面我们需要用到其中的一个强大工具箱 `jupyter notebook`。

![jupyter-notebook](http://www.justdopython.com/assets/images/2020/python/jupyter-notebook.jpg)



Anaconda安装完毕之后呢，接下来，在电脑的命令行(终端)中输入如下命令:

`jupyter notebook`来启动`notebook`，这时会打开浏览器，进入网址<http://localhost:8888/tree>，其界面如下~

![notebook-home](http://www.justdopython.com/assets/images/2020/python/notebook-home.png)



接下来，我们需要创建一个`notebook`文件，按下图操作，点`Files` -> `New` -> `Python 3`即可。

![create-python-notebook](http://www.justdopython.com/assets/images/2020/python/create-python-notebook.png)



创建好之后，可以按下图对`notebook`文件重命名:

![rename](http://www.justdopython.com/assets/images/2020/python/rename.gif)



### 画正方形

现在，我们先画一个正方形试试水~

想象一下，我们现在一个起点o，如何从这个起点o画一个正方形呢？好啦，考虑一下后发现是这样的:

- 先水平向右画一条直线，长度比如就为`100`像素吧
- 画完上一条边后，顺时针旋转90°角，再画一条等长度的边
- 循环上一步骤几次，正方形就画出来了
- 最后停止画笔



![draw-triangle-delay](http://www.justdopython.com/assets/images/2020/python/square-draw.png)

具体代码如下:

```python
# 画正方形
import turtle as t # 调用turtle库，并给它一个别名t
t.pensize(2) # 设置线的大小
for i in range(4): # 画四条边
    t.fd(100) # 每一次画100个像素
    t.left(90) # 画100个像素之后转动90°
t.done() # 绘图结束后停止画笔
```



### 画三角形

同理，我们现在一个起点o，如何从这个起点o画一个三角形呢？好啦，考虑一下后发现是这样的:

- 先水平向右画一条直线，长度比如就为`100`像素吧
- 画完上一条边后，逆时针旋转120°角，再画一条等长度的边
- 接着，顺时针旋转60°角，再画一条等长度的边
- 最后停止画笔

![draw-triangle-delay](http://www.justdopython.com/assets/images/2020/python/draw-triangle-delay.gif)



具体代码是:

```python
# 画三角形 
import turtle as t
import time
t.forward(100)
time.sleep(0.2)
t.left(120)
t.forward(100)
time.sleep(0.2)
t.right(60)
t.backward(100)
time.sleep(0.2)

time.sleep(0.3)
t.done()
```



### 画六边形

画六边形和正方形有点像，我们只需把之前每次画新边时旋转的90°改为60°，并把循环次数改为6即可。

![six-bian-xing](http://www.justdopython.com/assets/images/2020/python/six-bian-xing.png)

具体代码是:

```python
# 画六边形
import turtle
turtle.pensize(2) #设置线的大小
for i in range(6): #因为有六条边，所以我们画六次
    turtle.fd(100) #前进100个像素单位
    turtle.left(60) #向左旋转60度（每一个内角的外角都为60°）
turtle.done() # 画布停留
```



### 画两个六边形的叠边图

想象一下两个六边形对称性地错位，其特点是，有**九条边**，小乌龟最后会回到的自己的出发点，所以角度是360°的倍数，又因为有九条边所以我们可以得出每次转角为80°。

于是，画这个叠边图与画六边形有点像，我们只需把之前每次画新边时旋转的60°改为80°，并把循环次数改为9即可。

![six-bian-xing-overlap](http://www.justdopython.com/assets/images/2020/python/six-bian-xing-overlap.png)

其具体的代码为:

```python
# 画 两个六边形叠边图
import turtle
turtle.pensize(2)
for i in range(9):# 因为有九条边，所以我们选择画九次
    turtle.fd(150)
    turtle.left(80)# 每次转角为80°
turtle.done()
```



### 画同切圆

首先，同切圆是什么？直接给个图吧，就是这样(多个圆都切于同一条线，比如我们就用水平线):

![tong-qie-yuan](http://www.justdopython.com/assets/images/2020/python/tong-qie-yuan.png)

怎么画一个同切圆呢？观察后发现可以这么干:

- 先以一定长度为半径，画一个圆，画完后默认会回到原起点
- 增大半径，再重复上一步骤
- 重复上一步骤
- 最后停止画笔

我们这就画有4个圆同切吧~

![tong-qie-yuan-draw](http://www.justdopython.com/assets/images/2020/python/tong-qie-yuan-draw.png)

具体代码为:

```python
# 画同切圆
import turtle
turtle.pensize(2)#以左侧30像素处为圆心绘制360°即绘制一个圆（不给出弧度值则表示默认画一个圆）
turtle.circle(30)
turtle.circle(40)
turtle.circle(50)
turtle.circle(60)
turtle.done()
```



### 画五角星

在草稿纸上画了画之后，我们会发现五角星和正方形的画法类似，旋转角度为144°，边数为5。

![wu-jiao-xin](http://www.justdopython.com/assets/images/2020/python/wu-jiao-xin.png)

其具体代码为:

```python
# 画五角星

import turtle
p = turtle
p.pensize(3)
for i in range(5):
    p.forward(100)
    p.left(144)#左转144°
turtle.done()
```



### 画奥运五环

奥运五环正式版我们就不要求完全一样了，我们只需要画出如下近似的即可~

![wu-huan](http://www.justdopython.com/assets/images/2020/python/wu-huan.png)

观察之后，我们大概可以这样做:

- 画一个完整的圆，此时画笔回到的起点

  但我们需要将画笔搬到该点关于圆心对称的地方继续画，怎么办呢？这时我们可以使用`turtle`中的goto(x,y)函数，直接将画笔移动到坐标(x,y)‪‬‪‬‪‬‪‬‪‬‮‬‭‬‪‬‪‬‪‬‪‬‪‬‪‬‮‬‫‬‪‬‪‬‪‬‪‬‪‬‪‬‮‬‪‬‫‬‪‬‪‬‪‬‪‬‪‬‮‬‫‬‮‬‪‬‪‬‪‬‪‬‪‬‮‬‫‬‫‬

- 从新的起点继续画完整的圆，画完后移动画笔，直到画完最开始的3个圆，并按要求为边上色

- 用同样的方式画完最后两个圆，并按要求为边上色

  

  ![wu-huan-draw](http://www.justdopython.com/assets/images/2020/python/wu-huan-draw.png)

  

  其具体代码为:

  ```python
  # 画奥运五环
  import turtle
  p = turtle
  p.pensize(3)
  p.color("blue")
  p.circle(30,360)
  p.pu()
  p.goto(60,0)
  p.pd()
  p.color("black")
  p.circle(30,360)
  p.pu()
  p.goto(120,0)
  p.pd()
  p.color("red")
  p.circle(30,360)
  p.pu()
  p.goto(90,-30)
  p.pd()
  p.color("green")
  p.circle(30,360)
  p.pu()
  p.goto(30,-30)
  p.pd()
  p.color("yellow")
  p.circle(30,360)
  p.done()
  ```

  

### 画风轮

最后呢，我们来画一个风轮，其中要求每个风轮内角为45度，风轮边长150像素。

![feng-ye](http://www.justdopython.com/assets/images/2020/python/feng-lun.png)

结合画上一个图的经验，其实我们结合`goto(x,y)`函数来画4个45°的扇形即可~



![feng-lun-draw](http://www.justdopython.com/assets/images/2020/python/feng-lun-draw.png)



其具体的代码是:

```python
# 画风轮
import turtle
for i in range(4):
    turtle.fd(100)
    turtle.right(90)
    turtle.circle(-100,45)
    turtle.goto(0,0)
    turtle.left(45)
turtle.done()
```



今天，这些知识你都学会了嘛~















