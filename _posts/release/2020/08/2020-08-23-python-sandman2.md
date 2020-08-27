---
layout: post
category: python
title: 不用一行代码，用 API 操作数据库，你信吗
tagline: by 太阳雪
tags:
  - python
  - matplotlib
  - 定投
---
数据库的重要性不言而喻，但是数据库操作起来却不容易，需要用到各种管理工具，各种不同的连接方式，如果有方便的，屏蔽不同数据库细节的工具该多好，功夫不负有心人，我还真找了这样一个工具，不仅支持多种数据库，更厉害的是，不用为适配写一行代码，来了解下吧
<!--more-->

## 神器出场

今天的主角是 sandman2

可以基于已存在的数据库，自动生成一个 RESTful API 服务器，而不需要写任何代码，用作者的话说，简单地就像给食物加点盐

更厉害的是，从简单地 SQLite 数据库，到大型的商业数据 PostgreSQL， 都能完美支持，且不用写一行代码

目前支持的数据库：

- MySQL
- PostgreSQL
- Oracle
- Microsoft SQL Server
- SQLite
- Sybase
- Drizzle
- Firebird

这让我想起了曾经因为找不到合适的数据库框架手忙脚乱的日子，如果早点知道 sandman2 就好了

之所以叫 sandman2，是因为它的前辈是 sandman，sandman 已经有了很强的数据库支持能力，不过在 SQLAlchemy 0.9 版本中，增加了 `automap` 功能，可以进一步使 sandman 得到简化，于是重写了 sandman，就有了 sandman2，并且 sandman2 的功能远超 sandman

使用 pip 安装 `pip install sandman2`

安装成功后，就可以得到一个 `sandman2ctl` 命令行工具，用它来启动一个 RESTful API 服务器

不用写一行代码，直接启动：

```bash
sandman2ctl sqlite+pysqlite:///data.db
```

> **注意**：
如果用的 python 版本是 3.8 及以上，且在 Windows 上，执行时可能会遇到，`AttributeError: module 'time' has no attribute 'clock'` 的错误
> 这是因为 3.8 以后 `time` 模块的 `clock` 属性换成了 `perf_counter()` 方法，所以需要修改下 `lib\site-packages\sqlalchemy\util\compat.py` 的 331 行，将 `time_func = time.clock` 换成 `time_func = time.perf_counter()` 保存即可

启动之后，默认端口是 5000，访问地址是 `http://localhost:5000/admin` 就能看到服务器控制台了
![控制台](http://www.justdopython.com//assets/images/2020/08/sandman2/01.jpg)

## 数据库连接

前面已经看到连接 SQLite 数据的方法

sandman2 是基于 SQLAlchemy 的，所以使用连接 Url 来连接数据库

格式为

`dialect+driver://username:password@host:port/database`

- dialect 为数据库类型，如 mysql、SQLite 等
- driver 为数据库驱动模块名，例如 pymysql、psycopg2、mysqldb 等，如果忽略，表示使用默认驱动

以 mysql 数据库为例：

```python
sandman2ctl 'mysql+pymysql://bob:bobpasswd@localhost:3306/testdb'
```

> 如果环境中没有安装 `pymysql` 模块，必须先安装，才能正常启动

其他数据库的连接方式可参考 SQLAlchemy 的 `引擎配置` 章节, 在这里查看 <https://docs.sqlalchemy.org/en/13/core/engines.html>

## 控制台

需要快速预览数据，对数据进行简单调整的话，控制台很有用

左侧菜单除了 Home 外，其他的都是库表名称

点击相应库表名称，会在右侧显示表内数据，并且可以做增删改操作

![库表数据](http://www.justdopython.com//assets/images/2020/08/sandman2/02.jpg)

点击新增，打开新增页面：

![新增页面](http://www.justdopython.com//assets/images/2020/08/sandman2/03.jpg)

用过 Django 的同学会感觉很熟悉，不过字段并没有类型支持，只能以字符串输入，自行确保数据类型正确，否则保存时会收到错误信息

点击记录前面的笔状图标，会进入编辑页面

![编辑页面](http://www.justdopython.com//assets/images/2020/08/sandman2/04.jpg)

点击记录前的删除图标，来删除记录

另外多选数据后，可以通过 `With selected` 菜单下的 `Delete` 按钮来批量删除

控制台方便易用，适合一些简单的、数据量少的操作

> **注意**：由于控制台不能登录即可访问，建议将服务器创建在本地或内网环境中

## API

以 RESTful 的角度来看，库表相当于`资源`(`resource`)，一组资源相当于`集合`(`collection`)

> 以下测验，均采用 `curl` 工具进行，具体用法可参考 阮一峰的 《curl 的用法指南》(<http://www.ruanyifeng.com/blog/2019/09/curl-reference.html>)

### 查询

通过 Http GET 方法，以 JSON 格式将数据返回，例如返回 `学生表 student` 的所有记录：

```bash
$ curl http://localhost:5000/student/

{"resources":[{"age":18,"class":"1","id":1,"name":"\u5f20\u4e09","profile":"\u64c5\u957f\u5b66\u4e60"},...
```

> 注意：资源要以 `/` 结尾

通过参数 `page` 来分页，例如返回 `学生表 student` 的第一页数据

```bash
$ curl http://localhost:5000/student/?page=1
{"resources":[{"age":18,"class":"1"...
```

通过参数 `limit` 显示返回行数

如果要获取具体记录，可以用主键值作为节段，例如获取 id 为 3 的学生记录

```bash
$ curl http://localhost:5000/student/3
{"age":18,"class":"2","id":3,"name":"\u738b\u4e94","profile":"\u7231\u7f16\u7a0b"}
```

以字段名做参数，相当于查询条件，例如，查询 `name` 为 Tom 的学生记录：

```bash
$ curl http://localhost:5000/student/?name=Tom
{"resources":[{"age":19,"class":"1","id":7,"name":"Tom","profile":"Handsome"}]}
```

查询条件可以被组合，例如，查询班级为 1 年龄为 18 的学生:

```bash
$ curl http://localhost:5000/student/?class=1&age=19
{"resources":[{"age":19,"class":"1","id":2,"name":"\u674e\u56db","profile":"\u559c\u6b22\u7bee\u7403"},{"age":19,"class":"1","id":7,"name":"Tom","profile":"Handsome"}]}
```

### 修改

`POST` 方法用于新增，新增内容，由请求的数据部分提供，例如增加一个学生信息：

```bash
$ curl -X POST -d '{"name": "Lily", "age": 17, "class":1, "profile":"Likely"}' -H "Content-Type: application/json" http://127.0.0.1:5000/student/
{"age":17,"class":"1","id":8,"name":"Lily","profile":"Likely"}
```

> 注意：库表主键是自增长的，可以忽略主键字段，否则必须提供

`PATCH` 方法用于更新，更新内容，由请求的数据部分提供，例如将 id 为 1 的学生班级更改为 3

> 注意: 更新时主键信息通过 url 的主键值节段提供，而不在数据部分中

```bash
$ curl -X PATCH -d '{"class":3}' -H "Content-Type: application/json" http://127.0.0.1:5000/student/1
{"age":18,"class":"3","id":1,"name":"\u5f20\u4e09","profile":"\u64c5\u957f\u5b66\u4e60"}
```

`DELETE` 方法由于删除，例如删除 id 为 8 的学生记录:

```bash
$ curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/student/8
```

### 其他接口

获取表的字段定义信息，通过 `meta` 节段获取，例如获取 `学生表 student` 的字段定义：

```bash
$ curl http://127.0.0.1:5000/student/meta
{"age":"INTEGER(11)","class":"VARCHAR(255)","id":"INTEGER(11) (required)","name":"VARCHAR(255)","profile":"VARCHAR(500)"}
```

导出数据，通过查询字段 `export` 获取，数据格式为 csv，例如导出学生数据，存放到 student.csv 文件中：

```bash
$ curl -o student.csv http://127.0.0.1:5000/student/?export
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   202  100   202    0     0   2525      0 --:--:-- --:--:-- --:--:--  2525
```

还有更多的接口有待你的探索

## 部署服务

sandman2 的服务器是基于 Flask 的

前面的 [Python 100 天文章](https://mp.weixin.qq.com/s/hu57amNWZ_MGnTrZxoMsMw)中对 Flask 和 服务器部署有详细的说明

具体可参考，《[Web 开发 Flask 简介](https://mp.weixin.qq.com/s/jBom8hpmypTvdZLeZD-s_A)》，以及《[部署 Flask 应用](https://mp.weixin.qq.com/s/b9Mmp0bSCmNVDzaExJlJ0w)》

在此就不赘述了

## 总结

sandman2 之所以简单易用，是因组合了很多应用和技术，SQLAlchemy 做 ORM 层，Flask 做 RESTful 服务器，Bootstrap 做前台框架等

给我们提供便利的同时，展示了技术组合的强大，使得我们对一些细小知识点的学习不会再感到枯燥无味

可以回复关键字，下载示例代码，实践起来更方便

## 参考

- <https://www.cnblogs.com/Liu-Hui/p/13388194.html>
- <https://sandman2.readthedocs.io/en/latest/>
- <http://www.ruanyifeng.com/blog/2019/09/curl-reference.html>

>  示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/sandman2>
