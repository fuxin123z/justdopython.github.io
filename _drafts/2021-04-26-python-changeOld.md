---
layout: post
category: python
title: Python 制作抖音播放量为 30W+ 的一起变老素材
tagline: by 某某白米饭
tags: 
  - python100
---

前几天小编在抖音上刷到一个慢慢变老的视频，播放量居然有 30W+，当时就在想这视频 Python 可不可以做？ 经过一番搜索，小编找到了腾讯云的人脸年龄变化 API，上面介绍说只要用户上传一张人脸图片，基于人脸编辑与生成算法，就可以输出一张人脸变老或变年轻的图片，并支持实现人脸不同年龄的变化。
<!--more-->
### 准备工作

#### 获取 API 秘钥

第一步，在注册账号之后，打开API密钥管理页面(https://console.cloud.tencent.com/cam/capi)获取到 SecretId 和 SecretKey。

![](http://www.justdopython.com/assets/images/2021/04/changeOld/0.png)

第二步，安装腾讯云的 SDK

```python
pip3 install tencentcloud-sdk-python
```

#### 人脸属性

在人脸年龄变化 API 中有一个 AgeInfo 参数，它包含了 Age 和 FaceRect 两个属性，其中 FaceRect 属性必须填人脸在照片中基于左上角的 X、Y 坐标和人脸的高度与宽度。所以先要调用人脸检测与分析 API 得到这些数据。

![](http://www.justdopython.com/assets/images/2021/04/changeOld/1.png)

下面的示例图是在百度图片中截取的。

![](http://www.justdopython.com/assets/images/2021/04/changeOld/2.png)

```python
import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client
from tencentcloud.iai.v20200303 import models as models03

sid = "xxx"
skey = "xxx"
try: 

    filepath = '/Users/imeng/Downloads/face/face.png'
    file = open(filepath, "rb")
    base64_data = base64.b64encode(file.read())

    cred = credential.Credential(sid, skey) 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "iai.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = iai_client.IaiClient(cred, "ap-beijing", clientProfile) 

    req = models03.DetectFaceAttributesRequest()
    params = {
        "MaxFaceNum":2,
        "Action":"DetectFace",
        "Version":"2018-03-01",
        "Image": base64_data.decode()
    }
    req.from_json_string(json.dumps(params))
    resp = client.DetectFaceAttributes(req) 

    faceDetailInfos = resp.FaceDetailInfos
    for faceDetailInfo in faceDetailInfos:
        faceRect = faceDetailInfo.FaceRect
        print(faceRect)
except TencentCloudSDKException as err: 
    print(err) 
```

示例结果

```python
{"X": 62, "Y": 13, "Width": 145, "Height": 230}
{"X": 426, "Y": 113, "Width": 115, "Height": 139}
```

### 修改年龄

在上面已经得到了各个人脸的X、Y、Width、Height 属性，加上变老的年龄 Age，就可以用 Post 请求年龄变化 API 了。

这里需要注意的是 models 模块，人脸检测 models 模块是在 tencentcloud.iai.v20200303 包下，人脸年龄变化的 models 是在 tencentcloud.ft.v20200304 下，两个 models 模块并不兼容。

```python
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ft.v20200304 import ft_client, models

cred = credential.Credential(sid, skey) 
httpProfile = HttpProfile()
httpProfile.endpoint = "ft.tencentcloudapi.com"
clientProfile.httpProfile = httpProfile
client = ft_client.FtClient(cred, "ap-beijing", clientProfile) 

req = models.ChangeAgePicRequest()

for age in range(70, 80):
params = {
    "Image": base64_data.decode(),
    "AgeInfos": [
        {
            "Age": age,
            "FaceRect": {
                "Y": faceDetailInfos[0].FaceRect.Y,
                "X": faceDetailInfos[0].FaceRect.X,
                "Width": faceDetailInfos[0].FaceRect.Width,
                "Height": faceDetailInfos[0].FaceRect.Height
            } 
        },
        {
            "Age": age,
            "FaceRect": {
                "Y": faceDetailInfos[1].FaceRect.Y,
                "X": faceDetailInfos[1].FaceRect.X,
                "Width": faceDetailInfos[1].FaceRect.Width,
                "Height": faceDetailInfos[1].FaceRect.Height
            } 
        }
    ],
    "RspImgType": "base64"
}
req.from_json_string(json.dumps(params))
resp = client.ChangeAgePic(req) 
image_base64 = resp.ResultImage
image_data = base64.b64decode(image_base64)
file_path = '/Users/imeng/Downloads/face/{}.png'.format(age)
with open(file_path, 'wb') as f:
    f.write(image_data)
time.sleep(1)

```

示例结果

![](http://www.justdopython.com/assets/images/2021/04/changeOld/3.png)

最后的视频可以将图片一张一张插入 PPT 幻灯片，点击保存为视频。

### 总结

用 Python 制作抖音素材，下一个 30W+ 播放量等着你。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/changeOld/changeOld.py>
