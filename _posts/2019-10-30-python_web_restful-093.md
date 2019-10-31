---
layout: post
category: python
title: 第93天： Web 开发 RESTful
tagline: by 太阳雪
tags:
  - python100
---
现在单页 Web 项目很流行，使用各种 Js 框架，通过 Ajax 和服务器的 Api 进行交互，实现类似原生 app 效果，很酷，对 Flask 来说小菜一碟，是时候了解下 Flask-RESTful 了

<!--more-->

开始前先了解下 RESTful，阮一峰老师有这样的解释:

> 网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备......）。
>因此，必须有一种统一的机制，方便不同的前端设备与后端进行通信。这导致API构架的流行，甚至出现"API First"的设计思想。RESTful API是目前比较成熟的一套互联网应用程序的API设计理论

也就是说 RESTful 一个框架和互联网应用的设计原则，遵循这个设计原则，可以让应用脱离前台展现的束缚，支持不同的前端设备。

## 安装

Flask 的 RESTful 模块是 flask-restful ，使用 pip 安装:

```bash
pip install flask-restful
```

如果安装顺利，可以在 Python Shell 环境下导入

```python
>>> from flask_restful import Api
>>>
```

## 小试牛刀

安装好后，简单试试。
flask-restful 像之前的 bootstrop-flask 以及 flask-sqlalchamy 模块一样，使用前需要对 Flask 应用进行初始化，然后会得到当前应用的 api 对象，用 api 对象进行资源绑定和路由设置：

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)  # 初始化得到 api 对象
```

上面代码中从 flask_restful 中引入的 Resource 类是用来定义资源的，具体资源必须是 Resource 的子类，下面定义一个 HelloRESTful 资源:

```python
class HelloRESTful(Resource):
    def get(self):
        return {'greet': 'Hello Flask RESTful!'}
```

接着，给资源绑定 URI：

```python
api.add_resource(HelloRESTful, '/')

if __name__ == '__main__':   # 别忘了启动应用的代码
    app.run(debug=True)
```

在终端或者命令行下运行 `python app.py` 启动应用

访问 `localhost:5000` 或者 `127.0.0.1:5000` 查看效果，将会看到 JSON 格式的数据输出:

```json
{
  "greet": "Hello Flask RESTful!"
}
```

也可以用 curl 工具在终端或者命令行下发送请求:

```bash
$ curl http://localhost:5000 -s
{
    "greet": "Hello Flask RESTful!"
}
```

> curl 的参数 -s 是开启安静模式的意思

## 资源及路由

从上面代码中可以看到，资源是 Resource 类的子类，以请求方法( GET、POST 等)名称的**小写形式**定义的方法，能对对应方法的请求作出相应，例如上面资源类中定义的 `get` 方法可以对 `GET` 请求作出相应，还可以定义 `put`、`post`、`delete` 等，称之为视图方法。

Flask-RESTful 支持多种视图方法的返回值:

```python

```


## 请求解析

## 格式化输出

## 总结

本节课程简单介绍了 Flask 中数据库技术，主要是借助 Flask-SQLAlchamy 框架来操作数据库，以 SQLite 关系数据库为例讲解了数据的增删改查操作，最后展示了如何在视图函数中操作数据，以便与 Flask 应用相结合。

[示例代码](https://github.com/JustDoPython/python-100-day/tree/master/day-093)

参考

- [http://www.ruanyifeng.com/blog/2014/05/restful_api.html](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
- [http://www.ruanyifeng.com/blog/2011/09/restful.html](http://www.ruanyifeng.com/blog/2011/09/restful.html)
- [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/)