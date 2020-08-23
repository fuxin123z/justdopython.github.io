---
layout: post
category: python
title: 如何优雅地解析命令行选项
tagline: by 轩辕御龙
tags:
  - python
---

# 如何优雅地解析命令行选项

随着我们编程经验的增长，对命令行的熟悉程度日渐加深，想来很多人会渐渐地体会到使用命令行带来的高效率。

自然而然地，我们自己写的很多程序（或者干脆就是脚本），也希望能够像原生命令和其他程序一样，通过运行时输入的参数就可以设定、改变程序的行为；而不必一层层找到相应的配置文件，然后还要定位到相应内容、修改、保存、退出……

想想就很麻烦好吗

<!--more-->

![01](http://www.justdopython.com/assets/images/2020/08/getopt/01.jpg)

## 1. 手动解析

所以让我们开始解析命令行参数吧~

在以前关于模块的文章中我们提到过`sys.args`这个变量，其中保存的就是调用当前脚本时传入的命令行参数。

我们先观察一下这个变量：

```python
# test_sys.py
import sys

print(sys.argv)
```

通过命令行调用：

```shell
$ python test_sys.py -d today -t now --author justdopython --country China --auto
```

得到如下输出结果：

```shell
['test_sys.py', '-d', 'today', '-t', 'now', '--author', 'justdopython', '--country', 'China', '--auto']
```

可见，`sys.argv`其实就是将命令行参数按空格切分，得到的一个字符串列表。此外，命令行参数的第一个就是当前运行的脚本名称。

我们如果想要提取出各个参数及其对应的值，首先得区分出命令行的长参数和短参数，它们分别由“--”和“-”开头作为标识。所以我们也以此作为判断长短参数的条件：

```python
import sys


for command_arg in sys.argv[1:]:
    if command_arg.startswith('--'):
        print("%s 为长参数" % command_arg)
    elif command_arg.startswith('-'):
        print("%s 为短参数" % command_arg)
```

测试结果：

```shell
$ python manually_parse_argv.py -d today -t now --author justdopython --country China --auto


-d 为短参数
-t 为短参数
--author 为长参数
--country 为长参数
--auto 为长参数
```

紧接着，我们需要在解析出长短参数这一步的基础上，再解析出对应的参数值：

```python
# manually_parse_argv.py
import sys


# 由于sys.argv的第一个变量是当前脚本名称，因此略过
for index, command_arg in enumerate(sys.argv[1:]):
    if command_arg.startswith('--'):
        try:
            value = sys.argv[1:][index+1]
            if not value.startswith('-'):
                print("%s 为长参数，参数值为 %s" % (command_arg, value))
                continue
        except IndexError:
            pass
        
        print("%s 为长参数，无参数值" % command_arg)

    elif command_arg.startswith('-'):
        try:
            value = sys.argv[1:][index+1]
            if not value.startswith('-'):
                print("%s 为短参数，参数值为 %s" % (command_arg, value))
                continue
        except IndexError:
            pass
        
        print("%s 为短参数，无参数值" % command_arg)
```

再测试一下：

```shell
$ python manually_parse_argv.py -d today -t now --author justdopython --country China --auto

-d 为短参数，参数值为 today
-t 为短参数，参数值为 now
--author 为长参数，参数值为 justdopython
--country 为长参数，参数值为 China
--auto 为长参数，无参数值
```

看起来还不错。

但是再看看我们的代码……真正的逻辑还没开始，反倒是为了解析命令行参数已经写了几十行代码。这一点都不pythonic——这还不包括一些其他关于异常情况的处理。

更何况是要在每个类似的程序中加入这么一段程序了。

## 2. getopt模块帮您忙

Python的好处就在于，生态过于丰富，几乎你要用到的每个功能，都已经有人为你写好了现成的模块以供调用。

衣来伸手饭来张口的日子除了能在梦中想想，在用Python写程序的时候也不是不可以奢望。

比如命令行参数解析，就有一个名为getopt的模块，既能够准确区分长短命令行参数，也能够恰当地提取命令行参数的值。

咱们先来康康：

```python
# test_getopt.py
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], 'd:t:', ["author=", "country=", "auto"])

print(opts)
print(args)
```

打印结果：

```shell
$ python test_getopt.py -d today -t now --author justdopython --country China --auto
[('-d', 'today'), ('-t', 'now'), ('--author', 'justdopython'), ('--country', 'China'), ('--auto', '')]
[]
```

下面我们来分别解释一下相关参数的含义。

`getopt`模块中的`getopt`函数用于解析命令行参数。

该函数接受三个参数：args，shortopts和longopts，分别代表“命令行参数”，“要接收的短选项”和“要接收的长选项”。

其中args和longopts均为字符串组成的列表，而shortopts则为一个字符串。

同样地，由于`sys.argv`的第一个值为当前脚本名称，所以多数情况下我们会选择向args参数传入`sys.argv[1:]`的值。

而shortopts这个参数接受的字符串则表示需要解析哪些短选项，字符串中每个字母均表示一个短选项：

```python
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], 'dt')

print(opts)
print(args)
```

输出结果：

```shell
$ python test_getopt.py -d  -t
[('-d', ''), ('-t', '')]
[]
```

当然，如果输入的参数少于预期，也不会导致解析失败：

```shell
$ python test_getopt.py  -t
[('-t', '')]
[]
```

但要是给出了预期之外的参数，就会导致模块抛错：

```shell
$ python test_getopt.py -d  -t -k
Traceback (most recent call last):
  File "test_getopt.py", line 11, in <module>
    opts, args = getopt.getopt(sys.argv[1:], 'dt')
  	...
    raise GetoptError(_('option -%s not recognized') % opt, opt)
getopt.GetoptError: option -k not recognized
```

这样的处理逻辑也符合我们使用命令的体验，可以简单地理解为“宁缺毋滥”。

如果短参数相应的字母后带了一个冒号:，则意味着这个参数需要指定一个参数值。`getopt`会将该参数对应的下一个命令行参数作为参数值（而不论下一个参数是什么形式）：

```python
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], 'd:t')

print(opts)
print(args)

# $ python test_getopt.py -d  -t
# [('-d', '-t')]
# []
```

此外，一旦`getopt`在预期接收到长短选项的位置没有找到以“--”或“-”开头的字符串，就会终止解析过程，剩下的未解析字符串均放在返回元组的第二项中返回。

```shell
$ python test_getopt.py -d d_value o --pattern -t
[('-d', 'd_value')]
['o', '--pattern', '-t']
```

类似地，longopts参数表示需要解析的长参数。

列表中的每一个字符串代表一个长参数：

```python
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], '', ["author", "country"])

print(opts)
print(args)

# $ python test_getopt.py --author  --country
# [('--author', ''), ('--country', '')]
# []
```

要解析带有参数值的长参数，还应在每个长参数后附带一个等于号（=），以标识该参数需要带值：

```python
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], '', ["author=", "country"])

print(opts)
print(args)

# $ python test_getopt.py --author justdopython --country
# [('--author', 'justdopython'), ('--country', '')]
# []
```

所以最终就得到了我们一开始的解析结果：

```python
import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], 'd:t:', ["author=", "country=", "auto"])

print(opts)
print(args)

# $ python test_getopt.py -d today -t now --author justdopython --country China --auto
# [('-d', 'today'), ('-t', 'now'), ('--author', 'justdopython'), ('--country', 'China'), ('--auto', '')]
# []
```

解析完成后，我们再从opts中提取相应的值即可。

### 懒人福音

`getopt`除了替我们节省了编写命令行参数解析代码的时间和精力，另一方面还可以让你在输入命令行参数时少打几个字母——当然，严谨来讲，我们并不建议此类行为。慎用，慎用！

`getopt`对长参数的解析支持前缀匹配，只要输入的参数能够与某个指定参数唯一匹配，同样能够完成预期解析。

```shell
$ python test_getopt.py -d today -t now --auth justdopython --coun China --auto
[('-d', 'today'), ('-t', 'now'), ('--author', 'justdopython'), ('--country', 'China'), ('--auto', '')]
[]
```

可以看到，`author`和`country`两个参数我们都只输入了一部分，但是`getopt`依然进行了正确的解析。

## 总结

本文讲解了使用Python解析命令行参数的两种方式，一种是略显笨重的手动解析，即自己编写程序自定义解析；另一种则是调用现成、且更加健壮的`getopt`模块来完成解析。

从此以后，我们终于可以摆脱繁琐的配置文件，用一种优雅简洁的方式来修改程序的行为了。

## 参考

[getopt --- C 风格的命令行选项解析器](https://docs.python.org/zh-cn/3/library/getopt.html)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-08-23-getopt-parse-command-arguments>