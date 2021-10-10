---
layout: post
title: Python异常还能写得如此优雅！
category: python
tagline: by 闲欢
tags: 
  - python
  - 异常
---


![封面](http://www.justdopython.com/assets/images/2021/10/retry/00.jpg)


在写程序时，我们会经常碰到程序出现异常，这时候我们就不得不处理这些异常，以保证程序的健壮性。

处理异常的版本有以下几种，你通常的做法是哪种？

![](http://www.justdopython.com/assets/images/2021/10/retry/01.jpg)

#### 不负责任版本

这种情况下，不作任何处理，任由程序报错，从而导致程序中断。

针对简单的程序，这样做没什么问题，大不了我遇到问题之后把问题解决，然后重新运行。但是如果是复杂的系统就会很麻烦了，可能你一个异常阻塞了系统的运行，带来灾难性的后果。

#### 简单处理版本

简单处理版本，就是加上异常捕获，在发生异常时记录日志，时候可以通过日志来定位异常。

```python
def do_something():
    pass
def log_error(xxx):
    pass

try:
   do_something()
except:
    log_error(xxxx)

```

#### 改进处理版本

对于简单处理版本做了改进，增加重试次数。这个在爬虫程序中比较常见，第一次请求超时，可能过一会再请求就成功了，所以重试几次可能会消除异常。

```python
attempts = 0
success = False
while attempts < 3 and not success:
    try:
        do_something()
        success = True
    except:
        attempts += 1
        if attempts == 3:
            break

```


但是这样做仍然不够优雅，你可能要在很多地方去写这种重试的硬编码，程序看起来乱糟糟的。

![](http://www.justdopython.com/assets/images/2021/10/retry/02.jpg)

今天就给大家介绍一个第三方模块 —— retrying。它是对程序中异常重试的一种优雅的解决方案。


#### 安装与使用

#### 安装

安装命令还是那么平淡无奇：

> pip install retrying


#### 使用

下面给大家介绍一下这个装饰函数有哪些可以使用的参数。

##### 生命不息，奋斗不止

retrying 提供一个装饰器函数 retry，被装饰的函数会在运行失败的情况下重新执行，默认一直报错就一直重试。

```python
import random
from retrying import retry

@retry
def do_something_unreliable():
    if random.randint(0, 10) > 1:
        print("just have a test")
        raise IOError("raise exception!")
    else:
        return "good job!"

print(do_something_unreliable())

```

运行这个程序，大家可以看到每次打印“just have a test”这句话的次数都不一样。这是由于我们程序中只要随机整数大于1就会打印并且抛出异常。但是由于我们有装饰器函数 retry，所以在发生异常就会重新再次执行方法，直到随机整数大于1，就会打印“good job！”。


##### 做人不能太固执

这种无休止地重试，简直是浪费生命，浪费资源。我们要建设绿色家园，所以不妨加点限制：

```python
# 最大重试次数
@retry(stop_max_attempt_number=5)
def do_something_limited():
    print("do something several times")
    raise Exception("raise exception")

do_something_limited()

```

##### 珍惜有限的时间

一寸光阴一寸金，寸金难买寸光阴。我们要珍惜有限的时间，所以不妨给我们的重试加个时间限制：

```python
# 限制最长重试时间（从执行方法开始计算）
@retry(stop_max_delay=5000)
def do_something_in_time():
    print("do something in time")
    raise Exception("raise exception")

do_something_in_time()

```

##### 驻足欣赏路上风景

人生匆匆数十载，不要一路狂奔而忘记欣赏路边的美景，有时候我们需要花点时间来欣赏一路的美景：

```python
# 设置固定重试时间
@retry(wait_fixed=2000)
def wait_fixed_time():
    print("wait")
    raise Exception("raise exception")

wait_fixed_time()

```

##### 给失败设个限

虽说我们需要屡败屡战的韧性，但是失败也要有个限度，不能在失败中度过一生：

```python
# 设置重试时间的随机范围
@retry(wait_random_min=1000,wait_random_max=2000)
def wait_random_time():
    print("wait")
    raise Exception("raise exception")

wait_random_time()

```

##### 有些人值得等待

茫茫人海中，我就是要等到那个对的人：

```python
# 根据异常重试
def retry_if_io_error(exception):
    return isinstance(exception, IOError)

# 设置特定异常类型重试
@retry(retry_on_exception=retry_if_io_error)
def retry_special_error():
    print("retry io error")
    raise IOError("raise exception")

retry_special_error()

```

我们自己定义一个函数，判断异常类型，然后将函数作为参数传给装饰函数 retry ，如果异常类型符合，就会进行重试。


##### 有些结果是我们希望见到的

人生并不是一帆风顺，有些时候我们会遇到挫折，这些挫折也许在一开始就是我们想要的：

```python
# 通过返回值判断是否重试
def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    # return result is None
    if result =="111":
        return True


@retry(retry_on_result=retry_if_result_none)
def might_return_none():
    print("Retry forever ignoring Exceptions with no wait if return value is None")
    return "111"

might_return_none()

```

这里我们定义了一个判断返回值的函数，然后将这个函数作为参数传给 retry 装饰函数。当结果返回是“111”时，就会一直重试执行 `might_return_none` 函数。


##### 生活丰富多彩，并不单调

我们的生活是丰富多彩的，从来都没有很单调。所以上面这些参数，我们可以随意组合使用，并不限定每次只能用一个。比如你可以限定遇到 `IOError` 时进行重试，并且重试次数最多5次。


### 总结

人生不能再重来，但是Python可以重试！

我已经将`retrying` 这个装饰函数的使用方法毫无保留地奉献给各位看官了，赶快用起来吧！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan)