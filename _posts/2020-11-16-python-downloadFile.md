---
layout: post     
title:  Python 下载文件的多种方法
category: Python 下载文件的多种方法
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

本文档介绍了 Python 下载文件的各种方式，从下载简单的小文件到用断点续传的方式下载大文件。

<!--more-->

### Requests

使用 Requests 模块的 get 方法从一个 url 上下载文件，在 python 爬虫中经常使用它下载简单的网页内容

```python
import requests

# 图片来自bing.com
url = 'https://cn.bing.com/th?id=OHR.DerwentIsle_EN-CN8738104578_400x240.jpg'

def requests_download():

    content = requests.get(url).content

    with open('pic_requests.jpg', 'wb') as file:
        file.write(content)
```

### urllib

使用 python 内置的 urllib 模块的 urlretrieve 方法直接将 url 请求保存成文件

```python
from urllib import request

# 图片来自bing.com
url = 'https://cn.bing.com/th?id=OHR.DerwentIsle_EN-CN8738104578_400x240.jpg'

def urllib_download():
    request.urlretrieve(url, 'pic_urllib.jpg')
```

### urllib3

urllib3 是一个用于 Http 客户端的 Python 模块，它使用连接池对网络进行请求访问

```python
def urllib3_download():
    # 创建一个连接池
    poolManager = urllib3.PoolManager()

    resp = poolManager.request('GET', url)

    with open("pic_urllib3.jpg", "wb") as file:
        file.write(resp.data)

    resp.release_conn()
```

### wget

在 Linux 系统中有 wget 命令，可以方便的下载网上的资源，Python 中也有相应的 wget 模块。使用 pip install 命令安装

```python
import wget

# 图片来自bing.com
url = 'https://cn.bing.com/th?id=OHR.DerwentIsle_EN-CN8738104578_400x240.jpg'

def wget_download():
    wget.download(url, out='pic_wget.jpg')
```

也可以直接在命令行中使用 wget 命令

```
python -m wget https://cn.bing.com/th?id=OHR.DerwentIsle_EN-CN8738104578_400x240.jpg
```

### 分块下载大文件

在需要下载的文件非常大，电脑的内存空间完全不够用的情况下，可以使用 requests 模块的流模式，默认情况下 stream 参数为 False, 文件过大会导致内存不足。stream 参数为 True 的时候 requests 并不会立刻开始下载，只有在调用 iter_content 或者 iter_lines 遍历内容时下载

iter_content：一块一块的遍历要下载的内容
iter_lines：一行一行的遍历要下载的内容

```python
import requests

def steam_download():
    # vscode 客户端
    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    with requests.get(url, stream=True) as r:
        with open('vscode.exe', 'wb') as flie:
            # chunk_size 指定写入大小每次写入 1024 * 1024 bytes
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    flie.write(chunk)
```

### 进度条

在下载大文件的时候加上进度条美化下载界面，可以实时知道下载的网络速度和已经下载的文件大小，这里使用 tqdm 模块作为进度条显示，可以使用 `pip install tqdm` 安装

```python
from tqdm import tqdm

def tqdm_download():

    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    resp = requests.get(url, stream=True)

    # 获取文件大小
    file_size = int(resp.headers['content-length'])
    
    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True, desc='vscode.exe') as bar:
        with requests.get(url, stream=True) as r:
            with open('vscode.exe', 'wb') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))
```

tqdm 参数说明：
* total：bytes，整个文件的大小
* unit='B': 按 bytes 为单位计算
* unit_scale=True：以 M 为单位显示速度
* unit_divisor=1024：文件大小和速度按 1024 除以，默认时按 1000 来除
* ascii=True：进度条的显示符号，用于兼容 windows 系统
* desc='vscode.exe' 进度条前面的文件名

示例结果

![](http://www.justdopython.com/assets/images/2020/11/download/0.gif)

### 断点续传

HTTP/1.1 在协议的请求头中增加了一个名为 Range的字段域， Range 字段域让文件从已经下载的内容开始继续下载

如果网站支持 Range 字段域请求响应的状态码为 206(Partial Content)，否则为 416(Requested Range not satisfiable)

Range 的格式

```
Range:[unit=first byte pos] - [last byte pos]，即 Range = 开始字节位置-结束字节位置，单位：bytes
```

将 Range 加入到 headers 中

```python
from tqdm import tqdm

def duan_download():
    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    r = requests.get(url, stream=True)

    # 获取文件大小
    file_size = int(r.headers['content-length'])

    file_name = 'vscode.exe'
    # 如果文件存在获取文件大小，否在从 0 开始下载，
    first_byte = 0
    if os.path.exists(file_name):
        first_byte = os.path.getsize(file_name)
        
    # 判断是否已经下载完成
    if first_byte >= file_size:
        return

    # Range 加入请求头
    header = {"Range": f"bytes={first_byte}-{file_size}"}

    # 加了一个 initial 参数
    with tqdm(total=file_size, unit='B', initial=first_byte, unit_scale=True, unit_divisor=1024, ascii=True, desc=file_name) as bar:
        # 加 headers 参数
        with requests.get(url, headers = header, stream=True) as r:
            with open(file_name, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))
```

示例结果

启动下载一段时间后，关闭脚本重新运行，文件在断开的内容后继续下载

![](http://www.justdopython.com/assets/images/2020/11/download/1.gif)

### 总结

本文介绍了常用的 7 中文件下载方式，其他的下载方式大家可以在留言区交流交流共同进步

> 示例代码：[Python 下载文件的多种方法](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/download)