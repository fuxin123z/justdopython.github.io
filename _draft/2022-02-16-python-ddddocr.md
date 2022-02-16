---
layout: post
title: 带带弟弟 ocr 对各种类型验证码说不
category: python
tagline: by 某某白米饭
tags: 
  - python
  - 验证码
  - 爬虫
---

![封面](https://files.mdnice.com/user/15960/fa55c532-d45f-4069-93c5-659a0417c7dd.png)

在使用爬虫登录网站的时候，经常输入用户名和密码后会遇到验证码，简单一点的有字母验证码，复杂一点的有滑块验证码，点选文章和点选图片验证码。这些都是爬虫中的老大难问题，今天介绍一款通用验证码识别 SDK 对他们彻底说拜拜，它的名字是 ddddocr 带带弟弟 OCR 通用验证码识别 SDK 免费开源版。
<!--more-->
![](https://files.mdnice.com/user/15960/a047e1b6-3509-4533-b254-1fc2f520a87f.png)

#### 安装

将自动安装符合自己电脑环境的最新 ddddocr。Python 环境需要小于等于 3.9。

```python
pip install ddddocr
```

### 使用

带带弟弟 OCR 可以识别三种验证码，小编就用这三种来实验一下。

#### 滑块验证码

滑块验证码这里用的是豆瓣的滑块验证。下滑块是单独的透明背景图 hycdn.png。

![hycdn.png](https://files.mdnice.com/user/15960/4f778147-382f-48d9-b725-9a1f68a636db.png)


背景图是带小滑块坑位的 background.jpg。

![background.jpg](https://files.mdnice.com/user/15960/22427f5b-4207-463f-a49a-cc798ad6310d.jpg)


```python
import ddddocr

det = ddddocr.DdddOcr(det=False, ocr=False)

with open('hycdn.png', 'rb') as f:
        target_bytes = f.read()
    
with open('background.jpg', 'rb') as f:
    background_bytes = f.read()

res = det.slide_match(target_bytes, background_bytes, simple_target=True)

print(res)
```

识别结果

```python
{'target_y': 0, 'target': [486, 126, 622, 262]}
```

target 属性的前两个值正好和豆瓣验证滑块 url 中提交的 ans 差不多。

![](https://files.mdnice.com/user/15960/4debbb84-7092-41b2-82a3-f4db8bae5528.png)

#### 点选类验证码

点选类验证码用的是网易登录

![eb.jpg](https://files.mdnice.com/user/15960/5c6bd24c-c702-458e-a9b6-192c90ca6464.png)


```python
det = ddddocr.DdddOcr(det=True)

    with open("eb.jpg", 'rb') as f:
        image = f.read()

    poses = det.detection(image)

    im = cv2.imread("eb.jpg")

    for box in poses:
        x1, y1, x2, y2 = box
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

    cv2.imwrite("result.jpg", im)
```

识别结果

![](https://files.mdnice.com/user/15960/8b237e9d-23ce-492a-9cf4-acd064807600.png)


#### 字母数字验证码

字母数字验证码的图片来自于 google 搜索

![](https://files.mdnice.com/user/15960/d746df99-6ee6-42b0-bade-d0afdbb68362.png)

```python
ocr = ddddocr.DdddOcr(old=True)

with open("z1.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)
```

识别结果

```
3n3d
8342
```

### 总结

ddddocr 让验证码变得如此简单与易用，,让不会用 opencv, pytorch, tensorflow 的小伙伴也能快速的破解网站的登录验证码。小伙伴们如果有其他好的 ocr 识别也可以在留言中分享出来。
