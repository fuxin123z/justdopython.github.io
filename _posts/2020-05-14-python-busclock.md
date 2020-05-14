---
layout: post
category: python
title: 公交闹钟 —— 再也不用白等车了 
tagline: by 太阳雪
tags:
  - python100
---

生活中很多麻烦的事情，比如等人，等饭，等车，等等，很多时候没法不等，虽然习以为常，但总会想着怎么才能更便捷，更高效。
今天我们用 Windows 服务、实现一个公交闹钟，让乘车更优雅，少说废话，开干

<!--more-->

## 问题及分析

我明天乘坐公交车上下班，虽然很方便，但经常和班车擦肩而过，眼看着师傅头也不回的离去，那心情真是相当复(狂)杂(躁)，怎么才能不错过班车，而且不会等待太久，我找了很多方法，从撞运气，到估算，在到后来，发现了很多 app、网站可以查询实时公交信息，不过每次打开，选择路线，选择站点，查询，很麻烦，而且还得不断的关注，稍不留神就错过了

既然能从网站上查询到公交实时信息，是否可以用爬虫帮忙呢？ 应该没问题，然后让程序不断的跑，并且设置一个提醒时间段，比如上班时或者下班时，发现公交离站不远了，提醒自己出发，感觉挺好。

语言选用强大的 Python，为了避免忘记启动，最好做成服务，Linux 最为方便，不过得有台 Linux 主机，因为平时办公用 Windows，所以选用了做成 Windows 服务。另外，虽然也可以用计划任务中执行，但设置提醒时间段不够灵活

确定了方案，就开始行动吧

## 实践

只有简单的想法，没有简单的项目，将时间过程拆分为 获取到站时间、发送通知、制作服务 和 完善几个部分

### 获取到站时间

很多城市都有实时公交的查询网站，例如北京的北京公交集团网站 <http://www.bjbus.com>，可以查询实时公交信息，选择线路，形式方向，上车站点，就可以得到实时公交的信息。

在浏览其上点击 F12，打开网络选项卡，在网上上点击查询，找到查询请求

![查询请求](http://www.justdopython.com/assets/images/2020/05/busclock/01.png)

可以看到时 GET 请求，网址是：<http://www.bjbus.com/home/ajax_rtbus_data.php?act=busTime&selBLine=1&selBDir=5276138694316562750&selBStop=2>

请求参数含义为：

- act： 查询类型，固定值是 busTime
- selBLine： 线路，值表示线路名，例如 1 表示 1 路车
- selBDir： 行驶方向，值比较复杂，需要通过实际查询获得
- selBStop： 上车站点，值为线路在形式方向上的序号，从 1 开始，例如 2 表示第二站

用 httpx， 测试一下

> httpx 是基于经典库 requests 实现的，接口更简洁高效，通过 `pip install httpx` 安装

在 python 环境下，执行

```python
>>> import httpx
>>> url = "http://www.bjbus.com/home/ajax_rtbus_data.php?act=busTime&selBLine=1&selBDir=5276138694316562750&selBStop=2"
>>> r = httpx.get(url)
>>> print(r.status_code)
200
>>> print(r.text)
'{"html":"<div class=\\"inquiry_header\\"><div class=\\"left fixed\\"> ...
```

`httpx.get` 可以发送一个 GET 请求，返回响应对象，`status_code` 为请求状态编码，`text` 为响应内容

可以看到，返回的是 JSON 格式数据，通过 httpx 响应对象的 `json` 方法，可以知道将结果转换为 Python 的词典对象：

```python
>>> ret.json()
{'html': '<div class="inquiry_header"><div class="left fixed"><h3 id="lh">1路</h3>< ...
```

分析返回的结果，发现在开始部分，就有较为详细的公交实时信息，例如：

```html
<p>最近一辆车距离此还有&nbsp;3&nbsp;站，&nbsp;<span>589</span>&nbsp;米，预计到站时间&nbsp;<span>1</span>&nbsp;分钟</p>
```

如果没有车辆信息为：

```html
<p>车辆均已过站</p>
```

所以只要提取到预计到站时间数值就可以了

利用 BeautifulSoup 对 html 解析，得到到站时间：

```python
import httpx
from bs4 import BeautifulSoup as bs4

url = "http://www.bjbus.com/home/ajax_rtbus_data.php?act=busTime&selBLine=1&selBDir=5276138694316562750&selBStop=2"
r = httpx.get(url).json()
b = bs4(r.get('html'), 'html.parser')
info = b.find('article')
i = info.find_all('p')[1]
ret = re.search(r'\d+(?=\s分钟)', i.text)
```

> BeautifulSoup 可以通过 `pip install beautifulsoup4` 来安装

- 引入 BeautifulSoup 库，起个别名 bs4
- 获取请求响应，并转换为词典对象
- 提取词典中的 html 属性，将其转为 BeautifulSoup 对象 `b`，使用 Python 自带的 `html.parser` 解析器，其他解析器可能需要安装
- 通过分析 html 内容，可知有效信息在 article 标签中，通过 find 来获取只包含 article 标签的 BeautifulSoup 对象 `info`
- 将 `info` 中的 p 标签提取出来，其中第 2 个（列表第一个元素索引为 0 ）元素，就是需要提取的内容，放入 `i`
- 从 `i` 中的文本中，利用正则表达式，提取车辆到达分钟数，正则表达式的意思是：匹配有一个或者多个 `数字` 组成的后面是 `空格` 和字符 `分钟` 的数字部分
- 匹配到，返回车辆到达分钟数，返回 None，表示车辆还未发车

上述方法实际上就是一个简单爬虫，反复执行，直到发现合适的时间，发出提醒，就完成了核心任务

### 发送通知

发送通知有多种方法，例如 Windows 下弹窗或者消息，不过在实践中遇到不少困难，所以选用了邮件通知，不仅实现简单，如果在手机上配置了邮件客户端，收到邮件会给出提醒，更加方便

用 Python 很容易发邮件，直接看代码:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart('alternative')  # 实例化email对象
msg['from'] = 'tom@example.com'  # 对应发件人邮箱昵称、发件人邮箱账号
msg['to'] = ';'.join(['lily@example.com'])  # 对应收件人邮箱昵称、收件人邮箱账号
msg['subject'] = '你好'  # 邮件的主题
msg.attach(MIMEText('你好，很高兴认识你...', 'html'))  # 附加正文

SMTP_SERVER = 'smtp.example.com'  # 邮箱服务器
SSL_PORT = '465'  # 端口
USER_NAME = 'username'  # 邮箱用户名
USER_PWD = 'password'  # 密码

smtp = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)  # 邮件服务器地址和端口
smtp.ehlo()  # 用户认证
smtp.login(USER_NAME, USER_PWD)  # 括号中对应的是发件人邮箱账号、邮箱密码
smtp.sendmail(FROM_MAIL, TO_MAIL, str(msg))  # 收件人邮箱账号、发送邮件
smtp.quit()  # 等同 smtp.close()  ,关闭连接

```

例如，我收到的一个邮件通知：

![邮件提醒](http://www.justdopython.com/assets/images/2020/05/busclock/02.png)

### 制作服务

万事俱备，只欠东风，接下了，需要将脚本做成可执行程序，注册为 Windows 服务

#### Windows 服务脚本

用 Python 写 需要借助于 `win32api` 库

安装 `win32api` 库

```bash
pip install pywin32
```

这是服务脚本框架:

```python
import win32api
import win32event
import win32service
import win32serviceutil
import servicemanager

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "服务名称"
    _svc_display_name_ = "在服务列表中显示的名称"
    _svc_description_ = "服务描述"
    def __init__(self, args):
      win32serviceutil.ServiceFramework.__init__(self, args)
      self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
      self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
      # 这里写服务启动后的业务逻辑
      win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def SvcStop(self):
      self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
      # 这里写服务即将停止时的业务逻辑
      win32event.SetEvent(self.stop_event)
      self.ReportServiceStatus(win32service.SERVICE_STOPPED)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MyService)
    servicemanager.StartServiceCtrlDispatcher()
  else:
    win32serviceutil.HandleCommandLine(MyService)
```

- 引入服务相关包
- 定义继承自 `win32serviceutil.ServiceFramework` 的服务类
- `_svc_name_`,`_svc_display_name_`,`_svc_description_` 为服务声明属性
- 服务类初始化 `__init__` 方法中, 定义服务停止事件，实际应用中可以初始化业务相关的属性
- `SvcDoRun` 为服务启动时的回调方法，可以写服务执行中的处理逻辑
- `SvcStop` 为服务结束时的回调方法，可以写服务结束时的处理逻辑
- `ReportServiceStatus` 为服务状态通知方法，以便服务管理器及时获取到服务状态
- 当脚本执行时，如果没有参数，表示服务在启动，如果有参数，将运行服务管理方法，例如 install(安装)、start（启动）等

#### 打包

写好服务代码之后，需要将其打包为 EXE

> 虽然 上述服务脚本可以不用打包为 EXE 也能注册为服务，但是常常会因为环境、组件引用问题导致注册的服务失败

Pyinstaller 工具可以将 Python 脚本打包成 Windows 的可执行文件

安装:

```bash
pip install pyinstaller
```

然后可以在命令行中直接使用，例如将 service.py 打包为 EXE:

```bash
pyinstaller service.py
```

打包过程较慢，会有大量信息输出，如果没有报错信息，即为打包成功。

打包成后，会在脚步所在目录创建 build 和 dist 目录，dist 目录下会有打包好的 EXE，名称与脚本名一样

> **注意:**
> 打包好的程序，注册服务后，启动时可能会报 win32timezone 找不到的错误，这时需要加一个参数:
> --hiddenimport win32timezone
> 打包命令换成：`pyinstaller --hiddenimport win32timezone -F service.py`
> 重新打包即可

#### 注册服务

做好了可执行文件，就可以注册为服务了

首先需要用管理员权限运行命令行

![管理员身份运行命令行](http://www.justdopython.com/assets/images/2020/05/busclock/03.png)

- 注册服务

  ```bash
  service.exe install
  ```

  注册后，可以在计算机管理的服务，或者从任务管理的服务列表中看到，名称为 脚本中 服务类 `_svc_display_name_` 所定义的名称
  ![注册好的服务](http://www.justdopython.com/assets/images/2020/05/busclock/05.png)
- 启动服务

  ```bash
  service.exe start
  ```

  也可以在服务列表中启动

- 停止服务

  ```bash
  service.exe stop
  ```

  也可以在服务列表中停止

- 注销服务

  ```bash
  service.exe remove
  ```

  注销服务时，需要先停止服务，不然会有个服务尸体在服务列表中

除了通过 install、start 参数管理服务外，还可以使用 Windows 命令 `sc` 来操作，有兴趣可以了解下

如果启动服务报错，可以在 Windows 的事件管理器中查看错误日志，以便得到详细信息：
![事件管理器日志](http://www.justdopython.com/assets/images/2020/05/busclock/04.png)

### 完善

从构建公交实时信息爬虫，到启动 Windows 服务，主要的工作已经完成了，整体跑一遍，至少可以确定方案是可行。

如果要实际应用，还有很多细节问题需要处理

#### 设置提醒时间段

作为 Windows 服务运行的话，会长时间处于运行状态，公交提醒功能，只需要在特定事件段有效就行，所以需要判断当前时间是否进入提醒时间窗口， `onTime` 方法可以做到这一点：

```python
import datetime
def onTime(begin, end):
  d_time = datetime.datetime.strptime(
    str(datetime.datetime.now().date())+begin, '%Y-%m-%d%H:%M')
  d_time1 = datetime.datetime.strptime(
    str(datetime.datetime.now().date())+end, '%Y-%m-%d%H:%M')
  n_time = datetime.datetime.now()
  if n_time > d_time and n_time < d_time1:
    return True
  else:
    return False
```

- 引入 datetime 包
- 方法接受两个参数，开始时间和结束时间，例如"18:00"，"18:30"
- 如果当前时间段在开始时间和结束时间之内，返回 `True`，否则返回 `False`

在服务的启动方法中，写一个循环，每次循环判断一下当前时间，如果 onTime 返回 True 就进入到提醒业务代码中

#### 支持多条线路

同一路车，但是不同方向需要看成不同的线路，所以在提醒方法 `run` 中，需要同时对多条线路进行判断：

```python
def run(self):
  for line in self.config.lines:
    if self.onTime(line['begin'], line['end']):
      if line.get('needSentMail', True):
        bustime = self.getBusTime(line)
        if  bustime is not None:
          if int(bustime) <= int(line.get('latestLeaveMinute', self.config.latestLeaveMinute)):
            self.mailClient.send_mail(self.config.alertMail, '班车提醒: '+line['line'], '车辆即将到站，现在出发正当时')
            line['needSentMail'] = False  # 发送通知后，不必再发了
    else:
        line['needSentMail'] = True
```

其中 `needSentMail` 表示是否需要发送通知，当在时间窗口中发送了通知，就不必再发了，如果过了时间窗口，需要将其设置为需要发送

线路配置为列表：

```python
lines = [{
  "line": "835快",
  "dir": "5066222788346588777",
  "stop": "13",
  "begin": "08:00",
  "end": "08:30"
}, {
  "line": "835快",
  "dir": "4997908670784162973",
  "stop": "3",
  "begin": "19:00",
  "end": "20:30"
}]
```

#### 配置

将业务相关信息写死在代码中不是个好主意，所以需要将通知邮件的配置，线路信息等写到配置中，这样如果业务发生变化时，只需修改下配置文件就可以了，我使用 json 格式的配置文件 config.json：

```json
{
  "loopWaitSeconds": 60,
  "spurtWaitSeconds": 10,
  "latestLeaveMinute": 5,
  "mailConfig": {
    "FROM": "tom@example.com",
    "HOST": "smtp.example.com",
    "PORT": "465",
    "USER": "tom",
    "PASS": "password",
    "SSL": true
  },
  "alertMail": "lily@example.com",
  "lines": [{
    "line": "835快",
    "dir": "5066222788346588777",
    "stop": "13",
    "begin": "08:00",
    "end": "08:30"
  }, {
    "line": "835快",
    "dir": "4997908670784162973",
    "stop": "3",
    "begin": "19:00",
    "end": "20:30"
  }]
}
```

配置字段比较简单，下面这些需要解释下:

- loopWaitSeconds:  空循环时的等待秒数
- spurtWaitSeconds:  进入提醒时间窗口的等待秒数
- latestLeaveMinute: 可以出发的时间，即具车辆到站还有多久时，需要发出通知

Python 可以方便的读取 json 配置文件，读取之后，将其转换为一个类，在代码中使用更方便:

```python

class Config:
  def __init__(self, config):
    self.loopWaitSeconds = config.get("loopWaitSeconds", 60)
    self.spurtWaitSeconds = config.get("spurtWaitSeconds", 10)
    self.mailConfig = config.get("mailConfig", None)
    self.latestLeaveMinute = config.get("latestLeaveTime", 5)
    self.lines = config.get("lines", {})

import json

with open(r"C:\config.json", "r", encoding='UTF-8') as config_file:
  config = Config(json.load(config_file))  # 整体配置
```

这里需要注意的是，配置文件的位置，当程序以服务的形式运行时，当前路径是个临时目录，因此写绝对路径比较方便

## 总结

虽然解决了问题，不过想要同很多 app 那样优雅，还需要做很多工作。通过这次实践，可以了解了 Python 打包，Windows 服务，简单爬虫，邮件发送 等功能，为日后做其他应用奠定了基础，比如基于这个框架，可以做一个打卡签到功能，让自己更自由  
很多时候舒适让我们懒于行动，而行动带来的惊喜远胜过一时的安逸……  
感谢阅读，代码示例中有较为完整的代码，欢迎参考研究

## 参考

- [https://www.cnblogs.com/gopythoner/p/6337543.html](https://www.cnblogs.com/gopythoner/p/6337543.html)
- [https://blog.csdn.net/u014292858/article/details/88531597](https://blog.csdn.net/u014292858/article/details/88531597)
- [https://stackoverflow.com/questions/33212949/importerror-no-module-named-win32timezone-when-i-make-a-singleone-exe-from-a-py](https://stackoverflow.com/questions/33212949/importerror-no-module-named-win32timezone-when-i-make-a-singleone-exe-from-a-py)
- [https://blog.csdn.net/ghostfromheaven/article/details/8604738](https://blog.csdn.net/ghostfromheaven/article/details/8604738)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/busclock>
