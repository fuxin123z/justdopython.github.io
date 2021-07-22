---
layout: post
title: 自动抢票之 12306 登录篇
category: python
tagline: by 某某白米饭
tags: 
  - python
  - 爬虫

---
逢年过节 12306 的票总是要靠抢，前几天小编就在抢周一去上海的票，实在是抢不到呀，就撸了一个自动抢票的脚本。

抢票的思路就是使用 selenium 模拟用户登录 12306 网站购票行为，登录后抓取 12306 网站火车票数据并自动购票。

<!--more-->

![](http://www.justdopython.com/assets/images/2021/07/12306/-1.png)

### 准备工作

首先需要做一些准备工作，安装一些第三方库类和下载 chromedriver.exe 文件：

1. 下载和 Chrome 浏览器相同版本的 chromedriver.exe 文件
2. pip install selenium
3. 超级鹰打码，识别图片验证码


### 用户名和密码

用 `https://kyfw.12306.cn/otn/resources/login.html` 做为起始登录页。网页的默认登录就是扫码，我们需要账号登录网站。这里用 selenium 模拟点击账号登录按钮。

![](http://www.justdopython.com/assets/images/2021/07/12306/0.png)

账号登录的流程就是输入用户名和密码然后调用超级鹰 API 获取图片验证的坐标后，点击登录按钮。

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Ticket(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'

    
    def findElement(self, type, id):
        # 查找元素
        return EC.visibility_of_element_located((type, id))

    def login(self):
        self.driver = webdriver.Chrome(executable_path='D:\chromedriver.exe')

        self.wait = WebDriverWait(self.driver, 10, 0.1)
        self.driver.get(self.login_url)
        
        self.wait.until(self.findElement(By.LINK_TEXT,'账号登录')).click()

        self.wait.until(self.findElement(By.ID, 'J-userName')).send_keys(self.username)
        
        self.wait.until(self.findElement(By.ID, 'J-password')).send_keys(self.password)
       
if __name__ == '__main__':
    username = 'xxxx'
    password = 'xxxx'

    ticket = Ticket(username, password)
    ticket.login()
```

### 图片验证码

上面这段代码就是将用户名和密码放入文本框。下面我们调用超级鹰（`https://www.chaojiying.com/`）API 识别图片验证码。它的验证码类型是 9004。

![](http://www.justdopython.com/assets/images/2021/07/12306/1.png)

下面就是超级鹰的 Python 示例代码，把它改造成为 chaojiying 类。

![](http://www.justdopython.com/assets/images/2021/07/12306/3.png)

它返回的格式是这样的 JSON 串，pic_id 和 pic_str 都是我们需要的，pic_id 用来打错码后返还消费的题分，pic_str 是验证码的坐标轴。

```json
{'err_no': 0, 'err_str': 'OK', 'pic_id': '1147820166678300023', 'pic_str': '51,83|167,180', 'md5': '3a3a43edc56d5fb2e5370db186ddf299'}
```

12306 网站上图片是 base64 的，它上面的 `class=lgcode-success` 元素 style 可以用来判断验证是否通过，不通过可以继续调用打码 API。

![](http://www.justdopython.com/assets/images/2021/07/12306/2.png)

```python
import time,base64
import chaojiying
from selenium.webdriver import ActionChains

success_flag = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lgcode-success'))).get_attribute('style')

while success_flag == 'display: none;':
    img = self.wait.until(EC.visibility_of_element_located((By.ID, 'J-loginImg')))

    base64Img = img.get_attribute('src')
    base64Img = base64Img.replace('data:image/jpg;base64,', '')
    imgdata=base64.urlsafe_b64decode(base64Img)
    file=open('1.jpg','wb')
    file.write(imgdata)
    file.close()

    cj = chaojiying.Chaojiying_Client('xxxx', 'xxxx', 'xxxx')
    im = open('1.jpg', 'rb').read()
    cjy_result = cj.PostPic(im, 9004)
    print(cjy_result)											
    x_y = cjy_result['pic_str']
    pic_id = cjy_result['pic_id']

    all_list = []
    for i in x_y.split('|'):
        all_list.append([int(i.split(',')[0]), int(i.split(',')[1])])

    for rangle in all_list:
        ActionChains(self.driver).move_to_element_with_offset(img, rangle[0], rangle[1]).click().perform()

    self.wait.until(self.findElement(By.ID, 'J-login')).click()
    success_flag = self.driver.find_element_by_class_name('lgcode-success').get_attribute('style')

    if success_flag == 'display: none;':
        cj.ReportError(pic_id)
```

![](http://www.justdopython.com/assets/images/2021/07/12306/4.png)

### 滑块

登录之后又出现了滑块验证，这个问题不大 selenium 下的 ActionChains 可以完美解决。实验了几次之后居然一直不通过，一番 google 之后。才惊觉现在的滑块验证码是如此的狡猾，居然可以识别是不是用户滑动的。最后参考 《selenium篇之滑动验证码》<sup>①</sup> 这篇文章可以模拟用户先快速滑动然后慢下来的滑动行为。

![](http://www.justdopython.com/assets/images/2021/07/12306/5.png)

```python
from selenium.webdriver import ActionChains

nc_1_n1z = self.wait.until(self.findElement((By.ID, 'nc_1_n1z')))
tracks = [6,16,31,52,72,52,62,50]

action = ActionChains(self.driver)

action.click_and_hold(nc_1_n1z).perform()
for track in tracks:
    action.move_by_offset(track, 0)
time.sleep(0.5)
action.release().perform()
```

![](http://www.justdopython.com/assets/images/2021/07/12306/6.png)

然后又又又出问题了，模拟用户滑块验证之后，居然还是没通过滑块验证。再次 google 一番，原来 selenium 容易被识别出来。参考 《最完美方案！模拟浏览器如何正确隐藏特征》<sup>②</sup> 这篇文章。安装了 Node Js，生成 stealth.min.js（注：已经放在了 github 上），并在浏览器打开登录页面加载 stealth.min.js。

```python
def login(self):
    self.driver = webdriver.Chrome(executable_path='D:\chromedriver.exe')

    with open('D:\stealth.min.js') as f:
        stealth = f.read()
    self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": stealth})
    # 下面是登录代码
    # ....
```

历经千辛万苦，终于登录成功啦。

![](http://www.justdopython.com/assets/images/2021/07/12306/7.png)

### 总结

12306 的登录是越来越严格了，不仅有图片验证码，还有滑块验证码。逢年过节买票是真真真的难。

### 参考资料

- [1] [selenium篇之滑动验证码](https://www.cnblogs.com/jackzz/p/11443193.html)
- [2] [最完美方案！模拟浏览器如何正确隐藏特征](https://cloud.tencent.com/developer/article/1755513)

> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/12306)
