---
layout: post
title: 圣诞节不买礼物，准备给她画一棵精美圣诞树！
category: python
tagline: by 闲欢
tags: 
  - python
  - 圣诞节
  - 圣诞树
  - 礼物
---

![封面](http://www.justdopython.com/assets/images/2021/12/christmastree/6.png)

圣诞节到了，你是不是想用 python 画一棵精美的的圣诞树？

![](http://www.justdopython.com/assets/images/2021/12/christmastree/1.png)

看了网上的效果，是不是都不太满意？

接下来，请跟我一起来绘制一棵圣诞树，重新定义“**精美**”这个词。

<!--more-->

### 效果

我们先来看看绘制的总体过程：

![](http://www.justdopython.com/assets/images/2021/12/christmastree/0.gif)


### 实现

#### 画五角星

圣诞树的顶部是一颗金光闪闪的五角星，我们第一步是画这个：

```python
for i in range(5):  # 画五角星
    forward(n / 5)
    right(144)  # 五角星的角度
    forward(n / 5)
    left(72)  # 继续换角度
end_fill()
right(126)

```


#### 画彩灯

我们的圣诞树上面有些小彩灯，这样会使我们的圣诞树显得不那么单调，也更贴近现实中的圣诞树：

```python
def drawlight():  
    if r.randint(0, 50) == 0:  # 如果觉得彩灯太多，可以把取值范围加大一些，对应的灯就会少一些
        color('tomato')  # 定义第一种颜色
        circle(3)  # 定义彩灯大小
    elif r.randint(0, 30) == 1:
        color('orange')  # 定义第二种颜色
        circle(4)  # 定义彩灯大小
    elif r.randint(0, 50) == 2:
        color('blue')  # 定义第三种颜色
        circle(2)  # 定义彩灯大小
    elif r.randint(0, 30) == 3:
        color('white')  # 定义第四种颜色
        circle(4)  # 定义彩灯大小
    else:
        color('dark green')  # 其余的随机数情况下画空的树枝

```

#### 画圣诞树

定义好彩灯之后，我们就开始画我们的圣诞树了，圣诞树以绿色为主体颜色，中间会点缀一些彩灯：

```python
def tree(d, s):
    speed(100)
    if d <= 0: return
    forward(s)
    tree(d - 1, s * .8)
    right(120)
    tree(d - 3, s * .5)
    drawlight()  # 同时调用小彩灯的方法
    right(120)
    tree(d - 3, s * .5)
    right(120)
    backward(s)

```

画完的圣诞树是这样子的：

![](http://www.justdopython.com/assets/images/2021/12/christmastree/2.png)


#### 画底部装饰

圣诞树画完了之后，我们会在树的底部加一些小装饰，让树的底部看起来比较斑驳：

```python
for i in range(200):
    a = 200 - 400 * r.random()
    b = 10 - 20 * r.random()
    up()
    forward(b)
    left(90)
    forward(a)
    down()
    if r.randint(0, 1) == 0:
        color('tomato')
    else:
        color('wheat')
    circle(2)
    up()
    backward(a)
    right(90)
    backward(b)

```

底部装饰效果图：

![](http://www.justdopython.com/assets/images/2021/12/christmastree/3.png)


#### 画雪人

有圣诞树，就得有雪人啊，这样才能衬托出冬日的圣诞气氛！

```python
def drawsnowman(n,m,a,b):
    speed(100)
    t.goto(n, m)
    t.pencolor("white")
    t.pensize(2)
    t.fillcolor("white")
    t.seth(0)
    t.begin_fill()
    t.circle(a)
    t.end_fill()
    t.seth(180)
    t.begin_fill()
    t.circle(b)
    t.end_fill()
    t.pencolor("black")
    t.fillcolor("black")
    t.penup()    # 右眼睛
    t.goto(n-a/4, m+a)
    t.seth(0)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()    # 左眼睛
    t.goto(n+a/4, m+a)
    t.seth(0)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()  # 画嘴巴
    t.goto(n, m+a/2)
    t.seth(0)
    t.pendown()
    t.fd(5)
    t.penup()       # 画扣子
    t.pencolor("red")
    t.fillcolor("red")
    t.goto(n, m-b/4)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()
    t.pencolor("yellow")
    t.fillcolor("yellow")
    t.goto(n, m-b/2)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()
    t.pencolor("orange")
    t.fillcolor("orange")
    t.goto(n, m-(3*b)/4)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()

drawsnowman(-200, -200, 20, 30)
drawsnowman(-250, -200, 30, 40)
```

一个雪人太孤单了，我们得画两个：

![](http://www.justdopython.com/assets/images/2021/12/christmastree/4.png)

#### 画雪花

天空中再飘洒一些白莹莹的雪花就更完美了：

```python

def drawsnow():  
    t.ht()  # 隐藏笔头，ht=hideturtle
    t.pensize(2)  # 定义笔头大小
    for i in range(200):  # 画多少雪花
        t.pencolor("white")  # 定义画笔颜色为白色，其实就是雪花为白色
        t.pu()  # 提笔，pu=penup
        t.setx(r.randint(-350, 350))  # 定义x坐标，随机从-350到350之间选择
        t.sety(r.randint(-100, 350))  # 定义y坐标，注意雪花一般在地上不会落下，所以不会从太小的纵座轴开始
        t.pd()  # 落笔，pd=pendown
        dens = 6  # 雪花瓣数设为6
        snowsize = r.randint(1, 10)  # 定义雪花大小
        for j in range(dens):  # 就是6，那就是画5次，也就是一个雪花五角星
            # t.forward(int(snowsize))  #int（）取整数
            t.fd(int(snowsize))
            t.backward(int(snowsize))
            # t.bd(int(snowsize))  #注意没有bd=backward，但有fd=forward，小bug
            t.right(int(360 / dens))  # 转动角度
 ```           
            
最终的效果如下：

![](http://www.justdopython.com/assets/images/2021/12/christmastree/6.jpg)


### 总结

到此为止，我们的圣诞树就画完了！觉得还不错的话，帮忙点个`赞`和`在看`，让更多的人看到吧！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/christmastree)