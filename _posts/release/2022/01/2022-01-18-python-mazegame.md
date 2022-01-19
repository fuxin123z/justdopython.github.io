---
layout: post
category: python
title: 程序员陪孩子，你还可以这么干……
tagline: by 李晓飞
tags:
  - python
  - 游戏
---
![封面](http://www.justdopython.com/assets/images/2022/01/mazegame/00.jpg)

周末在家，儿子闹着要玩游戏，让玩吧，不利于健康，不让玩吧，扛不住他折腾，于是想，不如一起搞个小游戏玩玩！

之前给他编过[猜数字](https://mp.weixin.qq.com/s/GQCWjTXAw5IWDt2h0xQgSA) 和 [掷骰子](https://mp.weixin.qq.com/s/-gf_N5DgtL8Vaxny-ZfjOg) 游戏，现在已经没有吸引力了，就对他说：“我们来玩个迷宫游戏吧。”

果不其然，有了兴趣，于是和他一起设计实现起来，现在一起看看我们是怎么做的吧，说不定也能成为一个陪娃神器~
<!--more-->

先一睹为快：
![效果](http://www.justdopython.com/assets/images/2022/01/mazegame/02.gif)

## 构思

迷宫游戏，相对比较简单，设置好地图，然后用递归算法来寻找出口，并将过程显示出来，增强趣味性。

不如想到需要让孩子一起参与，选择了绘图程序 [Turtle](https://docs.python.org/zh-cn/3/library/turtle.html 'Turtle') 作为实现工具。

这样就可以先在纸上绘制一个迷宫，然后编写成代码，让 Turtle 去绘制，因为孩子用笔画过，所以在实现代码时，他可以充分参与，不仅是为了得到最终的游戏，而且更是享受制作过程，开发编程思维，说不定省了一笔不小的少儿编程费用哈哈哈~

首先和孩子一起制作迷宫，在纸上画出 5 X 5 的小格子，然后，让他在格子中画一条通路，像这样：

![绘制迷宫](http://www.justdopython.com/assets/images/2022/01/mazegame/01.jpg)

然后，将这幅图转化为一个迷宫矩阵，用 `1` 表示墙，用 `空格` 表示通路，需要注意的是网格每条边线都是墙，连通部分的墙需要打通，成为路。

这时可以和他一起来实现，比如让他用自己的积木等摆设一个迷宫，而我们来做数字化转化，最后转化成的结果是：

```txt
1 1 1 1 1 1 1 1 1 1 1
        1       1 1 1
1 1 1   1   1   1 1 1
1       1   1       1
1   1 1 1   1 1 1   1
1       1   1       1
1 1 1   1   1   1 1 1
1       1   1       1
1   1 1 1   1 1 1   1
1           1 1 1   1
1 1 1 1 1 1 1 1 1   1
```

如果孩子看不清楚，可以将路径表示出来 哈哈哈：

```txt
1 1 1 1 1 1 1 1 1 1 1
->_____ 1 _____ 1 1 1
1 1 1 | 1 | 1 | 1 1 1
1 ____| 1 | 1 |___  1
1 | 1 1 1 | 1 1 1 | 1
1 |____ 1 | 1 ____| 1
1 1 1 | 1 | 1 | 1 1 1
1 ____| 1 | 1 |____ 1
1 | 1 1 1 | 1 1 1 | 1
1 |_______| 1 1 1 | 1
1 1 1 1 1 1 1 1 1\|/1
```

做完了迷宫数字化，就需要将迷宫在电脑上表示出来了。

## 绘制迷宫

之所以选择 Turtle，就是因为它会像用笔做图画一样，可以让孩子充分参与。

找出一张纸，用刚才整理的迷宫数字化结果作为指导绘图，遇到 `1` 就画一个小方格，遇到 `空格` 就跳过，可以和孩子一起画，主要是让他体会过程中的规律。

好了，趁他绘制的时候，我们来实现绘制代码吧。

首先需要知道 Turtle 的一些特点：

1. Turtle 的初始坐标在屏幕中心，可以将屏幕分成平面坐标系的四个象限
2. Turtle 画笔默认的移动最小单位是一个像素，因此需要做坐标点的初始化
3. Turtle 画笔移动都是相对于笔尖的朝向的，因此需要特别注意笔尖朝向

实现的方式和孩子用笔画是一样的，从第一个格子画起：

![效果](http://www.justdopython.com/assets/images/2022/01/mazegame/03.gif)

下面看看代码：

```python
def drawCenteredBox(self, x, y, color):
    self.t.up()
    self.t.goto(x - 0.5,    y - 0.5)
    self.t.color('black', color)
    self.t.setheading(90)
    self.t.down()
    self.t.begin_fill()
    for _ in range(4):
        self.t.forward(1)
        self.t.right(90)
    self.t.end_fill()
    update()
```

- `drawCenteredBox` 是 迷宫类 `Maze` 的成员方法，self 指的就是迷宫类本身，可以暂时将其理解为全局变量
- `self.t` 是一个 Turtle 模块实例，可以理解成画笔
- `up` 方法表示抬起笔尖
- `goto` 方法的作用是移动到指定的位置，这里需要移动到指定位置的左下角，所以各自减去了 0.5（这里做了坐标值转化，后面会有说明）
- `color` 表示设置颜色，两个参数分别是笔的颜色和填充颜色
- `setheading` 表示让笔尖朝上，即将笔尖朝向 90 度
- `down` 表示落下笔尖，意思是随后的移动相当于绘制
- `begin_fill` 表示准备填充，也就是它会把从调用起到调用 `end_fill` 为止所绘制的区域做填充
- 然后是循环四次，用来绘制方格，循环内，每次向前（笔尖朝向）绘制一个单位，向右转 90 度，这样就绘制好了一个方格
- `end_fill` 即为填充当前绘制的方格
- `update` 表示更新一下绘图区域

看看这个过程，是不是和孩子手工绘制一模一样！

现在遍历整个迷宫矩阵，不断调用 `drawCenteredBox` 就可以绘制出迷宫了：

![效果](http://www.justdopython.com/assets/images/2022/01/mazegame/04.jpg)

代码如下：

```python
def drawMaze(self):
    for y in range(self.rowsInMaze):
        for x in range(self.columnsInMaze):
            if self.mazelist[y][x] == 1:
                self.drawCenteredBox(x + self.xTranslate, -y + self.yTranslate, 'tan')
```

- `rowsInMaze`、`columnsInMaze` 表示迷宫矩阵的行和列
- `tan` 为[沙漠迷彩色](https://en.wikipedia.org/wiki/Tan_(color) '颜色 Tan')的颜色名称

## 走出迷宫

迷宫绘制好了，如何走出出呢？

可以先问问孩子，让他想想办法。

实现思路也很简单，就是超一个方向走，如果是墙，就换一个方向，如果不是墙，就继续走下去，如此往复……

但是，这里可以和孩子做个预演，比如迷宫很大的时候，记不住走过哪些路怎么办？

探索了一条路，走不通，返回后，不记得走过哪些路，这是非常危险的事情，如果有种方法可以记住走过的路，就好了。

这里我给儿子讲了一下[忒修斯大战牛头怪](https://zhidao.baidu.com/question/354469046.html '忒修斯大战牛头怪')的古希腊神话传说，启发他想出好的方法。

如何用代码实现呢，只要在迷宫矩阵种，标记一下走过的路就可以了：

```python
PART_OF_PATH = 0
OBSTACLE = 1
TRIED = 3
DEAD_END = 4

def search(maze, startRow, startColumn):  # 从指定的点开始搜索
    if maze[startRow][startColumn] == OBSTACLE:
        return False
    if maze[startRow][startColumn] == TRIED:
        return False
    if maze.isExit(startRow, startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        return True

    maze.updatePosition(startRow, startColumn, TRIED)

    found = search(maze, startRow-1, startColumn) or \
            search(maze, startRow, startColumn-1) or \
            search(maze, startRow+1, startColumn) or \
            search(maze, startRow, startColumn+1)
    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)

    return found
```

因为使用了递归方式，所以代码比较简短，我们来看看：

- `PART_OF_PATH`、`OBSTACLE`、`TRIED`、`DEAD_END` 是四个全局变量，分别表示迷宫矩阵中的通路，墙，探索过的路和死路
- `search` 方法用于探索迷宫，接受一个迷宫对象，和起始位置
- 然后看看指定的位置是否为墙、或者是走过的，以及是否是出口
- 然后继续探索，讲指定的位置标记为已走过
- 接下来朝四个方向探索，分别是像西、向东、向南、向北
- 每个方向的探索都是递归的调用 `search` 方法
- 如果探索的结果是找到了出口，就将当前的位置标记为路线，否则标记为死路

这里还需要看看 `updatePosition` 方法的实现：

```python
def updatePosition(self, row, col, val=None):
    if val:
        self.mazelist[row][col] = val
    self.moveTurtle(col, row)

    if val == PART_OF_PATH:
        color = 'green'
    elif val == OBSTACLE:
        color = 'red'
    elif val == TRIED:
        color = 'black'
    elif val == DEAD_END:
        color = 'red'
    else:
        color = None

    if color:
        self.dropBreadcrumb(color)

def moveTurtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate, -y+self.yTranslate))
        self.t.goto(x+self.xTranslate, -y+self.yTranslate)

def dropBreadcrumb(self, color):
    self.t.dot(color)
```

- `updatePosition` 方法本身不复杂，首先对迷宫矩阵做标记，然后将笔尖移动到指定的点，之后判断标记的值，在指定的点上画点
- 移动的方法是 `moveTurtle`，首先抬起笔尖，然后将笔尖转向将要移动过去的点
- Turtle 的 `towards` 方法会计算一个笔尖当前点到指定点之间的一个夹角，作用是让笔尖转向要移动过去的点，其中 `xTranslate` 和 `yTranslate` 是在坐标系中像素点的偏移量（后面会有说明）
- Turtle 的 `dot` 方法作用是绘制一个点

看一下效果：

![走出迷宫](http://www.justdopython.com/assets/images/2022/01/mazegame/05.gif)

## 更大的挑战

当孩子看到自己做的迷宫，被小乌龟走出来时，别提有多开心了。

不过，没多久，他就想要更复杂的迷宫，有多条分支的迷宫。

显然有手工的方式有点困难，而且无趣。需要让程序自动生成迷宫。

本来想大干一场，突然想到之前 [豆豆 写的一篇关于迷宫文章](https://mp.weixin.qq.com/s/2rbCWxscbn-qCMbJMYADMw '豆豆写的文章')，找来一看，刚好有迷宫生成算法，太好了。

> 关于如何动态生成迷宫，请参加 [豆豆的文章](https://mp.weixin.qq.com/s/2rbCWxscbn-qCMbJMYADMw)，其中有详细说明

分析代码之后，将其中的迷宫类移植过来，生成的结果之间导入到笔者写的迷宫类中，将迷宫规模设置为 100 X 100，震撼了：

![巨型迷宫](http://www.justdopython.com/assets/images/2022/01/mazegame/06.gif)

看着小乌龟在巨大的迷宫中蹒跚，还有种莫名的悲伤~

有了有了迷宫生成工具，就很多好玩的了：

- 如何让乌龟更快的找到出路
- 如何让乌龟随机出现在迷宫中
- 如何动态设置迷宫的出入口
- ……

对这些问题，我们一一做了实现，孩子在整个过程中，积极参与，时不时因为好的想法而手舞足蹈，不亦乐乎……

感兴趣的读者可以回复关键字，获得源码，研究一下解决方案，期待与你交流。

## 关于坐标系设置

前面留了几个坑，是关于 Turtle 坐标系的，这里统一做下说明。

### 第一个问题，坐标单位

默认情况下，Turtle 的坐标单位是一个像素，如果要放大显示的华，需要计算出来我们使用的单元相当于多少个像素，然后每次计算坐标时都得考虑到这个值，当现实区域发生变化时还得调整这个数值，非常麻烦，而且容易出错。

所以 Turtle 提供了一个设置我们自己坐标单位的方法 `setworldcoordinates`，它接受四个参数，分别是坐标系中，左下角的点 x坐标，y坐标，和 右上角的 x坐标、y坐标。

如果将左下角设置为 (-5, -5)，右上角设置为 (5, 5)，那么 Turtle 就会将坐标原点设置在屏幕中心，并将屏幕分割成 10 X 10 的方块，每个块的边长，相当于一个坐标单位，也就是说，当我们说将笔尖移动到 (3, 4) 这个坐标点时，Turtle 就会从屏幕中心向右移动三个单位，再向上移动4个单位。

这样就非常方便了，无论屏幕大小如何，像素大小如何，Turtle 都会按照我们的指令，做出正确的响应。

### 另一个问题是 两个偏移量 `xTranslate` 和 `yTranslate`

分别是这样计算得到的:

```python
self.xTranslate = -columnsInMaze/2
self.yTranslate = rowsInMaze/2
```

存在的意义就是从行和列值中，转化为 Turtle 坐标系的值，比如行列表示法中，(0, 0) 点，在我们变换后的 10 X 10 的坐标系中，对应的坐标点是 (-5, 5)。

因为我们查找数据时用行列表示法比较方便，但在坐标系中，以原点为基准表示比较方便。

## 总结

好了，关于 Turtle 实现的迷宫就介绍到这里，只是简单说明了实现思路，和孩子的互动，代码实现中还要需要细节和问题，限于篇幅，没有展开，有兴趣的读者可以下载源码，自己跑跑试试，也许还要更好玩的想法，欢迎在评论去交流。

我们学习代码不仅可以用来解决问题，完成工作，更多的时候还可以用了娱乐和陪伴孩子，在这个过程中，给予孩子的不仅仅是陪伴，还要处理问题的方式，以及生活的态度。

比心！

## 参考代码

> https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/mazegame
