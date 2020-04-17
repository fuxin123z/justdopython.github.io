---
layout: post
title: 想知道未来孩子长相？Python人脸融合告诉你
category: python
tagline: by 闲欢
tags: 
  - python
---

![](http://www.justdopython.com/assets/images/2020/facemerge/titlepic.png)

和换脸算法的简单粗暴相比，人脸融合算法就要弹性的多。顾名思义，人脸融合是对两张人脸进行融合处理，生成的人脸同时具备两张人脸的外貌特征。人脸融合有什么实际意义呢？一个简单的应用就是用父母双方的脸部图片融合，得到未来孩子可能的长相。

本文通过百度AI开放平台的人脸融合功能来做一个简单的试验。
<!--more-->

## 前期准备


### 账号注册

我们要使用百度AI开发平台的功能，必须先注册一个账号。访问 https://login.bce.baidu.com/ ，然后用你的百度账号登录就行。

![](http://www.justdopython.com/assets/images/2020/facemerge/login.png)

登录之后，在左边的菜单栏依次选择“产品服务 -> 人工智能 -> 人脸识别”子菜单，进入到人脸识别的产品界面:

![](http://www.justdopython.com/assets/images/2020/facemerge/menu.png)

然后点击“创建应用”，填写“应用名称”和“应用描述”即可创建应用:

![](http://www.justdopython.com/assets/images/2020/facemerge/createapp.png)

然后返回应用列表，就可以看到你创建的应用:

![](http://www.justdopython.com/assets/images/2020/facemerge/applist.png)

创建完应用，你需要将 API Key 和 Secret Key 记下来，我们待会的代码里面会用到。

### 阅读开发文档

应用创建完后，我们需要知道怎么调用百度的API来完成我们的试验，所以我们需要阅读官方文档。我们需要做两件事情：鉴权认证和图片融合。

#### 鉴权认证文档

如果要调用百度的 API 接口，必须先鉴权认证，也就是获取应用 token 。获取 token 的文档地址为：https://ai.baidu.com/ai-doc/FACE/5k37c1ti0。

文档中对我们有用的几处信息如下：

请求URL数据格式：

向授权服务地址https://aip.baidubce.com/oauth/2.0/token发送请求（推荐使用POST），并在URL中带上以下参数：
- grant_type： 必须参数，固定为client_credentials；
- client_id： 必须参数，应用的API Key；   
- client_secret： 必须参数，应用的Secret Key；

请求举例：
```
https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Va5yQRHlA4Fq5eR3LT0vuXV4&client_secret=0rDSjzQ20XUj5itV6WRtznPQSzr5pVw2&
```

服务器返回的JSON文本参数如下：
- access_token： 要获取的Access Token；
- expires_in： Access Token的有效期(秒为单位，一般为1个月)；   
- 其他参数忽略，暂时不用;

返回举例：

```
{
  "refresh_token": "25.b55fe1d287227ca97aab219bb249b8ab.315360000.1798284651.282335-8574074",
  "expires_in": 2592000,
  "scope": "public wise_adapt",
  "session_key": "9mzdDZXu3dENdFZQurfg0Vz8slgSgvvOAUebNFzyzcpQ5EnbxbF+hfG9DQkpUVQdh4p6HbQcAiz5RmuBAja1JJGgIdJI",
  "access_token": "24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",
  "session_secret": "dfac94a3489fe9fca7c3221cbf7525ff"
}
```

#### 图片融合文档

图片融合文档的地址为：https://ai.baidu.com/ai-doc/FACE/5k37c1ti0。

文档中对我们有用的几处信息如下：

请求注意事项：
- 请求体格式化：Content-Type为application/json，通过json格式化请求体。   
- Base64编码：请求的图片需经过Base64编码，图片的base64编码指将图片数据编码成一串字符串，使用该字符串代替图像地址。您可以首先得到图片的二进制，然后用Base64格式编码即可。需要注意的是，图片的base64编码是不包含图片头的，如data:image/jpg;base64。   
- 图片格式：现支持PNG、JPG、JPEG、BMP，不支持GIF图片。

请求示例：

- HTTP方法：POST
- 请求URL： https://aip.baidubce.com/rest/2.0/face/v1/merge
- URL参数：access_token
- Header：Content-Type  为application/json
- Body中放置请求参数

返回示例：

```
{    
    "error_code": 0,  
    "error_msg": "SUCCESS",     
    "log_id": 1234567890123,     
    "timestamp": 1533094576,     
    "cached": 0,     
    "result": {         
        "merge_image": "iVBORw0KGgoAAAANSUhEUgAAAeoAAAHqCAYAAADLb..."    
        }  
}  
```

## 编码

### 获取 token

根据上面的文档描述，我们调用鉴权接口的方法如下：

```
# 获取token
def get_token(client_id, client_secret):
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"
    params = {"client_id": client_id, "client_secret": client_secret}
    res = requests.get(url, params=params)
    result = res.json()
    return result['access_token']
```
这个接口很简单，我们传入我们应用的信息就可以直接获得。

### 获取图片的 base64 编码

我们调用百度人脸融合接口，需要传入图片的 base64 编码，所以我们先要将图片转为 base64 格式，转换方法如下：

```
# 读取图片，转换成base64
def read_pic(name):
    with open('./%s' % name, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s
```

我将图片放在程序同级目录下，方法传入图片文件名就可以。

### 调用人脸融合接口并保存结果

token 值和图片的 base64 编码准备好了，我们就可以来调用接口进行融合。根据官方的 API 文档，我们的调用方法如下：

```
# 融合图片
def merge(token, template, target):
    url = 'https://aip.baidubce.com/rest/2.0/face/v1/merge'
    request_url = url + '?access_token=' + token
    params = {
        "image_template": {
            "image": template,
            "image_type": "BASE64",
            "quality_control": "NORMAL"
        },
        "image_target": {
            "image": target,
            "image_type": "BASE64",
            "quality_control": "NORMAL"
        },
        "merge_degree": "HIGH"
    }
    params = json.dumps(params)
    headers = {'content-type': 'application/json'}
    result = requests.post(request_url, data=params, headers=headers).json()
    if result['error_code'] == 0:
        res = result["result"]["merge_image"]
        down_pic(res)
    else:
        print(str(result['error_code'])+result['error_msg'])
```

参数中的 template 指的是模板图片，target 指的是被融合图片。也就是说将 target 图片的人脸融合到 template 图片的人脸中，最后输出的图片是以 template 图片为模板的。

这里有一个将接口返回的图片转存到本地的方法 down_pic ，其实现如下：

```
# 下载图片
def down_pic(data):
    imagedata = base64.b64decode(data)
    file = open('./result.jpg', "wb")
    file.write(imagedata)
```

我们把融合的图片命名为 result.jpg ，存储在程序同级目录下。


### 主程序

主要的方法我们都完成了，下面我们通过编写主程序来测试我们的融合效果，代码如下：

```
if __name__ == '__main__':
    girl = read_pic('girl.jpg')
    boy = read_pic('boy.jpg')
    token = get_token(API_KEY, SECRET_KEY)
    merge(token, boy, girl)
```

我这里用一个男人的图片和一个女人的图片来做测试，以男人的图片作为模板，两张图片都是从百度图片搜索出来的。

男人的人脸图片为：

![](http://www.justdopython.com/assets/images/2020/facemerge/boy.jpg)

女人的人脸图片为：

![](http://www.justdopython.com/assets/images/2020/facemerge/girl.jpg)

融合后的人脸图片为：

![](http://www.justdopython.com/assets/images/2020/facemerge/man.jpg)

是不是很帅气，这个可能是这两个人未来儿子的模样。接着，我们调换一下模板，我们以女人的图片作为模板，看看他们未来女儿的模样，结果如下：

![](http://www.justdopython.com/assets/images/2020/facemerge/woman.jpg)

## 总结

本文通过调用百度AI开放平台的人脸融合接口，来实现两张正面人脸图片的融合试验。大家觉得融合的效果怎么样？我觉得如果这两个人结婚，生男孩子会好看些呢！大家也可以把自己和另一半的自拍照拿来试验一下，看看未来孩子长啥样？当然，如果你是单身狗，那可以找个漂亮明星图片来幻想一下。

> 示例代码：[](https://github.com/JustDoPython/python-examples/tree/master/xianhuan/facemerge)



