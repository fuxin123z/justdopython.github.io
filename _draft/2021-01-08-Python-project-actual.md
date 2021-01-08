---
layout: post     
title:  Python 小项目实战了解一下？   
category: Python 小项目实战了解一下？ 
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

最近无论是北方还是南方都迎来了强冷空气的袭击，北风呼呼吹，我所在的城市这两天则可随处溜冰，城市道路结冰橙色预警，全省交通到处管制、小学幼儿园停课休息；上班路上的行人则是小心翼翼怕摔跤；老家韭菜坪的风景更美，给大家来带张照片感受感受：

![韭菜坪雪景1](https://imgkr2.cn-bj.ufileos.com/d811e7b9-ac8d-4dec-a63b-cac2105b92ce.jpg?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=FAnoq4SBvm%252By9tL5vY0TQqjvnC0%253D&Expires=1610204016)

![韭菜坪雪景2](https://imgkr2.cn-bj.ufileos.com/95df56d1-b4a3-4b9a-bc2e-f73ac61065d1.jpg?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=SGVZKAEhyqCSxAmB%252FtaFIQHrlCI%253D&Expires=1610204075)


言归正传，今天的文章来点有趣的小项目实战，希望给繁忙工作中的朋友们减减压，也给这个严冬增添几分暖色；详细项目请见后文。

### 用 Python 画彩虹线

用 Python turtle 画个转圈圈的彩虹线，实现思路如下：
```python
# 导入 turtle 包
import turtle
# 打开画笔
q = turtle.Pen()
# 设置背景颜色
turtle.bgcolor("white")
sides = 7

# 设置彩虹线
colors =["red","orange","yellow","green","cyan","blue","purple"]
for x in range(360):
     q.pencolor(colors[x % sides])
     q.forward(x*3 / sides+x)
     q.left(360 / sides+1)
     q.width(x * sides/200)
```
实现结果如下：
![彩虹图](https://imgkr2.cn-bj.ufileos.com/0d537b90-63c5-4c92-8233-e27ea8a2ff6e.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=YFRdGOBxHyKXRokD6DhG4lwuqxY%253D&Expires=1610203473)

### 用 Python 实现有趣的图片转字符游戏

实现思路如下：
```python
#用 Python 实现图片转字符
from PIL import Image
import os

#设置参数输入像素的灰度值
def g2s(gray):
    pixel_str='''$#%@&MNBEFRWYLIkbtj?*984532menocvzst{}[]1|()<>=+~-;:i^"'. '''
    length=len(pixel_str)
    # 字符之间的灰度区间
    plus=255/length
    # str_gray表示字符所代表的灰度值
    str_gray=0
    for i in range(length):
        str_gray = str_gray + plus
        if gray <=str_gray:
            return pixel_str[i]

def img2str(img_path,save_path,num=0):
    txt_path=os.path.join(save_path,'img.txt')
    f=open(txt_path,'w')
    f.write('')
    # 因为此目录有可能已有内容，所以先清空
    f.close()
    # a表示在文件的末尾添加
    f=open(txt_path,'a')

    # 因为有些图片尺寸过于大，所以添加了一个修改大小的功能
    im=Image.open(img_path)
    if num==0:
        pass
    else:
        im=im.resize( ( int(im.size[0]/num),int(im.size[1]/num) ) )

    # 直接将图片转换成灰度模式
    im=im.convert('L')
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            s=g2s(im.getpixel((x,y)))
            f.write(s)
        f.write('\n')
    f.close()

if __name__=='__main__':
    img2str(r'test.jpg', r'D:\\Python_test', 4)
```
**测试图片：**
![](https://imgkr2.cn-bj.ufileos.com/54d583ad-9b90-4d29-9de4-11541de96bf8.jpg?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=n%252BbFYPHMgHC%252B2EZX8uUNfPBhtPk%253D&Expires=1610204856)

**实现效果如下：**
![](https://imgkr2.cn-bj.ufileos.com/f3758f6f-f9d2-431a-b4dd-261f94d226e6.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=LbbJh6VK%252Fswap9zRwHEo%252FYhIaW0%253D&Expires=1610205013)

### 总结

今天的文章主要是使用 Python 实现小项目减减压，希望对大家有所帮助！

> 示例代码 [Python 小项目实战了解一下？](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/python_acturl)

