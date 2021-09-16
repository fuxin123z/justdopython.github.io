---
layout: post
category: python
title: github 上高星的爬虫项目
tagline: by 某某白米饭
tags:
  - Python
  - 爬虫
---

github 是一个开源宝库，上面有许多第三方的爬虫库，是可以拿来直接使用和学习的。不需要我们花费大量的时间去研究特定的网站如何去抓取数据。

<!--more-->

### 1. gopup

GoPUP (https://github.com/justinzm/gopup) 项目所采集的数据皆来自公开的数据源，数据接口：百度、谷歌、头条、微博指数,宏观数据，利率数据，货币汇率，千里马、独角兽公司，新闻联播文字稿，影视票房数据，高校名单，疫情数据等等

![](http://www.justdopython.com/images/2021/09/pachong/0.png)

#### 安装

使用清华的 pip 源

```python
pip install gopup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 使用

查看文档 http://doc.gopup.cn/#/

```python
import gopup as gp
df_index = gp.weibo_index(word="疫情", time_type="3month")
print(df_index)
```

示例结果：

![](http://www.justdopython.com/images/2021/09/pachong/1.png)

### 2. weibo-spider

weibo-spider (https://github.com/dataabc/weiboSpider) 是一个微博的爬虫，可以连续的爬取一个或多个微博用户的数据，并将数据写入文件和数据库。支持下载微博中的原始图片/视频、转载图片/视频，Live Photo 中的视频。

![](http://www.justdopython.com/images/2021/09/pachong/2.png)

#### 安装

安装有两种方式，一种是源码安装，一种是pip 

```python
$ git clone https://github.com/dataabc/weiboSpider.git
$ cd weiboSpider
$ pip install -r requirements.txt

或者

python3 -m pip install weibo-spider
```

#### 使用

weibo-spider 爬虫已经在公众号文章 [《中秋不发女朋友，发追女神的方法》](https://mp.weixin.qq.com/s/lKPOmv036IumGLuiIlBnPw) 中使用了一次，可以抓取到用户的各种资料、图片、视频。

1. 安装后第一次运行命令行 `python3 -m weibo_spider` ，会自动在当前目录创建config.json配置文件
2. 修改 config.json 文件中 user_id_list 微博用户 ID。
3. 再次运行 `python3 -m weibo_spider`

示例结果：

![](http://www.justdopython.com/images/2021/09/pachong/3.png)

### 3. You-Get

you-get (https://github.com/soimort/you-get) 提供便利的方式来下载网络上的媒体信息,包括视频、音频、图片，支持 80+ 网站。小编经常用来下载 B 站视频。


#### 安装

在 pip 之前需要安装 FFmpeg (强烈推荐) 或 Libav、(可选) RTMPDump。

```python
pip3 install you-get

升级用 
pip3 install --upgrade you-get
```

#### 使用

只需要简单的使用 you-get 命令就可以下载视频、图片、音频

```pyton
you-get 网址

如:

you-get https://www.bilibili.com/video/BV1Dq4y1Z7zC?spm_id_from=333.851.b_7265636f6d6d656e64.1
```

示例结果：

![](http://www.justdopython.com/images/2021/09/pachong/4.png)

### 4. musicdl

Music-dl (https://github.com/0xHJK/music-dl) 是一个基于 Python3 的命令行工具，可以从多个网站搜索和下载音乐，解决音乐不知道在哪个网站的问题。Music-dl 的 API 是从公共网络获取的，下载不了 VIP 音乐。

Music-dl 支持 QQ音乐，酷狗音乐，网易云音乐，咪咕音乐和百度音乐。

![](http://www.justdopython.com/images/2021/09/pachong/5.png)

#### 安装

```python
pip install musicdl
```

#### 使用

```python
music-dl -k 周杰伦
```

示例结果：

![](http://www.justdopython.com/images/2021/09/pachong/6.png)

### 总结

介绍了 github 上高赞的爬虫项目，大家都可以看看源码，学习源码，让自己的 python 之道更加强大。
