---
layout: post
category: python
title: Python 告诉你疫情扩散有多可怕
tagline: by 太阳雪
tags:
  - python100
---
今年（2020年）是注定要铭记史册的一年，从年初开始新冠疫情，席卷了全球，中国人民众志成城，为战胜疫情做出了巨大牺牲。最近北京疫情形式又变得严峻，面对疫情我们不能掉以轻心。今天我们模拟一下病毒的扩散过程，增强对疫情的认识同时，还可以了解下 Python 模拟技术，开干
<!--more-->

## 解决思路

我们将模拟过程分为 数据模型 和 展示 两部分
首先设置正态分布的人群，然后在其中随机设置携带者，在设置传染条件，和潜伏期时间，最后，用迭代模拟时间，观察病毒的传播过程，先看下效果：
![模拟效果](http://www.justdopython.com/assets/images/2020/06/diffusionsimulator/01.gif)

## 数据模型

### 模拟人群

假设城市环境，人群集中度呈正态分布，即中心地带集中度高，边缘地带集中度低，每个人都是一个平面坐标位置，随机产生在平面中心位置的一组坐标点来代表一个人

我们用 numpy 的随机机制产生模拟数据：

> numpy 安装： `pip install numpy`

```python
import numpy as np

count = 100
people = np.random.normal(250, 100, (count, 2))
```

- `numpy.random.normal` 是产生正态分布数据方法，参数为 loc, scale, size
- `loc` 表示正态分布的中心点，比如横轴坐标总宽度为 500，中心点为 250
- `scale` 表示标准差，可以理解为距离中心的距离，值越大，分布图形越宽，越小，越窄
- `size` 表示产生的数量，可以是单值或者二维元组，元组中第一个表示数量，第二个表示每组数据的维度，我们要产生平面上的点，所以是二维的

人的属性除了位置，还需要有状态，我们用（0，1，2）来表示 健康、携带 和 确诊

由于 numpy 产生的事数据集合，所以状态数据用单独的数组表示，数组长度与人的数量相等：

```python
import numpy as np

count = 100
status = np.array([0] * count)
```

- array 方法可以产生一个数组，[0] 表示初始化数组，元素值为 0，即健康，然后乘以元素数量就可以得到初始化为 0 的数组。

有了人群的初始状态，可以为随机设置一些病毒携带者，通过一个随机过程来设置：

```python
import numpy as np

count = 100
index = np.random.randint(0, count)
status[index] = 1
```

- randint 可以在给定参数之间随机产生一个整数，我们在 0 和 人数的范围内得到一个随机数，作为携带者的下标
- 如果需要设置多个携带者，可以循环此过程，但需要排除掉状态已经是携带者的情况

另外由于病毒有潜伏期，所以需要记录感染的时间，以便在达到潜伏条件后变为确诊：

```python
import numpy as np

count = 100
timer = np.array([0] * count)
```

- 感染时间和状态类似，是一个数量为人数的数组

最后，一个人有三个属性：位置、状态和感染时间，在模拟过程中，会不断调整这些属性

#### 模拟移动

人群是运动的，需要设置一个随机运动的机制，这里采用随机小幅度移动来模拟人群移动，从而产生：

```python
count = 100
movement = np.random.normal(0, 1, (count, 2))

normal = np.random.normal(0, 1, count)
switch = np.where(normal < x, 1, 0)
movement[switch == 0] = 0

people = people + movement
```

- 产生一个中心点为 0，幅度为 1 的与人数相对的微小移动坐标数组 movement
- 为了一定比例不移动的情况，在得到一个正态一维数组，
- 并对数值进行筛选和归一，小于 0 的设置为 1，其他的设置为 0，做成一个动态开关
- 对移动数据中，对应开关为 0 的位置设置移动为 0，即不移动，从而随意模拟一下不移动的情况

#### 模拟传播

新冠病毒会在人与人之间传播，主要取决于接触程度，现实中接触过程很复杂，这里我们用人与人之间的距离作为传播依据，设置一个传播临界距离，健康者与携带者或者确诊者距离小于这个临界值，就会被传染

距离怎么计算呢，我们采用欧拉距离公式来计算，我们模拟的是平面位置，所以采用二维欧拉距离公式，假设平面中有两个坐标点 (x1, y1)  和 (x2, y2)，那么他们之间的距离公式为：

![欧拉距离](http://www.justdopython.com/assets/images/2020/06/diffusionsimulator/01.png)

如何引用这个公式呢？最容易想到的是用循环将传播源（携带者和确诊者）与每一个健康者之间的距离都算出来，将距离小于临界值的健康者标记为携带
不过 numpy 为我们提供了强大的集合运算能力，像写公式一样完成运算，而无需关注程序细节，先看代码：

```python
import numpy as np

safe_distance = 5
for inf in people[(status == 1) | (status == 2)]:
  dm = (people - inf) ** 2  # (x2-x1)^2 , (y2-y1)^2
  d = dm.sum(axis=1) ** 0.5
  sorted_index = d.argsort()
  for i in sorted_index:
    if d[i] >= safe_distance:
        break  # 超出范围，不用管了
    if status[i] > 0: # 已经感染的排除掉
        continue
    status[i] = 1 # 标记为感染
```

- 设置临界距离为 5
- 从人中选出已经携带和确诊者的位置坐标
  - status 为 ndarray 对象，`status == 1` 会返回一个布尔值数组，即每个元素与 1 比较的结果
  - 将 status 的结果作为参数，可以从 people 对象中筛选出位置结果为真的元素集合
- 遍历传播源的位置，并计算与每个人的距离，采用的是欧拉距离公式
  - `people - inf` 是个集合运算，会将 people 中 每个元素减去 inf，并做平方运算
  - 对集合做一维化合计，并做开平方运算，即得到距离集合
- 对距离进行排序，并且获得距离集合的索引集合 sorted_index，这个很有用
- 遍历索引集合，一旦发现大于等于安全距离的情况，就退出遍历，否则标记为感染

如果更实际一些，可以加入感染概率的考量，即并非每个在临界距离内的健康者都会感染

#### 模拟潜伏期

携带者需要经过一段时间的潜伏期，才会成为确诊者，例如潜伏期一般 3 到 7 天，14 天一定会成为确诊者：

```python
days = 10 # 时间线 表示从模拟开始到现在的天数
dt = days - timer
d = np.random.randint(3, 7)
timer[(status == 1) & ((dt == d) | (dt > 14))] = days
status[(status == 1) & ((dt == d) | (dt > 14))] += 1
```

- days 表示模拟的天数，例如现在模拟到到 10 天
- dt 是计算一个 timer 数组与天数的差值的数组
- 然后随机一个 3 到 7 之间的数，表示当时的确诊天数
- 选择状态为携带的 timer，并且时间间隔等于本次确诊天数或者时间间隔大于14天，如果符合条件标记确证时间，即哪一天确诊的
- 用同样的条件将状态为携带的标记为确证

### 图形化

有了数据模型，下一步是将数据展示出来，可选择的方式很多，这里我们选择 pygame 库，作为展示方式

> pygame 是一个 2D 游戏工具，简单易用，通过 `pip install pygame` 安装

#### 初始化

初始化 pygame :

```python
import pygame, sys
from pygame.locals import *

# 初始化pygame
pygame.init()

# 设置窗口与窗口标题
windowSurface = pygame.display.set_mode((WIDTH,HEIGHT),0,8)
pygame.display.set_caption('疫情模拟')

# 填充背景色
WHITE = (255,255,255)
windowSurface.fill(WHITE)
```

#### 绘制模拟点

将人模拟成屏幕上的小圆点，根据不同状态设置不同颜色，例如正常为黑色，携带为粉色，确诊为红色：

```python
POINT_RADIUS = 5
COLORS = [(0,0,0), (255,192,203),(255,0,0)]

for i in range(len(status)):  # 健康
  x_point = people[i][0]
  y_point = people[i][1]
  pygame.draw.circle(windowSurface,COLORS[status[i]],(int(x_point), int(y_point)), POINT_RADIUS)
```

- 循环人的状态，得到状态索引
- 用索引定位到人，得到人的坐标
- 通过 pygame.draw.circle 绘制到 windowSurface 上，其中填充颜色通过状态值作为索引获取

#### 事件循环

动态效果的实质时不断的刷新绘图，需要有个循环直接，动态更新：

```python
while True:
  windowSurface.fill(WHITE)  # 设置画布背景 起到擦除的作用
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  # 绘制模拟点
  <省略代码>

  # 更新到窗口中
  pygame.display.update()
  time.sleep(0.1)
```

- pygame.event.get 可以获取到收的意外事件，这里的逻辑时，如果收到退出事件，则退出程序
- pygame.display.update() 用于将绘制更新到屏幕上
- 每次绘制完成等等 0.2 秒，以便观察结果

将上面部分组合起来，运行就可以看到模拟效果了

## 总结

今天的模拟实验，主要依赖于 numpy 的随机机制，通过练习可以看到 numpy 处理在数据处理方面的强大功能。另外简单接触了 pygame，可以更高效的绘制动画效果，应为 pygame 就是为制作简单游戏而生的。 最后文章中主要以设计思路为主描述模拟程序的构成和原理，代码示例中有完整的可运行代码，欢迎把玩交流。

## 参考

- [https://cloud.tencent.com/developer/article/1490184](https://cloud.tencent.com/developer/article/1490184)
- [https://blog.csdn.net/qq_34465383/article/details/104373222](https://blog.csdn.net/qq_34465383/article/details/104373222)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/diffusionsimulator>
