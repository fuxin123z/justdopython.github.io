---
layout: post
title: 贼好玩！几行代码将童年游戏搬上屏幕！
category: python
tagline: by 闲欢
tags: 
  - python
  - python游戏
---



![封面](http://www.justdopython.com/assets/images/2021/10/freegames/00.jpg)


80后和90后的小伙伴们，你们是否还记得这个小小的掌上游戏机？

![掌上游戏机](http://www.justdopython.com/assets/images/2021/10/freegames/01.jpg)

没有玩过这个游戏机的小伙伴的童年是不完整的！

在那个物质匮乏的年代，没有 Switch 游戏机，没有手机，也没有 pad，我们只有掌上俄罗斯和小霸王学习机！

看到这个图片，是不是勾起了童年的记忆？

还想不想再玩一下，回味童年的感觉？

没问题！这就送给你！

<!--more-->

最近在浏览 GitHub 开源项目的时候，无意中发现了一个神奇的项目 —— free-python-games 。大家看这个项目名称，肯定能猜到这个项目的大致内容，跟 python 和 游戏有关。

没错，这个项目包含了好多我们小时候在掌上游戏机玩的小游戏，你只要几行代码就可以在电脑上开始玩。作为上班偶尔的摸鱼娱乐项目还是很不错的。


### 安装

#### 安装包

第一步，我们需要安装这个开源包：

> pip install freegames

#### 使用命令

我们可以通过下面的命令来查看命令行帮助：

> python -m freegames --help

运行命令后，我们可以看到命令行输出：

```python
usage: freegames [-h] {list,copy,show} ...

Free Python Games

positional arguments:
  {list,copy,show}  sub-command help
    list            list games
    copy            copy game source code
    show            show game source code

optional arguments:
  -h, --help        show this help message and exit

Copyright 2017 Grant Jenks


```

我们可以看到这里有 list，copy，show 操作，分别是列举游戏列表、复制游戏源码、展示游戏源码等。

下面我们使用一下 list 命令：

> python -m freegames list

我们可以看到小游戏列表：

```python
ant
bagels
bounce
cannon
connect
crypto
fidget
flappy
guess
life
maze
memory
minesweeper
pacman
paint
pong
simonsays
snake
tictactoe
tiles
tron

```

运行游戏也非常简单：

> python -m freegames.snake

下面是运行贪吃蛇的命令，运行命令之后，就会弹出一个 GUI 小方框来呈现贪吃蛇游戏了，我们只需要使用键盘的方向键就可以愉快地玩耍了。

至于其他的复制、查看代码之类的，由于每个小游戏的代码就一个文件，代码量也不多，大家可以到这个开源项目去拷贝源代码自己修改运行即可。



### 有哪些小游戏？

话不多说，我们先来看看这个项目里面有哪些小游戏。

#### Paint

画图。你只需要用鼠标在画布上点击一下代表开始，然后再点击一下代表结束，就可以画一条线段，通过线段来画画。

通过键盘可以控制线段的颜色（需要将键盘切换到大写字母模式）。

![paint](http://www.justdopython.com/assets/images/2021/10/freegames/02.gif)

#### Snake

贪吃蛇。这个不用介绍，大家应该都知道是什么游戏了。通过键盘的方向键就可以控制方向。

![snake](http://www.justdopython.com/assets/images/2021/10/freegames/03.gif)

#### Pacman

吃豆人。使用键盘操纵黄色的小饼饼吃完所有的小白点就算过关。但是不能碰到那四个移动的红饼饼。

![pacman](http://www.justdopython.com/assets/images/2021/10/freegames/04.gif)

#### Cannon

射击。通过鼠标在屏幕上点击来确定石头发射的方向，你需要在那些蓝色的移动物体移动到左侧之前把他们都消灭掉。

![cannon](http://www.justdopython.com/assets/images/2021/10/freegames/05.gif)

#### Flappy

小雷电。这个小游戏跟雷电类似，你需要上下移动以防止被从右往左移动的黑色大圆饼触碰到。

![flappy](http://www.justdopython.com/assets/images/2021/10/freegames/06.gif)

#### Tiles

拼图。开局给你一个乱序的数字拼图，中间留一个空格，你需要将这些数字按从小到大、从下向上的顺序排列起来。点击空格旁边的数字，就可以移动数字到空格。

![tiles](http://www.justdopython.com/assets/images/2021/10/freegames/07.gif)

还有很多个其他的小游戏，这里就不一一列举了，大家自己去探索吧！这些小游戏够你玩好长时间了。


### 总结

作为 Pythoner，不能只想着玩这些小游戏摸鱼，我们需要学习怎么设计和实现这些小游戏。这也是这个项目的初衷——帮助初学者学习 Python。源码也在那里，你可以自己拿来随意修改。作者也在一些游戏上设置了空实现（比如第一个画线的游戏，作者预留了一些实现各种形状的空函数），留待大家自己去完成。

希望大家在找回童年乐趣的同时，也能学到知识！

