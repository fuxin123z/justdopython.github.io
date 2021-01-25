---
layout: post
category: python
title: 强大！用 60 行代码自动抢微信红包
tagline: by 某某白米饭
tags: 
  - python
  - 微信
  - appium
---

春节来到，红包们大概率在微信各大群中肆虐，大家是否都一样不抢到红包们心里就感觉错过了一个亿，可总会被这事那事耽误而遗憾错过，下面用 Python 写一个自动抢红包代码
<!--more-->
![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/0.png)

### 启动入口

启动程序的配置和公众号文章[《用 Python + Appium 的方式自动化清理微信僵尸好友》](https://mp.weixin.qq.com/s/LuiyfqR5QVJyqM4t1B4Fkw)的配置一样

```python
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

desired_capabilities = {
    'platformName': 'Android', # 操作系统
    'deviceName': '2a254a02', # 设备 ID
    'platformVersion': '10.0.10', # 设备版本号，在手机设置中查看
    'appPackage': 'com.tencent.mm', # app 包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI', # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
# 设置等待超时时间
wait = WebDriverWait(driver, 60)
```

### 点击进入聊天窗口

微信在一般情况下最新的聊天记录将被放在第一个，所以只需要打开第一个聊天窗口检查有没有红包就可以了，用 id 为 `com.tencent.mm:id/e3x` 可以找到所有的聊天信息，我们取第一个聊天群的索引

![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/1.png)

```python
# 进入第一个聊天框
red_packet_group = driver.find_elements_by_id('com.tencent.mm:id/e3x')[0]
red_packet_group.click()
```

### 找到红包

进入聊天群后，红包图片检查是否存在红包，它的 id 为 `com.tencent.mm:id/r2`

![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/2.png)

```python
 # 检查红包
reds = driver.find_elements_by_id('com.tencent.mm:id/r2')
if len(reds) == 0:
    driver.keyevent(4)
```

### 抢红包

点击红包后会出现以下 3 种情况

1. 红包已经被自己领取了
2. 红包手慢了没抢到
3. 红包未领取

前两种情况红包已经失效了，最后一种才是可以打开的红包

#### 红包已经失效了

在上面代码中都是用 id 检查元素是否存在，这里使用查找文字`已存入零钱`和`手慢了`判断红包是否已经失效

![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/3.png)

```python
# 判断元素是否存在
def is_element_exist_by_xpath(driver, text):
    try:
        driver.find_element_by_xpath(text)
    except Exception as e:
        return False
    else:
        return True


# 领取了
is_open = is_element_exist_by_xpath(driver, '//android.widget.TextView[contains(@text, "已存入零钱")]')
# 没抢到
is_grabbed = is_element_exist_by_xpath(driver, '//android.widget.TextView[contains(@text, "手慢了")]')

if is_open or is_grabbed:
    driver.keyevent(4)
```

#### 打开红包

打开红包比较简单，只需要找到 `开` 字的 id

![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/4.png)

```python
wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/den"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/dm"))).click()
```

### 删除红包

最后我们将红包删除，防止红包被重复打开。当长按红包时，微信红包会出现删除按钮

![](http://www.justdopython.com/assets/images/2021/01/wxRedPacket/5.png)

```python
TouchAction(driver).long_press(red).perform()
wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/gam"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/doz"))).click()
```

### 总结

这是学习并使用 Appium 的第三篇文章，Appium 可以帮将手机操作自动化，大家学废了吗？

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/wxRedPacket>