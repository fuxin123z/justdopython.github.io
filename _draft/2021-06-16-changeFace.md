---
layout: post
title: 女友电脑私存思聪帅照，我用python偷梁换柱...
category: python
tagline: by 闲欢
tags: 
  - python
  - 照片
---

今天晚上，女朋友说电脑比较卡，让我帮她清理一下。作为她眼中的炒鸡技术男，我答应等她洗完澡出来就给她搞定。

解决电脑卡顿问题，无非就是扫一下毒，看看有没有自动运行的病毒，或者清理一下缓存和磁盘碎片，亦或者看看 C 盘剩余容量大小之类的。

我三下五除二就搞定了，但是在清理 C 盘文件时，我发现她的某个文件夹下面有好多照片，打开一看，我惊呆了，这不就是最近比较火的“撕葱”吗？

不光如此，图片还是以“老公1”、“老公2”等等的顺序命名的，居然暗地里做撕葱的小迷妹，还称呼“老公”！

虽然我从小吃鱼卡刺，喝了不少醋，但是看到这个比以往任何时候喝的醋都多。

![图片来源于网络](http://www.justdopython.com/assets/images/2021/06/changeFace/1.jpg)

老公？我突然灵机一动，我要丑化这些图片，让她下次打开时气得删掉它们，嘻嘻！

我打开 Photoshop ，想着用 PS 的方法替换头像。转念一想，不行，女朋友洗澡时间有限，一张张处理太耗时了，我得想个批量处理的办法。

突然想起来了以前做过类似的事情，借助人脸识别接口 API 可以搞定。

时间有限，废话不多说，赶紧撸起袖子加油干！


<!--more-->

### 寻找目标

我打算用人脸融合的方式来丑化图片，所以我先要找到一张比较丑的人脸照片。不知道为什么，第一反应是去搜黄渤黄老师的，对不住了！

![图片来源于网络](http://www.justdopython.com/assets/images/2021/06/changeFace/2.jpg)

我去百度上随手搜了一张，长这样：

![图片来源于网络](http://www.justdopython.com/assets/images/2021/06/changeFace/3.jpg)

### 人脸识别 API

我这里使用的是 Face++（旷视科技）的人工智能平台 API 接口，据说他们家比较专业，这一块做得比较好，想着还是要支持一下。

他们家的网站是：

> https://console.faceplusplus.com.cn/

首先需要注册一下，注册完了之后进入首页的“应用管理”功能，创建一个应用，然后就可以获取到一个 `API Key` 和 `API Secret`，这两个东西非常有用，基本上你使用他们家的接口都需要。

我们要实现两张图片的人脸融合，首先需要识别两张图片中的人脸，然后才能进行融合。

所以我们首先需要使用人脸识别功能里面的人脸检测 API ，文档说明：

> https://console.faceplusplus.com.cn/documents/4888373

这里有详细的 API 调用方法，参数和返回也都有列出，按照文档的方式使用即可。

检测到人脸之后，我们就可以进行融合了，这时需要使用另一个 API 接口，文档说明：

> https://console.faceplusplus.com.cn/documents/20813963


### 代码实现

根据上面的思路，我们可以先处理两张图片的人脸融合，代码如下：

```python

import base64
import requests
import json
import simplejson

# 第一步，获取人脸关键点
api_key = '你的apikey'
api_secret = '你的apisecret'

def find_face(imgpath):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": api_key,
            "api_secret": api_secret,
            "image_url": imgpath,
            "return_landmark": 1  # 是否检测并返回人脸关键点
            }
    files = {"image_file": open(imgpath, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = json.JSONDecoder().decode(req_con)
    this_json = simplejson.dumps(req_dict)
    this_json2 = simplejson.loads(this_json)
    faces = this_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    return rectangle

# 第二步，换脸
# number表示换脸的相似度
def merge_face(image_url1, image_url2, image_url, number):
    ff1 = find_face(image_url1)
    ff2 = find_face(image_url2)

    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])

    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    f1 = open(image_url1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_url2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    data = {"api_key": api_key,
            "api_secret": api_secret,
            "template_base64": f1_64,
            "template_rectangle": rectangle1,
            "merge_base64": f2_64,
            "merge_rectangle": rectangle2,
            "merge_rate": number
            }
    response = requests.post(url_add, data=data)
    req_con1 = response.content.decode('utf-8')
    req_dict = json.JSONDecoder().decode(req_con1)
    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()

# 思聪图
image1 = r"C:\Users\xx\Downloads\tmp\pic/2.jpg"
# 黄渤图
image2 = r"C:\Users\xx\Downloads\tmp\pic/3.jpg"
# 结果图
image = r"C:\Users\xx\Downloads\tmp\pic/n.jpg"

merge_face(image1, image2, image, 90)

```

我用的思聪的图片是这样子的：

![图片来源于网络](http://www.justdopython.com/assets/images/2021/06/changeFace/4.jpg)

运行程序，融合后的图像是这样的：

![图片来源于网络](http://www.justdopython.com/assets/images/2021/06/changeFace/5.jpg)

以上是针对一张图片的处理，批量处理，只需要扫描目录下的图片，然后针对每一张进行处理即可。

### 后记

我在批量处理的时候，加了一个步骤就是删除原来的图片，使得目录下的图片全部变得不可描述。

女朋友刚洗完澡，我差不多收工。她还夸我真棒，电脑速度有明显的提升。

不知道哪天她偷偷打开那个神秘的文件夹，双击图片，看到呈现出来的图片时，会是什么反应？我心里有点迫不及待的期待，嘿嘿！



> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/changeFace)