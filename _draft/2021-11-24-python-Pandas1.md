---
layout: post
category: python
title: 神器 Pandas 绘图大全(上)！
tagline: by 潮汐
tags: Pandas 绘图大全！
  - Python技巧
  - 编程
  - Pandas
---

今天的文章讲解如何利用 Pandas 来绘图，前面写过 matplotlib 相关文章，matplotlib   虽然功能强大，但是 matplotlib 相对而言较为底层，画图时步骤较为繁琐，比较麻烦，因为要画一张完整的图表，需要实现很多的基本组件，比如图像类型、刻度、标题、图例、注解等等。目前有很多的开源框架所实现的绘图功能是基于 matplotlib 的，pandas是其中之一，对于 pandas 数据分析而言，直接使用 pandas 本身实现的绘图方法比 matplotlib 更方便简单。
关于更多 Pandas 的相关知识请参考[官方文档](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html)

### Pandas 绘制线状图

使用 Pandas 绘制线状图代码如下：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def craw_line():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    ts = ts.cumsum()
    ts.plot()
    plt.show()

if __name__ == '__main__':
    craw_line()
```
显示结果如下：

![](https://files.mdnice.com/user/6478/e21f0452-fe1b-4e82-bba3-e59a51589f5e.png)

第二种绘画线状图方式如下：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def craw_line1():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
    df = df.cumsum()
    df.plot()
    plt.show()

if __name__ == '__main__':
    craw_line1()
```
线性图显示结果如下：

![](https://files.mdnice.com/user/6478/92cb4801-d212-426d-a95c-9d16f32132ee.png)

### Pandas 绘制条形图

除了绘制默认的线状图，还能绘制其他图形样式，例如通过以下方法绘制条形图。绘图方法可以作为plot()的kind关键字参数提供。

#### 绘制条形图1

通过如下方法绘制条形图1，详细代码如下：

```python
def craw_bar():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
    plt.figure()
    df.iloc[5].plot(kind="bar")
    plt.show()

if __name__ == '__main__':
    craw_bar()
```

**结果图显示如下：**

![](https://files.mdnice.com/user/6478/f958799d-172a-488b-b09d-bff422219ce6.png)

#### 绘制条形图2

通过如下方法绘制条形图2，详细代码如下：

```python
def craw_bar1():
    #ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.bar()
    plt.show()

if __name__ == '__main__':
    craw_bar1()
```

图形结果展示如下：

![](https://files.mdnice.com/user/6478/64c7716a-812f-433e-ae7e-da26f702b3ad.png)

**生成堆叠条形图**

上面的条形图2可以生成堆叠条形图，加上`stacked=True`参数即可，详细代码如下：

```python
def craw_bar2():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.bar(stacked=True)
    plt.show()

if __name__ == '__main__':
    craw_bar2()
```
堆叠条形图展示如下：

![](https://files.mdnice.com/user/6478/d4159329-114d-4595-9b46-141d0f4b1d31.png)

将以上条形图设置为水平条形图，详细代码如下：

```python
def craw_bar3():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.barh(stacked=True)
    plt.show()

if __name__ == '__main__':
    craw_bar3()
```
展示结果图如下：

![](https://files.mdnice.com/user/6478/07b30b73-56f8-4299-923c-a67b25552b35.png)

### 总结

今天的文章就到这里啦，希望今天的文章对大家有帮助！更多关于 Pandas 绘制图形的方法咱们下集见分晓，希望自己进步的同时也对大家有更大的用处，咱们下期见！