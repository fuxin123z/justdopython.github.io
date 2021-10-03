---
layout: post
category: python
title: Python 清理微信缓存重复文件
tagline: by 某某白米饭
tags: 
  - python100
---

微信和 QQ 都有一个存放缓存文件的文件夹，微信在设置 --> 文件管理，QQ 在系统设置 --> 基本设置 --> 文件管理 --> 打卡个人文件中找到它，平时大家对这个文件夹关注度不高，这个文件夹慢慢的，偷偷的就占用了好几十个 G 的磁盘空间。下面就用 Python 写个删除重复文件的脚本清理这些空间。
<!--more-->

![](http://www.justdopython.com/assets/images/2021/09/remove/0.png)


### glob 模块

glob 模块非常简单，就是用来查找文件和文件夹。查找文件只用到三个匹配符："*", "?", "[]"。

通配符 功能
1. *：匹配0或多个字符
2. **：匹配所有文件,目录，子目录和子目录里面的文件
3. ?：匹配一个字符,这里与正则表达式? (正则?匹配前面表达式0次或者1次)
4. []：匹配指定范围内的字符,如: [1-9]匹配1至9内的字符
5. [!]：匹配不在指定范围内的字符


#### glob方法

这个方法返回所有匹配的文件路径列表

```python
# 当前路径下所有 py 文件
for fname in glob.glob("**/*.py",recursive=True):
    print(fname)

# 当前路径文件 py 下 py 文件
for fname in glob.glob("py/*.py"):
    print(fname)

# 单字通配符 ？,当前路径文件下以 Tem 开头后有一个字符文件夹
for fname in glob.glob("Tem?"):
    print(fname)

# 范围通配符[],当前路径文件下以 Tem 开头后一个数字符的 py 文件
for fname in glob.glob("Tem[0-9].py"):
    print(fname)

# 范围通配符[!],当前路径文件下以 Tem 开头后一个非数字符的 py 文件
for fname in glob.glob("Tem[!0-9].py"):
    print(fname)

windowns下
file = glob.glob(r'D:\logs\*\*')
```

### zlib.crc32

CRC32 算法概述 CRC 全称 Cyclic Redundancy Check，又叫循环冗余校验。和 md5 码一样都是 hash 的。当两个文件内容的 CRC32 相同的时候，这个文件也就是相同的。反之，两个文件就是不同的文件。

```python
def crc32(file_path):
    with open(file_path, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)
```

### 去重复

看到这里，想必都明白如何去重复文件了：1. 用 glob.glob 扫描所有文件，2. 把文件的 crc32 值放入字典中，3. 找到字典中已经存在的 crc32 值的key，删除当前文件。

```python

import os
import zlib
import glob

def scanning_floder(glob_path):
    
    crc32Dict = {}
    for fname in glob.glob(glob_path, recursive=True):
        if os.path.isfile(fname):
            crc = crc32(fname)
            if crc in crc32Dict:
                print('已经存在文件：' + crc32Dict.get(crc))
                print('重复文件：' + fname)
                print('删除文件：' + fname)
                os.remove(fname)
                print('')
            else:
                crc32Dict[crc] = fname

def crc32(file_path):
    with open(file_path, 'rb') as f:
        hash = 0
        while True:
            s = f.read(1024)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

scanning_floder(r"C:\Users\xxxx\Documents\WeChat Files\xxxx\FileStorage\**\*")    
```

![](http://www.justdopython.com/assets/images/2021/09/remove/1.png)

### 总结

本篇介绍了 glob 模块的用法和 crc32 值的计算，大家学废了吗？

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/remove>

