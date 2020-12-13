---
layout: post
category: python
title: 用 Python 教你画花样图
tagline: by 潮汐
tags: 
  - python100
---


在之前的一篇文章[Python可视化神器-Plotly动画展示](https://mp.weixin.qq.com/s/o6kHhkfPIMYt1qNPnv9sHQ)展现了可视化神器-Plotly的动画的基本应用,本文介绍如何在Python中使用 Plotly 创建地图并在地图上标相应的线。对于 Plotly的详解请参阅之前的文章。

<!--more-->

### 地球仪加线

根据地球仪的区域显示在相应的位置图形上加上线条，完美的线性地球仪详细代码如下：

```python
import plotly.express as px
df = px.data.gapminder().query("year == 2007")
fig = px.line_geo(df, locations="iso_alpha",
                  color="continent", # "continent" is one of the columns of gapminder
                  projection="orthographic")
fig.show()
```

显示结果为：**
![](https://imgkr2.cn-bj.ufileos.com/f3aa02e8-5e15-4d94-9c86-8e519c29fa07.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=JELrEs4GdruVpuo29pA8EtkyhMQ%253D&Expires=1607784971)



### 地图上加线
绘画出相应的地图后添加经纬度，再根据经纬度绘画出相应的线条，
详细代码如下：

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Scattergeo(
    lat = [3.86, 53.55],
    lon = [73.66, 135.05],
    mode = 'lines',
    line = dict(width = 2, color = 'red'),
))

fig.update_layout(
    geo = dict(
        resolution = 50,
        showland = True,
        showlakes = True,
        landcolor = 'rgb(203, 203, 203)',
        countrycolor = 'rgb(204, 204, 204)',
        lakecolor = 'rgb(255, 255, 255)',
        projection_type = "equirectangular",
        coastlinewidth = 3,
        lataxis = dict(
            range = [20, 60],
            showgrid = True,
            dtick = 10
        ),
        lonaxis = dict(
            range = [-100, 20],
            showgrid = True,
            dtick = 20
        ),
    )
)

fig.show()
```
显示结果如下：
![](https://imgkr2.cn-bj.ufileos.com/6faaf352-f6a7-4fcc-80d9-0cb51d9778a5.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=J6KY5YMAdNTlZasS7NDsHmUIpoA%253D&Expires=1607785428)
![](https://imgkr2.cn-bj.ufileos.com/3789a7eb-80c4-4dd5-a768-f3fae2d3eea6.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=3tLRevyeyqqdMAj8MUmg80KF%252Ft8%253D&Expires=1607785435)

### 最后的福利-3D图鉴赏
最后加入一个3D图像鉴赏，制作图像详细代码如下：
```python
# 导入包
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

N = 50

fig = make_subplots(rows=2, cols=2,
                    specs=[[{'is_3d': True}, {'is_3d': True}],
                           [{'is_3d': True}, {'is_3d': True}]],
                    print_grid=False)
for i in [1,2]:
    for j in [1,2]:
        fig.append_trace(
            go.Mesh3d(
                x=(50*np.random.randn(N)),
                y=(20*np.random.randn(N)),
                z=(40*np.random.randn(N)),
                opacity=0.5,
              ),
            row=i, col=j)

fig.update_layout(width=700, margin=dict(r=9, l=9, b=9, t=9))
# 将左上角子图中的比率固定为立方体
fig.update_layout(scene_aspectmode='cube')
# 手动强制z轴显示为其他两个的两倍大
fig.update_layout(scene2_aspectmode='manual',
                  scene2_aspectratio=dict(x=1, y=1, z=2))
# 绘制轴线与轴线范围的比例成比例
fig.update_layout(scene3_aspectmode='data')
# 使用“data”作为默认值自动生成比例良好的内容
fig.update_layout(scene4_aspectmode='auto')
#显示
fig.show()
```
显示结果如下：
![](https://imgkr2.cn-bj.ufileos.com/18acdcb5-a210-41f3-92b2-5ca3e8b3602b.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=mWqiu4ToVMywCwbSBO8NAF0Ka%252FY%253D&Expires=1607787941)
![](https://imgkr2.cn-bj.ufileos.com/d14340ed-a72f-48c0-82df-ea8c518d475e.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=9CUQdSEy9IEhzpmWY%252FCpmOF6xOs%253D&Expires=1607787946)

### 总结

希望今天文章和实战对大家有所帮助，在以后的成神路上越来越顺利！

### 参考
- <https://plotly.com/python/animations/>
- <https://plotly.com/python/maps/>

>示例代码：[https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Plotly-express](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Plotly-express)