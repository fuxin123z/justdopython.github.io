---
layout: post
category: python
title: 我用 Python 做了一个全球疫情数据大屏
tagline: by 豆豆
tags: 
  - python
---

2019 年年底这场袭击全国的突发性疫情，让我们过了一个有史以来最长春节长假的同时，也给我们带来了不少的损失，与此同时我们也认识到在大自然面前人类的渺小。好在在政府的正确且有力的领导下，经过全国人民群众的不懈努力，我们终于将疫情给遏制住了，打赢了这场没有硝烟的战争。

然而就在国内疫情已经明显好转，实现确诊病例零增长的时候，疫情开始在全球蔓延。今天，我用 Python 做了一个全球疫情数据大屏，我们一起来看下整体的效果图。

<!--more-->

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/001.png)

整个大屏分为全球数据和国内数据两个模块，每个模块总体分为三个部分，左侧是各个地区详细数据，中间是疫情数据地图，右边则是排行榜和最新动态。

## 项目结构

我们整个项目的结构图如下所示。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/002.jpg)

爬虫模块负责从腾讯新闻获取数据，之后存入 Redis。Flask 是一个 Web 框架，负责 URL 和后台函数的映射，以及数据的传输。换言之，也就是从 Redis 中获取到原始数据，然后整理成相应的格式之后传递给前端页面，前端页面在拿到数据之后，调用百度的 ECharts 来实现图表的展示即可。

引入项目所需的全部模块。

```python
import requests
import json
import redis
from flask import Flask, render_template
import datetime
import pandas as pd
```

## 数据获取

开始操作之前，需要先梳理下我们都需要什么数据。关于国内，我们需要的是各个省详细数据、全国数据总和、最新动态、以及境外输入人数 TOP 10 的省市。关于国外，我们需要的是各个国家详细数据、国外数据总和、最新动态、以及 24 小时新增人数 TOP 10 的国家。

本次我们的疫情数据是从腾讯新闻获取的，打开该网址（https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1）按 F12 将开发者工具调出来，然后切换到 Network 选项页，逐个接口分析之后，发现所有我们想要的数据都是接口返回的。各个数据接口如下：

+ 国内统计数据（数据总和以及各省份详细数据）：`https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5`
+ 国外各国家详细数据：`https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist`
+ 国外数据总和：`https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis`
+ 最新动态数据：`https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoNewsArticleList`

找到了接口之后，接下来就很简单了，直接调用接口将数据爬取下来即可。其中国内统计数据接口接口返回的 data 不是标准的 JSON 串，而是一个字符串，所以我们需要做下简单的转化。

为了方便h后续操作，我们将调用 request 库爬取数据的操作封装起来，方便调用。

```python
def pull_data_from_web(url):
    response = requests.get(url, headers=header)
    return json.loads(response.text) if response.status_code == 200 else None
```

最新动态数据我们只取发布时间，标题以及链接地址。

```python
# 获取最新动态数据
# 获取最新动态数据
def get_article_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoNewsArticleList')
    if data is None:
        return ''
    return [[item['publish_time'], item['url'], item['title']] for item in data['data']['FAutoNewsArticleList']]
```

国内数据我们需要获取数据总和以及各省份详细数据。

```python
# 获取国内统计数据【现有确诊 确诊 治愈 死亡 境外输入 & 各省份详细数据（现有确诊 确诊 治愈 死亡 境外输入）】
def get_china_data():
    data = pull_data_from_web('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5')
    if data is None:
        return ''
    dict = json.loads(data['data'])
    province_res = []
    for province in dict['areaTree'][0]['children']:
        name = province['name']
        now_confirm = province['total']['nowConfirm']
        confirm = province['total']['confirm']
        heal = province['total']['heal']
        dead = province['total']['dead']
        import_abroad = 0
        for item in province['children']:
            if item['name'] == '境外输入':
                import_abroad = item['total']['confirm']
                break
        province_res.append([name, import_abroad, now_confirm, confirm, heal, dead])
    return {'chinaTotal': dict['chinaTotal'], 'chinaAdd': dict['chinaAdd'], 'province': province_res}
```

获取国外各个国家及地区详细数据。

```python
# 获取各个国家当前【新增、确诊、治愈、死亡】数据
def get_rank_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist')
    if data is None:
        return ''
    return [[item['name'], item['confirmAdd'], item['confirm'], item['heal'], item['dead']] for item in data['data']]

```

国外数据总和。

```python
# 获取国外统计数据【现有确诊 确诊 治愈 死亡】
def get_foreign_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis')
    if data is None:
        return ''
    return data['data']['FAutoGlobalStatis']
```

将数据存入 Redis 后就这一步就大功告成了。

```python
article_data = get_article_data()
r.set('article_data', json.dumps(article_data))

rank_data = get_rank_data()
r.set('rank_data', json.dumps(rank_data))

china_data = get_china_data()
r.set('china_data', json.dumps(china_data))

foreign_data = get_foreign_data()
r.set('foreign_data', json.dumps(foreign_data))
```

## 数据处理

获取到源数据之后，需要对数据做一下整理，以符合前端页面的展示要求。

整理数据时我们用的是 pandas 这个库，在我们 100 天系列的文章中有做过介绍，忘记的小伙伴们可以翻翻历史文章复习下。

最新动态的数据是比较规整的，不需要做太多处理，直接拿来用即可。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/003.png)

再看国内的统计数据以及各省份详细数据。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/004.png)

可回看出当前国内的数据总和是在 chinaTotal 中，当日新增在 chinaAdd 中，各省市详细数据在 province 中，其中各省市详细数据中是按照境外输入、当前确诊、累计确诊、治愈、死亡来存放的。

对于各个省市详细数据，我们以当前确诊人数倒序排序。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/005.png)

可以看的，现在湖北的确诊人数已经非常少了，而鸡头黑龙江则稳居第一，成为国内确诊人数 TOP 1 的省份。

最后来看国外数据，统计数据比较规整，各个国家详细数据我们按照累计确诊人数倒序排序。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/006.png)

最后，我们还需要处理下「境外输入省市 TOP 10」和「24小时新增国家 TOP 10」的数据。直接从省市详细数据和各国家详细数据中获取即可。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/007.png)

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/008.png)

## 图表展示

我们先来简单看下 ECharts 的使用方法，首先要引入相应的 js 文件，然后写一个容纳图表的 div 标签。

```html
<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
<div id="top10" style="width: 300px;height:300px"></div>
```

最后编写图表的 js 代码即可。

```js
<script type="text/javascript">
    var top10 = echarts.init(document.getElementById('top10'));
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '测试图表',
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            show: true,
        },
        yAxis: {
            type: 'category',
            data: ['苹果', '橘子', '香蕉', '石榴'],
        },
        series: [
            {
                name: '',
                type: 'bar',
                barWidth: 10,
                data: [66, 88, 90, 20]
            }
        ]
    };

    top10.setOption(option);
</script>
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/04/2020-04-20-epidemic-big-screen/009.png)

但这里的数据是固定的，而我们的大屏展示数据都是动态变换的，怎么办呢，前端通过 Ajax 技术从后台接口获取即可，类似下面这样子。

```js
var top10_result = $.ajax({type : "GET", url : 'http://127.0.0.1:5200/china_top10', data : null, async : false});
top10_result = JSON.parse(top10_result.responseText);

// 设置数据
yAxis: {
    type: 'category',
    data: top10_result.country,
},
```

现在我们已经完成了一个简单的图表，并且已经可以动态设置数据了。现在缺少的就是把大屏的各个图表拼接起来，并且将我们之前准备好的数据设置进去即可。

首先我们初始化 Flask 并设置路由映射关系，然后将前端页面所需的统计数据一并返回。

```python
app = Flask(__name__)

@app.route('/global')
def global_index():
    context = {
        'date': get_date(),
        'statistics_data': json.loads(r.get('foreign_data')),
        'country_data': get_rank_data(),
        'article_data': json.loads(r.get('article_data'))
    }
    return render_template('global.html', **context)
```
其中地图数据以及 TOP 10 的数据需要以接口的方式提供出去，前端页面直接通过 Ajax 技术调用。

```python
@app.route('/global_top10')
def get_global_top10():
    df = pd.DataFrame(json.loads(r.get('rank_data')), columns=['name', 'confirmAdd', 'confirm', 'heal', 'dead'])
    top10 = df.sort_values('confirmAdd', ascending=True).tail(10)
    result = {'country': top10['name'].values.tolist(), 'data': top10['confirmAdd'].values.tolist()}
    return json.dumps(result)

@app.route('/global_map')
def get_global_map():
    df = pd.DataFrame(json.loads(r.get('rank_data')), columns=['name', 'confirmAdd', 'confirm', 'heal', 'dead'])
    records = df.to_dict(orient="records")
    china_data = json.loads(r.get('china_data'))
    result = {
        'confirmAdd': [{'name': '中国', 'value': china_data['chinaAdd']['confirm']}],
        'confirm': [{'name': '中国', 'value': china_data['chinaTotal']['confirm']}],
        'heal': [{'name': '中国', 'value': china_data['chinaTotal']['heal']}],
        'dead': [{'name': '中国', 'value': china_data['chinaTotal']['dead']}]
    }

    for item in records:
        result['confirmAdd'].append({'name': item['name'], 'value': item['confirmAdd']})
        result['confirm'].append({'name': item['name'], 'value': item['confirm']})
        result['heal'].append({'name': item['name'], 'value': item['heal']})
        result['dead'].append({'name': item['name'], 'value': item['dead']})

    return json.dumps(result)    
```

至此，我们完成了从获取数据，到整理数据，再到前端页面展示的整一个过程，还是需要很多知识的。

## 总结

今天我们完成了一个全球疫情数据大屏可视化程序，步骤清晰，难度不大，只是页面上各个图表组件的位置以及样式调试起来比较繁琐些，但这不是本文重点。

你需要着重理解的是前端页面的 URL 是如何和后台函数做路由映射的，数据又是如何传递和绑定的，以及后台逻辑和数据的处理过程这才是 Web 开发的精髓。

最后，你可以从公众号获取源码后，修改程序使之支持定时从数据源获取数据，更新前端图表，而无需手动操作。

## 代码地址

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/doudou/2020-04-20-epidemic-big-screen

## 参考资料

https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1