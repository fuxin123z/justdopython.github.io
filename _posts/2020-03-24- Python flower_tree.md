---
layout: post
category: python
title: Python 版繁花盛开
tagline: by 潮汐
tags:
  - python100
---

今天请各位读者朋友欣赏用 Python 实现的鲜花盛宴，你准备好了吗？
整体实现思路清晰明了,90 行代码即可实现一棵美丽的鲜花盛开树。
小编也是鲜花爱护协会者之一，但是想要看到美丽的花朵，得历经很多；对于知识的运用也是如此，需要不断吸收新知识，学习新技能，才能盛开出美丽的花朵。
接下来就看看一棵迷人的花树是怎么实现的吧！

<!--more-->

### 夏天的花

![鲜花树](http://www.justdopython.com/assets/images/2020/flower/flower.png)

## 实现思路

实现思路主要是利用之前学过的 Python 绘图模块 Turtle，Turtle 详细学习课程请参考[趣玩 Python 之绘制基本图形](https://mp.weixin.qq.com/s/zqoAZQ4aNzruXTd4QUGzmQ/) 或 [官网](https://docs.python.org/3/library/turtle.html) 再结合随机函数生成任意的一棵树，樱花树主要组成部分有树干和花瓣以及飘落的花瓣构成。

### 亭亭玉立的树干

绘画的树干使用了 Python 中的随机函数，这样每次生成的树干都是随机的，树干的选择也是随机设置参数进行调整。

示例图：

![树干和花瓣](http://www.justdopython.com/assets/images/2020/flower/trunk.png)

**代码如下所示：**

```python

def cherryTree(branch, t):
    if branch > 4:
        # 枝干数
        if 7 <= branch <= 13:
            # 随机数生成
            if random.randint(0, 3) == 0:
                t.color('snow')  # 花瓣心的颜色
            else:
                t.color('pink')  #花瓣颜色
            # 填充的花瓣大小
            t.pensize( branch / 6)
        elif branch < 8:
            if random.randint(0, 2) == 0:
                t.color('snow')
            else:
                # 设置树叶颜色
                t.color('green')
            t.pensize(branch / 5)
        else:
            t.color('Peru')  # 树干颜色
            t.pensize(branch / 11)  #调整树干的粗细
        t.forward(branch)

        a = 1 * random.random()
        t.right(20 * a)
        b = 1 * random.random()
        cherryTree(branch - 10 * b, t)
        t.left(60 * a)
        cherryTree(branch - 10 * b, t)
        t.right(40 * a)
        t.up()
        t.backward(branch)
        t.down()
        
```

以上代码实现的是随机树干以及花瓣颜色、树叶的颜色填充，同时还调整了花瓣大小和树干粗细。使整个树干看起来更协调。

### 花瓣随风飘

 赏花最美不过是花瓣随风飘落的场景，示例图：

![花瓣图](http://www.justdopython.com/assets/images/2020/flower/petal.png)

**代码实现：**

```python

def petal(m, t):
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.up()
        t.forward(b)
        # 向左移动
        t.left(75)
        # 向前移动
        t.forward(a)
        # 放下画笔
        t.down()
        # 设置花瓣颜色
        t.color('pink')  # 粉红色
         # 画个小圆当作花瓣
        t.circle(1)
        # 提起画笔
        t.up()
        # 画笔向后退
        t.backward(a)
        # 画笔向前行
        t.right(70)
        t.backward(b)
```

### 鲜花配文字

一棵盛开的鲜花树怎么能少得了合适的文案呢？这里我们再利用小海龟绘图将文字配上

代码如下：

```python
def des_word():
    t.color('LightCoral') # 字体颜色设置
    t.hideturtle()
  #  t.goto(-50, -130)
    t.goto(-60,-170)
    t.pu()
    t.write('姹紫嫣红桃花笺,',move=False, align='center', font=('Arial', 20, 'normal'))
    t.pd()

    t.pu()
    #  t.goto(90, 130)
    t.goto(150,-170)
    t.write('繁花似锦为君妍', move=False, align='center', font=('Arial', 20, 'normal'))
    t.pd()

```

### 画笔样式调整

```python

t = turtle.Turtle()
# 画布大小 获取到屏幕
w = turtle.Screen()
t.hideturtle()  # 隐藏画笔
t.getscreen().tracer(8, 0)  # 获取屏幕大小
w.screensize(bg='LightCyan')  # 设置屏幕背景颜色
t.left(80)
t.up()
t.backward(140)
t.down()
t.color('sienna')
cherryTree(50, t)
petal(300, t)

```
### 最终结果

![完美的繁花盛开](http://www.justdopython.com/assets/images/2020/flower/result.png)

## 总结

至此，清风徐来，繁花已开！
桃花细逐杨花落
繁花似锦弄轻柔
姹紫嫣红桃花笺
繁花似锦为君妍
今天的赏花序曲暂且落幕，望伙伴们幕后自行品鉴！

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/chaoxi/flower>
