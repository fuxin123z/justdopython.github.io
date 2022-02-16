---
layout: post
title: 情人节，25 行代码生成微信朋友圈的爱心九宫格。
category: python
tagline: by 某某白米饭
tags: 
  - python
---

![封面](https://files.mdnice.com/user/15960/0c3fdffc-fb69-4972-b6c9-418e4116ab1c.png)
情人节到了，小伙伴们给女朋友买礼物了吗？都有在朋友圈发亿点点狗粮吗？今天小编就教大家在朋友圈发爱心九宫格图片，让女朋友心情更美丽并且有求必应。

<!--more-->

上成品图：

![](https://files.mdnice.com/user/15960/c4b13815-94af-4c98-ac21-29ed5a1895f4.png)


### 上代码

朋友圈可以发 3 * 3 的 9 张图，把每一个小图分解成为 3 * 3 的小图编号为 (1-9)，红色部分就是需要用爱心覆盖的地方。

![](https://files.mdnice.com/user/15960/24d167e9-b8aa-46ea-809b-9dae7b61233c.png)


每一个小方格的长宽都是爱心的长框，将爱心的图像用 python 代码修改为正方形，长宽都为：w，那么：

* 1 号的起始坐标为: (0, 0)
* 2 号的起始坐标为：(w，0)
* 3 号的起始坐标为：(2 * w，0)
* 4 号的起始坐标为: (0, w)
* 5 号的起始坐标为：(w，w)
* 6 号的起始坐标为：(2 * w，w)
* 7 号的起始坐标为：(0, 2 * w)
* 8 号的起始坐标为：(w，2 * w)
* 9 号的起始坐标为：(2 * w，2 * w)

将爱心图片设置长宽都相同：

```python
from PIL import Image

xin_img = Image.open('xinxin.png')
w,y = xin_img.size
xin = xin_img.resize((w, w),Image.BILINEAR)
```

将爱心图片四周加上 15 像素的白色边框，这样可以看起来不紧凑。

```python
border = 15
img_new = Image.new('RGB', (w + 2 * border, w + 2 * border), (255,255,255))
img_new.paste(xin, (border, border), xin)
xin = img_new.convert('RGBA')
w, y = xin.size
```

![黑色是透明背景](https://files.mdnice.com/user/15960/6bb1b414-4f30-4825-9986-fbf35560bb90.PNG)


points 就是每个小图的起始坐标列表，imgs 就是爱心小图的位置。

```python
points = [(0, 0), (w, 0), (2 * w, 0), (0, w),(w,w),(2 * w,w),(0, 2 * w),(w,2 * w),(2 * w,2 * w)]

imgs = [(6,8,9), (4,6,7,8,9), (4,7,8), (1,2,3,4,5,6,8,9), (1,2,3,4,5,6,7,8,9), (1,2,3,4,5,6,7,8), (3,-1), (1,2,3,4,5,6,8), (1,-1)]
```

先创建 3 * 3 的白色 (255,255,255) 背景图，然后调用 pil 的 paste() 方法将爱心图像往背景图上面粘贴。

```python
file_name = 0

for img in imgs:
    bgimg = Image.new("RGB",(w * 3,w * 3), (255,255,255))
    for item in img:
        if(item == -1):
            continue
        bgimg.paste(xin, points[item - 1], xin)

    file_name = file_name + 1
    bgimg.save(f"{file_name}.png")
    
```

![](https://files.mdnice.com/user/15960/9993b7bf-d23e-4c30-b9f1-0b8f95fab2e7.png)


最后在发朋友圈的时候将 5.png 替换为女朋友的头像。

### 总结

虽然情人节过去了，但是将这九宫格照片往微信朋友发准没错。
