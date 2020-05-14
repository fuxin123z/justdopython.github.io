---
layout: post     
title:  发布代码到 PyPI                 
category: 发布代码到 PyPI
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

## 发布代码到 PyPI

写 Python 程序的童鞋们都知道安装模块使用 pip install xxxx 命令，那么知道怎样将自己的代码发布到 PyPI 让全世界 Python 程序员使用吗？下面让我们开始一起学一下将代码上传到 PyPI 吧...
<!--more-->

### PyPI 概念

PyPI 全称 Python Package Index ，是一个 Python 的模块管理工具。提供对 Python 模块的查找、下载、安装、卸载等操作。

### 项目结构

首先让我们来看看上传 PyPI 需要的项目结构，然后再慢慢填代码。

![](http://www.justdopython.com/assets/images/2020/pip/pip.png)

各个文件的详细介绍如下：

1. simple_pip_upload：项目的根目录
2. example：模块名，代码写法: from example import math
3. \_\_init\_\_.py：这里可以写代码，也可以是空文件
4. math.py：代码模块，可以有多个 py 文件
5. setup.py：setuptools 的构建脚本
6. README.md：关于项目的描述，描述如何安装、使用等情况
7. LICENSE：开源的 LICENSE，如：Apache License 2.0，MIT License 等等，在（https://choosealicense.com/）选择，这里选择 MIT License

### 编写代码

#### 编写 math.py

math.py 里面只写了简单的加减乘除代码

```python
def add(i, y):
    print(str(i) + " + " + str(y) + " = " + str((i + y)))


def sub(i, y):
    print(str(i) + " - " + str(y) + " = " + str((i - y)))


def mul(i, y):
    print(str(i) + " * " + str(y) + " = " + str((i * y)))


def div(i, y):
    print(str(i) + " / " + str(y) + " = " + str((i / y)))
```

#### 编写 setup.py

setup.py 是一个 setuptools 的构建脚本，其中包含了项目和代码文件的信息

```python
import setuptools

setuptools.setup(
    name="simple_pip_upload",
    version="0.0.2",
    author="moumoubaimifan",
    author_email="example@example.com",
    description="一个简单的四则运算 PyPI 上传例子",
    long_description="一个简单的 PyPI 上传测试",
    long_description_content_type="text/markdown",
    url="https://github.com/JustDoPython/justdopython.github.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

setuptools.setup 的参数信息如下：

* name：项目的名称
* version：项目的版本
* author，author_email：作者和作者邮件
* description：项目的简单介绍
* long_description：项目的详细介绍
* long_description_content_type：表示用哪种方式显示long_description，一般是 md 方式
* url：项目的主页地址
* packages：项目中包含的子包，find_packages() 是自动发现根目录中的所有的子包。
* classifiers：其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。 

### 编译

在上传代码之前，我们需要将代码编译，编译代码需要使用 setuptools 和 wheel 模块，安装它们

```python
pip3 install --user --upgrade setuptools wheel
```

安装完成后使用如下命令编译

```python
python3 setup.py sdist bdist_wheel
```

编译之后会在项目中会生成多个文件夹，其中一个 dist 文件夹中包含 simple_pip_upload-0.0.2.tar.gz 源码包 和 simple_pip_upload-0.0.2-py3-none-any.whl 文件

```python
dist\
    simple_pip_upload-0.0.2.tar.gz
    simple_pip_upload-0.0.2-py3-none-any.whl
```

### 上传 

到这里就只剩下上传代码了，我们需要注册（https://pypi.org/account/register/）账号和创建一个 token（https://pypi.org/manage/account/token/），并保存到 `$HOME/.pypirc` 文件里面。

![token.png](http://www.justdopython.com/assets/images/2020/pip/token.png)

PyPI 上传使用的是 Twine 模块，安装它

```python
python3 -m pip install --user --upgrade twine
```

安装完成之后，使用如下命令上传 dist 文件夹里面的文件

```python
python3 -m twine upload --repository pypi dist/*
```

![](http://www.justdopython.com/assets/images/2020/pip/upload.png)

最后让我们在网站（https://pypi.org/）上查询 simple-pip-upload 项目是否被上传上去

![](http://www.justdopython.com/assets/images/2020/pip/result.png)

### 使用模块

使用 pip 命令安装 simple-pip-upload 项目

```python
pip3 install simple-pip-upload
```

在 Python 终端中使用 simple-pip-upload 项目

```python
>>> from example import math
>>> math.add(1,2)
1 + 2 = 3
>>> math.sub(5,2)
5 - 2 = 3
>>>
```

### 总结

将一个项目发布到 PyPI 很简单，就是步骤繁琐了一些。大家学会了吗？

### 参考

[https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)

> 示例代码 [发布代码到 PyPI](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/simple_pip_upload)