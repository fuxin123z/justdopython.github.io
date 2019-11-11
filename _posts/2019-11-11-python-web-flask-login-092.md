---
layout: post
category: python
title: 第92天： Flask 用户登录 Flask-Login
tagline: by 太阳雪
tags:
  - python100
---
用户登录功能是 Web 系统一个基本功能，是为用户提供更好服务的基础，在 Flask 框架中怎么做用户登录功能呢？今天我们学习一下 Flask 的用户登录组件 Flask-Login

<!--more-->

Python 之所以如此强大和流行，除了本身易于学习和功能丰富之外，最重要的是因为各种类库和组件，可以说没有 Python 做不了的事情，只有你不知道的组件。

但是同一个问题领域中的组件或类库名称、功能可能近似，版本多而混乱，会给使用者造成了困扰，比如之前讲述的 `Flask-Bootstrap` 和 `Bootstrap-Flask` ，以及今天要讲述的用户登录，由于方式多样，功能相似，所以出现了很多类似的框架，比如 `Flask-Login` 、`Flask-Auth` 、`Flask-Security` 等等

之所以选择 `Flask-Login`，是因为它基于 `Session`，适合作有 UI 交互的用户登录，前面我们刚刚学习了 Flask 表单，将方便演示，更容易理清用户登录功能的流程

## 用户登录说明

`Flask-Login` 和其他 Flask 组件并没有太大区别，不过开始之前得先厘清用户登录的步骤：

- 1 登录：用户提供登录凭证（如用户名和密码）提交给服务器
- 2 建立会话：服务器验证用户提供的凭证，如果有效，建立会话（ `Session` ），并返回给用户一个会话号（ `Session ID` ）
- 3 验证：用户在后续的交互中提供会话号，服务器将根据会话号（`Session id`）确定用户是否有效
- 4 登出：当用户不再与服务器交互时，注销与服务器建立的会话

依据以上步骤，我们设计一个应用场景，作为实现：

- 提供一个主页，需要登录才能看到
- 如果没有登录，跳转到登录页面，登录成功再跳回
- 登录成功后，可以点击登出退出登录
- 在登录页面提供注册连接，点击后跳转到注册页面
- 注册完成后，跳转到登录页面

## 安装

使用 `pip` 安装 `Flask-Login` 组件：

```shell
pip install flask-login
```

如果一切正常，可以将 `Flask-Login` 模块引入:

```python
>>> from flask-login import LoginManager
>>>
```

> 本次实践中，会用到 `Flask Form` 相关功能，请确保已经安装了 `Flask-WTF` 组件，详见 **Web 开发 Form**

## 初始化

先实例化 `login_manager` 对象，然后用它来初始化应用：

```python
from flask import Flask
from flask_login import LoginManager
# ...
app = Flask(__name__)  # 创建 Flask 应用

app.secret_key = 'abc'  # 设置表单交互密钥

login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint
```

- 因为需要用到表单交互，所以要设置 `secret_key`，以防 CSRF (跨域攻击)
- 登录管理对象 `login_manager` 的 `login_view` 属性，指定登录页面的视图函数 (登录页面的 `endpoint`)，即验证失败时要跳转的页面，这里设置为登录页

## 用户模块

### 用户数据

要做用户验证，需要维护用户记录，为了方便演示，使用一个全局列表 `USERS` 来记录用户信息，并且初始化了两个用户信息：

```python
from werkzeug.security import generate_password_hash
# ...
USERS = [
    {
        "id": 1,
        "name": 'lily',
        "password": generate_password_hash('123')
    },
    {
        "id": 2,
        "name": 'tom',
        "password": generate_password_hash('123')
    }
]
```

用户信息只包含最基本的信息：

- `name` 为登录用户名
- `password` 为登录密码，**切忌：无论如何不要在系统中存放用户密码的明文**，幸运的是模块 `werkzeug.security` 提供了 `generate_password_hash` 方法，使用 sha256 加密算法将字符串变为密文
- `id` 为用户识别码，相当于主键

基于用户信息，定义两方法，用来创建( `create_user` )和获取( `get_user` )用户信息:

```python
from werkzeug.security import generate_password_hash
import uuid
# ...
def create_user(user_name, password):
    """创建一个用户"""
    user = {
        "name": user_name,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    USERS.append(user)

def get_user(user_name):
    """根据用户名获得用户记录"""
    for user in USERS:
        if user.get("name") == user_name:
            return user
    return None
```

- `create_user` 接受用户名和密码，创建用户记录，对密码明文进行加密，并添加用户 ID (使用 `uuid` 模板的 `uuid4` 方法生成一个唯一编号)，存储到 USERS 列表中
- `get_user` 接受用户名，从 `USERS` 列表中查找用户记录，如果没有返回空

### 用户类

下面创建一个用户类，类维护用户的登录状态，是生成 `Session` 的基础，`Flask-Login` 为此提供了用户基类 `UserMixin`，方便我们定义自己的用户类 `User`：

```python
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash
# ...
class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None
```

- 实例化方法接受一个用户记录，即 `USERS` 列表中的一个元素，用来初始化成员变量
- `get_id` 方法返回用户实例的 ID，这是必须实现的，不然 `Flask-Login` 将无法判断用户是否被验证
- `get` 是个静态方法，即可以通过类之间调用，是为了在获取验证后的用户实例时用的，必须接受参数 ID，返回 ID 所以对应的用户实例
- `verify_password` 方法接受一个明文密码，与用户实例中的密码做校验，将被用在用户验证的判断逻辑中

### 加载登录用户

有了用户类，并且实现了 get 方法，就可以实现 login_manager 的 `user_loader` 回调函数了，根据用户 ID，返回一个用户实例，用于根据 Session 信息加载登录用户:

```python
@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)
```

## 登录页面

页面包括后台和展现(可以理解成前台)两部分

### 后台

根据前面介绍的 `Form` 相关知识 (参见 **Web 开发 Form**)，需要定义一个 `Form` 类，用来设置页面的元素和规则:

```python
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
# ...
class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
```

- 定义用户名和密码两个字段，分别是字符类型字段和密码类型字段，密码类型字段会在页面上显示为密码形式，以提高安全性
- 为两个字段设置必填规则

然后定义一个用户登录的视图函数 `login`:

```python
from flask import render_template, redirect, url_for, request
from flask_login import login_user
# ...
@app.route('/login/', methods=('GET', 'POST'))  # 登录
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = "用户名或密码密码有误"
    return render_template('login.html', form=form, emsg=emsg)
```

我们来分析下视图函数的逻辑:

- 视图函数同时兼容了 `GET` 和 `POST` 方法
- `form.validate_on_submit()` 可以判断用户是否完整的提交了表单，只对 `POST` 有效，所以可以用来判断请求方式
- 如果是 `POST` 请求，获取提交数据，通过 `get_user` 方法查找是否存在该用户
- 如果用户存在，则创建用户实体，并交验登录密码
- 校验通过后，调用 `login_user` 方法创建用户 `Session`，然后跳转到请求参数中 `next` 所指定的地址或者首页 (不用担心如何设置 `next`，还记得上面设置的 `login_manager.login_view = 'login'` 吗？ 对，当没有登录是访问需要验证页面会跳转到 `login`，并且带上 `next`)
- 如果不是 `POST` 请求，或者验证有问题，直接显示 `login.html` 模板渲染后的结果

### 前台

在 `templates` 模板下创建登录页面的模板 `login.html`:
{% raw %}

```html
{% macro render_field(field) %} <!-- 定义字段宏 -->
  <dt>{{ field.label }}:
  <dd>{{ field(**kwargs)|safe }}
  {% if field.errors %}
    <ul class=errors>
    {% for error in field.errors %}
      <li>{{ error }}</li>
    {% endfor %}
    </ul>
  {% endif %}
  </dd>
{% endmacro %}

<!-- 登录表单 -->
<form method="POST">
    {{ form.csrf_token }}
    {{ render_field(form.username) }}
    {{ render_field(form.password) }}
    {% if emsg %}  <!-- 如果有错误信息 则显示 -->
        <h3> {{ emsg }}</h3>
    {% endif %}
    <input type="submit" value="登录">
</form>
```

{% endraw %}

- `render_field` 是 Jinja2 模板引擎的宏，接受表单字段将其渲染成表单字段，并且处理字段的错误信息
- `emsg` 错误信息单独做了处理，如果存在会显示出来
- `form` 中并没有 `action` 属性，默认为当前路径

## 需要验证的页面

为了方便演示，我们将首页作为需要验证的页面，功能很简单，显示一下登录者的用户名，另外有个登出链接，用来退出当前登录

先看首页视图函数 `index`:

```python
from flask import render_template, url_for
from flask_login import current_user, login_required
# ...
@app.route('/')  # 首页
@login_required  # 需要登录才能访问
def index():
    return render_template('index.html', username=current_user.username)
```

- 注解 `@login_required` 会做用户登录检测，如果没有登录要方法此视图函数，就被跳转到 `login` 接入点( endpoint )
- current_user 是 Flask-Login 提供的在当前请求环境下访问登录用户信息的全局变量，是 User 类的实例
- 将当前登录者的用户名传入 `index.html` 模板

然后是登出视图函数 `logout`:

```python
from flask import redirect, url_for
from flask_login import logout_user
# ...
@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
```

- 只有登录了才有必要登出，所以也加了注解 `@login_required`
- `logout_user` 方法和 `login_user` 相反，即删除用户的 `Session`
- 登出视图不需要模板，直接跳转到登录页，实际项目中可以增加一个登录页，用于展示有趣的东西

首页模板 `index.html` 很简单:
{% raw %}

```html
<h1>欢迎 {{ username }}！</h1>
<a href='{{ url_for('logout')}}'>登出</a>
```

{% endraw %}

## 小试牛刀

终于可以试试了，加上启动代码:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

启动项目，如果一切正常将看到类似的反馈：

```shell
python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 176-611-251
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

访问 [localhost:5000](localhost:5000)，将看到登录页，主要浏览器地址上的 next 参数:

![显示结果](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2019/python/python_web_auth_01.png)

填写初始化中的用户名和密码，登录将进入首页，且看到登录者的用户名:

![显示结果](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2019/python/python_web_auth_02.png)

## 用户注册

上面的演示已经存在的用户登录的情况，用户注册功能和登录类似，在注册页面上多了密码确认字段，提交注册时需要验证两次输入的密码是否一致，以及用户是否存在，如果通过检验将用户数据保存到 `USERS` 列表中，并跳转到 `login` 页面

因为注册流程和登录很类似，这里不做详细讲解，可以参考本节的代码示例。

如果您来实现注册功能的话打算怎么做？欢迎交流

## Flask-Login 其他特性

演示中用到了一些 `Flask-Login` 的基本特性，可以满足基本的用户登录需求，`Flask-Login` 还提供了一些重要特性，这里简单介绍一下

### 记住我

记住我，并不是用户登出之后，再次登录是自动填写用户名和密码（自动填写一般属于浏览器功能），而是在用户意外退出后（比如关闭浏览器）不用再次登录，如果用户本地的 `cookie` 失效了，`Flask-Login` 会自动将用户 `ID`，即 `Session` 放入 `cookie` 中。

`login_user` 方法的命名参数 `remember` 设置为 `True` 开启记住我功能

### Session 防护

`Session` 信息一般存放在 `cookie` 中，以方便用户再次访问，但是 `cookie` 容易受到攻击，会被窃取 `cookie` 中的 `Session` 信息，伪造用户登录系统，幸运的是 `Flask-Login` 提供了 `Session` 防护机制，并提供 `basic` 和 `strong` 两种保护等级，通过 `login_manager.session_protection` 来设置，默认等级为 `basic`，如果设置为 `None` 将关闭 `Session` 防护机制。

在保护机制开启的情况下，每次请求会根据用户的特征（一般指有用户IP、浏览器类型生成的哈希码）与 `Session` 中的对比，如果无法匹配则要求用户重新登录，在强模式下( `strong` )一旦匹配失败会删除以及创建的 `Session`，从而消除攻击者重构 `cookie` 的可能

### Request Loader

有时候因为一些原因不想或者无法使用 `cookie` 记录 `Session` 信息的时候，可以选择记录在其他地方，比如 `Header` 中或者请求参数中，那么构造用户 `Session` 时就需要用 `request_loader` 代替 `user_loader`，`request_loader` 接受 `request` 作为参数，就可以做更个性化的创建 `Session` 的机制了

## 总结

本节课程主要介绍了 `Flask-Login` 组件的使用，通过用户登录的实例，讲述了实践中的一些问题和细节，主要是引入 `Flask-Login` 模块，初始化应用，构造登录用户类，设置登录页面入口，使用 `user_loader` 创建用户 `Session`，以及在视图函数中进行用户验证的方法，最后还介绍了一些额外的 `Flask-Login` 特性。

`Web` 应用的验证是个常用而又复杂的功能，除了今天介绍的 `Session` 方式之外，还有基于 `RESTful` 的非状态的 `token` 方式，已经第三方认证机制，比如微信、支付宝等，后面我们会陆续讲解，敬请期待。

[示例代码](https://github.com/JustDoPython/python-100-day/tree/master/day-092)

参考

- [https://zhuanlan.zhihu.com/p/23137867](https://zhuanlan.zhihu.com/p/23137867)
- [https://blog.csdn.net/sinat_29315627/article/details/74177792](https://blog.csdn.net/sinat_29315627/article/details/74177792)
- [http://www.bjhee.com/flask-ext9.html](http://www.bjhee.com/flask-ext9.html)
- [http://www.pythondoc.com/flask-restful/third.html](http://www.pythondoc.com/flask-restful/third.html)
- [https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)
- [https://flask-httpauth.readthedocs.io/en/latest/](https://flask-httpauth.readthedocs.io/en/latest/)
- [https://www.jianshu.com/p/8c87099f72a5](https://www.jianshu.com/p/8c87099f72a5)
