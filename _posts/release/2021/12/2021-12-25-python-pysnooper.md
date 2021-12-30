---
layout: post
category: python
title:  一行代码干掉 debug 和 print，助力算法学习
tagline: by 某某白米饭
tags:
  - pysnooper
---


在写算法的时候，总是要每行每个变量一个个的 debug，有时候还要多写几个 print，一道算法题要花好长时间才能理解。pysnooper 模块可以把在运行中变量值都给打印出来。

<!--more-->

### 模块安装

```python
pip3 install pysnooper
```

### 简单例子

下面是道简单的力扣算法题作为一个简单的例子

```python
import pysnooper

@pysnooper.snoop()
def longestCommonPrefix(strs):
    res = ''
    for i in zip(*strs):
        print(i)
        if len(set(i)) == 1:
            res += i[0]
        else
            break
    return res
 
if __name__ == 'main':
    longestCommonPrefix(["flower","flow","flight"])
```

结果：

``` python
3:38:25.863579 call         4 def longestCommonPrefix(strs):
23:38:25.864474 line         5     res = ''
New var:....... res = ''
23:38:25.864474 line         6     for i in zip(*strs):
New var:....... i = ('f', 'f', 'f')
23:38:25.865479 line         7         print(i)
('f', 'f', 'f')
23:38:25.866471 line         8         if len(set(i))==1:
23:38:25.866471 line         9             res+=i[0]
Modified var:.. res = 'f'
23:38:25.866471 line         6     for i in zip(*strs):
Modified var:.. i = ('l', 'l', 'l')
23:38:25.866471 line         7         print(i)
('l', 'l', 'l')
23:38:25.867468 line         8         if len(set(i))==1:
23:38:25.867468 line         9             res+=i[0]
Modified var:.. res = 'fl'
23:38:25.868476 line         6     for i in zip(*strs):
Modified var:.. i = ('o', 'o', 'i')
23:38:25.868476 line         7         print(i)
('o', 'o', 'i')
23:38:25.869463 line         8         if len(set(i))==1:
23:38:25.869463 line        11             break
23:38:25.869463 line        12     return res
23:38:25.869463 return      12     return res
Return value:.. 'fl'
Elapsed time: 00:00:00.008201
```

我们可以看到 pysnooper 把整个执行程序都记录了下来，其中包括行号， 行内容，变量的结果等情况，我们很容易的就看懂了这个算法的真实情况。并且不需要再使用 debug 和 print 调试代码。很是省时省力，只需要再方法上面加一行 @pysnooper.snoop()。

### 复杂使用

pysnooper 包含了多个参数，一起来看看吧

#### output

output 默认输出到控制台，设置后输出到文件，在服务器中运行的时候，特定的时间出现代码问题就很容易定位错误了，不然容易抓瞎。小编在实际中已经被这种问题困扰了好几次，每次都掉好多头发。

```python
@pysnooper.snoop('D:\pysnooper.log')
def longestCommonPrefix(strs):
```

示例结果:

![](https://files.mdnice.com/user/15960/9144370f-259c-431f-b2ae-d98db194c73b.png)

#### watch 和 watch_explode

watch 用来设置跟踪的非局部变量，watch_explode 表示设置的变量都不监控，只监控没设置的变量，正好和 watch 相反。

```python
index = 1
@pysnooper.snoop(watch=('index'))
def longestCommonPrefix(strs):
```

示例结果

没有加 watch 参数 

```python
Starting var:.. strs = ['flower', 'flow', 'flight']
00:12:33.715367 call         5 def longestCommonPrefix(strs):
00:12:33.717324 line         7     res = ''
New var:....... res = ''
```

加了watch 参数，就会有一个 Starting var:.. index

```python
Starting var:.. strs = ['flower', 'flow', 'flight']
Starting var:.. index = 1
00:10:35.151036 call         5 def longestCommonPrefix(strs):
00:10:35.151288 line         7     res = ''
New var:....... res = ''
```

#### depth

depth 监控函数的深度

```python
@pysnooper.snoop(depth=2)
def longestCommonPrefix(strs):
    otherMethod()
```

示例结果

```python
Starting var:.. strs = ['flower', 'flow', 'flight']
00:20:54.059803 call         5 def longestCommonPrefix(strs):
00:20:54.059803 line         6     otherMethod()
    00:20:54.060785 call        16 def otherMethod():        
    00:20:54.060785 line        17     x = 1
    New var:....... x = 1
    00:20:54.060785 line        18     x = x + 1
    Modified var:.. x = 2
    00:20:54.060785 return      18     x = x + 1
    Return value:.. None
00:20:54.061782 line         7     res = ''
```

监控的结果显示，当监控到调用的函数的时候，记录上会加上缩进，并将它的局部变量和返回值打印处理。

#### prefix

prefix 输出内容的前缀

```python
@pysnooper.snoop(prefix='-------------')
def longestCommonPrefix(strs):
```

示例结果

```python
-------------Starting var:.. strs = ['flower', 'flow', 'flight']
-------------00:39:13.986741 call         5 def longestCommonPrefix(strs):
-------------00:39:13.987218 line         6     res = ''
```

#### relative_time

relative_time 代码运行的时间

```python
@pysnooper.snoop(relative_time=True)
def longestCommonPrefix(strs):
```

示例结果

```python
Starting var:.. strs = ['flower', 'flow', 'flight']
00:00:00.000000 call         5 def longestCommonPrefix(strs):
00:00:00.001998 line         6     res = ''
New var:....... res = ''
00:00:00.001998 line         7     for i in zip(*strs):
```

#### max_variable_length

max_variable_length 输出的变量和异常的最大长度，默认是 100 个字符，超过 100 个字符就会被截断，可以设置为 `max_variable_length=None` 不截断输出

```python
@pysnooper.snoop(max_variable_length=5)
def longestCommonPrefix(strs):
```

示例结果

```python
Starting var:.. strs = [...]
00:56:44.343639 call         5 def longestCommonPrefix(strs):
00:56:44.344696 line         6     res = ''
New var:....... res = ''
00:56:44.344696 line         7     for i in zip(*strs):      
New var:....... i = (...)
```

### 总结

本文介绍了怎么使用 pysnooper 工具，pysnooper 不仅可以少一些 debug 和 print，更能帮助理解算法题。
