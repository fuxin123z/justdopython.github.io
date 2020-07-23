---
layout: post     
title:  Python 排序了解一下？        
category: Python 排序了解一下？ 
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

排序是每个开发人员都需要掌握的技能。排序是对程序本身有一个全面的理解。不同的排序算法很好地展示了算法设计上如何强烈的影响程序的复杂度、运行速度和效率。今天的文章和谈谈大家都熟悉的各种排序使用 Python 如何实现，废话就不多说啦，开干！

<!--more-->

### 选择排序

选择排序一般是将初始值设为初始值，再循环后面每个元素与第一个元素比较，最终筛选出一个最小或最大值，最后将有序的数值排在前面，每次选择当前序列的最小值，将其与当前序列的第一个元素交换位置，每迭代一次，当前序列长度减一。迭代结束，即可得到有序序列。
实现代码如下：

```python
def select_s(data):
    # 第一层循环：取出数组中的每个元素
    for i in range(len(data)):
        temp = i   # 拿取一个元素用来比较
        # 第二层循环：从第i后面的一个值开始循环，与data[i]进行比较
        for j in range(i+1,len(data)):
            if data[j] < data[temp]:
                data[temp], data[j] = data[j], data[temp]
    print(data)
```

**调用运行结果：**

```
if __name__ == '__main__':
    data = [14, 31, 14, 6, 18, 24, 2, 40]
    select_s(data)
```
**输出结果：**

`[2, 6, 14, 14, 18, 24, 31, 40]`

### 插入排序

插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，算法适用于少量数据的排序，时间复杂度为O(n^2)。是稳定的排序方法。

插入算法把要排序的数组分成两部分：第一部分包含了这个数组的所有元素，但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部分就只包含这一个元素（即待插入元素）。在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部分中。

![插入排序思路](https://imgkr.cn-bj.ufileos.com/4e054069-f53c-4d8a-bf86-471defa3f2ee.gif)

**实现代码如下：**

```python
def insert_s(data):
    # 第一层循环： 从第二个元素开始循环取出元素，取出的元素再与有序区元素进行比较
    for i in range(1,len(data)):
        temp = data[i]
        j = i-1
        while j>=0 and temp < data[j]:
            data[j+1] = data[j]    
            j = j-1    # 在与前面一个元素进行比较，所以j 需要减1
        # 当j = -1 就跳出循环，将temp值赋给第一个值，即data[0]
        data[j+1] = temp
    print(data)
```

**调用运行结果：**

```python
if __name__ == '__main__':
    data = [12, 3, 13, 56, 10, 22, 2, 40]
    insert_s(data)
```

**输出结果：**

`[2, 3, 10, 12, 13, 22, 40, 56]`

### 冒泡排序

冒泡排序（顺序形式），从左向右，两两比较，如果左边元素大于右边，就交换两个元素的位置。

其中，每一轮排序，序列中最大的元素浮动到最右面。也就是说，每一轮排序，至少确保有一个元素在正确的位置。

这样接下来的循环，就不需要考虑已经排好序的元素了，每次内层循环次数都会减一。

其中，如果有一轮循环之后，次序并没有交换，这时我们就可以停止循环，得到我们想要的有序序列了。

![冒泡排序思路](https://imgkr.cn-bj.ufileos.com/e12f9a67-4555-4beb-bb56-2dbfe168ccef.gif)

```python
def insert_s(data):
    # 第一层循环： 从第二个元素开始循环取出元素，取出的元素再与有序区元素进行比较
    for i in range(1,len(data)):
        temp = data[i]
        j = i-1
        while j>=0 and temp < data[j]:
            data[j+1] = data[j]    
            j = j-1    # 在与前面一个元素进行比较，所以j 需要减1
        # 当j = -1 就跳出循环，将temp值赋给第一个值，即data[0]
        data[j+1] = temp
    print(data)
```

**调用运行结果：**

```python
if __name__ == '__main__':
    data = [12, 3, 13, 56, 10, 22, 2, 40]
    insert_s(data)
```
**输出结果：**

`[2, 3, 10, 12, 13, 22, 40, 56]`

### 快速排序

首先要打乱序列顺序，以防算法陷入最坏时间复杂度。所以快速排序使用 “分而治之” 的方法。 

对于一串序列，首先从中选取一个数，凡是小于这个数的值就被放在左边，凡是大于这个数的值就被放在右边。然后，继续对左右两摞进行快速排序。

直到进行快速排序的序列长度小于 2 （即序列中只有一个值或者空值）。

![快速排序思路](https://imgkr.cn-bj.ufileos.com/61373202-e4d0-42ee-a216-e9adf75f7f53.gif)

**代码如下：**

```python
# 快速排序
def partition(data, left, right):
    temp = data[left]
    while left < right:
        # 如果最右边的值大于中间值，则最右边值往后退一个位置，反之，就将值赋值给最左边位置
        while left < right and data[right] >= temp:
            right = right - 1
        data[left] = data[right]
        # 如果最左边的值小于中间值，则最左边值往前进一个位置，反之，就将值赋值给最右边位置
        while left < right and data[left] <= temp:
            left = left + 1
        data[right] = data[left]
    # 循环结束，即可定位到中间位置，将初始值，赋值到这个位置
    data[left] = temp
    return left


def quick_sort(data, left, right):
    if left < right:
        mid = partition(data, left, right)
        quick_sort(data, left, mid)
        quick_sort(data, mid + 1, right)
```
  
### 总结

今天的文章主要是使用 Python 实现各大排序程序，以及排序算法实现思路的梳理，自己学习的同时给大家整理思路！


> 示例代码 [Python 排序了解一下？](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/python_sort)