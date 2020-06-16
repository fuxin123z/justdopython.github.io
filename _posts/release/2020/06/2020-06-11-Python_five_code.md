---
layout: post
title: Python 5 行代码的神奇操作
category: python
tagline: by 潮汐
tags: 
  - python
---
Python  语言实现功能直接了当，简明扼要，今天咱们就来一起看看 Python 5 行代码的神奇操作！

<!--more-->

![我能行](https://imgkr.cn-bj.ufileos.com/d4fc767f-f709-4aff-b324-e0d39f26ac52.jpg)

### 1、古典兔子问题

有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？

```python
def count(n):
    if (1 == n or 2 == n):
        return 1
    elif (n >= 2):
        return count(n - 2) + count(n - 1)
print(count(36) * 2)

```

### 2、加法计算器

 ```python
num1 = input("第一个数：")
num2 = input("第二个数：")
new_num1 = int(num1)
new_num2 = int(num2)
print(new_num1 + new_num2)
 ```

### 3、循环问答

```python
while(True):
    question = input()
    answer = question.replace('吗', '呢')
    answer = answer.replace('？', '！')
    print(answer)
```

**输出：**
```
在吗
在呢
吃饭了吗
吃饭了呢
要下班了吗
要下班了呢
最近好吗
最近好呢
```

### 4、实现一个简单的服务器

```python
from http import server
from http.server import SimpleHTTPRequestHandler
server_address = ('127.0.0.1', 8888)
httpd = server.HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()
```

### 5、九九乘法表1

```python
for i in range(1, 10):
    for j in range(1, i+1):
        print('{}x{}={}\t'.format(j, i, i*j), end='')
    print()
```
**输出：**

```python
1x1=1	
1x2=2	2x2=4	
1x3=3	2x3=6	3x3=9	
1x4=4	2x4=8	3x4=12	4x4=16	
1x5=5	2x5=10	3x5=15	4x5=20	5x5=25	
1x6=6	2x6=12	3x6=18	4x6=24	5x6=30	6x6=36	
1x7=7	2x7=14	3x7=21	4x7=28	5x7=35	6x7=42	7x7=49	
1x8=8	2x8=16	3x8=24	4x8=32	5x8=40	6x8=48	7x8=56	8x8=64	
1x9=9	2x9=18	3x9=27	4x9=36	5x9=45	6x9=54	7x9=63	8x9=72	9x9=81	
```

### 6、九九乘法表2

```python
for i in range(1, 10):
    for j in range(i, 10):
        print(f'{i}x{j}={i*j}',end='\t')
    print(" ")
print("\n")
```

**输出：**

```python
1x1=1	1x2=2	1x3=3	1x4=4	1x5=5	1x6=6	1x7=7	1x8=8	1x9=9	 
2x2=4	2x3=6	2x4=8	2x5=10	2x6=12	2x7=14	2x8=16	2x9=18	 
3x3=9	3x4=12	3x5=15	3x6=18	3x7=21	3x8=24	3x9=27	 
4x4=16	4x5=20	4x6=24	4x7=28	4x8=32	4x9=36	 
5x5=25	5x6=30	5x7=35	5x8=40	5x9=45	 
6x6=36	6x7=42	6x8=48	6x9=54	 
7x7=49	7x8=56	7x9=63	 
8x8=64	8x9=72	 
9x9=81	 
```
### 7、逆序打印数字

给一个不多于5位的正整数,逆序打印出各位数字,实现思路如下：
```python
def nixu(n):
    l = str(n)
    l_str = l[::-1]
    print("逆序:%s" % ( l_str))
nixu(2020)
```
**输出：**

```
逆序:0202
```

### 8、生成词云

```python
from wordcloud import WordCloud
import PIL.Image as image
```
```python
with open('wordcloud.txt') as fp:
    text = fp.read()
    wordcloud = WordCloud().generate(text)
    img = wordcloud.to_image()
    img.show()
```
![词云](https://imgkr.cn-bj.ufileos.com/53d10ced-1b02-4b71-a205-bf93d6357e0a.png)

### 9、快速生成二维码

以百度为例，生成二维码
```python
from MyQR import myqr
myqr.run(
    words='https://www.baidu.com/',
    colorized=True,
    save_name='baidu_code.png')
```
![百度二维码](https://imgkr.cn-bj.ufileos.com/46e1b653-0539-4007-9f89-03129b1b777e.png)

### 10、实现批量抠图

抠图具体教程详见 [Python装逼指南--五行代码实现批量抠图](https://mp.weixin.qq.com/s/xj_JDqC8T3YoHqgBXPqoOA)
```python
import os, paddlehub as hub
huseg = hub.Module(name='deeplabv3p_xception65_humanseg') # 加载模型
path = './imgs/' # 文件目录
files = [path + i for i in os.listdir(path)] # 获取文件列表
results = huseg.segmentation(data={'image': files}) # 抠图
```

### 总结

今天文章安利一些小技巧，希望对大家有一定的帮助，继续向前吧！
