---
layout: post
category: python
title: 喜欢玩荣耀的有福了，用 Python 获取全英雄皮肤
tagline: by 極光
tags:
  - python
---

很多朋友都喜欢玩王者荣耀，也很喜欢里面的英雄和各种风格的皮肤，而今天为大家介绍的，就是如果用 Python 一键获取全英雄的皮肤图片，保存到电脑上，用来做背景图片循环切换，是不是也很美……

<!--more-->

## 安装模块

这里需要安装以下模块，当然如果已安装就不用再装了：

```sh
# 安装引用模块
pip3 install bs4
pip3 install requests
```

## 分析获取

由先打开王者荣耀官网英雄介绍页面(http://pvp.qq.com/web201605/herolist.shtml)，在这个页面列出了所有的英雄，然后打开 Chrome 开发者工具，刷新后在 Network 看到如下图请求 url，会返回包含所有英雄信息的 Json 串。

![](http://www.justdopython.com/assets/images/2020/05/heros/python-heros-01.png)

把这个 Json 文件下载下来，我们可以看到里面的内容如下：

![](http://www.justdopython.com/assets/images/2020/05/heros/python-heros-02.png)

然后当我们点击某个英雄进到详细介绍页面，会看到以这个英雄各种皮肤的图片，再次打这开发者工具，在源码里找到皮肤图片对应的 url，如下图所示：

![](http://www.justdopython.com/assets/images/2020/05/heros/python-heros-03.png)

通过查看多个皮肤，我们可以发现这个 url（http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/531/531-bigskin-2.jpg）是有规律的变化，可以看出 url 中数字`531`对应的就是上面 json 文件中的 `ename`，而其中 `531-bigskin-` 后面的数字，则对应的是第几个皮肤。

好了，找到了规律，剩下就好办了，因为这个用代码实现一点也不复杂。

## 代码实现

直接上代码吧，我已经在代码里加了注释如下：

```py
# get_heros.py
# 引入模块
import requests
import json
import os
import time

#程序开始时间
st = time.time()
url = 'http://pvp.qq.com/web201605/js/herolist.json'
# 获取 json 内容
response=requests.get(url).content

# 提取 Json 信息
jsonData=json.loads(response)
# 打印查看
print(jsonData)

# 初始化下载数量
x = 0

hero_dir='/Users/mm/python/python-examples/heros/imgs/'
#目录不存在则创建
if not os.path.exists(hero_dir):
     os.mkdir(hero_dir)

for m in range(len(jsonData)):
    # 英雄编号
    ename = jsonData[m]['ename']
    # 英雄名称
    cname = jsonData[m]['cname']
    # 皮肤名称，一般英雄会有多个皮肤
    skinName = jsonData[m]['skin_name'].split('|')
    # 皮肤数量
    skinNumber = len(skinName)

    # 循环遍历处理
    for bigskin in range(1,skinNumber+1):
        # 拼接下载图片url
        picUrl = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(ename)+'/'+str(ename)+'-bigskin-'+str(bigskin)+'.jpg'
        #获取图片内容
        picture = requests.get(picUrl).content
        # 保存图片
        with open( hero_dir + cname + "-" + skinName[bigskin-1]+'.jpg','wb') as f:
            f.write(picture)
            x=x+1
            print("当前下载第"+str(x)+"张皮肤")
# 获取结束时间
end = time.time()
# 计算执行时间
exec_time = end-st
print("找到并下载"+str(x)+"张图片,总共用时"+str(exec_time)+"秒。")
```

代码写好，接下我们执行命令 `python get_heros.py` 运行程序，就会看到皮肤图片已经瞬间下载到了电脑里。

![](http://www.justdopython.com/assets/images/2020/05/heros/python-heros-05.png)

下载完成的皮肤图片：

![](http://www.justdopython.com/assets/images/2020/05/heros/python-heros-06.png)

## 总结

本文为大家介绍了如何通过 Python 实现王者荣耀全英雄皮肤图片的下载，喜欢玩游戏的朋友们，以后再也不用愁没有图片做桌面壁纸了，如果你喜欢记得点`在看`。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/jiguang/heros>