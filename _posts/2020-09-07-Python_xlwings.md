---
layout: post     
title:  xlwings-能让 Excel 飞上天
category: xlwings-能让 Excel 飞上天
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---
  人生苦短，我用 Python！
  
  Python 作为一种脚本语言，其编程方式越来越受程序员们的青睐，同时其应用也越来越广泛，其中数据分析岗位人才需求也日益渐增，运用 Python 相关模块进行数据分析能大大提升工作效率，减轻数据分析人员的工作负担。
在日常办公中，使用 Python 的场景也越来越多，很多重复的工作直接交给程序执行效率会大大提高，所以 Python 操作 Excel 也成为每一个数据分析人员的必备技能，今天的文章就一起来看看 Python 中能操作 Excel 工作表的神器。 

### Python 操作 Excel 模块简介
  
 Python 操作 Excel 的模块，网上提到的模块大致有：xlwings、xlrd、xlwt、openpyxl、pyxll 等，他们提供的功能归纳起来无非有两种形式：
	
- 1、用 Python 读写 Excel 文件，实际上就是读写有格式的文本文件，操作 excel 文件和操作 text、csv 文件没有区别，Excel 文件只是用来储存数据。
	
- 2、除了操作数据，还可以调整Excel文件的表格宽度、字体颜色等。另外需要提到的是用 COM 调用 Excel 的 API 操作 Excel 文档同样也是可行的，相当麻烦基本和 VBA 没有区别。

### 关于 xlwings

为什么 xlwings 能让 Excel 飞起来呢，因为 xlwings 支持 Excel 的读写操作。具体使用请参照 [官网](https://www.xlwings.org/) ，一切技术的出现都是为了满足人的惰性，因此 xlwings 能让繁琐的工作简单化、简洁化。

Xlwings 是开源且免费的工具，能够非常方便的读写 Excel 文件中的数据，并且能够进行单元格格式的修改。

xlwings 还可以和 matplotlib、numpy 以及 pandas 无缝连接，支持读写 numpy、pandas 数据类型，将 matplotlib 可视化图表导入到 excel 中。

最重要的是 xlwings 可以调用 Excel 文件中 VBA 写好的程序，也可以让 VBA 调用用 Python 写的程序。

### xlwings 优点

- xlwings 能够非常方便的读写 Excel 文件中的数据，并且能够进行单元格格式的修改
- xlwings 可以和 Matplotlib 以及 Pandas 无缝连接
- xlwings 可以调用 Excel 文件中 VBA 写好的程序，也可以让 VBA 调用 Python 写的程序。
- xlwings 开源免费，并且一直在更新

### xlwings 基本操作

![xlwings 基本对象](https://imgkr2.cn-bj.ufileos.com/2a908c79-94c5-4c45-bd1d-c7fa31f24262.webp?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=9CKYSHVJOj29v8kCQ4Czyg4MQNw%253D&Expires=1599534813)

### xlwings 安装和使用

和其他模块使用一样，xlwings 在使用之前也需要安装，本文环境为 Python 3.6 版本的 Windows 环境。

#### **模块安装**

安装xlwings的最简单方法是通过pip：

```python

 pip install xlwings
 
```
**或者使用conda：**

```python

 conda install xlwings
 
 ```
 
**再或者**
 
 ```python
 
 conda install -c conda-forge xlwings
 
```

#### 引入模块使用

```python 

import xlwings as xw

```

### Python to Excel

连接到工作簿最简单便捷的方法是由 xw.Book 提供：它在所有应用程序实例中查找该工作簿并返回错误，但如果同一个工作簿在多个实例中打开，要连接到活动应用程序实例中的工作簿，则需要使用 `xw.books` 并引用特定应用程序，
使用区别如下：

| Header1   | Header2     |Header3     |
|---------|--------------------|-------|
| New book  | xw.Book() |xw.books.add()|
| Unsaved book  | xw.Book('Book1') |xw.books['Book1']|
| UBook by (full)name  | xw.Book(r'D:/test/file.xlsx') |xw.books.open(r'D:/test/file.xlsx')|

> **注**：在 Windows 上指定文件路径时，应该通过在字符串前放置一个 r 来使用原始字符串，或者使用双反斜杠：D:\\Test\\file.xlsx


#### Excel 活动对象

```python

# 活动应用程序（即Excel实例）
app = xw.apps.active

# 活动工作簿
wb = xw.books.active  # 在活动app
wb = app.books.active  # 在特定app

# 活动工作表
sht = xw.sheets.active  # 在活动工作簿
sht = wb.sheets.active  # 在特定工作簿

# 活动工作表的Range
xw.Range('A1')  #在活动应用程序的活动工作簿的活动表上

```

#### 基本操作

以下代码展示相关基本操作：
- 打开表格
- 引用工作表
- 引用单元格
- 引用区域
- 写入数据（数据写入默认按照行写入，如果要指定相应的列写入则需要添加相应参数，指定参数为：transpose = True）
- 读取数据

```python

import xlwings as xw
# 打开表格
file_path = r'D:/test/file.xlsx'

xw.Book(file_path)   # 固定打开表格
xw.books.open(file_path) # 频繁打开表格

# 引用工作表
sht = wb.sheets['sheet1']

# 引用单元格
rng = xw.Range('A1')
# rng = sht[0,0] # 此代码第一行的第一列即a1,相当于 pandas 的切片

# 引用区域
rng = sht.range('a1:a5')
# rng = sht['a1:a5']
# rng = sht[:5,0]

# 写入数据

sht.range('a1').value = 'Hello Excel' # 指定一个单元格写入数据

# 按行写入数据
sht.range('a1').value = [1, 2, 3, 4,5,6,7,8]

# 按照列写入数据
sht.range('a2').options(transpose=True).value = [2, 3, 4, 5, 6, 7, 8]

# 按照二维列表的方式写入数据

sht.range('a9').expand('table').value = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],['j', 'k', 'l']]

# 读取写入的数据

print(sht.range('A1:D5').value)

```

### xlwings 结合 matplotlib
xlwings 结合 Matplotlib 使用能讲图画贴入到 Excel 中，具体使用 pictures.add() 方法就可以很容易地将Matplotlib图作为图片粘贴到表格中。
详细代码如下：

```python

 fig = plt.figure()  # 指定画布
 # plt.plot([1, 2, 3, 4, 5])
 plt.plot([36,5,3,25,78])
 plt.plot([9,10,31,45])
 plt.plot([6,14,45,31])
 sht = xw.Book(r'G:/test/test.xlsx').sheets[0]
 sht.pictures.add(fig, name='myplt', update=True)

```

![结果图片](https://imgkr2.cn-bj.ufileos.com/acb2422f-51bd-474e-9360-81f4e4231e7a.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=31EA9owFHVvdB6bGe8QZZU8wsbU%253D&Expires=1599534767)


### 总结

磨刀不误砍柴工，今天的文章主要是操作 Excel 的工具 xlwings 介绍，大家都用工具操练起来，好好修炼如何拧好螺丝的内功，奥利给！

> 示例代码 [xlwings-能让 Excel 飞上天](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Python_xlwings)