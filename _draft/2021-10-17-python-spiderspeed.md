---
layout: post
title: 知乎热门：如何提高爬虫速度？
category: python
tagline: by 闲欢
tags: 
  - python
---



![封面](http://www.justdopython.com/assets/images/2021/10/spiderspeed/0.png)


今天在浏览知乎时，发现一个有趣的问题：
> 如何优化 Python 爬虫的速度？

他的问题描述是：
> 目前在写一个 Python 爬虫，单线程 urllib 感觉过于慢了，达不到数据量的要求（十万级页面）。求问有哪些可以提高爬取效率的方法？

这个问题还蛮多人关注的，但是回答的人却不多。

我今天就来尝试着回答一下这个问题。

程序提速这个问题其实解决方案就摆在那里，要么通过并发来提高单位时间内处理的工作量，要么从程序本身去找提效点，比如爬取的数据用gzip传输、提高处理数据的速度等。

我会分别从几种常见的并发方法去做同一件事情，从而比较处理效率。

<!--more-->


### 简单版本爬虫

我们先来一个简单的爬虫，看看单线程处理会花费多少时间？

```python
import time
import requests
from datetime import datetime


def fetch(url):
    r = requests.get(url)
    print(r.text)

start = datetime.now()

t1 = time.time()
for i in range(100):
    fetch('http://httpbin.org/get')

print('requests版爬虫耗时：', time.time() - t1)

# requests版爬虫耗时： 54.86306357383728

```

我们用一个爬虫的测试网站，测试爬取100次，用时是54.86秒。


### 多线程版本爬虫

下面我们将上面的程序改为多线程版本：

```python
import threading
import time
import requests


def fetch():
    r = requests.get('http://httpbin.org/get')
    print(r.text)

t1 = time.time()

t_list = []
for i in range(100):
    t = threading.Thread(target=fetch, args=())
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()

print("多线程版爬虫耗时：", time.time() - t1)

# 多线程版爬虫耗时：0.8038511276245117
```

我们可以看到，用上多线程之后，速度提高了68倍。其实用这种方式的话，由于我们并发操作，所以跑100次跟跑一次的时间基本是一致的。这只是一个简单的例子，实际情况中我们不可能无限制地增加线程数。


### 多进程版本爬虫

除了多线程之外，我们还可以使用多进程来提高爬虫速度：

```python
import requests
import time
import multiprocessing
from multiprocessing import Pool

MAX_WORKER_NUM = multiprocessing.cpu_count()

def fetch():
    r = requests.get('http://httpbin.org/get')
    print(r.text)

if __name__ == '__main__':
    t1 = time.time()
    p = Pool(MAX_WORKER_NUM)
    for i in range(100):
        p.apply_async(fetch, args=())
    p.close()
    p.join()

    print('多进程爬虫耗时：', time.time() - t1)

多进程爬虫耗时： 7.9846765995025635
```

我们可以看到多进程处理的时间是多线程的10倍，比单线程版本快7倍。


### 协程版本爬虫

我们将程序改为使用 aiohttp 来实现，看看效率如何：

```python
import aiohttp
import asyncio
import time


async def fetch(client):
    async with client.get('http://httpbin.org/get') as resp:
        assert resp.status == 200
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)

loop = asyncio.get_event_loop()

tasks = []
for i in range(100):
    task = loop.create_task(main())
    tasks.append(task)

t1 = time.time()

loop.run_until_complete(main())

print("aiohttp版爬虫耗时：", time.time() - t1)

aiohttp版爬虫耗时： 0.6133313179016113

```

我们可以看到使用这种方式实现，比单线程版本快90倍，比多线程还快。


### 结论

通过上面的程序对比，我们可以看到，对于多任务爬虫来说，多线程、多进程、协程这几种方式处理效率的排序为：aiohttp > 多线程 > 多进程。因此，对于简单的爬虫任务，如果想要提高效率，可以考虑使用协程。但是同时也要注意，这里只是简单的示例，实际运用中，我们一般会用线程池、进程池、协程池去操作。

这就是问题的答案了吗？

对于一个严谨的程序员来说，当然不是，实际上还有一些优化的库，例如grequests，可以从请求上解决并发问题。实际的处理过程中，肯定还有其他的优化点，这里只是从最常见的几种并发方式去比较而已，应付简单爬虫还是可以的，其他的方式欢迎大家在评论区留言探讨。


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/spiderspeed)





