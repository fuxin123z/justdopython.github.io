---
layout: post
category: python
title: Python 可视化神器--Plotly
tagline: by 潮汐
tags: 
  - python100
---

学习Python是做数分析的最基础的一步，数据分析离不开数据可视化。Python第三方库中我们最常用的可视化库是 pandas，matplotlib，pyecharts，
当然还有 Tableau，另外最近在学习过程中发现另一款可视化神器-Plotly，它是一款用来做数据分析和可视化的在线平台，功能非常强大,
可以在线绘制很多图形比如条形图、散点图、饼图、直方图等等。除此之外，它还支持在线编辑，以及多种语言 python、javascript、matlab、R等许多API。
它在python中使用也非常简单，直接用`pip install plotly` 安装好即可使用。本文将结合 `plotly` 库在 `jupyter notebook` 中来进行图形绘制。

<!--more-->

使用 Plotly 可以画出很多媲美Tableau的高质量图，如下图所示：
![](https://imgkr2.cn-bj.ufileos.com/694d2ce0-8839-4ac8-bd79-fda10a3021c6.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=iknF9Kr76SV4V5tHvHbntwqUx4Y%253D&Expires=1604901502)
![](https://imgkr2.cn-bj.ufileos.com/7e2d9fce-dee9-4799-8883-f5e572d42dc6.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=pSV936XBi1H5yVx%252BXRVsAgWpVr4%253D&Expires=1604901516)

### 折线点图

折现点图画图步骤如下：
首先在 Pycharm 界面输入 `jupyter notebook`后进入网页编辑界面，新建一个文件，导入相应的包即可进行图形绘制：

```python
# import pkg
from plotly.graph_objs import Scatter,Layout
import plotly
import plotly.offline as py
import numpy as np
import plotly.graph_objs as go

```

```python
#设置编辑模式
plotly.offline.init_notebook_mode(connected=True)

```

```python
#制作折线图
N = 150
random_x = np.linspace(0,1,N)
random_y0 = np.random.randn(N)+7
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-7

trace0 = go.Scatter(
    x = random_x,
    y = random_y0,
    mode = 'markers',
    name = 'markers'
)
trace1 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'lines+markers',
    name = 'lines+markers'
)
trace2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'lines',
    name = 'lines'
)
data = [trace0,trace1,trace2]
py.iplot(data)
```

显示结果如下：
![折线点图](https://imgkr2.cn-bj.ufileos.com/dad33d00-2638-4c94-81e9-7723f8c9f127.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=DGpxZQX5%252F%252BSwQgGriYqCp%252F4XkWQ%253D&Expires=1604903293)

### 直方图

```python
# 直方图
trace0 = go.Bar(
    x = ['Jan','Feb','Mar','Apr', 'May','Jun',
         'Jul','Aug','Sep','Oct','Nov','Dec'],
    y = [20,15,25,16,18,28,19,67,12,56,14,27],
    name = 'Primary Product',
    marker=dict(
        color = 'rgb(49,130,189)'
    )
)
trace1 = go.Bar(
    x = ['Jan','Feb','Mar','Apr', 'May','Jun',
         'Jul','Aug','Sep','Oct','Nov','Dec'],
    y = [29,14,32,14,16,19,25,14,10,12,82,16],
    name = 'Secondary Product',
    marker=dict(
        color = 'rgb(204,204,204)'
    )
)
data = [trace0,trace1]
py.iplot(data)
```
显示结果如下：
![直方图](https://imgkr2.cn-bj.ufileos.com/092ab6e7-0af7-4f4e-83c1-580b52ec185e.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=UyWtJG7rzcLEhjqUK5S%252F6ZGgOv4%253D&Expires=1604905209)

### 散点图

```python
# 散点图
trace1 = go.Scatter(
     y = np.random.randn(700),
    mode = 'markers',
    marker = dict(
        size = 16,
        color = np.random.randn(800),
        colorscale = 'Viridis',
        showscale = True
    )
)
data = [trace1]
py.iplot(data)
```

显示结果如下：
![散点图](https://imgkr2.cn-bj.ufileos.com/65731ef9-4fe8-4649-a9b3-910d50ee5633.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=w6lCNChD%252FTxD0GqbPb56y0RbU9c%253D&Expires=1604906021)


## 总结

今天的文章主要学习可视化神器-plotpy 的相关操作，希望在平时的工作中有所应用。更多的内容详见 [plotly官网](https://plotly.com/python/)

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/chaoxi/2020-11-08-plotly
