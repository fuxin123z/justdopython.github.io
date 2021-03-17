---
layout: post
title: 开眼界！Python 遍历文件可以这样做！
category: python
tagline: by 闲欢
tags: 
  - python
  - 文件
---

Python 对于文件夹或者文件的遍历一般有两种操作方法，一种是至二级利用其封装好的 walk 方法操作：

```python

import os
for root,dirs,files in os.walk("/Users/cxhuan/Downloads/globtest/hello"):
    for dir in dirs:
        print(os.path.join(root, dir))
    for file in files:
        print(os.path.join(root, file))

```

上面代码运行结果如下：

```
/Users/cxhuan/Downloads/globtest/hello/world
/Users/cxhuan/Downloads/globtest/hello/.DS_Store
/Users/cxhuan/Downloads/globtest/hello/hello3.txt
/Users/cxhuan/Downloads/globtest/hello/hello2.txt
/Users/cxhuan/Downloads/globtest/hello/hello1.txt
/Users/cxhuan/Downloads/globtest/hello/world/world1.txt
/Users/cxhuan/Downloads/globtest/hello/world/world3.txt
/Users/cxhuan/Downloads/globtest/hello/world/world2.txt

```

上述程序，将 os.walk 读取到的所有路径 root 、目录名 dirs 与文件名 files ，也就是三个文件数组利用 foreach 循环输出。join方法就是将其路径与目录名或者文件名连接起来，组成一个完整的目录。

另一种是用递归的思路，写成下面的形式：

```python

import os
files = list()
def dirAll(pathname):
    if os.path.exists(pathname):
        filelist = os.listdir(pathname)
        for f in filelist:
            f = os.path.join(pathname, f)
            if os.path.isdir(f):
                dirAll(f)
            else:
                dirname = os.path.dirname(f)
                baseName = os.path.basename(f)
                if dirname.endswith(os.sep):
                    files.append(dirname+baseName)
                else:
                    files.append(dirname+os.sep+baseName)


dirAll("/Users/cxhuan/Downloads/globtest/hello")
for f in files:
    print(f)

```

运行上面代码，得到的结果和上面一样。

这两种方法都没问题，就是写起来比较麻烦，特别是第二种，一不小心还有可能写出 bug 。

今天我们来介绍第三种方法——利用 glob 模块来遍历文件。


### 简介

glob 是 python 自带的一个操作文件的模块，以简洁实用著称。由于这个模块的功能比较简单，所以也很容易上手和使用。它主要用来查找符合特定规则的文件路径。使用这个模块来查找文件，只需要用到`*`、`?` 和 `[]` 这三个匹配符：

```
 * ： 匹配0个或多个字符；
 ? ： 匹配单个字符；
 [] ：匹配指定范围内的字符，如：[0-9]匹配数字。
```

### glob.glob 方法

glob.glob 方法主要返回所有匹配的文件路径列表。它只有一个参数 pathname ，定义了文件路径匹配规则，这里可以是绝对路径，也可以是相对路径。

#### 使用 `*` 匹配

我们可以用 `*` 匹配零个或者多个字符。

输出目录下的子目录或者文件：

```python

for p1 in glob.glob('/Users/cxhuan/Downloads/globtest/*'):
    print(p1)

```

运行上面代码，会将 globtest 文件夹下仅有的目录输出出来，输出内容如下：

```

/Users/cxhuan/Downloads/globtest/hello

```

我们也可以通过制定层级来遍历文件或者文件夹：

```python

for p in glob.glob('/Users/cxhuan/Downloads/globtest/*/*'):
    print(p)

```

上面的代码会遍历 globtest 文件夹以及子文件夹，将所有的文件或文件夹路径打印出来：

```
/Users/cxhuan/Downloads/globtest/hello/world
/Users/cxhuan/Downloads/globtest/hello/hello3.txt
/Users/cxhuan/Downloads/globtest/hello/hello2.txt
/Users/cxhuan/Downloads/globtest/hello/hello1.txt
```

我们也可以对文件或者文件夹进行过滤:

```python

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/*3.txt'):
    print(p)

```

上面代码值匹配 hello 目录下的文件名末尾为 ‘3’ 的 txt 文件，运行结果如下：

```
/Users/cxhuan/Downloads/globtest/hello/hello3.txt
```

#### 使用 `?` 匹配

我们可以用问号(?)匹配任何单个的字符。

```python

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/hello?.txt'):
    print(p)

```

上面的代码输出 hello 目录下的以 ‘hello’ 开头的 txt 文件，输出结果如下：

```

/Users/cxhuan/Downloads/globtest/hello/hello3.txt
/Users/cxhuan/Downloads/globtest/hello/hello2.txt
/Users/cxhuan/Downloads/globtest/hello/hello1.txt

```

#### 使用 `[]` 匹配

我们可以使用 `[]` 来匹配一个范围：

```python

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/*[0-2].*'):
    print(p)

```

我们想要得到 hello 目录下的文件名结尾数字的范围为 0到2的文件，运行上面代码，获得的输出为：

```
/Users/cxhuan/Downloads/globtest/hello/hello2.txt
/Users/cxhuan/Downloads/globtest/hello/hello1.txt
```

### glob.iglob 方法

python 的 glob 方法可以对文件夹下所有文件进行遍历，并返回一个 list 列表。而 iglob 方法一次只获取一个匹配路径。下面是一个简单的例子来说明二者的区别：

```
p = glob.glob('/Users/cxhuan/Downloads/globtest/hello/hello?.*')
print(p)

print('----------------------')

p = glob.iglob('/Users/cxhuan/Downloads/globtest/hello/hello?.*')
print(p)

```

运行上面代码，结果返回是：

```

['/Users/cxhuan/Downloads/globtest/hello/hello3.txt', '/Users/cxhuan/Downloads/globtest/hello/hello2.txt', '/Users/cxhuan/Downloads/globtest/hello/hello1.txt']
----------------------
<generator object _iglob at 0x1040d8ac0>

```

从上面的结果我们可以很容易看到二者的区别，前者返回的是一个列表，后者返回的是一个可迭代对象。

我们针对这个可迭代对象做一下操作看看：

```python
p = glob.iglob('/Users/cxhuan/Downloads/globtest/hello/hello?.*')
print(p.__next__())
print(p.__next__())

```

运行结果如下：

```
/Users/cxhuan/Downloads/globtest/hello/hello3.txt
/Users/cxhuan/Downloads/globtest/hello/hello2.txt
```

我们可以看到，针对这个可迭代对象，我们一次可以获取到一个元素。这样做的好处是节省内存，试想如果一个路径下有大量的文件夹或者文件，我们使用这个迭代对象不用一次性全部获取到内存，而是可以慢慢获取。

 
### 总结

今天分享的模块虽然功能简单，但是对于我们遍历文件或者目录来说足够使用了，并且方法简单易懂，值得大家经常使用。如果你觉得今天分享的模块有用，点个“**在看**”支持一下吧！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/glob)