---
layout: post
category: python
title: 别再问我 Python 打包成 exe 了
tagline: by 某某白米饭
tags: 
  - python
---

python 可以做网站应用，也可以做客户端应用。但是客户端应用需要运行 py 脚本，如果用户不懂 python 就是一件比较麻烦的事情。幸好 pyton 有第三方模块可以将脚本可以转成 exe 执行。

有些人可能要问了既然可以做成网站，为啥还要做成客户端的，直接部署到服务器给客户不就可以了吗？我的回答是当然是为了追小姐姐呀。在公司给小姐姐写点 python 脚本打包成 exe 减轻上班的工作量。再弄出点 bug，一来二去不就会产生故事了？

<!--more-->

python 上常见的打包方式目是通过 pyinstaller 来实现的。

```python
pip install pyinstaller 
```

上面安装比较慢，用下面的清华源飞快。

```python
# 清华源
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 详细步骤

pyinstaller 是一个命令行工具，下面是详细步骤：

1、cmd 切换到 python 文件的目录。

![](http://www.justdopython.com/assets/images/2021/10/pyinstaller/0.png)

2、执行命令 pyinstaller -F -w -i python.ico watermark.py，

执行完毕会发现生成了 3 个文件夹

![](http://www.justdopython.com/assets/images/2021/10/pyinstaller/1.png)

其中 dist 文件夹就有我们已经打包完成的 exe 文件。

![](http://www.justdopython.com/assets/images/2021/10/pyinstaller/2.png)

3、双击 exe 就可以运行成功了。

### 详细参数

在上面的打包命令中，用到了好几个参数：-F，-W，-i，这些参数的含义如下面的表格：

参数 | 用法
-- | --
-F | 生成结果是一个 exe 文件，所有的第三方依赖、资源和代码均被打包进该 exe 内
-D | 生成结果是一个目录，各种第三方依赖、资源和 exe 同时存储在该目录（默认）
-a | 不包含unicode支持 
-d | 执行生成的 exe 时，会输出一些log，有助于查错
-w | 不显示命令行窗口
-c | 显示命令行窗口（默认）
-p | 指定额外的 import 路径，类似于使用 python path
-i | 指定图标
-v | 显示版本号
-n | 生成的 .exe 的文件名

pyinstaller -F -w -i python.ico watermark.py 就表示 -F，打包只生成一个 exe 文件，-w，在运行程序的时候不打打开命令行的窗口，-i 就是打包带有自己设置的 ico 图标。

### 图形窗口打包

有些人可能感觉命令行打包还需要记忆各种参数的含义，有没有窗口化的打包方式，还别说，真有。auto-py-to-exe 一个将 pyinstaller 封装成为 GUI 窗口的模块。

```python
pip install auto-py-to-exe -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

安装完成之后，在命令行输入 `` 打开打包窗口。

![](http://www.justdopython.com/assets/images/2021/10/pyinstaller/3.png) 

在窗口中主要有几个参数：

1. Script Location：就是 python 脚本的路径
2. Onefile (--onedir / --onefile)：就是上面的 -D 和 -F 参数，生成单个 exe 文件或者生成一个文件夹
3. Console Window (--console / --windowed)：就是上面的 -w 和 -c 参数，表示在运行的时候是否出现命令行窗口
4. ICON：就是 ico 图标的地址

设置完这几个参数之后，在下面的 Current Command 框就会显示 pyinstaller 命令。点击最后的按钮，生成 exe 文件。

![](http://www.justdopython.com/assets/images/2021/10/pyinstaller/4.png)

### 总结

多学 python，多多关注本公众号文章，为找到小姐姐打上良好基础。 
