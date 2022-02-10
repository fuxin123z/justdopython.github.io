---
layout: post
title: 20 行代码，微信头像上加冰墩墩
category: python
tagline: by 某某白米饭
tags: 
  - python
  - 微信头像
  - 冰墩墩
---

冬奥会的吉祥物冰墩墩真的是火到爆炸了，听说冰墩墩已经被转手到上千元了。打工人的小编是买不起也买不到了。只能用 Python 在微信头像上加一个冰墩墩了。
<!--more-->

![](https://files.mdnice.com/user/15960/639bd912-9461-4304-86b3-2119205122fc.png)

### 安装模块

PIL（Python Imaging Library）是Python中一个强大的图像处理库，虽然只支持 Python 2.7，但是 pillow 是 PIL 的一个分支，我们可以安装 pillow 达到目的。

```python
pip install Pillow
```

### 图像叠加

准备两张图像，一张冰墩墩的图片，小编是在网上下载的透明背景色的图像。一张是自己的头像。

![背景是透明的](https://files.mdnice.com/user/15960/2c16cb6a-d2f8-41ad-af34-f61fcec02a70.png)

将头像和冰墩墩都转为 RGBA 模式的 32 位彩色图像。

```python
import os

path = 'D:/bdd/'

tx_img = Image.open(os.path.join(path,'tx.jpg'))
bdd_img = Image.open(os.path.join(path,'bdd.png'))

tx_rgba = tx_img.convert('RGBA')
bdd_rgba = bdd_img.convert('RGBA')
```

将冰墩墩的原图像是 3307 * 3294 像素大小的。比头像的像素大了 N 倍，需要缩放一定的比例。scale 就是比例值。

```python
scale = 5
img_scale = max(tx_x / (scale * bdd_x), tx_y / (scale * bdd_y))
new_size = (int(bdd_x * img_scale), int(bdd_y * img_scale))
bdd = bdd_rgba.resize(new_size, resample=Image.ANTIALIAS)

bdd.show()
```

示例结果：

![](https://files.mdnice.com/user/15960/0df3193f-5fa9-4b8b-8ede-5bde4d75ca86.png)



最后调用 image.paste() 方法，将两个图像黏贴在一起。

```python
bdd_x, bdd_y = bdd.size
tx_rgba.paste(bdd, (tx_x - bdd_x, tx_y - bdd_y), bdd)

tx_rgba.show()

tx_rgba.save(os.path.join(path,'tx_bdd.png'))
```

示例结果：

![](https://files.mdnice.com/user/15960/1119fba1-54d4-4d55-bba2-0b90178d689d.png)

### 总结

本文用 PIL 模块的简单方法实现了图像的放大\缩小、黏贴以及保存为图片，让冰墩墩出现在了微信头像上，小伙伴们快去试试吧。
