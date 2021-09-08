---
layout: post
category: python
title: 我用 Selenium 爬了京东商城，结果……
tagline: by 極光
tags:
  - 
---

![封面](http://www.justdopython.com/assets/images/2021/08/selenium/jd.png)


上次介绍了下 `selenium` 定位元素的多种方法，以及我们找到元素后，可以对它进行什么操作。并写了一个自动化操作的简单例子，给大家学习参考。今天就来继续跟大家一起学习下 `Python` 如何使用 `Selenium` 进行自动化操作网页。

<!--more-->

## 如何加载元素

众所周知现在的网站，页面内容非常复杂，而且加载的内容种类繁多，所以加载时间就会比较长。平时我们看到的大部分网站页面都做了优化，比如 `baidu.com`，或者 `jd.com`，但为了提升页面打开速度，他们又都采用了不同的方案：

- 百度首页采用了极简的方式，让自己搜索首页尽量加载少量的内容，以提高打开页面的速度。

- 京东首页则不可能采用百度那样的方案，因为业务方向不同，京东作为电商需要给客户展示尽量多的内容，所以它采用了延时加载的方式，也就是先加载用户能看到的内容，然后再慢慢加载那些用户不能直观看到的内容，从而大大提高了页面打开的速度。
 
上次我们用 `selenium` 写了个爬取京东商城搜索出来的 `ps5国行` 的产品名称和价格，在这里把代码再放出来看下。

```python
# 导入库
from selenium import webdriver
import time

# executable_path 用于指定driver存放路径
browser = webdriver.Chrome(executable_path='/Users/xx/python/chromedriver')
# 打开京东官网
browser.get('https://www.jd.com/')

# browser.find_element_by_id("kw").send_keys("python selenium")

# 获取输入框对象
search = browser.find_element_by_xpath('//*[@id="key"]')

# 输入想要搜索的关键词,如"ps5国行"
search.send_keys('ps5国行')

# 获取搜索按钮对象并单击
browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()

# 将滚动条移动到页面底部，用于加载所有信息
javascript = "var q=document.documentElement.scrollTop=50000"
# 执行 javascript 移动滚动条
browser.execute_script(javascript)
# 等待3秒，有些异步加载的数据加载慢
time.sleep(3)

# 通过查看页面源码得到金额的 xpath 路径，并获取金额 
prices = browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[2]/strong/i')
# 通过查看页面源码得到商品标题的 xpath 路径，并获取商品标题
names = browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/a/em')

# 遍历打印出当前页所有标题和金额
for name,price in zip(names,prices):
    print(name.text.replace('\n',''),price.text)

#退出浏览器
browser.quit()

```

## 元素等待

上面代码中，在搜索完成后，我们只看到第一页内容，其实还没在屏幕上展示的内容是没有加载的，这样我们就没办法获取所有搜索出的产品信息。

这里就需要我先用 `selenium` 操作滚动条，将滚动条移动到页面底部，用于加载所有信息，这时你会发现，产品信息不会立刻加载出来，还需要等待几秒钟，当然等多久主要还是看网速。

在这里我设置的是等待 3 秒，调用了 `time.sleep(3)` 方法来实现。

- 强制等待

强制等待是一种简单又粗暴的方式，也就是强制将进程暂停，等待参数传入的相应时间。比如我们上面用的 `time.sleep(3)`，它不会管你页面是否已经加载完，都会等 3 秒的时间。

如果 3 秒后内容加载完了还好，如果没有加载完，它也不会再等了，直接开始执行下面的代码，所以经常会遇到不可预知的问题。

这种方式主要用来简单调试代码时使用，平时非常不建议使用。

- 隐式等待

隐式等待也叫隐性等待，跟强制等待最大的不同就是，隐性等待可以实现智能等待，只要设置一个最大等待时间，在这个时间内网页内容只要加载完成就可以立即进行后续操作，不需要再等到最大时间。

```python
# 导入库
from selenium import webdriver
import time

# executable_path 用于指定driver存放路径
browser = webdriver.Chrome(executable_path='/Users/xx/python/chromedriver')

# 隐性等待最长等20秒
driver.implicitly_wait(20)  

# 打开京东官网
browser.get('https://www.jd.com/')


#退出浏览器
browser.quit()

```

不过使用隐性等待有几点需要注意：

1. 如果等待到最大时间，网页还没有加载完成，那依然还会继续执行下一步操作。

2. 这里指的网页加载完成，是指浏览器的加载页面状态显示完成（也就是加载的小圈不再转），实际使用中经常会遇到大部分内容都加载完了，但有少量 js 脚本一直加载中，导致整个页面状态还是加载中，这时就会仍需要等待 20 秒才会执行下一步操作。

3. 跟 `sleep()` 方法不同，隐式等待方法 `implicitly_wait(20) ` 设置一次后是全局有效的，也就是在整个 driver 的周期都起作用，不用每个操作前都设置一遍。

那这些问题有没有解决方法？或者有没有其他更好的方法实现元素等待？当然有，那就是显式等待。

- 显式等待

显式等待其实就是 `wait` 模块下的 `WebDriverWait` 类对象，通过 `until()` 方法和 `until_not()` 方法实现元素等待。

`until()`：当某个元素加载完成，或者其他设置的条件成立，则会继续执行后续操作。如果还不满足条件，则会间隔一定时间检测一下条件是否成立，直到达到设置的最大时间，最后抛出异常 `TimeoutException`。

`until_not()`：跟 `until()`  方法相反，当判断某个元素，或者某个条件不成立时，才会继续执行下一步操作。

```python
# 方法参数说明
WebDriverWait(driver, 超时时间, 频率, 忽略异常).until(可执行的方法, 超时会返回信息内容)
```

下面我们来看这段代码

```python
# 导入库
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECS
from selenium.webdriver.common.by import By
import time

# executable_path 用于指定driver存放路径
browser = webdriver.Chrome(executable_path='/Users/xx/python/chromedriver')

# 打开京东官网
browser.get('https://www.jd.com/')

# 定位要查找的元素
loc = (By.LINK_TEXT, "打开")

try:
  # 等待5秒，直到发现元素
    WebDriverWait(driver, 5).until(ECS.presence_of_element_located(loc))
except:
  # 没有发现元素则会打印提示
    print("没有找到对应元素！")
finally:
  # 发现元素则执行下面的方法
    driver.find_element_by_link_text('打开').click()

#退出浏览器
browser.quit()

```

使用 `WebDriverWait` 调用可执行方法，除了可定位的元素，还可以使用 `selenium` 提供的 `expected_conditions` 模块中的各种条件，也可以使用 `WebElement` 的 `is_enabled()`，`is_selected()`，`is_displayed()` 等等方法。

## 总结

好了，今天我们又介绍了下 `selenium` 元素加载时的三种等待方法，以及等待方法的优缺点，在使用场景下该如何操作等。并写了一些简单例子，给大家学习参考，后续还会为大家介绍更多。OK，今天就聊这些，如果你喜欢记得点 `在看`。
