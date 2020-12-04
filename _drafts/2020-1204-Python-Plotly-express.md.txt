---
layout: post
category: python
title: Python可视化神器-Plotly动画展示
tagline: by 潮汐
tags: 
  - python100
---


在之前的一篇文章[Python可视化神器-Plotly](https://mp.weixin.qq.com/s/pAajBlrA7g3Z4qaXdE34Lw)展现了可视化神器-Plotly的基本使用,接下来继续本着学习的姿态继续探索可视化神器-Plotly的神奇之旅。本文介绍如何在Python中使用Plotly创建动画。

<!--more-->

### 可视化神器 Plotly_Express 详解

Plotly 是新一代的数据可视化神器，TopQ量化开源团队，虽然plotly功能强大，却一直没有得到广泛应用，大部分py开发人员，还在使用陈旧的matplotlib，其中最重要的原因，就是plotly的设置过于繁琐。为此，plotly推出了其简化接口：Plotly Express，简称：px。

Plotly Express是对 Plotly.py 的高级封装，内置了大量实用、现代的绘图模板，用户只需调用简单的API函数，即可快速生成漂亮的互动图表。

Plotly Express内置的图表组合，涵盖了90%常用的绘图需要，Python画图，首推Plotly Express。

### 封装图表说明

- scatter：散点图
在散点图中，每行data_frame由2D空间中的符号标记表示；

- scatter_3d：三维散点图
在3D散点图中，每行data_frame由3D空间中的符号标记表示；

- scatter_polar：极坐标散点图
在极坐标散点图中，每行data_frame由极坐标中的符号标记表示；

- scatter_ternary：三元散点图
在三元散点图中，每行data_frame由三元坐标中的符号标记表示；

- scatter_mapbox：地图散点图
在Mapbox散点图中，每一行data_frame都由Mapbox地图上的符号标记表示；

- scatter_geo：地理坐标散点图
在地理散点图中，每一行data_frame都由地图上的符号标记表示；

- scatter_matrix：矩阵散点图
在散点图矩阵(或SPLOM)中，每行data_frame由多个符号标记表示，在2D散点图的网格的每个单元格中有一个，其将每对dimensions彼此相对绘制；

- density_contour：密度等值线图（双变量分布）
在密度等值线图中，行data_frame被组合在一起，成为轮廓标记，以可视化该值的聚合函数histfunc(例如：计数或总和)的2D分布z；

- density_heatmap：密度热力图（双变量分布）
在密度热图中，行data_frame被组合在一起，成为彩色矩形瓦片，以可视化该值的聚合函数histfunc(例如：计数或总和)的2D分布 z；

- line：线条图
在2D线图中，每行data_frame表示为2D空间中折线标记的顶点；

- line_polar：极坐标线条图
在极线图中，每行data_frame表示为极坐标中折线标记的顶点；

- line_ternary：三元线条图
在三元线图中，每行data_frame表示为三元坐标中折线标记的顶点；

- line_mapbox：地图线条图
在Mapbox线图中，每一行data_frame表示为Mapbox地图上折线标记的顶点；

- line_geo：地理坐标线条图
在地理线图中，每一行data_frame表示为地图上折线标记的顶点；

- parallel_coordinates：平行坐标图
在平行坐标图中，每行data_frame由折线标记表示，该折线标记穿过一组平行轴，每个平行轴对应一个平行轴 dimensions；

- parallel_categories：并行类别图
在并行类别(或平行集)图中，每行data_frame与其他共享相同值的行组合，dimensions然后通过一组平行轴绘制为折线标记，每个平行轴对应一个dimensions；

- area：堆积区域图
在堆积区域图中，每行data_frame表示为2D空间中折线标记的顶点。连续折线之间的区域被填充；

- bar：条形图
在条形图中，每行data_frame表示为矩形标记；

- bar_polar：极坐标条形图
在极坐标条形图中，每一行都data_frame表示为极坐标中的楔形标记；

- violin：小提琴图
在小提琴图中，将data_frame每一行分组成一个曲线标记，以便可视化它们的分布；

- box：箱形图
在箱形图中，data_frame的每一行被组合在一起成为盒须标记，以显示它们的分布；

- strip：长条图
在长条图中，每一行data_frame表示为类别中的抖动标记；
l
- histogram：直方图
在直方图中，每一行data_frame被组合在一起成为矩形标记，以可视化该值的聚合函数histfunc(例如，计数或总和)的1D分布y(或者x，如果orientation是'h'时)；

- choropleth：等高(值)区域地图
在等值区域图中，每行data_frame由地图上的彩色区域标记表示；


### 绘制动画散点图
绘画散点图的图表是：scatter，详细代码如下：

```python
import plotly.express as px
df = px.data.gapminder()
px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])
```

**显示结果为：**
![显示结果图](https://imgkr2.cn-bj.ufileos.com/4cf32c0f-1ef8-4587-8fcf-35722b2b699e.gif?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=MlWjzXwD9GdYwlzrrgRwdYduqfU%253D&Expires=1607163261)

### 动画条形图

```python
import plotly.express as px

df = px.data.gapminder()

fig = px.bar(df, x="continent", y="pop", color="continent",
  animation_frame="year", animation_group="country", range_y=[0,4000000000])
fig.show()
```
**显示结果如下：**
![显示结果图](https://imgkr2.cn-bj.ufileos.com/7c6be9ae-3a54-407a-9ae8-b61171147947.gif?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=6FjDCjodiIOa0ZaFnRJs4tVl75c%253D&Expires=1607164615)

### 总结

希望今天文章和实战对大家有所帮助，在以后的成神路上越来越顺利！

### 参考
- <https://www.jianshu.com/p/41735ecd3f75?utm_campaign=hugo>
- <https://plotly.com/python/animations/>

>示例代码：[https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Plotly-express](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Plotly-express)