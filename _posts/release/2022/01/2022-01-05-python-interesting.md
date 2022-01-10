---
layout: post
category: python
title: 涨姿势！这些鲜为人知的 Python 骚操作你知道几个
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/01/interesting/logo.png)

众所周知，Python 以简洁著称，这个从我们写的第一行 Python 代码中就能看出来。今天派森酱就给大家整理了一些经典的一行代码操作，可能有些你还不知道，但对你未来的工作（装逼）肯定有大用处。

## 0x01 进制转换

平时的编码过程中，进制转换是非常常用的一个功能，尤其是涉及到一些算法的时候更是频繁。事实上 Python 已经内置了各个进制转换的 Api，咱们直接调用即可。

```python
In [1]: int('1100', 2)
Out[1]: 12

In [2]: int('30', 8)
Out[2]: 24

In [3]: int('ac9', 16)
Out[3]: 2761
```
## 0x02 斐波纳契数列

斐波纳契数列是一个很经典的数列，其通项公式为第一项和第二项都为 1，从第三项开始，每一项都等于前两项之和。

```python
In [4]: fibonacci = lambda x: x if x <= 1 else fibonacci(x - 1) + fibonacci(x - 2)

In [5]: fibonacci(15)
Out[5]: 610
```

## 0x03 快速排序

快速排序是初级工程师常考的一个算法题，整个算法写下来的话基本都需要八九行，来看看 Python 是如何一行代码搞定快速排序的。

```python
In [6]: quick_sort = lambda l: l if len(l) <= 1 else quick_sort([x for x in l[1:] if x < l[0]]) + [l[0]] + quick_sort([x for x in l[1:] if x >= l[0]])

In [7]: quick_sort([18, 20, 12, 99, 200, 59, 66, 34, 22])
Out[7]: [12, 18, 20, 22, 34, 59, 66, 99, 200]
```

## 0x04 写入文件

文件操作也是我们常用的操作之一，但你见过用 print 函数来写入文件的么。

```python
print("Hello, Python!", file=open('file.txt', 'w'))
```

## 0x05 字母异位词

顾名思义，字母异位词就是通过交换单词中字母的顺序，两个单词最终是一样的。

```python
In [9]: from collections import Counter

In [10]: s1, s2 = 'apple', 'orange'

In [11]: 'anagram' if Counter(s1) == Counter(s2) else 'not an anagram'
Out[11]: 'not an anagram'
```

## 0x06 矩阵转换

对于数据分析工作者，经常会接触到矩阵，那么就需要熟悉对矩阵的各种操作。而矩阵转换就是常规操作之一。

```python
In [12]: num_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

In [13]: result = list(list(x) for x in zip(*num_list))

In [14]: result
Out[14]: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

## 0x07 字典数

虽然现在很多常用的算法都被封装成 Api 直接调用就好了，但并不意味着我们的工作就不需要写算法了。在写算法的过程中会用到一些常见的字典数，比如大写字母、小写字母、数字等。而这些 Python 都考虑到了，直接调用即可。

```python
In [15]: import string

In [16]: string.ascii_lowercase
Out[16]: 'abcdefghijklmnopqrstuvwxyz'

In [17]: string.ascii_uppercase
Out[17]: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

In [18]: string.digits
Out[18]: '0123456789'
```

## 0x08 合并列表

在对接外部接口或者数据处理时，嵌套列表是非常常见的数据结构，但显然整合成一个列表更容易处理。

```python
In [19]: num_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

In [20]: result = [item for sublist in num_list for item in sublist]

In [21]: result
Out[21]: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## 0x09 推导式

推导式是 Python 的精华所在，极大的方便了我们创建列表和字典。

```python
In [22]: num_list = [num for num in range(0, 10)]

In [23]: num_list
Out[23]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [24]: num_set = {num for num in range(0, 10)}

In [25]: num_set
Out[25]: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

In [26]: num_dict = {x: x * x for x in range(1, 5)}

In [27]: num_dict
Out[27]: {1: 1, 2: 4, 3: 9, 4: 16}
```


## 总结

今天派森酱带大家一起梳理了一些看起来比较有用（装逼）的一行代码操作，方便小伙伴们在以后的工作中提高工作效率，更愉快的摸鱼。

关于 Python 的简洁操作，你还有什么独家秘笈想和大家分享呢，评论区可以多多交流哦～