---
layout: post     
title:  我将实时疫情数据爬取下来并做了展示                                                
category: 我将实时疫情数据爬取下来并做了展示         
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

今天是全中国按下暂停键的第 25 天，在全中国按下暂停键的日子里，主人翁每天早上睁眼第一件事就是打开手机看着疫情实时数据的变化，看看每一条催泪的新闻。揪着的心却在默默祈祷疫情赶快过去。

言归正传，对于一个热衷技术且大有前途的青年来说，数据看久了是不是想到要展示一个技术大白的真正技术了呢？今天的文章主人翁就抱着学习的态度将腾讯每天推送的实时疫情数据爬取下来进行数据展示。

思路：

 1. 网页分析
 2. 实时数据抓取
 3. 数据可视化展示
 

### 网页分析：

 在百度中搜索 [腾讯肺炎](https://news.qq.com/zt2020/page/feiyan.htm) 即可获得疫情实时追踪展示信息：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020022415331294.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70) 
 
 在此网页任意地方`右键单击`--->`检查或者审查元素`查看源代码,或者打开浏览器开发者模式，然后直接安 F12 查看源代码，再查看网络反馈的消息，如下图所示：
 
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224160730691.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

消息响应具体信息如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224161658528.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

由上可知数据为 JSON 类型的数据。

### 实时数据抓取

通过网页分析后了解到疫情数据是 JSON 类型，因此爬取的主要原理是通过 Requests 获取 Json 请求。然后再获取到各省份的相关数据，数据抓取代码如下：

```python
import time, json, requests
# 腾讯疫情实时数据数据 URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
# 加载 JSON 数据并解析
data = json.loads(requests.get(url=url).json()['data'])
#　打印数据
print(data)
print(data.keys())
```

**输出数据部分信息如下：**

```
data：{
	'lastUpdateTime': '2020-02-24 16:04:30',
	'chinaTotal': {
		'confirm': 77262,
		'heal': 24839,
		'dead': 2596,
		'nowConfirm': 49827,
		'suspect': 3434,
		'nowSevere': 9915
	},
	'chinaAdd': {
		'confirm': 416,
		'heal': 1932,
		'dead': 151,
		'nowConfirm': -1667,
		'suspect': -714,
		'nowSevere': -1053
	},
……

keys: dict_keys(['lastUpdateTime', 'chinaTotal', 'chinaAdd', 'isShowAdd', 'showAddSwitch', 'areaTree', 'chinaDayList', 'chinaDayAddList', 'dailyNewAddHistory', 'dailyHistory', 'wuhanDayList', 'articleList'])

```
至此疫情数据就获取完毕，So yesy 的有木有，接下来需要统计疫情数据的 34 个省份信息，首先分析输出的数据，经过分析发现省份数据的 Json 头为 areaTree,详细信息如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224165155450.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

**获取省份详细代码如下：**

```python
import time, json, requests
# 腾讯疫情实时数据数据 URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
# 加载 JSON 数据并解析
data = json.loads(requests.get(url=url).json()['data'])
#　打印数据
print(data)
print(data.keys())

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
num = data['areaTree'][0]['children']
print(len(num))
# 遍历所有数据后输出，直到输出结束
for item in num:
    print(item['name'],end=" ")
else:
    print("\n")
```

**输出信息如下：**

```
{'lastUpdateTime': '2020-02-24 17:06:26', 'chinaTotal': {'confirm': 77262, 'heal': 24839, 'dead': 2596, 'nowConfirm': 49827, 'suspect': 3434, 'nowSevere': 9915}, 'chinaAdd': {'confirm': 416, 'heal': 1932, 'dead': 151, ……
dict_keys(['lastUpdateTime', 'chinaTotal', 'chinaAdd', 'isShowAdd', 'showAddSwitch', 'areaTree', 'chinaDayList', 'chinaDayAddList', 'dailyNewAddHistory', 'dailyHistory', 'wuhanDayList', 'articleList'])
34
湖北 广东 河南 浙江 湖南 安徽 江西 山东 江苏 重庆 四川 黑龙江 北京 上海 河北 福建 广西 陕西 云南 海南 贵州 天津 山西 辽宁 吉林 甘肃 新疆 内蒙古 香港 宁夏 台湾 青海 澳门 西藏 

```
34 个省份数据获取完毕后接下来需要解析全国已确诊的省份对应数据，详细代码如下：

```python
import time, json, requests
# 腾讯疫情实时数据数据 URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
# 加载 JSON 数据并解析
data = json.loads(requests.get(url=url).json()['data'])
#　打印数据输出数据
print(data)
print(data.keys())

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
num_area = data['areaTree'][0]['children']
print(len(num_area))
# 遍历所有数据后输出，直到输出结束
for item in num_area:
    print(item['name'],end=" ")
else:
    print("\n")

# 解析所有确诊数据
all_data = {}
for item in num_area:
    # 输出省市名称
    if item['name'] not in all_data:
        all_data.update({item['name']:0})
    #输出省市对应的数据
    for city_data in item['children']:
        all_data[item['name']] +=int(city_data['total']['confirm'])
#　输出结果
print(all_data)

```
**结果输出为：**

```
{'lastUpdateTime': '2020-02-24 17:06:26', 'chinaTotal': {'confirm': 77262, 'heal': 24839, 'dead': 2596, 'nowConfirm': 49827, 'suspect': 3434, ……owSevere': 9915}
dict_keys(['lastUpdateTime', 'chinaTotal', 'chinaAdd', 'isShowAdd', 'showAddSwitch', 'areaTree', 'chinaDayList', 'chinaDayAddList', 'dailyNewAddHistory', 'dailyHistory', 'wuhanDayList', 'articleList'])
34
湖北 广东 河南 浙江 湖南 安徽 江西 山东 江苏 重庆 四川 黑龙江 北京 上海 河北 福建 广西 陕西 云南 海南 贵州 天津 山西 辽宁 吉林 甘肃 新疆 内蒙古 香港 宁夏 台湾 青海 澳门 西藏 

{'湖北': 64287, '广东': 1345, '河南': 1271, '浙江': 1205, '湖南': 1016, '安徽': 989, '江西': 934, '山东': 755, '江苏': 631, '重庆': 575, '四川': 527, '黑龙江': 480, '北京': 399, '上海': 335, '河北': 311, '福建': 293, '广西': 251, '陕西': 245, '云南': 174, '海南': 168, '贵州': 146, '天津': 135, '山西': 132, '辽宁': 121, '吉林': 93, '甘肃': 91, '新疆': 76, '内蒙古': 75, '香港': 74, '宁夏': 71, '台湾': 28, '青海': 18, '澳门': 10, '西藏': 1}

```
接下来我们对比一下抓取的数据是否正确：
实时数据为：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224171905547.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

**抓取的数据为：**

	'湖北': 64287,
	'广东': 1345,
	'河南': 1271,
	'浙江': 1205,
	'湖南': 1016,
	'安徽': 989,
	'江西': 934,
	'山东': 755,
	'江苏': 631,
	'重庆': 575,
	'四川': 527,

由此可见抓取的数据和实时的数据无差异。

### 数据可视化展示

接下来我们将对已经解析好的数据进行可视化展示，本文可视化知识点使用的是公众号 100 天学习计划的知识点 Matplotlib，详情参考文章：[第91天：Python matplotlib introduction](https://mp.weixin.qq.com/s/hLrnOxuuaFQ8yVhh69oI6g) 和  [第92天：Python Matplotlib 进阶操作](https://mp.weixin.qq.com/s/uUgQt_1Z-_1vQ0qTOh4qWg)

数据展示思路和代码如下：

```python
# 使用 Matplotlib 绘制全国确诊病例柱状图
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  #正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    #正常显示负号

#获取数据
names = all_data.keys()
nums = all_data.values()
print(names)
print(nums)

# 绘图
plt.figure(figsize=[11,7])
plt.bar(names, nums, width=0.8, color='purple')

# 设置标题
plt.xlabel("地区", fontproperties='SimHei', size=15)
plt.ylabel("人数", fontproperties='SimHei', rotation=90, size=12)
plt.title("全国疫情确诊图", fontproperties='SimHei', size=16)
plt.xticks(list(names), fontproperties='SimHei', rotation=-60, size=10)

# 显示数字
for a, b in zip(list(names), list(nums)):
    plt.text(a, b, b, ha='center', va='bottom', size=6)
    
#　图形展示
plt.show()
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224174248455.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)
疫情数据可视化展示完毕！

### 总结
本文用到的思路及知识点总结如下：

数据爬取思路：
	网站分析 -->  获取数据 --> 解析数据
	
数据可视化思路：
	Matplotlib 基本知识的运用 --> 分析数据-->画图--> 展示图形

最后希望疫情早点结束，没有一个冬天不可逾越，没有一个春天不会到来，中国加油！武汉加油！ 

### 参考
https://blog.csdn.net/Eastmount/article/details/104298388
https://blog.csdn.net/xufive/article/details/104282093
https://blog.csdn.net/xufive/article/details/104093197
https://blog.csdn.net/shineych/article/details/104173449

> 文中示例代码：[python-100-days](https://github.com/JustDoPython/python-100-day)