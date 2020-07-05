---
layout: post
category: python
title: 干掉公式 —— numpy 就该这么学
tagline: by 太阳雪
tags:
  - python100
---

机器学习和数据分析变得越来越重要，但在学习和实践过程中，常常因为不知道怎么用程序实现各种数学公式而感到苦恼，今天我们从数学公式的角度上了解下，用 python 实现的方式方法。
> 友情提示：不要被公式吓到，它们都是纸老虎
<!--more-->

## 关于 Numpy

NumPy 是使用 Python 进行科学计算的基础软件包。除其他外，它包括：

- 功能强大的N维数组对象
- 精密广播功能函数
- 集成 C/C+和Fortran 代码的工具
- 强大的线性代数、傅立叶变换和随机数功能

机器学习和数据分析，numpy 是最常用的科学计算库，可以用极简的、符合思维习惯的方式完成代码实现，为学习和实践提供了很大的便利

## 环境准备

创建虚拟环境（可省略），安装 numpy 包：

```bash
pip install numpy
```

测试安装：

```bash
>>> import numpy
>>>
```

在下面实践中，默认将 numpy 引用为 np：

```python
import numpy as np
...
```

## 基础运算

编程语言大多数运算都是针对简单数值的，复杂运算是通过相应的数据结构结合程序逻辑计算的。numpy 虽然是针对复杂数据结构（例如矩阵）构造的，但它提供了和简单数值计算一样方便的操作。

### 幂运算

幂运算的运算符为 `**` ，即两个星号（一个星号表示乘），例如计算 x 的平方：`x**2`，x 的立方：`x**3`，等等

开方，相当于计算 1/2 次方，即 `x**(1/2)` 或者 `x**0.5`，因为常用 numpy 提供了便捷函数，`sqrt`，例如对数字 x 开平方，就是 `np.sqrt(x)`.
> 实际上平方运算也有便捷方法：`np.square`

### 绝对值

绝对值表示一个数轴上的值距原点的距离，表示为 `|x|`，numpy 提供便捷方法 `abs` 来计算，例如 `np.abs(x)`，就为 x 的绝对值

## 理解向量和矩阵

线性代数是机器学习和数据分析的基础数学之一，而向量和矩阵式又是线性代数的基础概念，所以理解向量和矩阵非常重要。

### 向量

一般数据被分为标量和向量，标量比较容易理解，即数轴上的一个数值

向量直观的认识是一组数值，可以理解为一维数组，但是为啥常见定义表示：具有方向的数值，方向指的是啥？这个问题困扰了我很多年（苦笑）。实际是因为在开始学习线性代数时，直接从公式定理开始，而没有了解它的原理和来源。

向量的方向指得是，向量所在坐标系的原点指向该向量在坐标系中表示的点的方向，例如在平面直角坐标系中，向量 [1,2] 表示 x 轴为 1，y 轴为 2 的一个点，从原点，即 [0,0] 点指向这个点的方向，就是这个向量的方向，扩展的三维坐标系，再到 n 为坐标系（当然超过三位人类就比较难以理解了），向量元素的个数表示向量属于几维坐标系，但无论多少维，都可以画出原点指向向量点的方向。

因为线性代数研究的是向量及向量组（矩阵）的纯数学计算，所以丢弃了坐标系的概念，只保留了向量的样子，所以造成了向量难以理解的现象。

简单说，向量就是一个数值的数组。

### 矩阵

理解了向量，矩阵理解起来就容易了，相当于一组向量，即坐标系中的多个点的集合，矩阵运算，就相当于多个向量的运算或变换。

> 可能这里比较绕或冗余，先解释到这里，后面的文章中会进一步解释向量和矩阵的实际意义

### 初始化

numpy 中，提供了多种产生向量和矩阵的方法，例如用 array 可以将 python 数组初始化为 numpy 矩阵：

```python
m = np.array([(1,2,3),(2,3,4),(3,4,5)])
```

就可以创建一个 向量维度为 3，个数为 3 的矩阵

### 基本运算

numpy 特别擅长处理向量和矩阵的运算，例如乘法，即给向量中的每个数值乘以乘数，之间写代码的话，可以遍历向量，为每个值乘以乘数。

用 numpy 就简单很多：`x * 2`，就像做标量运算一样，感觉向量同一个数值一样。

- 加法 `x+2`，
- 减法 `x-2`
- 处罚 `x/2`

### 矩阵幂运算

向量、矩阵既然可以看成一个数，幂运算就很容易理解了，例如矩阵
![矩阵 m](http://www.justdopython.com/assets/images/2020/07/simplenumpy/01.png?2323)

m 平方就可以写成  `m**2`, 结果为：

![矩阵平方](http://www.justdopython.com/assets/images/2020/07/simplenumpy/02.png)

### 矩阵点积

不同维度的矩阵可以做乘法操作，但不是一般的乘法操作，操作被称为点积，为了用 numpy 表示，需要用 dot 函数，例如矩阵 m 和 n

![矩阵 m、n](http://www.justdopython.com/assets/images/2020/07/simplenumpy/03.png)

代码为 `m.dot(n)`，就会得到如下结果：

![矩阵点积](http://www.justdopython.com/assets/images/2020/07/simplenumpy/04.png)

### 求和与连乘

统计学公式中，求和运算很常见，例如对矩阵求和：
![矩阵求和](http://www.justdopython.com/assets/images/2020/07/simplenumpy/05.png)

表示对矩阵 m 中所有元素进行求和，nunpy 通过 `sum` 完成计算：
`m.sum()`

连乘和求和类似，将矩阵中所有元素做乘积运算:
![矩阵连乘](http://www.justdopython.com/assets/images/2020/07/simplenumpy/06.png)

numpy 通过 `prod` 完成计算，如矩阵 m 的连乘为 `m.prod()`

## 实践

了解了上面的各种基础运算后，做些实践

### 计算均值

向量均值公式为：
![向量均值公式](http://www.justdopython.com/assets/images/2020/07/simplenumpy/07.png)

分析公式，其中 n 为向量 x 的元素数量，numpy 的向量，通过 size 获取，后面是向量求和，用 sum 完成，最后代码如下：

```python
(1/x.size)*x.sum()
```

或者

```python
x.sum()/x.size
```

### 实现 Frobenius 范数

现在来个复杂点的，Frobenius 范数，公式如下:
![Frobenius 范数公式](http://www.justdopython.com/assets/images/2020/07/simplenumpy/08.png)

先不用纠结 Frobenius 公式的意义，我们只看如何用 python 实现，分析公式，可以看到，首先对矩阵的每个元素做平方运算，然后求和，最后对结果进行开方，那么就从里向外写

矩阵元素求和，根据前面所述，写成 `m**2`，会得到新的矩阵，然后求和，直接可写为：

```python
np.sqrt((m**2).sum())
```

借助 numpy 实现公式，极为简洁。

### 样本方差

我们在看一个公式：

![样本方差公式](http://www.justdopython.com/assets/images/2020/07/simplenumpy/09.png)

其中 ![样本方差公式](http://www.justdopython.com/assets/images/2020/07/simplenumpy/10.png)表示向量 x 的均值，上面计算过，那么套用起来就是：

```python
np.sqrt(((x-(x.sum()/x.size))**2).sum()/(x.size-1))
```

基本依据上面了解的写法可以理解和写出，不过括号有点多，如果不参考公式，估计看不清实现的啥，好在 numpy 将均值运算通过 mean 方法简化了，例如向量 x 的均值，可以写为：`np.mean(x)`，所以上面的代码可以简化为：

```python
np.sqrt(((x-np.mean(x))**2).sum()/(x.size-1))
```

上面公式实际上是样本标准差公式，对于标准差，numpy 提供了简便方法 std, 直接用 
`np.std(x)` 就可以计算，当然现在我们根据标准差公式：
![标准差](http://www.justdopython.com/assets/images/2020/07/simplenumpy/11.png)

很容易写出来 numpy 实现，赶紧试试吧。

### 欧拉距离

前面写模拟疫情扩散时，用到了欧拉距离，当时没有理解好 numpy 公式表达能力，所以计算时分了三步，现在如果要计算两个向量之间的欧拉距离，一行代码就能搞定，先复习下欧拉距离公式，向量 a 与 向量 b 的欧拉距离为：

![欧拉距离公式](http://www.justdopython.com/assets/images/2020/07/simplenumpy/12.png)

numpy 实现为：

```python
np.sqrt(((a-b)**2).sum())
```

由于欧拉距离应用广泛，所以 numpy 在线性代数模块中实现了，所以了解 numpy 实现数学公式的方法后，可以简化为：

```python
np.linalg.norm(a-b)
```

## 总结

numpy 是个博大精深的数学计算库，是 python 实现科学计算的基础，今天我们从数学公式的角度，了解了如何转换为 numpy 的代码实现，限于篇幅，虽然仅是 numpy 的冰山一角，但却可以成为理解 numpy 运算原理的思路，在数据分析或者机器学习，或者论文写作过程中，即使不了解 numpy 中简洁的运算，也可以根据数学公式写出代码实现，进而通过实践学习和了解 numpy 就更容易了

## 参考

- [https://blog.csdn.net/garfielder007/article/details/51386683](https://blog.csdn.net/garfielder007/article/details/51386683)
- [https://blog.csdn.net/robert_chen1988/article/details/102712946](https://blog.csdn.net/robert_chen1988/article/details/102712946)
- [https://mathtocode.com/](https://mathtocode.com/)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/simplenumpy>
