---
layout: post     
title: 如何用 Python 制作地球仪？                                  
category: 如何用 Python 制作地球仪？     
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

Python 功能真的很强，强大到让人吃惊，它能做的事囊括爬虫、数据分析、数据可视化、游戏等等各方面，这些功能在实际的使用中应用广泛，开发程序讲究页面的美观与炫酷效果，
今天的文章将给各位读者朋友们带来不一样的视觉盛宴，感兴趣的朋友欢迎一起尝试。

<!--more-->

写在前面的话：在之前的文章 [Python 图表利器 pyecharts](https://mp.weixin.qq.com/s/3EFi_8ONFNjikajvPE-fOQ) 中有介绍了 pyecharts 的安装及使用,详细教程请到 [官网](https://pyecharts.org/#/zh-cn/intro) 学习

pyecharts 功能很强大，只需要导入相应的模块就配置相应的选项即可生成对应的超文本文件，使用浏览器访问即可！具体实例请见下文


### 盛宴1-2D世界地图

先来个 2D 的瞅瞅~

![世界地图](https://imgkr.cn-bj.ufileos.com/def408a5-f31e-4b94-a581-6345acb043e0.gif)

实现代码如下：

```python 
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

c = (
    Map(init_opts=opts.InitOpts(width='1500px', height='1200px',bg_color='#E0EEEE'))
    # 加载世界地图实例
    .add("世界地图", [list(z) for z in zip(Faker.country, Faker.values())], "world")
   # 不显示地图标志
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        # 配置项标题设置
        title_opts=opts.TitleOpts(title="世界地图示例"),
        visualmap_opts=opts.VisualMapOpts(max_=200)
    )
    # 生成超文本文件
    .render("world_map.html")
)
```

### 盛宴2-中国3D地图

通过导入 Map3D 等实现中国地图的 3D 呈现：

![中国地图](https://imgkr.cn-bj.ufileos.com/053fbabd-33b9-4ef4-b281-b01bf7be7574.gif)


实现代码如下：

```python
from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

c = (
    Map3D(init_opts=opts.InitOpts(width='1300px', height='1300px',bg_color='#EBEBEB'))

    .add_schema(
        itemstyle_opts=opts.ItemStyleOpts(
            color="#CDBA96",
            opacity=1,
            border_width=0.8,
            border_color="rgb(62,215,213)",
        ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=True,
            text_style=opts.TextStyleOpts(
                color="#104E8B", font_size=16, background_color="rgba(0,0,0,0)"
            ),
        ),
        emphasis_label_opts=opts.LabelOpts(is_show=True),
        light_opts=opts.Map3DLightOpts(
            main_color="#FFEBCD",
            main_intensity=1.2,
            is_main_shadow=False,
            main_alpha=55,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    )
    .add(series_name="", data_pair="", maptype=ChartType.MAP3D)
    # 全局设置地图属性
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全国行政区划地图"),
        visualmap_opts=opts.VisualMapOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    .render("map3d_china_base.html")
)

```

### 盛宴3-贵州地图

现在用另一种方式来实现我家乡的地图，一起来一睹为快~

![贵州地图](https://imgkr.cn-bj.ufileos.com/67fafb1d-4280-4261-b91f-6b8c5c1c750b.gif)


**代码实现如下：**
```python
# 写入省份内各地区经纬度
example_data = [
    [[106.70722,26.59820, 1000],[106.63024, 26.64702, 1000]],
    [[104.83023, 26.59336], [106.92723, 27.72545]],
    [[105.30504, 27.29847], [107.52034, 26.29322]],
    [[107.89868, 26.52881], [104.948571, 25.077502]],
    [[105.9462, 26.25367], [109.18099, 27.69066]],
]
#　添加 3D 地图
c = (
    Map3D(init_opts=opts.InitOpts(width='1200px', height='1200px'))
    .add_schema(
        maptype="贵州",
        itemstyle_opts=opts.ItemStyleOpts(
            color="rgb(5,101,123)",
            opacity=1,
            border_width=0.8,
            border_color="rgb(62,215,213)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.2,
            is_main_shadow=True,
            main_alpha=55,
            main_beta=10,
            ambient_intensity=0.3,
        ),
        view_control_opts=opts.Map3DViewControlOpts(center=[-10, 0, 10]),
        post_effect_opts=opts.Map3DPostEffectOpts(is_enable=True),

    )
    .add(
        series_name="",
        data_pair=example_data,
        type_=ChartType.LINES3D,
        effect=opts.Lines3DEffectOpts(
            is_show=True,
            period=4,
            trail_width=3,
            trail_length=0.5,
            trail_color="#f00",
            trail_opacity=1,
        ),
        label_opts=opts.LabelOpts(is_show=True),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-GuiZhou3D"))
    .render("guizhou_map_3d.html")
)

```


### 盛宴4-地球村实现

一起来看看旋转的地球吧^^

![旋转的地球](https://imgkr.cn-bj.ufileos.com/d25afe28-beaf-4cb3-b7f1-95996360f5f5.gif)

**实现代码如下：**

```python
import pyecharts.options as opts
from pyecharts.charts import MapGlobe
from pyecharts.faker import POPULATION


data = [x for _, x in POPULATION[1:]]
low, high = min(data), max(data)
c = (
    MapGlobe(init_opts=opts.InitOpts(width='1000px', height='1000px',bg_color='#FFFAFA',))
    .add_schema()
    .add(
        maptype="world",
        series_name="World Population",
        data_pair=POPULATION[1:],
        is_map_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=True),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="3D 地球示例"),
        # 设置地球属性
        visualmap_opts=opts.VisualMapOpts(
            min_=low,
            max_=high,
            range_text=["max", "min"],
            is_calculable=True,
            range_color=["lightskyblue", "yellow", "orangered"],
        )
    )
    .render("world_map_3d.html")
)
```

### 总结

希望今天的分享能给大家带来不一样的视觉享受，同时伙伴们也别忘了要多多实践。
实践是检验真理的唯一标准！


### 参考
[http://gallery.pyecharts.org/#/Map3D/](http://gallery.pyecharts.org/#/Map3D/)

> 示例代码 (https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Earth_view)
