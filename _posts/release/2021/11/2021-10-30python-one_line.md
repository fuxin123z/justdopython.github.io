---
layout: post
category: python
title: 
tagline: by 潮汐
tags: Python 一行代码的神奇之处！！
  - Python技巧
  - 编程
---

你们知道今天聊聊关于 Python 一行代码的神奇之处！！！


### 十六进制转十进制

```python

decimal = int('1010', 5)
print(decimal)   #130

```
输出：
```python
130
```

### 转换大小写字母

#### 转换大写字母
```python
# 转换大小写字母
str = "hi Python".upper()
print(str) #HI PYTHON
```
输出：
```python
HI PYTHON
```

#### 转换小写字母

```python
# 转换小写字母
str_lower1 = "HI PYTHON".lower()
print(str_lower1)

str_lower2 = "HI PYTHON".casefold()
print(str_lower2)
```
输出：

```python
hi python
hi python
```

### 求一个数字的因数

```python
import math

fact_5 = math.factorial(5)
print(fact_5)
```
输出：
```python
120
```

### 从列表中得到一个最长的字符串
```python
words = ['Hello', 'Python', 'Hello', 'world']
print(max(words, key=len))
```
输出：
```python
Python
```
### 用 print()写入文件
```python
print("Hello, World!", file=open('test.txt', 'w'))
```

###  获取日期
```python
import time;
print(time.ctime())
```
输出：
```python
Sun Oct 30 22:52:41 2021
```

### 从字符串中删除数字
```python
test_str = ''.join(list(filter(lambda x: x.isalpha(), 'abc4532def4fg56vcg2')))
print(test_str)
```

输出：
```python
abcdeffgvcg
```
### 一行代码求 n 个连续数之和
```python
# 第一种方式
n = 50
sum_n1 = sum(range(0, n+1))
print(sum_n1)
#第二种方式
sum_n2 = n*(n+1)//2
print(sum_n2)
```
### 求某字符串中某个字符出现的频率
```python
print("hello python".count('l')) # 2
```

### 从列表中删除重复元素
```python
list(set['p','y','t','h','o','n'])
```
### 按"键"对字典进行排序
```python
# d = {'five': 5, 'one': 1, 'four': 4, 'eight': 8}  
{key:d[key] for key in sorted(d.keys())}  
# {'eight': 8, 'five': 5, 'four': 4, 'one': 1}
```
### 按值对字典进行排序
```python
# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}  
{k: v for k, v in sorted(x.items(), key=lambda item: item[1])}  
# {0: 0, 2: 1, 1: 2, 4: 3, 3: 4}
```

### 过滤列表中的偶数
```python
list(filter(lambda x: x%2 == 0, [1, 2, 3, 4, 5, 6] ))  
# [2, 4, 6]
```
### 总结

关于 Python 小技巧-一行代码的操作还很多，后面咱们慢慢探索，希望大家一起进步。
