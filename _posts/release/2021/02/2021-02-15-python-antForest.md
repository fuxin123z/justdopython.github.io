---
layout: post
category: python
title: 用 Appium 自动收取蚂蚁森林能量
tagline: by 某某白米饭
tags: 
  - python
  - 蚂蚁森林
  - appium
---

支付宝集 5 福让小编打开了尘封已久的蚂蚁森林小程序，它刚出来那会儿小编也算是一个重度用户，看着一直被偷的能量总想以德服人。今天就用 Python + Appium 写一个自动收取能量的脚本，完成之后再也没人能从小编手上将能量偷走了

![](http://www.justdopython.com/assets/images/2021/02/antforest/0.png)

### 启动入口

还不会使用 Appium 的小伙伴可以先看看本公众号上的[《解放双手，提高生产力，这款神器你值得拥有》](https://mp.weixin.qq.com/s/RzGxuiqXF8tCsdY3TZgoAw)学习和使用 Appium

下面代码是支付宝的配置文件

```python
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

desired_capabilities = {
    'platformName': 'Android',  # 操作系统
    'deviceName': '2a254a02',  # 设备 ID
    'platformVersion': '10.0.10',  # 设备版本号，在手机设置中查看
    'appPackage': 'com.eg.android.AlipayGphone',  # app 包名
    'appActivity': 'AlipayLogin',  # app 启动时主 Activity
    'noReset': True  # 是否保留 session 信息 避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
# 设置等待超时时间
wait = WebDriverWait(driver, 60)
```

### 点击进入蚂蚁森林

支付宝上的蚂蚁森林的图标按钮位置每个人按照各自的习惯都不相同，小编的图标位置在`全部-->最近使用`里面，可以用`蚂蚁森林`文字找到图标并点击

![](http://www.justdopython.com/assets/images/2021/02/antforest/1.png)

```python
# 点击全部图标
wait.until(EC.element_to_be_clickable((By.ID, 'com.alipay.android.phone.openplatform:id/more_app_icon'))).click()
# 找到蚂蚁森林
wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[contains(@text, "蚂蚁森林")]'))).click()
time.sleep(1)
```

### 收集能量

在蚂蚁森林中并不能通过用 id 的方式定位到能量球，只能用在能量球可能出现的区域用坐标点击，start_x，end_x，start_y，end_y 是这个区域左上角和右下角的坐标位置

![](http://www.justdopython.com/assets/images/2021/02/antforest/2.png)

```python
# 获取手机屏幕宽高
width = int(driver.get_window_size()['width'])
height = int(driver.get_window_size()['height'])

# 收取能量
def collect_energy(driver, width, height):
    # 能量球可能出现的区域坐标
    start_x = 150
    end_x = 900
    start_y = 540
    end_y = 900

    for x in range(start_x, end_x, 50):
        for y in range(start_y, end_y, 50):
            x_scale = int((int(x) / width) * width)
            y_scale = int((int(y) / height) * height)
            # 点击指定坐标
            TouchAction(driver).press(x=x_scale, y=y_scale).release().perform()
    print('能量收取完毕')
```

### 收取好友能量

自己的能量收取完之后，点击 `找能量` 进入好友的蚂蚁森林收取好友的能量，直到出现`返回我的森林`页面

```python
def search_energy(driver, width, height):
    x = int((int(1000) / width) * width)
    y = int((int(1550) / height) * height)
    # 点击指定坐标
    TouchAction(driver).press(x=x, y=y).release().perform()
    time.sleep(1)
    is_collected = is_element_exist_by_xpath(driver, '//android.widget.Button[contains(@text, "返回我的森林")]')
    if is_collected:
        print('能量全部收集完毕')
        return

    collect_energy(driver, width, height)
    search_energy(driver, width, height)
```

### 总结

用 Appium 很简单的就将蚂蚁森林的能量球自动化了，看完这篇文章后希望小伙伴可以活学活用将其他 APP 应用中的重复的操作也自动化，省事又省力

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/AntForest>