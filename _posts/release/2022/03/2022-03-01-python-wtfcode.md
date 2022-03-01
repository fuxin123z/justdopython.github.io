---
layout: post
title: 那些让人直呼卧槽的Python代码
category: python
tagline: by 闲欢
tags: 
  - python
  - code
  - 代码
---


![封面](http://www.justdopython.com/assets/images/2022/03/wtfcode/0.jpg)


Python 是一个设计优美的解释型高级语言, 它提供了很多能让程序员感到舒适的功能特性。 但有的时候, Python 的一些输出结果对于初学者来说似乎并不是那么一目了然。

如果您是一位经验比较丰富的 Python 程序员, 你可以尝试挑战看是否能一眼看出运行的结果。

<!--more-->

### 只运行一次？

下面的代码，会运行几次？

```python
for i in range(4):
    print(i)
    i = 10

```

运行之后，输出：
```python
0
1
2
3
```
What? 难道不是输出 `0` ？

原理解析：

- 由于循环在 Python 中工作方式, 赋值语句 i = 10 并不会影响迭代循环, 在每次迭代开始之前, 迭代器(这里指 range(4)) 生成的下一个元素就被解包并赋值给目标列表的变量(这里指 i)了。


### 捣蛋的 hash

```python
some_dict = {}
some_dict[5.5] = "Ruby"
some_dict[5.0] = "JavaScript"
some_dict[5] = "Python"
print(some_dict[5.5])
print(some_dict[5.0])
print(some_dict[5])
```

运行之后输出：

```python
Ruby
Python
Python
```
原理解析：

- Python 字典通过检查键值是否相等和比较哈希值来确定两个键是否相同。
- 当执行 some_dict[5] = "Python" 语句时, 因为Python将 5 和 5.0 识别为 some_dict 的同一个键, 所以已有值 "JavaScript" 就被 "Python" 覆盖了


### 到处返回

```python
def some_func():
    try:
        return 'from_try'
    finally:
        return 'from_finally'

print(some_func())
```

运行之后输出：

```python
from_finally
```

难道不是 `from_try` ？

原理解析：

- 当在 "try...finally" 语句的 try 中执行 return, break 或 continue 后, finally 子句依然会执行。
- 函数的返回值由最后执行的 return 语句决定， 由于 finally 子句一定会执行, 所以 finally 子句中的 return 将始终是最后执行的语句。

### 非也非也

```python
print('something' is not None)
print('something' is (not None))
```

运行结果：

```python
True
False
```

原理解析：

- is not 是个单独的二元运算符, 与分别使用 is 和 not 不同。
- 如果操作符两侧的变量指向同一个对象, 则 is not 的结果为 False, 否则结果为 True 。

### 从有到无

```python
some_list = [1, 2, 3]
some_dict = {
    "key_1": 1,
    "key_2": 2,
    "key_3": 3
}
some_list = some_list.append(4)
some_dict = some_dict.update({"key_4": 4})
print(some_dict)
print(some_list)
```

运行结果：

```python
None
None
```

原理解析：

- 大多数修改序列/映射对象的方法, 比如 list.append, dict.update, list.sort 等等，都是原地修改对象并返回 None。 


### 同人不同命

先来看一个程序片段：

```python
a = [1, 2, 3, 4]
b = a
a = a + [5, 6, 7, 8]
print(a)
print(b)
```

运行之后结果：

```python
[1, 2, 3, 4, 5, 6, 7, 8]
[1, 2, 3, 4]
```

再来看另一个程序片段：

```python
a = [1, 2, 3, 4]
b = a
a += [5, 6, 7, 8]
print(a)
print(b)
```

运行之后结果：

```python
[1, 2, 3, 4, 5, 6, 7, 8]
[1, 2, 3, 4, 5, 6, 7, 8]
```

按照常规理解来说，这两个程序片段返回的结果应该是一样的？

原理解析：

- `a += b` 并不总是与 `a = a + b` 表现相同， 类实现运算符 `=` 运算符的方式也许是不同的, 列表就是这样做的。

- 表达式 `a = a + [5,6,7,8]` 会生成一个新列表, 并让 `a` 引用这个新列表, 同时保持 `b` 不变。

- 表达式 `a += [5,6,7,8]` 实际上是使用的是 "extend" 函数, 所以 `a` 和 `b` 仍然指向已被修改的同一列表。


### 总结

看了这些代码的运行结果之后，有没有直呼 WC ？有的话点个赞吧！

是 Python 老手也很有可能被这些代码给迷住，很难全对。这些代码就像是那些行测里面的逻辑题，很容易被表面迷惑！但是运行之后，看看其中的原理，对我们学习 Python 也是有很大帮助的！