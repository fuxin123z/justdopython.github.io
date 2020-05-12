---
layout: post     
title: 我用 Python 绘制日期差并表白团队                                  
category: 我用 Python 绘制日期差并表白团队     
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

很多时候学习一门语言最有成就感的事就是利用它做出自己想要的东西，包括小编也不例外，加入 Python 技术作者团队也有大半年之久了，今天突发奇想做了一个数码管式的时间轴，以此来怀念我和Python技术团队奋斗的时光。废话不多说，直接讲思路上代码，Let's go go go!

###  绘制数码管

其实平时我们在一些 LED 灯上看到的数字都是由一条条数码管组成的，最常见的是红绿灯数字，首先咱们先将单个数码管绘制出来，代码如下：

```python
def drawGap(): #绘制数码管间隔
    #提起画笔
    tl.pu()
    # 数码管间隔
    tl.fd(9)

def drawLine(draw):   #绘制单段数码管
    drawGap()
    tl.pendown() \
        if draw else tl.penup()
    tl.fd(40)
    # 开始绘画
    drawGap()
    tl.right(90)
```

当然以上代码不会出任何结果，就像我们要画画拿出一张白纸是一样的道理。
接下来我们需要构思 0-9 的数码管要怎么形成？大家一起来想想（想想红绿灯的数字跳转是怎么形成的）……
其实红绿灯的数字就是由数码管来显示的，数字 8 将数码管全部填满，它由 7 小段数码管构成，其它数字做相应数码管的加减；首先我们需要先绘制7 条数码管，思路清晰后我们需要打草稿上代码，部分代码如下：

```python
drawLine(True) if d in [2, 3, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 3, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 6, 8] else drawLine(False)
    tl.left(90)
    #
    drawLine(True) if d in [0, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine(False)
    tl.left(200)
    tl.penup()
    tl.fd(20)
```
调用代码：

```
if __name__ == '__main__':
    drawDigit(8)
```

**显示结果：**

![单数码管](https://imgkr.cn-bj.ufileos.com/cf738596-ed97-4e66-9d58-48183aaf40e6.png)


### 绘制日期数码管

接下来就要结合时间绘制日期数码管，给绘制的日期设置颜色和字体大小，部分代码如下：

```python
def drawDate(date):
    tl.pencolor("#AB82FF")
    for i in date: #根据设置的符号分隔年月日
        if i == '-':
            tl.write('年',font=("Arial", 22, "normal"))
            tl.pencolor("#B3EE3A")
            tl.fd(40)
        elif i == '=':
            tl.write('月',font=("Arial", 22, "normal"))
            tl.pencolor("#FFD700")
            tl.fd(40)
        elif i == '+':
            tl.write('日',font=("Arial", 22, "normal"))
        else:
            drawDigit(eval(i))
```

### 计算总天数

想达到的效果是，输入开始日期和当前日期后自动计算历经天数，经历总天数统计代码如下：

```python
def all(day):
    tl.goto(-350,-300)
    tl.pencolor("SlateBlue")
    tl.write('总共',font=("Arial", 40, "normal"))
    tl.fd(110)
    for j in day:
        drawDigit(eval(j))
    tl.write('天',font=("Arial", 40, "normal"))

def count(t1, t2, t3):
    t = t1*365
    if t2 in [1, 2]:
        t += t2*30
    if t2 in [3]:
        t = t+91
    if t2 == 4:
        t += 122
    if t2 == 5:
        t += 152
    if t2 == 6:
        t += 183
    if t2 == 7:
        t += 213
    if t2 == 8:
        t += 244
    if t2 == 9:
        t += 275
    if t2 == 10:
        t += 303
    if t2 == 11:
        t += 334
    t += t3
    return(str(t))
```

### 画出当前日期和加入团队日期

调用方法绘制出当前日期以及加入团队的日期，当前日期使用的是time 模块动态获取现在的日期，代码如下：


```python
def turtle_date():
    tl.color('MediumTurquoise')
    tl.penup()
    tl.goto(-350,370)
    tl.pendown()
    # 获取到当前日期
    tl.write('今天是：',font=("Arial", 22, "normal"))
    tl.pensize(5)
    tl.penup()
    tl.goto(-350,300)
    tl.pendown()
    drawDate(time.strftime('%Y-%m=%d+',time.gmtime()))
    tl.color('MediumTurquoise')
    tl.penup()
    tl.goto(-350,190)
    tl.pensize(1)
    tl.pendown()
    tl.pencolor("MediumTurquoise")
    tl.write('我加入 Python 团队的时间是：',font=("Arial", 22, "normal"))
    tl.penup()
    tl.goto(-350,110)
    tl.pendown()
    tl.pensize(5)
    # 加入团队的时间
    drawDate('2019-09=03+')
    tl.penup()
    tl.goto(-350,0)
    tl.pensize(1)
    tl.pendown()
    tl.pencolor("MediumTurquoise")
    # 从加入日期到当前日期的月和天数
    tl.write('我和团队成员一起经历了：',font=("Arial", 22, "normal"))
    tl.penup()
    tl.goto(0,-100)
    tl.pensize(1)
    tl.pendown()
```

**运行结果如下：**

![开始和结束日期](https://imgkr.cn-bj.ufileos.com/fea41b99-1937-40a4-812c-98e44e3e79f9.png)


### 计算时间差

计算当前时间和加入团队的时间差，部分逻辑代码如下：

```python
    t1 = time.gmtime()
    t2 = t1.tm_year-2019
    t3 = t1.tm_mon-9
    if t3<0:
        t2 -= 1
        t3 += 12
    t4 = t1.tm_mday-3
    if t4 < 0:
        t3 -= 1
        if t1.tm_mon-1 in [1, 3, 5, 7, 8, 10, 12]:
            t4 += 31
        else:
            t4+=30
```


### 最终结果

![最终结果](https://imgkr.cn-bj.ufileos.com/bd1d65ca-9228-411d-b439-3267d6f91afa.png)


最终的纪念日期已经展示，大家可以根据自己的兴趣爱好学习，修行看个人噢！

### 爱 Python

最后我用 Python 给咱们团队实现了一个大大的爱心，希望大家继续努力！

实现代码如下：

```Python
def love_python():
    word = "Python技术"
    for char in word.split():
        allChar = []
        for y in range(12, -12, -1):
            lst = []
            lst_con = ''
            for x in range(-30, 30):
                # 心型函数实现
                formula = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
                if formula <= 0:
                    lst_con += char[(x) % len(char)]
                else:
                    lst_con += ' '
            lst.append(lst_con)
            allChar += lst
        print('\n'.join(allChar))

if __name__ == '__main__':

    love_python()
```

**实现效果如下：**

![表白团队](https://imgkr.cn-bj.ufileos.com/d3123582-7177-495a-a97a-4b75d7c0894c.png)


### 总结

今天的文章主要运用了turtle 绘图工具实现日期差来纪念一些重要的时日，同时运用了一个心形函数来绘制了一个爱心表白团队成员，因为他们真的很优秀，希望今天能给大家安利到有用的知识！