---
layout: post
category: python
title: 提高效率必备之 Python 办公黑科技！
tagline: by 潮汐
tags:
  - Python技巧
  - 编程
---

学习 Python 这么久了，今天我们来聊聊如何利用 Python 提升办公效率，在工作中提升工作效率的同时也让提升自己的专项技能，让自己得成神之路越来越近！
废话不多说啦，请上才艺！

<!--more-->

## Python 打怪兽之计算中文字数

在平时的工作中，有时候需要统计某些文件的字符数，既然都学会了 Python 技能，咱们就用技术来解决工作中所遇的问题，安排上：
```python
#coding:utf-8
import re
#读取目标文本文件
def get_str(path):
    f = open(path)
    data = f.read()
    f.close()
    return data
# 输入目标路径
path=input("请输入文件路径：")

word=re.findall('([\u4e00-\u9fa5])',get_str(path))

# 计算出特殊字符外的字数
print("中文字符,除特殊字符外共：",len(word))

```
**文本：**

![](https://files.mdnice.com/user/6478/e296f0b6-e5af-4fe1-8fae-4011bc353475.png)


**运行效果如下：**

![](https://files.mdnice.com/user/6478/a4315ade-09b8-4b8a-897b-cda66602ca92.png)


## Python 打怪兽之提取文本中手机号

在平时的工作中，有时候可能也需要根据一个文本的内容提取手机号或者邮箱，又或者是其他内容，这时候咱们学习 Python 的技能就派上了用场，运用的也都是 Python 基础知识，思路是：读取文件-->提取手机号-->写入文本-->写入Excel

### 将提取的手机号存入txt

```python
import re

#读取目标文本文件
def get_str(path):
    f = open(path,encoding="utf-8")
    data = f.read()
    f.close()
    return data

# 正则获取文本号码
def get_phone_number(str):
    res = re.findall(r'(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18\d{9})', str)
    return res

#保存得到号码
def save_res(res,save_path):
    save_file = open(save_path, 'w')
    for phone in res:
        save_file.write(phone)
        save_file.write('\n')
    save_file.write('\n号码共计：'+str(len(res)))
    save_file.close()
    print('号码读取OK，号码共计：'+str(len(res)))

if __name__ == '__main__':
    path=input("请输入文件路径：")
    save_path=input("请输入文件保存路径：")
    #read_str=get_str(path)
    res=get_phone_number(get_str(path))
    save_res(res,save_path)
```
**运行效果如下：**

![](https://files.mdnice.com/user/6478/7c8ecbf2-347c-4e99-b909-f561e59ece32.png)

**写出文件内容如下：**

![](https://files.mdnice.com/user/6478/9c8e524f-f5fa-4021-982b-1702c2c1c888.png)

### 将提取的手机号存入 Excel

```python
#coding:utf-8
import xlwt

#读取目标文本文件
def get_str(path):
    f = open(path, encoding="utf-8")
    data = f.read()
    f.close()
    return data


def save_excel(save_path,sheetname,column_name_list,read_list):
    workbook = xlwt.Workbook()

    sheet1 = workbook.add_sheet(sheetname=sheetname)

    for i in range(0,len(column_name_list)):
        sheet1.write(0,i,column_name_list[i])
        i = 1
        for v in read_list:
            kval = v.split('：')
            for j in range(0, len(kval)):
                sheet1.write(i + 1, j, kval[j])
                print(kval[j])
            i = i + 1
#保存为Excel文件
def save_excel(save_path,sheetname,column_name_list,read_list):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(sheetname=sheetname)
    for i in range(0,len(column_name_list)):
        sheet1.write(0,i,column_name_list[i])
    i=1
    for v in read_list:
        kval=v.split('：')
        for j in range(0,len(kval)):
            sheet1.write(i+1,j,kval[j])
        i=i+1
    workbook.save(save_path)
    print('信息保存 OK，记录条数共计：'+str(len(read_list)))

if __name__ == '__main__':
    path = input("请输入文件路径：")
    save_path = input("请输入文件保存路径：")
    sheet_name = input("请输入sheetname：")
    column_name = input("请输入列名，并且使用英文逗号隔开：")
    column_name_list = column_name.split(',')

    read_str = get_str(path)
    read_list = read_str.split('\n')
    save_excel(save_path, sheet_name, column_name_list, read_list)
    
```
**运行效果如下：**
![](https://files.mdnice.com/user/6478/e8678e30-16c3-40be-b554-d954407eab68.png)

**写出文件内容如下：**

![](https://files.mdnice.com/user/6478/119389fa-054a-4ce8-97f7-09fe577e2671.png)

### 总结

如果学习了某一项技能，在日常的工作或者生活中，我们应该好好利用已学习的技能为我们排忧解难，让所学知识运用到工作或者生活中，这样才能提高学习和工作效率，每个人都有属于自己学习或工作方式，所谓学以致用，希望今天的文章对大家有所帮助！

> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/chaoxi/work_pro)
