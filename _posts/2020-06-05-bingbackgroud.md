---
layout: post
category: python
title: 美图太多，Python 帮你挑选最合适的
tagline: by 太阳雪
tags:
  - python100
---

前几天，極光同学写了篇下载王者荣耀皮肤的文章，可以轻松的获取各种英雄背景图，甚是激动，也想将桌面背景换成漂亮的，不过我对王者荣耀不感冒（曝露年龄啦），时常会被必应搜索主页的背景图所震撼，于是想到从必应获取桌面壁纸，并且排除掉自己不喜欢的图片，应该是个不错的主意，说干就干
<!--more-->

## 问题分析

必应每天都会有新的壁纸，大都是自然风光、人文地理等等，非常漂亮，在页面上点击右键，保存背景图片，就能简单的保存下来。但是总是这么干，不是个好办法，最好能自动化。

自动化中，图片下载很简单，只要找到背景图片链接，下载保存即可。

但并非所有的图片都合乎自己的口味，怎么才能只选自己喜欢的图片呢？于是想到用图像识别，再加对识别结果的判断，从而得到是否合适的判断

经过分析，大概的处理流程是：先下载图片，进行图像识别，对得到的结果进行分析，对于合乎要求的，保存到桌面背景文件中。

重点是图像识别和结果判断，先从核心问题开始。

## 图像识别

图像识别属于机器学习或者人工智能的部分，需要相应的算法和资料库来训练识别模式，是个比较繁杂的工作，好在各大云服务商都提供了图像识别接口，可以轻松做到。最终选用百度的综合图像识别 API 来处理

### 申请服务

需要先创建帐号，然后选择服务，购买服务，购买服务是免费的，使用到一定频率是需要收费的，对于目前场景来说，免费的完全够用
购买服务后，可以用服务创建一个项目，随便写些项目信息，创建好后，就能得到 App `key` 和 `Secret`，即调用服务的凭证，需要妥善保管

### 编写接口

调用识别 API 之前需要先得到 `accessToken`，获取代码如下：

```python
import httpx

def getAccessToken():
    clientId = '<换成你的 clientid>'
    clientSecret = '<换成你的 clientsecret>'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (clientId, clientSecret)
    response = httpx.get(host)
    if response.status_code == 200:
        ret = response.json()
        return ret.get('access_token')
    else:
        raise "获取AccessToken失败:" + str(response.status_code)
```

- 引入 httpx，一个与 requests 类似的库
- 获取 `accesstoken` 请求结果是 json，直接调用 Response 对象的 json 方法将结果转为 Dict 对象
- 从结果中获取 `access_token` 并返回
- 如果出现请求错误，返回错误码

> `accessToken` 的默认有效期为 30 天，所以没必要每次请求都获取，所以最好将 `accessToken` 缓存起来，不必每次调用都获取，鉴于当前的业务场景，每天查下一次，就没必要缓存了，如果有兴趣可以自己实践下

有了 `accessToken` 就可以编写图像识别了，代码如下：

```python
import base64
import httpx

def imageRecognition(image):
    img = base64.b64encode(image)
    params = {"image":img}
    access_token = getAccessToken()
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = httpx.post(request_url, data=params, headers=headers)
    if response.status_code == 200:
        return response.json().get("result")
    else:
        raise "获取AccessToken失败:" + str(response.status_code)
```

- 接收一个图片参数，因为图片是从网站上下载的，所以参数类型为二定制数据
- 由于图像识别接口需要需要上传图片，必须是 base64 格式，所以将图片数据转换为 base64 数据格式
- 在得到的结果中，提取 result 并返回

result 是 JSON 数据，结构如下:

```js
[{
  'score': 0.819942,
  'root': '自然风景-天空',
  'keyword': '天空'
}, {
  'score': 0.64795,
  'root': '自然风景-海洋',
  'keyword': '海洋'
}, {
  'score': 0.475835,
  'root': '非自然图像-图像素材',
  'keyword': '风景矢量图'
}, {
  'score': 0.265258,
  'root': '非自然图像-图像素材',
  'keyword': '雪花背景'
}, {
  'score': 0.08247,
  'root': '非自然图像-图像素材',
  'keyword': '气泡'
}]
```

- score 为得分，表示百分比，就是识别程度，比如 0.82 表示确认度为 82%
- root 为识别分类
- keyword 为识别关键字，即对图像元素中识别定义

## 图像判别

得到了图像识别结果，如何从结果中得到是否符合要求呢？经过探索和实践，用以下方法来解决：

先将自己喜欢的图像整体识别一次，获取到得分为 0.5 以上的关键字，组成一个数组（这个过程相当于机器学习），去重后，得到一下特征描述:

```python
keywords = ['植物', '树', '天空', '阳光','霞光', '晚霞', '海洋', '大海', '森林', '湖泊', '草原', '沙漠', '高山', '瀑布']
```

然后，需要一个计算公式对图片做整体打分，设置一个分值作为判定条件，就可以挑选出符合自己胃口的图片了，算法如下：

```python
import difflib

score = 0
for r in result:
    # 进行对比
    for k in keywords:
        root = r.get('keyword', '')
        ratio = difflib.SequenceMatcher(None, root, k).ratio()
        mscore = r.get('score')
        score += mscore*ratio
```

部分识别过程如下，标记了的是得分项:

![识别过程](http://www.justdopython.com/assets/images/2020/06/bingbackground/01.png)

主要过程是，从结果中提取 keyword，和每个自己喜欢的描述去比较，得到一个相似度，然后与识别得分相乘，得到一个特征相对于一个关键描述的得分，将所有特征的分值相加，就得到了这个图像的整体得分，从而得到判断依据

这里的关键是如何比较两个描述的相似程度，相似程度并非是否相等，相似程度是一个 0 ~ 1 之间的数，用 Python 自带 difflib 模块 SequenceMatcher 来解决

SequenceMatcher 有三个参数，第一个参数是一个 lambda 表达式，可以理解成一个简写的回调函数，作用是排除掉不需要对比的字符串，例如排除掉空格的写法为`x:x==' '`，不用排除的话，传入 None

通过对测试图片的对比，符合胃口的图片综合得分值在 0.8 到 9.9 之间，分值越大，表示有多个元素符合要求，为了照顾图片识别的失误，以及数值化过程中的误差，将判断值设定为 0.5, 也就是综合评分大于等于 0.5 的就认为是自己喜欢的，当然这只是个经验值，可以根据自己的经验调整

如果符合要求，就对图片进行保存，代码如下:

```python
with open(r"C:\Users\alisx\Pictures\Saved Pictures\bing_%s.jpg" % datetime.date.today(), 'wb') as f:
    f.write(image)
```

## 图像获取

解决了图像识别问题，获取图像就是小菜一碟，直接上代码：

```python
def grabImage(file=None):
    if file:
        image = Image.open(file)
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG')
        return output_buffer.getvalue()
    else:
        rsp = httpx.get("https://cn.bing.com/")
        bs = BS(rsp.content, "html.parser")
        bglink = bs.find("link").get("href")
        url = str(rsp.url) + bglink
        image = httpx.get(url).content
        return image
```

- 参数 file，是为了测试方便，测试是提供本地图像的路径，grabImage 方法会将其转换为二定制数据，以到达抓取图片的效果
- 当不提供 file 参数时，会从必应中获取，通过解析页面数据，获取背景图片的 url
- 将图片通过 httpx 下载后，返回图片的二进制数据

这里并没有将图片存储到硬盘上，因为获取到的图片需要经过判定，只有符合要求的才会被保存，不符合要求的直接丢弃掉

## 识别效率

通过上面的过程就可以获得自己喜欢的背景图片了，但背景图片一般比较大，可能会导致识别效率较低，所以需要将图片处理下，以提高上传和识别效率

经过测试，将图片设置为原来图片的一半比较合适，所以在下载到图片后，需要对图片进行加工处理，代码如下：

```python
from PIL import Image
# 压缩图片
img = Image.open(io.BytesIO(image))
x, y = img.size
x_s = round(x/2)
y_s = int(y * x_s / x)
out = img.resize((x_s, y_s), Image.ANTIALIAS)

# 图片转码
output_buffer = io.BytesIO()
out.save(output_buffer, format='JPEG')
byte_data = output_buffer.getvalue()
```

- 下载的图片是二进制数据，所以将其转换为 IO 序列，使之可以像文件一样打开
- 打开得到 image 对象后，获取图片高度 (y) 和宽度 (x)
- 计算出宽度的一半，并且计算出等比例的高度
- 最后用 resize 方法对图像进行压缩
- 压缩完后得到新的 image 对象，再将内容转换为 IO 序列，最后获得图片的二进制码

经过转换后，再调用图像识别接口，会快很多

这个压缩过程比较简单，如果更精细一些，可以对图像的大小进行判断，对于不同大小的图像做不同的处理，不过在此场景下，作为背景的图像都差不多，所以采用固定的处理方式

## 总结

今天的实践虽然很小，但涉及到爬虫、图像识别、机器学习（虽然只是手工过程）、图像评价等，将很多单独的技术组合起来，就能解决个性化图像筛选问题，就像 SpaceX 一样，每个技术都不是业内顶尖的，但合理的组合，就能发挥更大的价值。文章中为了符合思维习惯，对代码做了解构，代码示例中有完整的代码，欢迎参考研究，有问题欢迎加入微信群进行交流，支持作者，请点`在看`

## 参考

- [https://www.cnblogs.com/li1992/p/10675769.html](https://www.cnblogs.com/li1992/p/10675769.html)
- [https://www.jianshu.com/p/2ff8e6f98257](https://www.jianshu.com/p/2ff8e6f98257)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/background>
