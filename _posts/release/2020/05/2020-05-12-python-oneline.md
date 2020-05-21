---
layout: post
category: python
title: 如果只写一行代码能实现什么？看完我彻底服了
tagline: by 極光
tags:
  - python
---

人生苦短，我用 Python。这句话大家应该相当熟悉了吧，那 Python 到底有多简单呢，今天就来带大家看看，如果只写一行代码，Python 可以实现什么？

<!--more-->

## 心形字符

这个比较容易理解，运行代码直接看结果：

```py
print('\n'.join([''.join([('Python技术'[(x-y)%len('Python技术')] if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-01.png)

## 9*9乘法口诀表

这个也简单，小时候上学天天都要背的，运行看结果：

```py
print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-02.png)

## 斐波拉契数列

这是个数列又称黄金分割数列，即数列从第3项开始，每一项都等于前两项之和。

```py
print([x[0] for x in [(a[i][0], a.append([a[i][1],a[i][0]+a[i][1]])) for a in ([[1,1]], ) for i in range(30)]])
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-03.png)

## 解决 FizzBuzz 问题

描述：给你一个整数 n. 从 1 到 n 按照下面的规则打印每个数：

1. 如果这个数被3整除，打印fizz；
2. 如果这个数被5整除，打印buzz；
3. 如果这个数能同时被3和5整除，打印fizz buzz。

```py
for x in range(1,101): print("fizz"[x%3*4:]+"buzz"[x%5*4:] or x)
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-04.png)

## Mandelbrot 图像

Mandelbrot 图实际上是由 Mandelbrot 集合构成的图像，Mandelbrot图像中的每个位置都对应于公式 N=x+y*i 中的一个复数。

```py
print('\n'.join([''.join(['*'if abs((lambda a: lambda z,c,n:a(a,z,c,n))(lambda s,z,c,n:z if n==0 else s(s,z*z+c,c,n-1))(0,0.02*x+0.05j*y,40))<2 else ' ' for x in range(-80,20)]) for y in range(-20,20)]))
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-05.png)

## 1000以内的素数

计算并输出1-1000之间的所有素数。

```py
print(' '.join([str(item) for item in filter(lambda x: not [x%i for i in range(2,x) if x%i==0],range(2,1001))]))
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-06.png)

## 八皇后问题

八皇后问题，一个古老而著名的问题，是回溯算法的典型案例。该问题由国际西洋棋棋手马克斯·贝瑟尔于 1848 年提出：在 8×8 格的国际象棋上摆放八个皇后，使其不能互相攻击，即任意两个皇后都不能处于同一行、同一列或同一斜线上，问有多少种摆法。

```py
[__import__('sys').stdout.write('\n'.join('.'*i+'Q'+'.'*(8-i-1) for i in vec)+"\n========\n") for vec in __import__('itertools').permutations(range(8)) if 8==len(set(vec[i]+i for i in range(8)))==len(set(vec[i]-i for i in range(8)))]
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-07.png)

## 生成迷宫

随机输出一个迷宫，看你能不能走出来。

```py
print(''.join(__import__('random').choice('\u2571\u2572') for i in range(50*24)))
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-08.png)

## 屏幕滚动输出

终端屏幕上无限滚动输出你定义的文字或字符。

```sh
python -c "while 1:import random;print(random.choice(' 一二三'), end='')"
```

![输出结果](http://www.justdopython.com/assets/images/2020/05/oneline/python-oneline-09.png)

## 总结

本文为大家介绍了如何通过 Python 写一行代码进行复杂的计算或者输出图像，是不是你也感觉到了 Python 的强大，这下又有在朋友面前装 X 的资本了。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/jiguang/oneline>