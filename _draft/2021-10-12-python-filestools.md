---
layout: post
category: python
title: 绝了! 2 行代码可以加水印、文件对比以及利好抓包
tagline: by 某某白米饭
tags: 
  - python100
---

python 中有许多有趣的第三方库，其中有一个 filestools 可以 2 行代码可以为图片增加水印、可以对比两个文件的差异还有利好抓包的curl 转为 pyton 的 requests 请求代码。大家一起来看看吧。

<!--more-->

### 安装

这个库有 4 个功能，
* 仿 Linux 树形目录显示 tree 命令
* 文件差异比较 diff 命令
* 图片加水印 marker 命令
* curl 请求命令转 python 请求代码

```python
pip install filestools -U
```

### 图片加水印

导入水印模块

```python
from watermarker.marker import add_mark
```

add_mark 方法有 8 个参数：
* file：图片文件或图片文件夹路径
* mark：要添加的水印内容
* out：添加水印后的结果保存位置，默认生成到 output 文件夹
* color：添加水印后的结果保存位置，默认生成到 output 文件夹
* space：水印直接的间隔, 默认 75 个空格
* angle：水印旋转角度，默认 30 度
* size：水印字体的大小，默认 50
* opacity：水印的透明度，默认 0.15

身份证经常需要被上传并用在实名认证上面，我们可以加上水印防止被盗用，原图如下：

![](http://www.justdopython.com/assets/images/2021/10/filestools/0.png)

经过水印处理

```python
from watermarker.marker import add_mark

add_mark(r"D:\personal\gitpython\maoyan\0.png", "学 python，看 python 技术公众号", angle=15, size=20, space=40, color='#c5094d')
```

![](http://www.justdopython.com/assets/images/2021/10/filestools/1.png)


### 文件对比

导入水印模块

```python
from filediff.diff import file_diff_compare
```

file_diff_compare 方法有 7 个参数：
* file1：被比较的文件 1
* file2：被比较的文件 2
* out：差异结果保存的文件名，默认值 diff_result.html
* max_width：每行超过多少字符就自动换行，默认值 70
* numlines：在差异行基础上前后显示多少行，默认是 0
* show_all：只要设置这个参数就表示显示全部原始数据，此时 numlines 参数无效；默认不显示全部
* no-browser：设置这个参数，在生成结果后不会自动打开游览器

举个例子，有以下两个文件：

![](http://www.justdopython.com/assets/images/2021/10/filestools/2.png)

经过文件对比

```python
from filediff.diff import file_diff_compare

file_diff_compare(r"D:\一线城市.log", r"D:\一线城市2.log", diff_out="diff_result.html", max_width=70, numlines=0, no_browser=True)
```

绿色表示新增，黄色表示修改，红色表示被删除。

![](http://www.justdopython.com/assets/images/2021/10/filestools/3.png)

当使用了 show_all 参数之后，将显示所有：

```python
from filediff.diff import file_diff_compare

file_diff_compare("D:\一线城市.log", "D:\一线城市2.log", diff_out="diff_result.html", show_all=True, no_browser=True)
```

![](http://www.justdopython.com/assets/images/2021/10/filestools/4.png)

### curl 请求命令转 python 请求代码

curl 转 python 的用法完全利好爬虫，可以少写一些抓包代码。这个 api 会生成 headers、requests.get() 等内容。

先在谷歌游览器中复制网络抓到的网络请求为cURL(bash)，如下图：

![](http://www.justdopython.com/assets/images/2021/10/filestools/5.png)

复制出来的内容类似：

```bash
curl 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/mancard/img/side/qrcode@2x-daf987ad02.png' \
  -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
  -H 'Referer: https://www.baidu.com/' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --compressed
```

使用 curl 转 python

```python
from curl2py.curlParseTool import curlCmdGenPyScript

curl_cmd = """curl 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/mancard/img/side/qrcode@2x-daf987ad02.png' \
  -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
  -H 'Referer: https://www.baidu.com/' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --compressed"""
output = curlCmdGenPyScript(curl_cmd)
print(output)
```

![](http://www.justdopython.com/assets/images/2021/10/filestools/6.png)

### 总结

python 中有趣并且好用的第三方库还有很多，小编会在后面的公众号文章中为大家继续介绍。
