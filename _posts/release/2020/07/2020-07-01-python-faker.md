---
layout: post
title: 自动造数据，Faker 了解一下？
category: python
tagline: by 闲欢
tags: 
  - python
---

在系统开发过程中，不管作为开发还是测试，我们都要造一些假数据到系统中，来模拟真实环境的运行。比如要创建一批用户，输入一些车牌，或者是电话号码，或者是街道地址等等。对于我来说，要么是大量的“测试XX”，要么是随手在键盘上一敲，都是些无意义的货真价实的假数据。看完这篇文章，你就能告别这样的烦恼了。

<!--more-->


## 安装及基本用法

### 安装

安装 Faker 很简单，使用 pip 方式安装：

> pip install Faker

### 基本用法

Faker 的使用也是很简单的，从 faker 模块中导入类，然后实例化这个类，就可以调用方法使用了：

```python
from faker import Faker

fake = Faker()
fake.name()
# Danny Clarke
print(fake.address())
# 909 Nichols Ferry 
# Abigailfort, MA 69479

```

这里我们造了一个名字和一个地址，由于 Faker 默认是英文数据，所以如果我们需要造其他语言的数据，可以使用 locale参数，例如：

```python
from faker import Faker           
 
fake = Faker(locale='zh_CN')       
fake.name()                        
# 史林
 
fake.address()                     
# 陕西省惠州市门头沟沈路d座 991298

```

是不是看起来还不错，但是有一点需要注意，这里的地址并不是真实的地址，而是随机组合出来的，也就是将省、市、道路之类的随机组合在一起。

## 地址相关方法

这里需要注意，有些方法是有地区倾向的，比如 province() 在中文中可以正常获取，但是在其他语种中可能会报错。

```python
fake.building_number() # 楼栋名称
# 'U座'

fake.postcode() # 邮政编码
# 257897

fake.street_address() # 街道地址
# 吴路e座

fake.street_name()  # 街道名称
# 嘉禾路

```

## 条形码相关方法

```python
fake.ean(length=13)    # EAN条形码
# '5427745056706'
 
fake.ean13()           # EAN13条形码
# '0937312282094'
 
fake.ean8()            # EAN8条形码
# '52227936'

```

## 颜色相关方法

```python
fake.color_name()        # 颜色名称
# 'White'
 
fake.hex_color()         # 颜色十六进制值
# '#f5db7c'
 
fake.rgb_color()         # 颜色RGB值
# '15,240,40'

```

## 货币相关方法

```python
fake.cryptocurrency() #加密货币代码+名称
# ('AMP', 'AMP')

fake.cryptocurrency_code()  # 加密货币代码
# 'XMR'
 
fake.cryptocurrency_name()  # 加密货币名称
# 'Feathercoin'
 
fake.currency()      # 货币代码+名称
('SEK', 'Swedish krona')

fake.currency_code()   # 货币代码
# 'CRC'
 
fake.currency_name()  # 货币名称
# ''Mozambican metical'

```

## 时间相关方法

```python
fake.date(pattern="%Y-%m-%d", end_datetime=None)  # 日期字符串(可设置格式和最大日期)
# '1992-02-13'
 
fake.date_between(start_date="-7y", end_date="today")  # 日期(可设置限定范围)
# datetime.date(2017, 1, 24)

fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=100)    # 出生日期（可设置最大最小年龄）
# datetime.date(1964, 2, 27)

fake.date_this_month(before_today=True, after_today=False)         # 本月中的日期
# datetime.date(2020, 7, 1)

fake.time(pattern="%H:%M:%S", end_datetime=None)      # 时间(可设置格式和最大时间)
# '13:00:18'

fake.timezone()    # 时区
# 'Africa/Kampala''

```

## 坐标相关方法

```python 
fake.latlng()           # 经纬度
# (Decimal('-84.6293375'), Decimal('106.942208'))

fake.local_latlng(country_code="CN", coords_only=False)    # 返回某个国家某地的经纬度
# ('46.51872', '86.00214', 'Hoxtolgay', 'CN', 'Asia/Urumqi')

```

## 联系方式相关方法

```python
fake.phone_number()       # 手机号
# '13920149907'

fake.email(*args, **kwargs)  
# caixiulan@35.cn'

```

## 文本相关方法

```python
fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)    # 单个段落
# '法律国际评论网站这是.个人其他不断报告公司.'

fake.text(max_nb_chars=200, ext_word_list=None)     # 单个文本
# '起来以后文章所以自己.一直一定以上电子.\n然后开始问题出来已经.信息这个空间各种经营.\n到了所有需要介绍支持.方式建设专业就是经营更多.主要功能比较事情帮助.\n之后点击成为选择资密码部分.'

fake.md5(raw_output=False)         # Md5
# '3f9824429336952484a70de210f0794f'

fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)          # 密码
# 'xNGUixHi$1'

fake.uuid4()
# 'a70b41c0-ccdb-4dd0-9c9b-9b650fa72a49'

```

## python 相关方法

最后，我们来看看 python 相关的方法，可以为我们写测试方法提供一些方便。

```python
fake.pydict(nb_elements=10, variable_nb_elements=True)    # Python字典
# {'女人': 'EsiJkxQOIyMEKMBLiraE', '系列': 'shenxiulan@gmail.com', '操作': 'VGiviSlGVputFAUSWfdL', '不过': 'CZJaxfxXXIDFOThUxxOR', '得到': 3637, '搜索': Decimal('-292113.66项目': datetime.datetime(2000, 1, 12, 0, 54, 5), '那些': 'SbQuGqOGEnFhdPEYRrou', '虽然': 'EvRyxlmTgrrhrVWxMXIu', '方面': -1623419454707.4, '历史': 'jsun@hotmail.com', '对//moxiang.cn/', '社区': 'http://lei.cn/'}

fake.pyiterable(nb_elements=10, variable_nb_elements=True)   # Python可迭代对象
# ['llyMSqurkCSNUwLcNJQg', 'bUxhBPmxovfOXixprnCr', 'nDNAnBFUWnqFTzJAPoYZ', 'aygoBknQESmPeMTdVoxz', 6393, 'http://ef.cn/category/posts/register/']

fake.pystruct(count=3)   # Python结构
# (['https://jieduan.cn/author/', 2690, 'http://litao.cn/category/'], {'还是': datetime.datetime(2000, 8, 20, 22, 17, 30), '一直': 9796, '音乐': 'https://www.laizhou.cn/hom{'全部': {0: 6397, 1: [Decimal('833148.6'), datetime.datetime(2014, 2, 10, 20, 27, 58), 2722], 2: {0: datetime.datetime(1977, 5, 16, 17, 32, 12), 1: 'WoIPYqFCHtXyQpbOJIBP 2: ['yLJmsrTnTksLqBmMhDul', datetime.datetime(2005, 2, 4, 6, 52, 20)]}}, '大小': {1: 'huangjun@gmail.com', 2: ['KLTasWcxRxpkodwDAaWn', 'kgmVQfTcQWSRWeznRLiC', 46.727079]3: {1: 'LNYNQybvzxVtioHSpdEC', 2: 'KtAnXvEEEoQjNuIORdul', 3: [8000, 52227.700775]}}, '地区': {2: 'junxiao@jingxia.cn', 3: ['zhaona@jiemo.net', 'DHKalOGzfcDKSZtTRLsK', 'doGiBbxvuKAuqrIPpS'], 4: {2: 9444, 3: 'RSqhHYIdViwynTTaIjuE', 4: [1515, 6512]}}})

```

## 总结

这些只是其中的一些常见的数据，Faker 可以造的数据远不止这些类型。相信通过本文的介绍，大家应该对 Faker 不陌生了吧。以后在需要造数据的时候，一定要想起 Faker 这个利器哦！



