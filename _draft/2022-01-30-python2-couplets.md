---
layout: post
title: python写春联，瑞雪兆丰年！
category: python
tagline: by 闲欢
tags: 
  - python
  - 春节
  - 春联
---



![封面](http://www.justdopython.com/assets/images/2022/01/couplets/0.png)

一年一度的春节马上就要到了，作为春节必不可少的一件事，就是家家户户门前都会贴春联。作为中国的传统文化元素之一，人们借春联描绘新年的美好景象，抒发美好愿望。

很遗憾，我自小没有学习毛笔字，不会写对联，每年家里的春联都是买的。但是作为一个 Python 程序员，我想用程序写一副春联，来抒发对新年美好的愿望。

<!--more-->

### 下载春联字体

```python
def get_word(ch, quality):
    fp = io.BytesIO(requests.post(url='http://xufive.sdysit.com/tk', data={'ch': ch}).content)
    im = Image.open(fp)
    w, h = im.size
    if quality == 'M':
        w, h = int(w * 0.75), int(0.75 * h)
    elif quality == 'L':
        w, h = int(w * 0.5), int(0.5 * h)

    return im.resize((w, h))

```

这个方法有两个参数，分别是：

> 汉字

> 分辨率


### 获取春联背景

```python
def get_bg(quality):
    """获取春联背景的图片"""

    return get_word('bg', quality)
```

还是使用获取字体的方法，只不过第一个参数传入 'bg'。

### 写春联

```python
def write_couplets(text, HorV='V', quality='L', out_file=None):
    usize = {'H': (640, 23), 'M': (480, 18), 'L': (320, 12)}
    bg_im = get_bg(quality)
    text_list = [list(item) for item in text.split()]
    rows = len(text_list)
    cols = max([len(item) for item in text_list])

    if HorV == 'V':
        ow, oh = 40 + rows * usize[quality][0] + (rows - 1) * 10, 40 + cols * usize[quality][0]
    else:
        ow, oh = 40 + cols * usize[quality][0], 40 + rows * usize[quality][0] + (rows - 1) * 10
    out_im = Image.new('RGBA', (ow, oh), '#f0f0f0')

    for row in range(rows):
        if HorV == 'V':
            row_im = Image.new('RGBA', (usize[quality][0], cols * usize[quality][0]), 'white')
            offset = (ow - (usize[quality][0] + 10) * (row + 1) - 10, 20)
        else:
            row_im = Image.new('RGBA', (cols * usize[quality][0], usize[quality][0]), 'white')
            offset = (20, 20 + (usize[quality][0] + 10) * row)

        for col, ch in enumerate(text_list[row]):
            if HorV == 'V':
                pos = (0, col * usize[quality][0])
            else:
                pos = (col * usize[quality][0], 0)

            ch_im = get_word(ch, quality)
            row_im.paste(bg_im, pos)
            row_im.paste(ch_im, (pos[0] + usize[quality][1], pos[1] + usize[quality][1]), mask=ch_im)

        out_im.paste(row_im, offset)

    if out_file:
        out_im.convert('RGB').save(out_file)
    out_im.show()

```

这里面也有几个参数：
> text 表示春联内容，以空格断行

> HorV 表示横排还是竖排。一般春联分为横幅和竖排

> quality 表示单字分辨率，H-640像素，M-480像素，L-320像素

> out_file 表示输出文件名


### 生成春联

既然明年是虎年，那么咱们就以虎为主题来生成一副对联。

我们先来生成竖联：

```python
text = '龙引千江水 虎越万重山'
write_couplets(text, HorV='V', quality='M', out_file='竖联.jpg')
```

生成的结果为：

![](http://www.justdopython.com/assets/images/2022/01/couplets/1.png)

接着我们来生成横联：

```python
text = '龙腾虎跃'
write_couplets(text, HorV='H', quality='M', out_file='横联.jpg')

```

生成的结果为：

![](http://www.justdopython.com/assets/images/2022/01/couplets/2.png)


### 总结

作为新时代的弄潮儿，我们也应该用自己的方式去表达对传统习俗的敬意，赶紧去“写”副对联吧！

