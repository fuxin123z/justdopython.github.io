---
layout: post
title: 程序员奶爸必修课——用 pygame 写小游戏
category: python
tagline: by 闲欢
tags: 
  - python
  - 小游戏
---

周末在家没事，大哥和嫂子要出去 happy，于是将他的儿子丢到我家，让我当奶爸陪玩一下。为了让这磨人的小妖精消停会，我好安静地打盘王者，我灵机一动，准备写个简单的小游戏给他玩一会。

<!--more-->

### 思路

对于这种三岁小孩，他们不需要复杂操作的游戏，而是要傻瓜式的，并且界面带有色彩的最好。并且写这个小游戏不能占用我太多时间，不然得不偿失！

基于这样的思路，我想起了以前在哪里看过的一个小游戏————七彩同心圆。它的玩法就是每次点击鼠标时，会以鼠标为圆心画一个圆，然后在这个圆的基础上不断向外扩展圆（类似于水波浪的扩散），从而形成一个同心圆，并达到随机大小后停止扩展，其中每个同心圆的颜色都是随机的。

这个小游戏正好满足目前的场景，于是我撸起袖子准备三下五除二式地实现它，为我的王者之路争取时间！


### 实现

首先，我需要初始化各种变量：

```python

pygame.init()
screen = pygame.display.set_mode([600, 400])
screen.fill((255, 255, 255))
# 圆的半径
radius = [0] * 10
# 圆的半径增量
circleDelt = [0] * 10
# 圆是否存在,False代表该索引值下的圆不存在，True代表存在
circleExists = [False] * 10
# 圆的坐标x轴
circleX = [0] * 10
# 圆的坐标y轴
circleY = [0] * 10
# 颜色RGB值
RGBx = [0] * 10
RGBy = [0] * 10
RGBz = [0] * 10

```

接着我需要监听鼠标事件，监听到之后，根据鼠标的位置画一个初始化的圆：

```python

# 鼠标按下
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 获取圆不存在的索引值
            num = circleExists.index(False)
            # 将该索引值的圆设置为存在
            circleExists[num] = True
            # 圆的半径设置为0
            radius[num] = 0
            # 获取鼠标坐标
            circleX[num], circleY[num] = pygame.mouse.get_pos()
            # 随机获取颜色值
            RGBx[num] = random.randint(0, 255)
            RGBy[num] = random.randint(0, 255)
            RGBz[num] = random.randint(0, 255)
            # 画圆
            pygame.draw.circle(screen, pygame.Color(RGBx[num], RGBy[num], RGBz[num]),
                               (circleX[num], circleY[num]), radius[num], 1)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
```

画了圆之后，我需要让它随机扩展出同心圆，这个同心圆需要一圈一圈地画：

```python

for i in range(10):
        # 圆不存在则跳过循环
        if not circleExists[i]:
            pass
        else:
            # 随机圆的大小
            if radius[i] < random.randint(10, 50):
                # 圆的随机半径增量
                circleDelt[i] = random.randint(0, 5)
                radius[i] += circleDelt[i]
                # 画圆
                pygame.draw.circle(screen, pygame.Color(RGBx[i], RGBy[i], RGBz[i]),
                                   (circleX[i], circleY[i]), radius[i], 1)
            else:
                #若圆已达到最大，这将该索引值的圆设置为不存在
                circleExists[i] = False
```

最终的效果是这样子的：

![](http://www.justdopython.com/assets/images/2020/12/circlegame/circlegame.jpg)


### 总结

虽然我还不是奶爸，但是我感觉我需要多琢磨琢磨 pygame，储备一些有意思的小游戏给未来的儿子玩，以彰显技术人的优势，此处应有喝彩！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/circlegame)
