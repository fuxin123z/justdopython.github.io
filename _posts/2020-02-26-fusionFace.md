---
layout: post     
title:  小游戏：换脸术                                             
category: 小游戏：换脸术         
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

## 小游戏：换脸术

最近估计大家都陆陆续续的复工了，大家经常在节后会得一个叫做节后综合征的病，具体表现为：提不起精神、上班效率低、没精神，严重的还会出现恶心、焦虑、神经衰落等等。这里给大家带来一个小游戏娱乐一下，放松上班焦虑心情，叫做"换脸术"，把自拍照变成沙雕图片。这时需要准备一张沙雕图片作为模板和一张为自拍照，自拍照脸部将替换沙雕图上的脸部。

![](http://www.justdopython.com/assets/images/2020/02/26/FusionFace/target.png)

#### 思路与代码

这个小游戏整体思路包含了以下几个部分：

第一步：自拍照

这里使用到了 Python 的 opencv 模块，调用摄像头并拍照，使用 pip 安装一下

```python
pip install opencv-contrib-python
```

安装完毕之后，将使用 opencv 模块调用摄像头拍照

```python
import cv2

def getPhoto():
    '''
    调用摄像头拍摄照片
    :return: 照片路径
    '''
    print("准备拍摄照片，请保持颜值在线...")
    photoSrc = '自拍照路径'
    cap = cv2.VideoCapture(0)
    while (1):
        ret, frame = cap.read()
        # 显示图像
        cv2.imshow("photo", frame)
        # 按 q 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(photoSrc, frame)
            print("照片已经拍摄完成！")
            break
    cap.release()
    cv2.destroyAllWindows()
    return photoSrc
```

运行程序时出现如下错误：
```
qt.qpa.plugin: Could not find the Qt platform plugin "cocoa" in ""
```
还需要安装 opencv-python-headless 模块

```python
pip install opencv-python-headless
```

第二步：将自拍照和沙雕图片变成 base64 格式的字符串

```python
def image2base64(image_path):
    '''
    图片转base64
    :param image_path: 图片地址
    :return: base64
    '''
    with open(image_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s

```

第三步利用百度 ai 开放平台上传 base64 格式字符串

在这一步中需要用到百度 ai 开放平台，需要登录百度 ai 开放平台并创建应用得到 Api Key 和 Secret Key 请求得到一个 access_token，此 access_token 在 30天后失效需要重新请求

![](http://www.justdopython.com/assets/images/2020/02/26/FusionFace/list.png)

```python
def getAccessToken():
    '''
    获取百度 ai 开放平台的 access_token
    :return: access_token
    '''
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + ak + '&client_secret=' + sk
    response = requests.get(host)
    if response:
        print(response.json())
        return response.json()['access_token']
```

最后将沙雕图的 base64 格式字符串和你的照片 base64 格式字符串加上 access_token 请求百度开放 API，返回得到融合人脸后的 base64 字符串

```python
def faceFusion(templateBase64, targetBase64, access_token):
    '''
    换脸术
    :param templateBase64: 模板图片
    :param targetBase64: 目标图片
    :param access_token: access_token
    :return: 换脸后的 base64
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/face/v1/merge"

    params = "{\"image_template\":{\"image\":\"" + templateBase64 + "\",\"image_type\":\"BASE64\",\"quality_control\":\"NONE\"},\"image_target\":{\"image\":\"" + targetBase64 + "\",\"image_type\":\"BASE64\",\"quality_control\":\"NONE\"}}"

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())
    return response.json()['result']['merge_image']
```

参数介绍

image_template：模板照片
image_target：目标照片
image：图片的 base64 字符串
image_type：照片类型，有URL，base64，FACE_TOKEN人脸标识
quality_control：照片质量控制，有 NONE 不控制，LOW 低质量，NORMAL一般质量，HIGH 高质量


第四步通过百度开放平台返回的 base64 格式逆向生成图片

```python
def base642image(base64str):
    '''
    base64转图片
    :param base64str: base64
    '''
    imgdata = base64.b64decode(base64str)
    with open('换脸后照片路径', 'wb') as f:
        f.write(imgdata)
    print('successful')
```

### 总结

本文主要使用 opencv 模块调用摄像头并拍摄和使用百度 ai 开放平台，这些功能只是其中的一小块，大家如果感兴趣可以试试其他有趣的功能。

> 示例代码：[小游戏：换脸术](https://github.com/JustDoPython/python-100-day/tree/master/FusionFace)