---
layout: post
category: python
title: 神器 Pandas 绘图大全(中)！
tagline: by 潮汐
tags: Pandas 绘图大全！
  - pandas
  - python
---
神器 Pandas 绘图续集来啦，今天来聊聊 Pandas 另外几种绘图方式。

### 饼图

在画饼图的时候可以使用DataFrame.plot.pie()或Series.plot.pie()创建饼图。 如果您的数据包含任何NaN，它们将被自动填充为0， 如果数据中有任何负值，将引发ValueError。  画饼图详细代码如下：

```python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def craw_pie():

    series = pd.Series(3 * np.random.rand(4), index=["1", "2", "3", "4"], name="series")
    series.plot.pie(figsize=(6, 6));
    plt.show()

if __name__ == '__main__':
    craw_pie()
```

显示结果如下：

![](https://files.mdnice.com/user/6478/f946bf4a-b073-4be3-a35f-f8a455272477.png)

对于饼状图，最好使用正方形图形，即图形长宽比为1。 您可以创建宽度和高度相等的图形，或者通过在返回的axes对象上调用ax.set_aspect('equal')来绘制后强制宽高比相等。  
 
**注意*:* 带DataFrame的饼图要求您通过y参数指定目标列，或者subplot =True。 当指定y时，将绘制选定列的饼图。 如果指定subplot =True，则将每个列的饼图绘制为子图。 默认情况下，将在每个饼图中绘制一个图例; 指定legend=False来隐藏它。  

例如：将每个列的饼图绘制为子图实例如下：

```python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_pie1():
    df = pd.DataFrame(
        3 * np.random.rand(4, 2), index=["a", "b", "c", "d"], columns=["x", "y"])
    df.plot.pie(subplots=True, figsize=(8, 4))
    plt.show()

if __name__ == '__main__':
    draw_pie1()
```
显示结果图如下：

![](https://files.mdnice.com/user/6478/9b888400-153b-40e4-8619-a6dd782454d1.png)

根据上图显示可知，加了`subplots=True`参数后，图形显示的颜色代表在长方形图片中已展示出来。

如果要隐藏，加`legend=False`即可隐藏，实例如下:

```python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_pie1():
    df = pd.DataFrame(
        3 * np.random.rand(4, 2), index=["a", "b", "c", "d"], columns=["x", "y"])
    df.plot.pie(subplots=True, figsize=(8, 4), legend=False)
    plt.show()

if __name__ == '__main__':
    draw_pie1()
```

结果图如下：

![](https://files.mdnice.com/user/6478/8ae2d721-10e1-48c7-803d-cbbfc4982fdc.png)

咱们在绘画的时候也可以可以使用标签和颜色关键字来指定每个楔形的标签和颜色,例如：  

```python

def draw_pie2():
    series = pd.Series(3 * np.random.rand(4), index=["1", "2", "3", "4"], name="series")
    series.plot.pie(
        labels=["A", "B", "C", "D"],
        colors=["r", "g", "b", "c"],
        autopct="%.2f",
        fontsize=20,
        figsize=(6, 6),)
    plt.show()

if __name__ == '__main__':
    draw_pie2()
```

展示结果如下：

![](https://files.mdnice.com/user/6478/4e425ccc-2d6e-42ec-8886-6320733e4c0e.png)

如果传递的值的总和小于1,matplotlib会画一个半圆。  

实例如下：

```python
def draw_pie3():
    series = pd.Series([0.1] * 4, index=["a", "b", "c", "d"], name="series2")
    series.plot.pie(figsize=(6, 6))
    plt.show()

if __name__ == '__main__':
    draw_pie3()
```

![](https://files.mdnice.com/user/6478/1bbf8a43-ee4d-4977-9a3d-bde75167b3b6.png)

### 散射矩阵图 

你可以使用 pandas.plotting 绘图板中的 scatter_matrix方法创建一个散点图矩阵,实例如下：
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
def draw_pie4():

    df = pd.DataFrame(np.random.randn(1000, 4), columns=["a", "b", "c", "d"])

    scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal="kde")
    plt.show()

if __name__ == '__main__':
    draw_pie4()
```
显示结果图如下：
![](https://files.mdnice.com/user/6478/45f93677-30a7-486a-965b-85ec10e09f41.png)


### 总结

今天的文章就到这里啦，希望今天的文章对大家有帮助！更多关于 Pandas 绘制图形的方法咱们下集见分晓，希望自己进步的同时也对大家有更大的用处，咱们下期见！