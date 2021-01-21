---
layout: post
category: python
title: 用 Python + Appium 的方式自动化清理微信僵尸好友
tagline: by 某某白米饭
tags: 
  - python
  - 微信
  - appium
---

随着微信的使用时间越长，微信好友也越来越多，有些好友将你删除了你也不知道。当我们发消息的时候会出现下面扎心的一幕，然后默默将他删除
<!--more-->
![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_0.png)

### 使用 Appium

基础的 appium 使用在公众号文章 [《解放双手，提高生产力，这款神器你值得拥有》](https://mp.weixin.qq.com/s/RzGxuiqXF8tCsdY3TZgoAw) 中已经讲过了，这里使用最新 1.20.0 版本的 appium，旧版本会出现真机微信闪退的情况

安装一下 Python 用到的模块

```
pip install Appium-Python-Client
```

### 获取好友列表

在 Pycharm 中配置一下启动环境

```json
desired_capabilities = {
    'platformName': 'Android', # 操作系统
    'deviceName': '2a254a02', # 设备 ID，使用 cmd 中 adb devices 命令得到
    'platformVersion': '10.0.10', # 设备版本号，在手机设置中查看
    'appPackage': 'com.tencent.mm', # app 包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI', # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
print('微信启动')
```

下图是 appium 启动后截图

![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_1.png)

点击红框中按钮，将上面的参数填上，点击 start Session

![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_2.png)

启动后点击刷新按钮，看到的界面和真机上一样了，在真机上点击通讯录按钮并刷新界面

![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_3.png)

在 appium 界面点击一个好友，可以看到这个好友有一个 content-desc 和 resource-id 代表了昵称和资源 id

![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_4.png)

然后我们用 Python 获取所有的好友昵称

```python
# 所有好友
friends = []
def get_friends():
    # 好友id
    address_list = driver.find_elements_by_id('com.tencent.mm:id/dy5')
    for address in address_list:
        # 昵称
        friend = address.get_attribute('content-desc')
        # 过滤掉自己、微信团队、文件夹传输助手
        if friend != '某某白米饭' and friend != '微信团队' and friend != '文件夹传输助手':
            friends.append(friend)
        # 获取到最后一个好友返回
        if friend == '🔥Jiuki🔥':
            return
    # 向上滚动获取好友，获取好友会重复，最后结果需过滤
    driver.swipe(100, 1000, 100, 500)
    # 递归循环得到所有好友
    get_friends()
```

### 得到被对方删除的好友

在微信中被对方删除后，是不能进行转账的，这也是用来判断被对方删除的依据

![](http://www.justdopython.com/assets/images/2021/01/wxDelFriends/w_5.png)

下面四步骤就是用 Python 模拟微信转账操作

1. 按上面获取的昵称搜索得到好友
2. 在好友对话框中点击 + 号，获取到转账按钮
3. 在转账界面输入 1 元，点击转账按钮，得到是否为好友结果
4. 最后返回到搜索页面清空搜索框内容

```python
# 判断是否被删
def is_del(f):

    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(2)
    # 在搜索框输入搜索信息
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(f)
    time.sleep(2)
    #点击好友
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(2)
    # 转账操作 + 号
    driver.find_element_by_id('com.tencent.mm:id/aks').click()
    time.sleep(2)
    # 转账按钮
    driver.find_elements_by_id('com.tencent.mm:id/pa')[5].click()
    time.sleep(2)
    # 数字 1
    driver.find_element_by_id('com.tencent.mm:id/cx_').click()
    time.sleep(1)
    # 付款界面转账按钮
    driver.find_element_by_id('com.tencent.mm:id/cxi').click()
    time.sleep(2)

    # 判断是否被删
    is_exist = is_element('com.tencent.mm:id/dos')
    if is_exist:
        # 不能转账就点击确定按钮
        driver.find_element_by_id('com.tencent.mm:id/doz').click()

        time.sleep(2)
    else:
        # 可以转账就后退
        driver.press_keycode(4)

    # 后退到 搜索页面
    driver.press_keycode(4)
    driver.press_keycode(4)
    driver.press_keycode(4)
    driver.press_keycode(4)
    # 清空文本框
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys('')
    
    return f

def is_element(id):
    flag = None
    try:
        driver.find_element_by_id(id)
        flag = True
    except NoSuchElementException:
        flag = False
    finally:
        return flag
```

因为 appium 操作 APP 有延迟，所以在每个操作后延迟 2 秒

#### 删除好友

在得到被删好友的联系人之后，用个步骤在 Python 中微信删除好友

1. 在搜索框中用昵称搜索被删好友的联系人
2. 进入对话界面后，点击界面右上角的...
3. 点击好友头像
4. 点击个人信息界面右上角的...
5. 点击删除按钮
6. 在选择框中点击删除

```python
# 删除好友
def del_friend(friend):
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(friend)
    time.sleep(2)
    #点击好友
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(2)
    # 右上角...
    driver.find_element_by_id('com.tencent.mm:id/cj').click()
    time.sleep(2)
    # 头像
    driver.find_element_by_id('com.tencent.mm:id/f3y').click()
    time.sleep(2)
    # 右上角...
    driver.find_element_by_id('com.tencent.mm:id/cj').click()
    time.sleep(2)
    # 删除按钮
    driver.find_element_by_id('com.tencent.mm:id/g6f').click()
    time.sleep(2)
    # 选中删除
    driver.find_element_by_id('com.tencent.mm:id/doz').click()
```

### 总结

学习了 appium 的使用，并用它自动化清理了微信僵尸好友。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/wxDelFriends>