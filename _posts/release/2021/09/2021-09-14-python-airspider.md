---
layout: post
title: 神器！五分钟完成大型爬虫项目！
category: python
tagline: by 闲欢
tags: 
  - python
---

![封面](http://www.justdopython.com/assets/images/2021/09/airspider/fm.jpg)

对于学习 Python 爬虫的人来说，Scrapy 这个框架是一个绕不过去的槛。它是一个非常重量级的 Python 爬虫框架，如果你想要做一些复杂的爬虫项目，可能就需要用到它。

但是，由于 Scrapy 框架很复杂，它的学习成本也非常高，学习的道路上布满了很多坑，并且都很难找到解决办法。对于初学者来说，学习 Scrapy 框架需要极大的耐心和勇气，一般人很有可能在中途就放弃了。

![太难了](http://www.justdopython.com/assets/images/2021/09/airspider/0.jpg)

不要担心，既然有痛点，肯定就有人来抚慰。今天给大家介绍一个类似于 Scrapy 的开源爬虫框架——feapder。它的架构逻辑和 Scrapy 类似，但是学习成本非常低，不需要繁琐的配置，不需要复杂的项目架构，也可以轻松应对复杂爬虫需求。


<!--more-->

### 简介

feapder 是一款上手简单，功能强大的 Python 爬虫框架，使用方式类似 scrapy，方便由 scrapy 框架切换过来，框架内置三种爬虫：

- AirSpider 爬虫比较轻量，学习成本低。面对一些数据量较少，无需断点续爬，无需分布式采集的需求，可采用此爬虫。
- 
- Spider 是一款基于 redis 的分布式爬虫，适用于海量数据采集，支持断点续爬、爬虫报警、数据自动入库等功能
- 
- BatchSpider 是一款分布式批次爬虫，对于需要周期性采集的数据，优先考虑使用本爬虫。

feapder 支持断点续爬、数据防丢、监控报警、浏览器渲染下载、数据自动入库 Mysql 或 Mongo，还可通过编写 pipeline 对接其他存储。

今天我主要介绍一下 AirSpider 这种爬虫。


### 安装

通用版

> pip3 install feapder

完整版：

> pip3 install feapder[all]

通用版与完整版区别在于完整版支持基于内存去重。


### AirSpider 使用

我们今天通过爬取东方财富网的股票研报数据（http://data.eastmoney.com/report/stock.jshtml）来讲解怎样使用 AirSpider 进行数据爬取。

#### 创建爬虫

创建爬虫的语句跟 Scrapy 类似：

> feapder create -s report_spider

运行完成后，就会在当前目录下生成一个 report_spider.py 的文件，打开文件后，我们可以看到一个初始化的代码：

```python
import feapder


class ReportSpider(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://www.baidu.com")

    def parse(self, request, response):
        print(response)


if __name__ == "__main__":
    ReportSpider().start()

```

这代码是可以直接运行的，运行之后，你会看到控制台信息：

![](http://www.justdopython.com/assets/images/2021/09/airspider/1.jpg)

默认生成的代码继承了feapder.AirSpider，包含 start_requests 及 parser 两个函数，含义如下：

1. feapder.AirSpider：轻量爬虫基类。
2. start_requests：初始任务下发入口。
3. feapder.Request：基于requests库类似，表示一个请求，支持requests所有参数，同时也可携带些自定义的参数。
4. parser：数据解析函数。
5. response：请求响应的返回体，支持xpath、re、css等解析方式。


#### 自定义解析函数

开发过程中解析函数往往不止有一个，除了系统默认的parser外，还支持自定义解析函数，比如我要写一个自己的解析函数，写法如下：

```python
    def start_requests(self):
        yield feapder.Request("http://reportapi.eastmoney.com/report/list?cb=datatable1351846&industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2021-09-13&endTime=2021-09-14&pageNo=1&fields=&qType=0&orgCode=&code=*&rcode=&p=2&pageNum=2&_=1603724062679",
                              callback=self.parse_report_info)

    def parse_report_info(self, request, response):
        html = response.content.decode("utf-8")
        if len(html):
            content = html.replace('datatable1351846(', '')[:-1]
            content_json = json.loads(content)
            print(content_json)

```

只需要在 Request 请求中加个 callback 参数，将自定义解析函数名放进去即可。

#### 携带参数

如果你需要将请求中的一些参数带到解析函数中，你可以这样做：

```python
    def start_requests(self):
        yield feapder.Request("http://reportapi.eastmoney.com/report/list?cb=datatable1351846&industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2021-09-13&endTime=2021-09-14&pageNo=1&fields=&qType=0&orgCode=&code=*&rcode=&p=2&pageNum=2&_=1603724062679",
                              callback=self.parse_report_info, pageNo=1)

    def parse_report_info(self, request, response):
        print(request.pageNo)
        html = response.content.decode("utf-8")
        if len(html):
            content = html.replace('datatable1351846(', '')[:-1]
            content_json = json.loads(content)
            print(content_json)
```

在 Request 里面添加你需要携带的参数，在解析函数中通过 request.xxx 就可以获取到（本例中我将请求的页码 pageNo 作为携带参数传递到解析函数中，运行程序就可以看到打印了1）。

#### 下载中间件

下载中间件用于在请求之前，对请求做一些处理，如添加cookie、header等。写法如下：

```python
    def download_midware(self, request):
        request.headers = {
            "Connection": "keep-alive",
            "Cookie": "qgqp_b_id=0f1ac887e1e3e484715bf0e3f148dbd8; intellpositionL=1182.07px; st_si=32385320684787; st_asi=delete; cowCookie=true; intellpositionT=741px; st_pvi=73966577539485; st_sp=2021-03-22%2009%3A25%3A40; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=4; st_psi=20210914160650551-113300303753-3491653988",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
            "Host": "reportapi.eastmoney.com"
        }
        return request

```

这里我主要添加了一些请求头信息，模拟真实浏览器访问场景。

#### 校验

校验函数, 可用于校验 response 是否正确。若函数内抛出异常，则重试请求。若返回 True 或 None，则进入解析函数，若返回 False，则抛弃当前请求。可通过 request.callback_name 区分不同的回调函数，编写不同的校验逻辑。

```python
    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200") # 重试
```


#### 失败重试机制

框架支持重试机制，下载失败或解析函数抛出异常会自动重试请求。默认最大重试次数为100次，我们可以引入配置文件或自定义配置来修改重试次数。上面的校验中，我们抛出异常，就可以触发重试机制。

#### 爬虫配置

爬虫配置支持自定义配置或引入配置文件 setting.py 的方式。我们只需要在当前目录下映入 setting.py 就可以了。我们可以在配置里面配置 数据库信息、Redis 信息、日志信息等等。

这里给出一份最全的配置：

```python
import os


# MYSQL
MYSQL_IP = ""
MYSQL_PORT = 3306
MYSQL_DB = ""
MYSQL_USER_NAME = ""
MYSQL_USER_PASS = ""

# REDIS
# IP:PORT
REDISDB_IP_PORTS = "xxx:6379"
REDISDB_USER_PASS = ""
# 默认 0 到 15 共16个数据库
REDISDB_DB = 0

# 数据入库的pipeline，可自定义，默认MysqlPipeline
ITEM_PIPELINES = ["feapder.pipelines.mysql_pipeline.MysqlPipeline"]

# 爬虫相关
# COLLECTOR
COLLECTOR_SLEEP_TIME = 1  # 从任务队列中获取任务到内存队列的间隔
COLLECTOR_TASK_COUNT = 100  # 每次获取任务数量

# SPIDER
SPIDER_THREAD_COUNT = 10  # 爬虫并发数
SPIDER_SLEEP_TIME = 0  # 下载时间间隔 单位秒。 支持随机 如 SPIDER_SLEEP_TIME = [2, 5] 则间隔为 2~5秒之间的随机数，包含2和5
SPIDER_MAX_RETRY_TIMES = 100  # 每个请求最大重试次数

# 浏览器渲染下载
WEBDRIVER = dict(
    pool_size=2,  # 浏览器的数量
    load_images=False,  # 是否加载图片
    user_agent=None,  # 字符串 或 无参函数，返回值为user_agent
    proxy=None,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
    headless=False,  # 是否为无头浏览器
    driver_type="CHROME",  # CHROME 或 PHANTOMJS,
    timeout=30,  # 请求超时时间
    window_size=(1024, 800),  # 窗口大小
    executable_path=None,  # 浏览器路径，默认为默认路径
    render_time=0, # 渲染时长，即打开网页等待指定时间后再获取源码
)

# 重新尝试失败的requests 当requests重试次数超过允许的最大重试次数算失败
RETRY_FAILED_REQUESTS = False
# request 超时时间，超过这个时间重新做（不是网络请求的超时时间）单位秒
REQUEST_LOST_TIMEOUT = 600  # 10分钟
# 保存失败的request
SAVE_FAILED_REQUEST = True

# 下载缓存 利用redis缓存，由于内存小，所以仅供测试时使用
RESPONSE_CACHED_ENABLE = False  # 是否启用下载缓存 成本高的数据或容易变需求的数据，建议设置为True
RESPONSE_CACHED_EXPIRE_TIME = 3600  # 缓存时间 秒
RESPONSE_CACHED_USED = False  # 是否使用缓存 补采数据时可设置为True

WARNING_FAILED_COUNT = 1000  # 任务失败数 超过WARNING_FAILED_COUNT则报警

# 爬虫是否常驻
KEEP_ALIVE = False

# 设置代理
PROXY_EXTRACT_API = None  # 代理提取API ，返回的代理分割符为\r\n
PROXY_ENABLE = True

# 随机headers
RANDOM_HEADERS = True
# requests 使用session
USE_SESSION = False

# 去重
ITEM_FILTER_ENABLE = False  # item 去重
REQUEST_FILTER_ENABLE = False  # request 去重

# 报警 支持钉钉及邮件，二选一即可
# 钉钉报警
DINGDING_WARNING_URL = ""  # 钉钉机器人api
DINGDING_WARNING_PHONE = ""  # 报警人 支持列表，可指定多个
# 邮件报警
EMAIL_SENDER = ""  # 发件人
EMAIL_PASSWORD = ""  # 授权码
EMAIL_RECEIVER = ""  # 收件人 支持列表，可指定多个
# 时间间隔
WARNING_INTERVAL = 3600  # 相同报警的报警时间间隔，防止刷屏; 0表示不去重
WARNING_LEVEL = "DEBUG"  # 报警级别， DEBUG / ERROR

LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME  # log存储路径
LOG_LEVEL = "DEBUG"
LOG_COLOR = True  # 是否带有颜色
LOG_IS_WRITE_TO_CONSOLE = True # 是否打印到控制台
LOG_IS_WRITE_TO_FILE = False  # 是否写文件
LOG_MODE = "w"  # 写文件的模式
LOG_MAX_BYTES = 10 * 1024 * 1024  # 每个日志文件的最大字节数
LOG_BACKUP_COUNT = 20  # 日志文件保留数量
LOG_ENCODING = "utf8"  # 日志文件编码
OTHERS_LOG_LEVAL = "ERROR"  # 第三方库的log等级

```

各位自己可以从这些配置中选一些自己需要的进行配置。

#### 数据入库

框架内封装了MysqlDB、RedisDB，与pymysql不同的是，MysqlDB 使用了线程池，且对方法进行了封装，使用起来更方便。RedisDB 支持 哨兵模式、集群模式。

如果你在 setting 文件中配置了数据库信息，你就可以直接使用：

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.db = MysqlDB()
```

如果没有配置，你也可以在代码里面进行配置：

```python
db = MysqlDB(
        ip="localhost",
        port=3306,
        user_name="feapder",
        user_pass="feapder123",
        db="feapder"
    )

```

建立数据库连接后，你就可以使用这个框架内置的数据库增删改查函数进行数据库操作了。具体方法可以根据代码提示来查看：

![](http://www.justdopython.com/assets/images/2021/09/airspider/2.jpg)

我们的示例程序，运行之后，就可以在数据表中看到数据了：

![](http://www.justdopython.com/assets/images/2021/09/airspider/3.jpg)



### 总结

今天主要给大家介绍了一下 feadper 框架的三剑客之一——AirSpider，这是这个框架最简单的一种爬虫方式，也是最容易入门的。当然，今天介绍的每一项里面还有一些更细节的东西，由于篇幅原因，这里没有介绍，大家可以自己去探索和发现。码文不易，点个`在看`送鼓励~


