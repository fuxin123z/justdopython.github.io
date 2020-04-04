---
layout: post
category: python
title: 不到 150 行代码写一个 Python 版的贪吃蛇
tagline: by 豆豆
tags: 
  - python100
---

相信大家小时候应该都玩过贪吃蛇这个游戏吧，反正我小时候超喜欢玩，没其他原因，因为家里的手机上只有这一个游戏可以消磨时光。后来随着移动互联网的普及，智能手机逐渐取代了诺基亚，但这款游戏的确堪称经典之作。

今天我们就用 pygame 来自己写一个贪吃蛇出来，重温经典。

<!--more-->

先来看看我们最终实现的效果。

视频正在上传...

## 安装

使用 pygame 之前需要先安装，直接使用 pip 安装即可。

```python
pip install pygame
```

使用之前需要先将相应模块引入我们的程序。

```python
import pygame, sys
from pygame.locals import *
```

## Hello World

一般大家学习新的编程语言时写的第一个程序基本都是 Hello World，那么我们今天的入门 demo 就是用 pygame 在屏幕上输出 Hello World。

在使用 pygame 之前需要将其初始化，然后在新建一个游戏窗口，用于和用户交互。

```python
# 初始化
pygame.init()
# 新建窗口
screen = pygame.display.set_mode((640, 480))
```

接下来我就就需要设置要输出的字体了。

```python
# 设置窗口标题
pygame.display.set_caption("Hello World")
# 设置字体
font = pygame.font.Font(None, 30)
text = font.render('Hello World', True, pygame.Color("#FFFFFF"))
```

字体设置好之后，直接把字体输出至画布即可，记得，完成画布上的工作之后不要忘记刷新画布，不然不会有任何东西显示的。

```python
# 填充字体到画布
screen.blit(text, (100, 100))
# 刷新画布
pygame.display.update()
```

其中 `screen.blit()` 函数的入参分别是字体，以及字体的输出位置。

说到位置，就需要说一下 pygame 中的坐标系，坐标系以游戏窗口的左上角为原点（0，0），x 轴向右递增，y 轴向下递增。

运行上面的程序之后你会发现，窗口一闪而过，所以我们需要将该操作放入一个死循环中。

```python
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(text, (100, 100))
    pygame.display.update()
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-04-greedy-snake/001.png)

在这个循环中，我们监听用户是否点击了窗口的关闭按钮，如若点击我们直接退出程序即可。

这里需要说一下 pygame 的事件监听机制，在 pygame 中，所有事件都会依次传递到一个队列中去，我们可以通过 `pygame.event.get()`获取队列中的所有事件，然后根据事件类型做不同的操作即可。比如监听键盘点击事件或者鼠标事件等。


## 贪吃蛇

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-04-greedy-snake/002.png)

我们先来看下游戏布局，左上角的「0/0」表示「当前得分/历史最高分」。红色小方块是食物，由五个小方块组成的矩形是蛇，蛇头向右，初始运动方向也向右，游戏作战区域在大矩形内。当贪吃蛇的头部触碰到墙壁或者自己的身体时则游戏结束。

为了写程序的方便，我们先定义一些默认参数。如各种颜色、长度单位、蛇的默认位置和朝向、上下左右四个方向、以及分数等。

### 颜色设置

```python
# 颜色配置
snake_color = pygame.Color("#8B7D1C")
food_color = pygame.Color("#8B0000")
background_color = pygame.Color("#BACB03")
text_color = pygame.Color("#EFEFEF")
```

### 坐标设置

游戏中的坐标计算尤其关键。因为贪吃蛇和食物都是由小方块组成的，所以我们设定小方块为占据 15 个像素单位的正方形，游戏中均是以一个小方块的边长为长度单位来计算坐标的。下文我们简称小方块的边长为一个长度单位。

在此基础上，我们设定游戏窗口的宽和高分别为 44 个长度单位和 36 个长度单位，游戏作战区域距窗口上边框、下边框、左边框和右边框的距离分别是四个长度单位、两个长度单位、两个长度单位、两个长度单位。

因此，游戏窗口宽高以及游戏作战区域四个顶点坐标设置如下：

```python
# 长度单位
pixel = 15
line = 44
row = 36
window_width = pixel * line
window_high = pixel * row

point_left_up = [pixel * 2, pixel * 4]
point_left_down = [pixel * 2, pixel * (row - 2)]
point_right_up = [pixel * (line - 2), pixel * 4]
point_right_down = [pixel * (line - 2), pixel * (row - 2)]
```

蛇的位置坐标如下：

```python
# 蛇头位置
snake_head = [pixel * 8, pixel * 8]
# 蛇 默认五个小方块
snake_body = [[snake_head[0] - x * pixel, snake_head[1]] for x in range(5)]
```

### 方向设置

在这个游戏中，我们分别以 0、90、180、270 代表右、上、左、下。很多程序喜欢用字符串来表示方向，我们这里之所以用数字是因为数字更容易处理蛇的转向问题，只需计算二者的夹角是否为 90 度即可。即二者的差值绝对值为 90 或者 270 即代表转向。

```python
# 方向
direction_right = 0
direction_up = 90
direction_left = 180
direction_down = 270
```

### 分数设置

最后，因为要记录玩家的历史最高分，简单起见这里直接将最高分写入文件中，游戏初始化时加载一下即可。

```python
# 分数设置
score = 5
filename = 'db.txt'

def write_score(content):
    with open(filename, 'w+') as f:
        f.write(str(content))


def read_score():
    with open(filename, 'w+') as f:
        result = f.readline()
        return 0 if result.strip() == '' else int(result)
```

### 画蛇

我们先把分数和边框画起来。

```python
# 显示文字
def display_message(text, color, size, postion):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, postion)
    pygame.display.update()

# 画边线
def draw_box():
    for point in [[point_left_up, point_right_up], [point_right_up, point_right_down],
                  [point_right_down, point_left_down], [point_left_down, point_left_up]]:
        pygame.draw.line(screen, snake_color, point[0], point[1], 1)
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-04-greedy-snake/003.png)

嗯嗯，看起来不错，然后我们再将蛇和食物也一并画上去。

```python
# 随机产生食物
def create_food():
    while True:
        x = random.randint(point_left_up[0] / pixel, point_right_down[0] / pixel - 1) * pixel
        y = random.randint(point_left_up[1] / pixel, point_right_down[1] / pixel - 1) * pixel
        if [x, y] not in snake_body:
            break
    return [x, y]

def draw_snake(food_position):
    # 画蛇
    for point in snake_body:
        pygame.draw.rect(screen, snake_color, Rect(point[0], point[1], pixel, pixel))
    # 画食物
    pygame.draw.rect(screen, food_color, Rect(food_position[0], food_position[1], pixel, pixel))
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-04-greedy-snake/002.png)

画蛇和食物就是画矩形，给定颜色，坐标，长和宽即可。

画食物这里需要注意下，要在游戏作战区域内画，且要去除蛇占据的位置。

### 让蛇动起来

一切准备就绪，那么如何让蛇动起来呢。

很简单，在游戏中蛇是由小方块组成的，而小方块的坐标是存放在列表 snake_body 中的，画蛇时我们将一个个的小方块分别渲染出来，所以肯定需要在 snake_body 上做文章了。

每向右移动一格，相当于 x 坐标增加一个长度单位，反之则减少一个长度单位，上下运动同理，只不过变化的是 y 轴的坐标。所以，我们只需要监听键盘事件，然后根据不同的方向改变 x 轴或者 y 轴的坐标即可。

当然如果每运动一个长度单位就需要遍历一次 snake_body，那未免有点太麻烦了。仔细思考一下，其实我们只需要将蛇尾去掉，然后插入一个新的蛇头即可。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-04-greedy-snake/004.png)

因此我们将向不同方向运动时，x 轴和 y 轴需要移动的长度单位放入 move 这个字典中，便于计算。

```python
move = {direction_right: [pixel, 0], direction_left: [-pixel, 0], direction_up: [0, -pixel], direction_down: [0, pixel]}

# 插入新的蛇头
snake_head[0] += move[origin_direction][0]
snake_head[1] += move[origin_direction][1]
snake_body.insert(0, list(snake_head))
# 移除蛇尾
snake_body.pop()
```

那如何处理吃到食物的问题呢。其实跟处理运动没什么大的区别，唯一的区别就是吃到食物后不需要移除蛇尾而已。

那如何判断是否吃到食物呢，当然是蛇头坐标和食物坐标一样嘛。

最后，我们将所有的操作都封装进一个入口函数 run 中来。

```python
# 入口函数
def run():
    food_position = create_food()
    max_score = read_score()
    current_score = 0
    is_dead = False
    origin_direction = direction_right
    target_direction = origin_direction
    while True:
        # 监听键盘按键 退出 OR 换方向
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(max_score, current_score)
            if event.type == KEYDOWN:
                # 箭头 OR asdw 控制方向
                if event.key == K_RIGHT or event.key == K_d:
                    target_direction = direction_right
                if event.key == K_LEFT or event.key == K_a:
                    target_direction = direction_left
                if event.key == K_UP or event.key == K_w:
                    target_direction = direction_up
                if event.key == K_DOWN or event.key == K_s:
                    target_direction = direction_down
                # esc 退出
                if event.key == K_ESCAPE:
                    game_over(max_score, current_score)
            # 夹角为 90 or 270 可以转换方向
            angle = abs(origin_direction - target_direction)
            if angle == 90 or angle == 270:
                origin_direction = target_direction

        if not is_dead:
            snake_head[0] += move[origin_direction][0]
            snake_head[1] += move[origin_direction][1]

        if not is_dead and is_alive():
            # 按 origin_direction 方向运动
            snake_body.insert(0, list(snake_head))
            # 吃到食物后重新生成
            if snake_head[0] == food_position[0] and snake_head[1] == food_position[1]:
                food_position = create_food()
                current_score += score
            else:
                # 移除最后一格
                snake_body.pop()
        else:
            is_dead = True

        # 画背景
        screen.fill(background_color)
        # 画边框
        draw_box()
        # 画蛇
        draw_snake(food_position)
        # 刷新画面
        pygame.display.update()
        # 更新分数
        display_message(f"{current_score}/{max_score}", text_color, 30, (pixel * 2, pixel * 2))
        if is_dead:
            display_message(f"Game Over", text_color, 50, (pixel * 16, pixel * 15))
        # 控制游戏速度
        time_clock.tick(speed)


if __name__ == '__main__':
    run()
```

## 总结

今天我们使用 pygame 写了一个属于自己的贪吃蛇小游戏，代码行数不超过 150 行。写这款游戏其实不难，只是需要你在脑海中构建一套坐标系，然后在不同时刻不同坐标点上画不同的图案即可。当图片较多且切换速度很快时，人的眼睛已经分不清是图片了，这也就形成了动画。

大家也可以用 pygame 写一个自己喜欢玩的小游戏出来。

## 代码地址

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/doudou/2020-04-04-greedy-snake