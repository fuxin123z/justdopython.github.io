---
layout: post     
title:  一文吃透 Jupyter Notebook                                             
category: 一文吃透 Jupyter Notebook 
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

notebook 是 Jupyter项目的重要组件之一，它是一个代码、文本（有标记或无标记）、数据可视化或其它输出的交互式文档。Jupyter Notebook 需要与内核互动，内核是 Jupyter 与其它编程语言的交互编程
协议。Python 的 Jupyter 内核是使用 IPython。Jupyter Notebook 是基于网页的用于交互计算的应用程序。其可被应用于全过程计算：开发、文档编写、运行代码和展示结果。，除此之外，它还提供了一系列魔法操作，今天的文章着重讲解关于 Jupyter notebook 的魔法操作。

<!--more-->

## Jupyter Notebook 基本操作

### 安装 Jupyter Notebook

要使用 Jupyter，首先得安装 Jupyter notebook

安装 Jupyter Notebook 有两种方式：

1. 直接使用命令安装

```python
pip3 install jupyter
```

2. 使用 Anaconda 安装

 除了使用 pip 命令安装后，还可以使用 Anaconda 来安装，Anaconda 的下载网址详见[官网下载](https://www.anaconda.com/distribution/)，进入 到这个页面后选择相应的操作系统以及计算机已安装的 Python 对应版本后安装，按照步骤安装好后配置环境变量即可。安装好 Anaconda 后使用命令安装 Jupyter Notebook，安装命令如下：

```python
conda install jupyter notebook
```
以上两步骤等待安装完即可。

### 启动 Jupyter notebook

启动程序也很简单，直接在终端输入 Jupyter notebook

```
jupyter notebook
```

以上命令运行结果如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330113708120.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

这样 Jupyter notebook 就启动成功了，在众多平台中，Jupyter notebook 启动成功后会自动打开默认浏览器（在不指定浏览器的情况下），或者可以在启动 notebook 后，手动打开网页  http://localhost:8888/，启动成功后如下图所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330115125705.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

> Jupyter notebook 一般都作为本地计算环境，但它也可以部署到服务器上远程访问。


### Jupyter notebook 的使用

#### 1、Jupyter 帮助文档 

对于 Jupyter notebook 的使用可以在命令行短使用 `jupyter notebook -h` 或者 `jupyter notebook --help` 即可查看相关使用命令，终端输入 
`jupyter notebook -h` 后显示如下：

```
The Jupyter HTML Notebook.

This launches a Tornado based HTML Notebook Server that serves up an
HTML5/Javascript Notebook client.
...

--gateway-url=<Unicode> (GatewayClient.url)
    Default: None
    The url of the Kernel or Enterprise Gateway server where kernel
    specifications are defined and kernel management takes place. If defined,
    this Notebook server acts as a proxy for all kernel management and kernel
    specification retrieval.  (JUPYTER_GATEWAY_URL env var)

To see all available configurables, use `--help-all`

Examples
--------

    jupyter notebook                       # start the notebook
    jupyter notebook --certfile=mycert.pem # use SSL/TLS certificate
    jupyter notebook password              # enter a password to protect the server
    
```

#### 2、操作页面介绍

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330115956596.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330140343662.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

要新建一个 notebook，点击按钮 New，选择 “Python3。后进入到操作页面，在操作页面中输一行 Python 代码后按快捷键 Shift-Enter 执行。如下图所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330151928361.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

在 Jupyter notebook 中，最重要的是对文件中的 cell 或者 cells 进行操作，Cell 菜单主要包含了运行cells、运行cells后并在之后插入新的cell、运行所有cells、运行当前之上的所有cell、运行当前之下的所有cell、改变cell类型（code、markdown、raw nbconvert）等，cell 操作菜单栏如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330135803872.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

菜单栏详细介绍：

- **File**: File 菜单中主要包含了以下功能：创建新的 Notebook、打开新的界面、拷贝当前 Notebook、重命名 Notebook、保存还原点、恢复到指定还原点、查看 Notebook 预览、下载 Notebook 、关闭 Notebook。

这里重点强调下下载 Notebook 选项，它可以将当前 Notebook 转为py文件、html文件、markdown 文件、rest 文件、latex 文件、pdf 文件。

![File 菜单用法](https://img-blog.csdnimg.cn/20200330141256567.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

- **Edit**: Edit 菜单主要是对 Cells 剪切、复制、删除、向上/向下移动等。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330141543707.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

 - **Insert**: 插入 Cell，插入方式有两种：一种是在当前 cell 上方插入，一种是在当前 cell 下方插入。
 - **Cell**：Cell 菜单主要包含了运行 cells、运行cells后并在之后插入新的 cell、运行所有 cells、运行当前之上的所有 cell、运行当前之下的所有cell、改变cell类型（code、markdown、raw nbconvert）等.

 - **Kernel** ：Kernel 菜单主要包含了中断 kernel、重启 kernel、重启 kernel 并清除输出、重启 kernel 并运行所有 cell、重连 kernel、关闭 kernel、改变 kernel 类型等。

 - **Help**：Help 菜单主要包含了用户交互引导、键盘快捷键、修改键盘快捷键、Notebook 帮助、Markdown 帮助、Jupyter-notebook-extensions 帮助、Python 帮助、IPython 帮助、Numpy 帮助、Scipy 帮助、Matplotlib 帮助、Sympy 帮助、pandas 帮助等

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020033015111428.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

同样的 Jupyter notebook 也能写 Markdown 语法，在如图位置选择 `标题`  后按照 Markdown 语法书写即可，例如：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330152443694.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

Jupyter notebook 的基本操作先介绍到这里，接下来开始 Jupyter notebook 的魔法操作。

### Jupyter notebook 优点

- 编程时具有语法高亮、缩进、tab补全的功能。

- 可直接通过浏览器运行代码，同时在代码块下方展示运行结果。

- 以富媒体格式展示计算结果。富媒体格式包括：HTML，LaTeX，PNG，SVG等。

- 支持使用LaTeX编写数学性说明。


## Jupyter notebook 魔法操作

### 魔法命令

IPython 中特殊的命令（在 Python 中没有）被称作“魔术”命令。这些命令可以使普通任务更便捷，更容易
控制 IPython 系统。魔法命令是 magic 函数主要包含两大类：
- 一类是行魔法（Line magic）前缀为 %
- 一类是单元魔法 (Cell magic) 前缀为 %%； 

使用 %lsmagic 命令查看所有的魔法命令：
 
```
%lsmagic
```

**输出为所有的魔法命令**

```
Available line magics:
%alias  %alias_magic  %autoawait  %autocall  %automagic  %autosave  %bookmark  %cd  %clear  %cls  %colors  %conda  %config  %connect_info  %copy  %ddir  %debug  %dhist  %dirs  %doctest_mode  %echo  %ed  %edit  %env  %gui  %hist  %history  %killbgscripts  %ldir  %less  %load  %load_ext  %loadpy  %logoff  %logon  %logstart  %logstate  %logstop  %ls  %lsmagic  %macro  %magic  %matplotlib  %mkdir  %more  %notebook  %page  %pastebin  %pdb  %pdef  %pdoc  %pfile  %pinfo  %pinfo2  %pip  %popd  %pprint  %precision  %prun  %psearch  %psource  %pushd  %pwd  %pycat  %pylab  %qtconsole  %quickref  %recall  %rehashx  %reload_ext  %ren  %rep  %rerun  %reset  %reset_selective  %rmdir  %run  %save  %sc  %set_env  %store  %sx  %system  %tb  %time  %timeit  %unalias  %unload_ext  %who  %who_ls  %whos  %xdel  %xmode

Available cell magics:
%%!  %%HTML  %%SVG  %%bash  %%capture  %%cmd  %%debug  %%file  %%html  %%javascript  %%js  %%latex  %%markdown  %%perl  %%prun  %%pypy  %%python  %%python2  %%python3  %%ruby  %%script  %%sh  %%svg  %%sx  %%system  %%time  %%timeit  %%writefile

Automagic is ON, % prefix IS NOT needed for line magics.
```

魔术函数默认可以不使用百分号，只要没有变量和函数名相同。这个特点被称为“被动魔术”，可以
使用 %automagic 打开或关闭，一些魔术函数与 Python 函数很像，它的结果可以赋值给一个变量，例如：

```
path = %pwd
path
```
输出：

```
'D:\\Software\\python3\\study'
```

### 部分魔法命令详解

|魔法函数|	函数说明|
|--|--|
|%run|	运行脚本文件（执行外部的代码）|
|%timeit|	测试代码性能（测试一行Python语句的执行时间）|
|%%itmeit	|测试代码性能（执行多行语句）|
|%lsmagic|	列出所有魔法命令|
|%命令?	|查看魔法命令详细说明|
|%history	|输入的历史记录|
|%xmode	|【异常控制 】可以在轨迹追溯中找到错误的原因|
|%xmode Plain	|以紧凑的方式显示异常信息|
|%debug|	用来在交互环境中，调试程序|
|%pwd|用来显示当前路径|
|%matplotlib|集成绘图工具 Matplotlib|
|%paste|执行剪贴板中的代码|

#### 1、%run

%run 表示在 Jupyter notebook 中运行指定的 .py 文件，例如：
创建一个新的 test .py 文件 输入内容后保存，输入内容:

```python
import numpy as np
import pandas as pd
# 创建一个多维数组
data=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'),columns=list('ABCDE'))
print(data)
```

使用 %run  test .py 运行结果如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330172432175.png)

#### 2、 %命令?

%命令? 用来显示命令的用法，例如：

```python
%timeit?
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330173414478.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

#### 3、%timeit 和 %%timeit

- %timeit 命令用来帮助测试系统性能，例如：

```python
strings = ['foo', 'bazzle', 'quxix', 'python'] * 100
%timeit [x for x in strings if x[:3] == 'foo']
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020033017445635.png)

- %%time 将会给出cell的代码运行一次所花费的时间，例如：

```
%%time
data=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'),columns=list('ABCDE'))
data
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330174913374.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

#### 4、%matplotlib 

%matplotlib 表示集成绘图工具 Matplotlib，在IPython shell中，运⾏ %matplotlib 可以进⾏设置，可以创建多个绘图窗口，而不会干扰控制台 session：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330175432133.png)
在这里还用到另一个命令：`%matplotlib inline` ，它表示将 Matplotlib 内嵌到 Jupyter notebook 中，具体使用方法如下：

```python
import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
plt.plot(np.random.randn(60).cumsum())
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200330180144426.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

至此 Matplotlib 模块就集成成功了。

### 总结 

本文详细介绍了 Jupyter notebook 使用以及魔法命令，使用 Jupyter notebook 做数据分析或者模型训练是很多工程师的选择工具之一，希望今天的这篇文章给使用 Jupyter notobook 的伙伴提供帮助，欢迎大家进群交流，我们一起努力，一起进步！

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/chaoxi/2020-03-30-jupyter_notebook >
 