---
layout: post     
title:  实战！用 Python 给母亲送祝福!
category: 实战！用 Python 给母亲送祝福!
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

今天是母亲节，小阿酱在这里祝天下所有的母亲节日快乐，作为女儿的我除了买礼物送惊喜外还要用 Python 送上特殊的祝福！

母亲节（Mother’s Day），是一个感谢母亲的节日。妈妈曾经也是一个女孩子，怕黑怕虫子，也会掉眼泪，笨手笨脚怕扎针，但她温柔了我，温柔了岁月。

借此祝全天下妈妈母亲节快乐！

### 制作母亲节词云图-祝福方式1

这个世界只有一个母亲，包容我的一千万任性！

今天我用 Python 制作一个词云图给妈妈送祝福，制作代码如下：
```python
import numpy
import multidict
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator

def transform_format(val):
    """
    用于去除杂色
    Arguments:
        val {[array]} -- RGB颜色组
    Returns:
        [array] -- 去除杂色后的值
    """
    if val[0] > 245 and val[1] > 245 and val[2] > 245:
        val[0] = val[1] = val[2] = 255
        return val
    else:
        return val


def gen_happy_birthday_cloud(file, name):
    words = multidict.MultiDict()
    # 必须先初始化两个最大权重的
    words.add('母亲节快乐', 10)
    words.add(name, 12)

    # 随意插入新的词语
    for i in range(1000):
        words.add('妈妈', numpy.random.randint(1, 5))
        words.add('您辛苦了', numpy.random.randint(1, 5))
        words.add(name, numpy.random.randint(1, 5))

    # 设定图片
    bimg = imread(file)
    for color in range(len(bimg)):
        bimg[color] = list(map(transform_format, bimg[color]))

    wordcloud = WordCloud(
        background_color='white',
        mask=bimg,
        font_path='simhei.ttf'
    ).generate_from_frequencies(words)

    # 生成词云
    bimgColors = ImageColorGenerator(bimg)

    # 渲染词云
    plt.axis("off")
    plt.imshow(wordcloud.recolor(color_func=bimgColors))
    plt.savefig(name + '.png')
    plt.show()

gen_happy_birthday_cloud("mother.jpg", "母亲节快乐")
```
**思路为：** 导入一张图片后再输入节日祝福语后进行图片渲染，最后再根据图片形状生成相应词云图。

运行结果如下：
![](https://files.mdnice.com/user/6478/3ef47279-9fcf-4d54-ba01-3ec897b8bcce.png)

另一个形状图片生成的词云图：
![](https://files.mdnice.com/user/6478/707137a1-e71e-4d35-bae2-2aeeb2b062d7.png)

### 飘落爱心玫瑰-祝福方式2
接下来还要制作一个唯美飘落桃心给妈妈们送祝福！

```python
import time
from random import randint

for i in range(1, 35):  # 打印抬头
    print('')

heartStars = [2, 4, 8, 10, 14, 20, 26, 28, 40, 44, 52, 60, 64, 76]  # *的位置
heartBreakLines = [13, 27, 41, 55, 69, 77]  # 空格的位置
flowerBreakLines = [7, 15, 23, 31, 39, 46]  # 玫瑰的空列位置

def addSpaces(a):  # 添加空列
    count = a
    while count > 0:
        print(' ', end='')
        count -= 1


def newLineWithSleep():  # 添加空行
    time.sleep(0.3)
    print('\n', end='')


play = 0
while play == 0:
    Left_Spaces = randint(8, 80)
    addSpaces(Left_Spaces)

    for i in range(0, 78):  # 比心的形状
        if i in heartBreakLines:
            newLineWithSleep()
            addSpaces(Left_Spaces)
        elif i in heartStars:
            print('*', end='')
        elif i in (32, 36):
            print('M', end='')
        elif i == 34:
            print('O', end='')
        else:
            print(' ', end='')

    newLineWithSleep()
    addSpaces(randint(8, 80))
    print("H a p p y  M o t h e r ' s   D a y !", end='')
    newLineWithSleep()
    newLineWithSleep()

    Left_Spaces = randint(8, 80)
    addSpaces(Left_Spaces)
    for i in range(0, 47):  # 向母亲献花
        if i in flowerBreakLines:
            newLineWithSleep()
            addSpaces(Left_Spaces)
        elif i in (2, 8, 12, 18):
            print('{', end='')
        elif i in (3, 9, 13, 19):
            print('_', end='')
        elif i in (4, 10, 14, 20):
            print('}', end='')
        elif i in (27, 35, 43):
            print('|', end='')
        elif i in (34, 44):
            print('~', end='')
        elif i == 11:
            print('o', end='')
        else:
            print(' ', end='')

    print('\n', end='')

```
实现效果如下：
![](https://files.mdnice.com/user/6478/ef377751-be1e-4709-9fe9-635cdf5e36d1.png)

### 总结

今天是母亲节，借此希望大家能够好好陪陪父母，或者给母亲送上一份祝福和好礼。也希望今天的文章对大家有帮助。

### 写在最后

亲爱的妈妈，其实我爱你要比你爱我久一点，你从 20 岁就开始爱我，而我一出生就开始爱你，你只能爱我几十年，而我爱你一辈子！

岁月从不败美人，祝全天下妈妈母亲节快乐！


> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/chaoxi/mother_day>