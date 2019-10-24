---
layout: post
title: 第43天：python statistics模块
category: python statistics
copyright: python
tagline: by 千阳
tags:
    -python100
---

本节介绍 Python 中的另一个常用模块 —— statistics模块，该模块提供了用于计算数字数据的数理统计量的函数。它包含了很多函数，具体如下表：

| 名称 | 描述 
| - | :-: 
| mean() | 数据的算术平均数（“平均数”）
| harmonic_mean() | 数据的调和均值
| median() | 数据的中位数（中间值）
| median_low() | 数据的低中位数
| median_high()| 数据的高中位数
| median_grouped() | 分组数据的中位数，即第50个百分点
| mode() | 离散的或标称的数据的单模

<!--more-->

### mean(data)函数

`mean(data)`函数用于计算一组数字的平均值，参数 data 可以是多种形式的，比如 int 型数组或 decimal 型数组等。举例说明函数的具体用法：

```
>>> statistics.mean([1, 2, 3, 4, 5])
3

>>> from fractions import Fraction as F
>>> statistics.mean([F(4, 7), F(4, 21), F(5, 4), F(1, 4)])
Fraction(95, 168)

>>> from decimal import Decimal as D
>>> statistics.mean([D("0.5"), D("0.78"), D("0.88"), D("0.988")])
Decimal('0.787')
```

### harmonic_mean(data)函数

调和平均数又称倒数平均数，是平均数的一种。  `harmonic_mean(data)`函数用于求调和平均数，是总体各统计变量倒数的算术平均数的倒数。例如：

```
>>> statistics.harmonic_mean([4, 5, 7])
5.0602409638554215
```

### median(data)函数

`median(data)`函数用于计算一组数据的中值。如果数据的个数是单数，则中值是中间的数；如果数据的个数是复数，则中值是中间两个数的平均数。例如：

```
>>> statistics.median([1, 4, 7])
4
>>> statistics.median([1, 4, 7, 10])
5.5
```

### median_low(data)函数

`median_low(data)`函数用于计算一组数据的中小值。如果数据的个数是单数，则中小值是中间的数；如果数据的个数是复数，则中小值是中间两个数中最小的数。例如：

```
>>> statistics.median_low([1, 4, 7])
4
>>> statistics.median_low([1, 4, 7, 10])
4
```

### median_high(data)函数

`median_high(data)`函数用于计算一组数据的中大值。如果数据的个数是单数，则中大值是中间的数；如果数据的个数是复数，则中大值是中间两个数中最大的数。例如：

```
>>> statistics.median_high([1, 4, 7])
4
>>> statistics.median_high([1, 4, 7, 10])
7
```

### median_grouped(data, interval=1)函数

`median_grouped(data, interval=1)`函数用于计算分组连续数据的中位数。其中 interval 表示数据之间的间隔，即组距。此函数计算方法较复杂，可参考公式`中位数=中位数所在组下限+{[(样本总数/2-到中位数所在组下限的累加次数)/中位数所在组的次数]*中位数的组距}`,如果数据是空的会报 StatisticsError 错误。例如：

```
>>> statistics.median_grouped([1, 2, 2, 3, 4, 4, 4, 4, 4, 5])
3.7
>>> statistics.median_grouped([3, 4, 4, 5, 6], interval=1)
4.25
>>> statistics.median_grouped([1, 3, 5, 5, 7], interval=2)
4.5
```
示例说明：
```
[1, 2, 2, 3, 4, 4, 4, 4, 4, 5]中位数在4这个分组里面 
默认组距为1
所在分组的下限为3.5
样本总数为10
4分组里有5个数
小于3.5的有4个数
所以中位数为：3.5+(10/2-4)/5*1=3.5+1/5=3.7
```

### mode(data)函数

`mode(data)`函数用于计算一组数据的众数，即在数据中出现次数最多的数。例如：

```
>>> statistics.mode([1, 1, 2, 3, 3, 3, 3, 4])
3
>>> statistics.mode(["red", "blue", "blue", "blue", "green", "green", "red"])
'blue'
```

## 总结

本节给大家介绍了 Python 中 statistics 模块的常用操作，在实际开发中方便对数据进行灵活的处理，对于实现数据统计的功能提供了支撑。

> 示例代码：[Python-100-days-day043](https://github.com/JustDoPython/python-100-day/tree/master/day-043)

参考
[1] https://docs.python.org/3.7/library/statistics.html