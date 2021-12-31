---
layout: post
category: python
title: 神操作！居然有人用 Python 在 Excel 中画画
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/img-excel/logo.png)

十字绣大家都知道吧，今天咱们来玩个电子版的十字绣。

用 Python 读取图片的像素值，然后输出到 Excel 表格中，最终形成一幅像素画，也就是电子版的十字绣了。

## 准备

既然要读取图片，那就需要用到 Pillow 库，操作 Excel 需要用到 openpyxl 库，先把这两个库安装好。

```python
$ pip3 install openpyxl
$ pip3 install Pillow
```

## 色值转换

从图片读取的像素块色值是 RGB 值，而 openpyxl 向 Excel cell 内填充颜色是十六进制色值，因此咱们先写一个 RGB 和十六进制色值转换的一个函数。

```python
def rgb_to_hex(rgb):
    rgb = rgb.split(',')
    color = ''
    for i in RGB:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color
```

## 图片转换

有了色值转换函数，接下来要做的操作就是逐行读取图片的 RGB 色值，之后将 RGB 色值转换为十六进制色值填充到 Excel 的 cell 中即可。

```python
def img2excel(img_path, excel_path):
    img_src = Image.open(img_path)
    # 图片宽高
    img_width = img_src.size[0]
    img_height = img_src.size[1]

    str_strlist = img_src.load()
    wb = openpyxl.Workbook()
    wb.save(excel_path)
    wb = openpyxl.load_workbook(excel_path)
    cell_width, cell_height = 1.0, 1.0

    sheet = wb["Sheet"]
    for w in range(img_width):
        for h in range(img_height):
            data = str_strlist[w, h]
            color = str(data).replace("(", "").replace(")", "")
            color = rgb_to_hex(color)
            # 设置填充颜色为 color
            fille = PatternFill("solid", fgColor=color)
            sheet.cell(h + 1, w + 1).fill = fille
    for i in range(1, sheet.max_row + 1):
        sheet.row_dimensions[i].height = cell_height
    for i in range(1, sheet.max_column + 1):
        sheet.column_dimensions[get_column_letter(i)].width = cell_width
    wb.save(excel_path)
    img_src.close()
```

最后再来个入口函数，就大功告成啦～

```python
if __name__ == '__main__':
    img_path = '/Users/xyz/Documents/tmp/03.png'
    excel_path = '/Users/xyz/Documents/tmp/3.xlsx'
    img2excel(img_path, excel_path)
```

## 惊艳时刻

激动的心，颤抖的手，来看下最终效果咋样。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2021/12/img-excel/001.png)

是不是觉得有那么一丝丝韵味呢...

## 总结

今天派森酱带大家一起实现了 Excel 像素画，小伙伴们可以发挥自己的想象，比如把女神的头像藏进 Excel 中然后发她，你猜女神会不会被惊艳到呢。

对此你还有什么好玩的想法，可以在评论区和其他小伙伴一起交流哦～