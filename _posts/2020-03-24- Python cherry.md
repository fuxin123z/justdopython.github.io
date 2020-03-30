---
layout: post
category: python
title: Python 之樱花小技
tagline: by 潮汐
tags:
  - python100
---

亲爱的朋友们：
	想要一起来看樱花吗? 听说武汉这座英雄城市的樱花已经开了，但是在疫情的影响下，我们只能隔幕观花，小编也是一个爱花使者，今天我们就以另一种方式来呈现樱花之美，想要看到美丽的花朵，得每天保持学习状态，不断吸收新知识，学习新技能，接下来和小编一起欣赏一棵别样的樱花树。

<!--more-->

### 初夏的樱花

![樱花树](https://img-blog.csdnimg.cn/20200323154207597.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

## 樱花树实现思路

实现思路主要是利用之前学过的 Python 绘图模块 Turtle，Turtle 详细学习课程请参考[趣玩 Python 之绘制基本图形](https://mp.weixin.qq.com/s/zqoAZQ4aNzruXTd4QUGzmQ/) 或 [官网](https://docs.python.org/3/library/turtle.html) 再结合随机函数生成任意的一棵树，樱花树主要组成部分有树干和花瓣以及飘落的花瓣构成。

### 亭亭玉立的树干

绘画的树干使用了 Python 中的随机函数，这样每次生成的树干都是随机的，树干的选择也是随机设置参数进行调整。

示例图：

![树干和花瓣](https://img-blog.csdnimg.cn/20200323154330802.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

**代码如下所示：**

```python

def cherryTree(branch, t):
    if branch > 4:
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
                # 设置樱花树叶颜色
                t.color('green')  # 樱花树颜色
            t.pensize(branch / 5)
        else:
            t.color('Peru')  # 树干颜色
            t.pensize(branch / 11)  #调整树干的粗细
        t.forward(branch)
        a = 1 * random.random()
        t.right(20 * a)
        b = 1 * random.random()
       # 调用函数本身绘画　
        cherryTree(branch - 10 * b, t)
        t.left(60 * a)
       # 调用函数本身绘画
        cherryTree(branch - 10 * b, t)
        t.right(40 * a)
       # 提笔 
        t.up()
        t.backward(branch)
        # 落笔
        t.down()
        
```

以上代码实现的是随机树干以及花瓣颜色、树叶的颜色填充，同时还调整了花瓣大小和树干粗细。使整个树干看起来更协调。

### 花瓣随风飘

 欣赏樱花最美不过是樱花随风飘落的场景，示例图：

![花瓣图](https://img-blog.csdnimg.cn/2020032315443518.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

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

### 文字

一棵好看的樱花树少不了合适的文案，这里我们再利用小海龟绘图将文字配上

详细代码如下：

```python
def des_word():
    t.color('LightCoral') # 字体颜色设置
    t.hideturtle()
    t.goto(-50,-130)
    t.pu()
    # 昨日雪如花，今日花如雪，山樱如美人，红颜易消歇。
    t.write('昨日雪如花,',move=False, align='center', font=('Arial', 20, 'normal'))
    t.pd()

    t.pu()
    t.goto(90,-130)
    t.write('今日花如雪', move=False, align='center', font=('Arial', 20, 'normal'))
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

![完美的樱花树](https://img-blog.csdnimg.cn/20200324110105307.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

## 总结

  樱花的实现过程主要就是看个人对知识点的理解以及应用，每学习一项技能都需要付出很多的努力，实践和运用并存才能运用得如鱼得水。
今天分享的内容素材来源于周末和朋友出去看樱花的突发灵感，希望大家都能在疫情结束后与摘下口罩尽情赏花。


> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/chaoxi/cherry_tree>
