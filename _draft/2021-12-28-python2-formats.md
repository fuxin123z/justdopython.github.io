---
layout: post
category: python
title: 字符串格式化，就服她……
tagline: by 李晓飞
tags:
  - Python
  - 字符格式化
  - 技巧
---
![封面](http://www.justdopython.com/assets/images/2021/12/formats/00.png)

字符串处理是编程中最基础的活动，几乎无处不用。

很多编程入门教材，也是用打印九九乘法表等字符串操作，作为练习的。

Python 中的字符串格式化可谓五花八门，提供多种选择的同时，也为选择增加了负担，有时用 C 风格的字符串，有时用 str.format，有时用 f-string。

今天我就聊聊这些方法的优略，看看谁最优。
<!--more-->
## 不老先驱

Python 中，最常用的字符串格式化方法是，采用 `%` 格式化操作符，了解 C 语言的同学，对这种方式可能比较习惯，这种字符串格式化方法也被称作 C 风格字符串格式化。

使用起来很简单，通过一些类型描述符，可以格式化数字，字符串等类型的值，例如：

```python
temp = 'Binary is %d, hex is %d'

a = 0b10111011
b = 0xc5f

print(temp % (a, b))

'''
输出为:
Binary is 187, hex is 3167
'''
```

再如：

```python
key = 'my_var'
value = 1.234
temp = '%-10s = %.2f'

print(temp % (key, value))

'''
输出为：
my_var    = 1.23
'''
```

- %-10s 表示替换字符串，并占位 10 个位置
- %.2f 表示替换小数，保留两位小数

虽然方便，在实践中，存在三个问题，我们来一一展开：

### 1 依赖顺序

要替换的变量，必须与字符串模板中代替换的位置保持一致，否则可能替换出错，甚至出现异常，例如在上面的例子中，将 key 和 value 调换位置：

```python
print(temp % (value, key))

'''
报错：
Traceback ...

TypeError: must be real number, not str
'''
```

报错信息显示，需要的是数字，而非字符串。

这个问题会导致编写代码时，需要耗费更多的时间来检查列表，特别是在模板比较复杂时，工作量会大大增加。

### 2 不灵活

如果需要调整下模板中的替换位置，那么所有使用模板的替换代码都要调整。

例如，需要增加一个显示信息：

```python
key = 'my_var'
value = 1.234
temp = '%-10s = %.2f #%d'

print(temp % (key, value))

'''
报错：
Traceback ...
TypeError: not enough arguments for format string
'''
```

去掉一个替换位置呢？

```python
key = 'my_var'
value = 1.234
temp = '%-10s'

print(temp % (key, value))


'''
报错：
Traceback ...
TypeError: not all arguments converted during string formatting
'''
```

可以看到只要是调整，必须调整参数结构。

### 3 重复

如果需要将一个值重复替换，那么就需要将替换位置和替换值重复多次：

```python
name = 'python'
print("%s %s %s" % (name, name, name))
```

首先这样写起来很麻烦，更麻烦的是，一定取值方式，或者模板方式发生的变化，就就需要改所有的地方。

例如，name 的取值变为 name.title

又如 模板中，需要占用 10 个字符，`%-10s`，那么所有的地方都得改。

## 勇于创新

鉴于 C 风格格式化有种种问题，Python 做出了一些扩展。

将参数用 dict 取代了 tuple，也就是不再受位置的限制了。

相应的，字符串模板中需要指定使用 dict 中的哪个属性作为替换：

```python
temp = '%(key)-10s = %(value).2f'

print(temp % {'key': 'my_var', 'value': 1.234})
```

虽然这样的改进，解决了位置依赖问题，但是，让代码更加不灵活了，因为需要再模板中定义替换属性名。

一旦发生了调整，改动的地方就更多了。

而且还会引入一个问题，就是，会让代码量更大，因为有时必须为了合成字符串，不得不创造一个 dict 变量：

```python
one = {
    'name': 'lily',
    'age': 25,
    'interest': 'movies'
}

temp = ('名字：%(name)s\n'
        '年龄：%(age)d\n'
        '兴趣：%(interest)s')

print(temp % one)
```

上面代码中，one 就是被创造处理，专门做字符串格式化的。

## 别有洞天

如果说 C 风格格式化有很多问题，那么 `str` 的 `format` 方法，可谓是别有洞天，是自 Python 3 加入的高级字符串格式化机制。

format 函数不再使用 % 操作符，只需要针对需要格式化的值，调用内置的 format 函数，传入这个值对于的格式，便可实现格式化处理。

```python
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)

b = 'my string'
formatted = format(b, '^20s')
print('*', formatted, '*')

'''
输出为:
1，234.57
*      my string       *
'''
```

其中 `^` 表示居中对齐。

如果有多个值需要替换，可以用 `{}` 预留出待替换的位置：

```python
key = 'my_value'
value = 1.234

formatted = '{:<10s} = {:.2f}'.format(key, value)
print(formatted)

'''
输出为:
my_value   = 1.23
'''
```

从以上代码可以看出，不仅可以用 `{}` 占位，而且可以使用 C 风格格式化中的语法。

不过 format 格式化法依然无法摆脱灵活性差和重复性的问题，这些方面和 C 风格格式化没有太大区别。

## 大道至简

从 Python 3.6 开始，引入了一个叫作 **插值格式化字符串**（interpolated format string），简称 f-string。

竟然可以解决以上所有问题，简约而不简单！

```python
key = 'my_value'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)

'''
输出为:
my_value = 1.234
'''
```

是不是太帅了，只要模板前加 `f`，然后将需要替换的值写用大括号包裹，写进去就好了。

眼尖的同学已经发现，这不是什么新技术，再 Linux Shell 编程中早就用到了。

有同学说，如果需要指定特殊格式怎么办？

不用担心，写起来一样简单：

```python
key = 'my_value'
value = 1.234

formatted = f'{key:<10} = {value:.2f}'
print(formatted)

'''
输出为:
my_value   = 1.23
'''
```

比起 C 风格格式化和 format 格式化，f-string 更灵活，因为无论是模板还是参数，在 f-string 这里都大道归一了，因为只需要写一遍，无论怎么调整，也只需要调整一次。

而我们日常使用时，直接将字符串写成 f-string 随即，便可完成格式化操作：

```python
key = 'my_value'
value = 1.234

print(f'{key:<10} = {value:.2f}')
```

更加节省了。

最让笔者感动的地方是，我不必为构造格式化额外定义变量了。

## 总结

一个问题总有很多种解决方案，太多，会让我们纠结选择，太少会让我们拘于形式，而仔细研究和扩展，必然会找到合适的便捷的价值巨大的解决方案。

Python 之所以大受欢迎，正是她不断地成长与精进，汲取精化，发展特长，只为让使用者更加便利。

正应了 ——

> 人生苦短，我用 Python ！

比心！
