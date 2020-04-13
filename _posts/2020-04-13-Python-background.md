---
layout: post     
title:  不到100行代码制作各种证件照                                   
category: 不到100行代码制作各种证件照        
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

## 不到100行代码制作各种证件照

生活中经常需要使用各种版本的电子版证件照，如：红底、蓝底、白底、一寸、两寸等等。在 Python 中替换图片背景色可以用 Image 模块，利用 Image 模块可以改变图片大小、背景色等操作。
<!--more-->
![](http://www.justdopython.com/assets/images/2020/background/result.png)

#### 人像分离

第一步将原图片中的人物与背景分离，我们使用百度 AI 开放平台中的人像分割功能,它的免费版有 50000次/天。使用百度的产品都知道需要一个 SK 和 AK。

![](http://www.justdopython.com/assets/images/2020/background/bdai.png)

```python
def get_access_token(self):
    """
    获取 access_token
    """
    # 注意 SK 与 AK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ak&client_secret=sk'
    response = requests.get(host)
    if response:
        return response.json()['access_token']

def get_foreground(self, originalImagePath, ):
    """
    人像分割
    """
    
    # 二进制方式打开图片文件
    f = open(originalImagePath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}

    # 请求 百度 AI 开放平台
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg?access_token=" + get_access_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": img}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        foreground = response.json()['foreground']
        img_data = base64.b64decode(foreground)
        # 人像图片存放地址
        foreground_path = 'foreground.png'
        with open(foreground_path, 'wb') as f:
            f.write(img_data)
```

结果示例

![](http://www.justdopython.com/assets/images/2020/background/foreground.png)

#### 创建背景图片

第二步将创建一个底色为红色、蓝色、白色的图片，它的大小为一寸（295px × 413px）和二寸（413px × 579px）。

```python
def get_background():
    """
    背景图片
    """
    color = ('red', 'blue', 'white')
    imgs = []
    for c in color:
        # 一寸照片大小
        img = Image.new("RGBA", (295, 413), c)
        imgs.append(img)
    return imgs
```

#### 合并图片

第三步将红蓝白背景图与人像图片合并，这里需要使用 Image 模块的 resize() 将人像图片裁剪到合适的像素，再使用 paste() 方法将图像合并。

```python
def main():
    fore = get_foreground('original.jpg')
    # 将图像裁剪到合适的像素
    p = fore.resize((330, 415))
    # 分离图片
    r,g,b,a = p.split()

    imgs = get_background()
    for img in imgs:
        # 将底色图像和人物图像合并，mask参数为去掉透明背景色
        img.paste(p, (-30, 50), mask = a)
        img.show()
```

结果示例

![](http://www.justdopython.com/assets/images/2020/background/effect.png)

### 结语

使用 Image 模块可以制作我们需要的各种电子版证件照，如果将背景图换成风景图我们就可以在朋友圈旅游了。

> 示例代码：[不到100行代码制作各种证件照](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/background)