---
layout: post
category: python
title: 2020 年 GitHub 上十大最火 Python 项目，看完之后我裂开了
tagline: by 豆豆
tags: 
  - python100
---

![封面](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/000.png)

GitHub 作为程序员每天必逛的网站之一，上面有着太多优秀的开源项目，今天派森酱就带大家来梳理下在过去的一年里，GitHub 上最火的 Python 项目 Top10。

<!--more-->

## 数据获取

如果你留心看过 GitHub 的文档的话，你就会知道关于 GitHub 上的大部分数据，GitHub 官方都是提供了接口了的。比如我们今天要获取的数据就可以从下面这个接口拿到。

```python
https://api.github.com/search/repositories?q=language:python+created:%3E2019-12-31&sort=stars&order=desc&per_page=10
```

如上所示，我们只获取语言为 Python 的开源项目，且创建时间晚于 2019-12-31，也就是 2020 年新创建的开源项目才做统计，接下来我们按照 stars 数倒序排序，取前十条记录就拿到我们需要的数据啦。

由于该接口返回的开源项目信息过于庞大，我们只取项目名称，URL，fork 数，star 数以及 watch 数。

```python
# 获取数据
def get_data():
    base_url = 'https://api.github.com/search/repositories?q=language:python+created:%3E2019-12-31&sort=stars&order=desc&per_page=10'
    response = requests.get(base_url)
    result = response.json()
    data = {}
    for item in result['items']:
        data[item['name']] = [item['html_url'], item['stargazers_count'], item['watchers_count'], item['forks']]
    return data
```

## 可视化

```python
# 可视化
def show_img():
    data = get_data()
    names = list(data.keys())
    values = [data[name][1] for name in names]

    bar = (
        Bar()
            .add_xaxis(names[::-1])
            .add_yaxis("星标数", values[::-1])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name_rotate=0, name="项目", axislabel_opts={'interval': -10, "rotate": 0}),
            title_opts=opts.TitleOpts(title="2020 GitHub Python TOP 10"))
    )
    bar.render_notebook()
```

将获取到的数据，按照 star 数从大到小生成柱状图，如下所示：

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/001.png)

## 00 Depix

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/002.png)

伴随着移动互联网的普及，我们的生活越来越便利，衣食住行一个手机全搞定，可手机在给我们带来便利的同时，也在威胁着我们的个人隐私安全。比如很多 App 动不动就要你实名认证，甚至人脸识别等。

以至于现在的我们都变得格外的小心翼翼，有时候发个朋友圈都要打马赛克，生怕泄漏一点点隐私。

可如果现在我告诉你，「打马赛克」已经不在安全了，你想要隐藏的信息，已犹如裸奔你会作何感想。

最近 GitHub 上出现了一个火的一塌糊涂的项目，它就是号称能抹去马赛克让原图重现的神器 Depix。截至目前，该项目的星标数已经超过 14K。

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/003.png)

上面是一个官方给出的示例图，我们可以看出使用 Depix 恢复后，基本上已经可以看清大部分内容了，太恐怖了。

## 01 diagrams

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/004.png)

作为程序员的我们可能平时画图比较少，顶多也就是写写文档。但画图可是架构师必备技能之一，熟话说不想当架构师的程序员不是合格的程序员，画图我们还是有必要学习一下的。

说到画图，你肯定想到的是各种在线离线工具等，你有试过用代码来画图吗？

没错，你没有听错，用代码来画图完全可行。利用 diagrams 库，我们就可以通过以代码的方式来绘制诸如阿里云、AWS、K8S 等系统架构图。

真正做到了图表即代码，代码即图表。

## 02 EasyOCR

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/005.png)

OCR （Optical Character Recognition）光学字符识别，即识别图像中的文字。

EasyOCR 就是一个识别图像中文字的库，且其是全语种的（目前涵盖 70+ 门语言，包括中文，日文，韩文，泰文）。

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/006.png)

## 03 avatarify

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/007.png)

变脸作为川剧的绝活之一，赢得了很多人的喜爱。

而 avatarify 则可以帮你在 ZOOM、skype 等视频会议软件中实现变脸，将名人的脸套在自己的脸上。想象一下，当同事和你视频会议室，你搞一个名人的脸来用是不是很酷呢。

## 04 PaddleOCR

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/008.png)

同样是一个款 OCR 识图库，拥有超过 8.1K+ 的星标， 但于 EasyOCR 一比，PaddleOCR 的则就显得相形见绌了。

## 05 eat_tensorflow2_in_30_days

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/009.png)

作为机器学习的必学技能 TensorFlow，其入门门槛并不低，尽管 TensorFlow2.0 宣称已经为改善用户体验做出了巨大的改进，但大家依然觉得用起来并不轻松。

而 eat_tensorflow2_in_30_days 这个项目则可以让你轻松入门 TensorFlow2.0。作为比比官方文档更容易入门的教程，其具有以下优点。

本教程按照内容难易程度、读者检索习惯和 TensorFlow 自身的层次结构设计内容，循序渐进，层次清晰，方便按照功能查找相应范例。

不同于官方文档冗长的范例代码，本教程在范例设计上尽可能简约化和结构化，增强范例易读性和通用性，大部分代码片段在实践中可即取即用。

可以看出作者是非常用心了，完完全全站在一个小白的身份角度去思考和写作的，非常适合小白跟着节奏一步步走向巅峰。

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/010.png)

## 06 GHunt

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/011.png)

这是一款可嗅探 Google 账户的 OSINT 工具，包括但不限于姓名，谷歌 ID，YouTube 频道以及其他谷歌服务等。

官方称 GHunt 可让安全团队浏览由 Google 账户创建的数据，甚至仅根据电子邮件来分析目标 Google 的轨迹。「白帽子和渗透测试人员」可以使用 GHunt 来测试所发现的电子邮件是否合理。

但我能想到的是我们的信息又要泄漏了，呃，我们的隐私保护起来怎么就那么费劲呢。

## 07 jd_seckill

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/012.png)

这是一个于 2020-12-11 创建的用于在京东抢茅台的 Python 脚本。

现如今抢茅台倒卖茅台已经发展成为一个完整的生意链条了，因为这其中蕴藏着巨大的利益。茅台出厂官方指导价是 1499 元，注意，这是厂家卖给经销商的价格，普通消费者是完全买不到的。

经销售转手之后的售卖价格在 2599 元左右，而且茅台作为中国白酒的 NO.1 根本不愁销售，可以说茅台的经销商是躺着赚钱了。

如今得益于互联网的发展，各大电商平台为了留住用户纷纷推出 1499 限量抢茅台的活动，基本上全是秒杀。因为抢到之后可以轻轻松松以 2000+ 的价格出手，大把人要，500+ 大洋到手。

于是就有了 jd_seckill 这个用于自动抢茅台的脚本，但由于不可抗力，现在已经删除了，太魔幻了。

## 08 yolov5

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/013.png)

这是一款目标检测神器，换言之就是要找出图片中物体的边界框，并判定框内物体的类别。比如识别图中的小汽车，猫咪等。我们都知道现在计算机视觉非常火，这就是计算机视觉领域的典型应用。

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/014.png)

## 09 Bringing-Old-Photos-Back-to-Life

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/015.png)

这是一个由微软发起的人工智能修复老照片的应用。它可以让破损、残旧的图片焕发新生，包括划痕修复，整体颜色复原和面部修复等过程，截至目前已获得 7.2K+ 的 star 数。

![](http://www.justdopython.com/assets/images/2021/01/GitHub-Python-Top10/016.png)

## 总结

今天和大家介绍了 2020 年 GitHub 上最火的十个 Python 项目，小伙伴们用过哪几个呢。

> 示例代码：https://github.com/JustDoPython/python-examples/tree/master/doudou/2021-01-02-GitHub-Python-Top10
