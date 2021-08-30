---
layout: post
category: python
title: 用 Jupyter Notebook 爬取微博图片保存本地！
tagline: by 潮汐
tags:
  - Python技巧
  - 编程
---

今天咱们用 Jupyter-Notebook 并结合框架（Selenium）模拟浏览器抓取微博图片并将图片保存本地。

Selenium 是一个用电脑模拟人的操作浏览器网页，可以实现自动化测试，模拟浏览器抓取数据等工作。

<!--more-->

###  环境部署

#### 安装 Jupyter notebook

关于 Jupyter notebook 的详细知识点在以往的文章中有做过详细的介绍，详情请参考文章[一文吃透 Jupyter notebook](https://t.1yb.co/xc5a)

这里只需要在命令行中输入：jupyter notebook 启动跳转到浏览器编辑界面即可。
![](https://files.mdnice.com/user/6478/a62d16d8-3dae-496d-957c-8aec40d1e3f2.png)

浏览器页面：

![](https://files.mdnice.com/user/6478/c6e99102-79ba-4648-9bfc-aa8f215d9e23.png)

#### 安装 Selenium 

安装 Selenium 非常简单，只需要用命令 'pip install Selenium' 即可，安装成功提示信息如下：

![](https://files.mdnice.com/user/6478/07ab0b60-51ad-4775-977e-9723e34c700f.png)

#### 下载浏览器驱动

下载驱动地址如下：

[Firefox浏览器驱动](https://link.zhihu.com/?target=https%3A//github.com/mozilla/geckodriver/releases)

[Chrome浏览器驱动：chromedriver](https://link.zhihu.com/?target=https%3A//npm.taobao.org/mirrors/chromedriver)

[IE浏览器驱动：IEDriverServer](https://link.zhihu.com/?target=http%3A//selenium-release.storage.googleapis.com/index.html)

[Edge浏览器驱动：MicrosoftWebDriver](https://link.zhihu.com/?target=https%3A//developer.microsoft.com/en-us/microsoft-edge/tools/webdriver)

需要把浏览器驱动放入系统路径中，或者直接告知 selenuim 的驱动路径。

环境都搭建好后就可以直接开始爬取数据了。

### 抓取微博数据

首先导入包，模拟浏览器访问微博主页，详细代码如下：

```python

from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://weibo.com/')
```
此时浏览器会打开一个新页面，如下图所示：

![](https://files.mdnice.com/user/6478/e047d04b-b185-4fb7-bfe6-abf5a527c250.png)

接下来开始分析页面数据：
微博页面搜索奥运会关键字后出现新的页面，然后复制网址，抓取和奥运会相关的图片保存于本地，搜索界面如下：

![](https://files.mdnice.com/user/6478/02072bb9-42c2-4a51-a668-f5426b1e7dd0.png)

输入网址获取网页内容：
```python
driver.get('https://s.weibo.com/weibo/%25E5%25A5%25A5%25E8%25BF%2590%25E4%25BC%259A?topnav=1&wvr=6&b=1')
contents = driver.find_elements_by_xpath(r'//p[@class="txt"]')
print(len(contents))
```
输出内容如下：

![](https://files.mdnice.com/user/6478/725c1638-9b58-4972-ab21-ab6ac611e9c2.png)

查看网页详细信息：

```python

for i in range(0,3):
    print("==============================")
    print(contents[i].get_attribute('innerHTML'))
    
```

![](https://files.mdnice.com/user/6478/718510da-870c-4612-bb42-0832a8b6cc9a.png)

获取图片信息：

```python

contents = driver.find_elements_by_xpath(r'//img[@action-type="fl_pics"]')

print(len(contents))

for i in range(0,20):
    print("==============================")
    print(contents[i].get_attribute('src'))
```

![](https://files.mdnice.com/user/6478/1e7b6740-0ac3-412d-b29e-f903040b1c55.png)

下载图片在本地：

```python

import os
import urllib.request

for i in range(0,20):
    print("==============================")
    image_url=contents[i].get_attribute('src')
    file_name="downloads//p"+str(i)+".jpg"
    print(image_url,file_name)
    urllib.request.urlretrieve(image_url, filename=file_name)
```

![](https://files.mdnice.com/user/6478/98d5d0b7-b21d-4b02-b566-e921e7dce93c.png)

至此微博页面关于奥运会的相关图片已保存于本地，图片保存详情如下：


![](https://files.mdnice.com/user/6478/96b46ea1-7fbd-4593-8ef0-200e247b4078.png)

#### 汇总代码如下

```python

from selenium import webdriver
import urllib.request

driver = webdriver.Chrome()
driver.get('https://weibo.com/')

driver.get('https://s.weibo.com/weibo/%25E5%25A5%25A5%25E8%25BF%2590%25E4%25BC%259A?topnav=1&wvr=6&b=1')

contents = driver.find_elements_by_xpath(r'//p[@class="txt"]')

for i in range(0,3):
    print("==============================")
    print(contents[i].get_attribute('innerHTML'))

contents = driver.find_elements_by_xpath(r'//img[@action-type="fl_pics"]')

print(len(contents))

for i in range(0,20):
    print("==============================")
    print(contents[i].get_attribute('src'))


for i in range(0,20):
    print("==============================")
    image_url=contents[i].get_attribute('src')
    file_name="downloads//p"+str(i)+".jpg"
    print(image_url,file_name)
    urllib.request.urlretrieve(image_url, filename=file_name)
    
```

以上汇总代码给没有安装 Jupyter Notebook 的朋友们使用，希望对大家有帮助。

### 总结

今天的文章主要讲解用 Jupyter Notebook 工具和 Selenium 框架抓取微博数据，希望对大家有所帮助。

> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/chaoxi/craw_weibo)
