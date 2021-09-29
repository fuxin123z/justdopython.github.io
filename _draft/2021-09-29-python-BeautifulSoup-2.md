---
layout: post
category: python
title: 巨细！小姐姐告诉你关于 BeautifulSoup 的一切(续)！
tagline: by 潮汐
tags:
  - Python 爬虫
 
---

![首图](https://files.mdnice.com/user/6478/1a1bfd05-710b-4b59-aa29-96847e9253d9.png)

### 详细了解 BeautifulSoup 爬虫

前面第一篇文章是关于 BeautifulSoup 爬虫的基础知识详解第一部分，主要介绍了 BeautifulSoup 爬虫的安装过程及简介，同时又快速学习了利用 BeautifulSoup 技术定位标签、获取标签内容的相关知识点，今天的文章将深入地介绍 BeautifulSoup 技术的详细语法及其相关用法。

#### 1.BeautifulSoup 对象

BeautifulSoup 将复杂的 HTML 文档转换成一个树形结构，每个节点都是 Python 对象，BeautifulSoup 官方文档将所有的对象归纳为以下四种：

- **Tag**
- **NavigableString**
- **BeautifulSoup**
- **Comment**

接下来详细介绍 BeautifulSoup 的四个对象：

**Tag**

Tag 对象表示 XML 或 HTML 文档中的标签，通俗地讲就是 HTML 中的一个个标签，该对象与 HTML 或 XML 原生文档中的标签相同。Tag 有很多方法和属性，BeautifulSoup 中定义为 soup.Tag，其中 Tag 为 HTML 中的标签，比如 a、title 等，其结果返回完整的标签内容，包括标签的属性和内容等。例如以下实例就是 Tag:

```
<title>BeautifulSoup 技术详解</title>
<p class="title">Hello</p>
<p class="con">Python 技术</p>
```
以上的 HTML 代码中，title、p 都是标签，起始标签和结束标签之间加上内容就是 Tag。标签获取方法代码如下：

```
 #创建本地文件soup对象
    soup = BeautifulSoup(open('test.html','rb'), "html.parser")
    #获取a标签
    a = soup.a  #Tag
    print('a标签的内容是:', a)
```

除此之外，Tag 中最重要的属性是 name 和 attrs 。

- **name**

name 属性用于获取文档树的标签名字，如果想获取 title 标签的名字，只要使用 soup.title.name 代码即可，对于内部标签，输出的值便为标签本身的名称。

- **attrs**
attrs是属性（attributes）的英文简称，属性是网页标签的重要内容。一个标签（Tag）可能有很多个属性，例如：

```
<a href="https://www.baidu.com" class="xiaodu" id="l1">ddd</a>
```
以上实例存在两个属性，一个是class属性，对应的值为“xiaodu”；一个是id属性，对应的值为“l1”。Tag属性操作方法与Python字典相同，获取p标签的所有属性代码如下，得到一个字典类型的值，它获取的是第一个段落 p 的属性及属性值。

```python
# 获取属性
print(soup.p.attrs)

# 获取属性值
print(soup.a['class'])
#[u'xiaodu']
print(soup.a.get('class'))
#[u'l1']
```
 
BeautifulSoup 每个标签 tag 可能有很多个属性，可以通过 “.attrs” 获取属性，tag 的属性可以被修改、删除或添加。

**NavigableString**

NavigableString 也叫可遍历的字符串，字符串常被包含在 tag 内,BeautifulSoup 用 NavigableString 类来包装tag中的字符串，

BeautifulSoup 用 NavigableString 类来包装 tag 中的字符串，NavigableString 表示可遍历的字符串。一个 NavigableString 字符串与 Python 中的 Unicode 字符串相同，并且支持包含在遍历文档树和搜索文档树中的一些特性。下述代码可查看 NavigableString 的类型。

```python
# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title
print(type(tag.string))

```

输出结果如下：

```python
<class 'bs4.element.NavigableString'>
```

**BeautifulSoup**

`BeautifulSoup` 对象表示的是一个文档的全部内容，通常情况下把它当作 `Tag` 对象，该对象支持遍历文档树和搜索文档树中描述的大部分的方法，下面代码是输出 `soup` 对象的类型，输出结果就是 `BeautifulSoup`  对象类型。

```python
# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title

print(type(soup))
```

输出结果如下：

```python
<class 'bs4.BeautifulSoup'>
```

因为 BeautifulSoup 对象并不是真正的 HTML 或 XML 的标签 tag，所以它没有 name 和 attribute 属性。但有时查看它的`.name` 属性是很方便的，故 BeautifulSoup 对象包含了一个值为`[document]`的特殊属性`soup.name`。下述代码即是输出 BeautifulSoup 对象的 name 属性，其值为 [document]。

**Comment**

Comment 对象是一个特殊类型的 NavigableString 对象，它用于处理注释对象。下面这个示例代码用于读取注释内容，代码如下：

```python

markup = "<b><!-- hello comment code --></b>"
    soup = BeautifulSoup(markup, "html.parser")
    comment = soup.b.string
    print(type(comment))
    print(comment)
    
if __name__ == '__main__':
    mark()
```

输出结果如下：

```python
<class 'bs4.BeautifulSoup'>
<class 'bs4.element.Comment'>
 hello comment code 
```

#### 2.遍历文档树

以上内容讲解完 4 个对象后，下面的知识讲解遍历文档树和搜索文档树以及 BeatifulSoup 常用的函数。在 BeautifulSoup 中，一个标签（Tag）可能包含多个字符串或其它的标签，这些称为这个标签的子标签。

咱们继续用以下超文本协议来讲解：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>BeautifulSoup 技术详解</title>
</head>
<body>
<p class="title">Hello</p>
<p class="con">Python 技术</p>

<a href="https://www.baidu.com" class="xiaodu" id="l1">ddd</a>

</body>
</html>
```
- **子节点**

一个Tag可能包含多个字符串或其它的Tag,这些都是这个Tag的子节点，Beautiful Soup 提供了许多操作和遍历子节点的属性。

例如获取标签子节点内容：
```python
# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title

print(soup.head.contents)
```

**输出结果如下：**

```
['\n', <title>BeautifulSoup 技术详解</title>, '\n']
```

注意: Beautiful Soup中字符串节点不支持这些属性,因为字符串没有子节点。

**节点内容**

如果标签只有一个子节点，需要获取该子节点的内容，则需要使用 string 属性，以此输出节点的内容：

```python
# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title

print(soup.head.string)

print(soup.title.string)
```

输出结果如下：

```python

None
BeautifulSoup 技术详解
```

- **父节点**

调用 parent 属性定位父节点，如果需要获取节点的标签名则使用 parent.name。实例如下：

```python

# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title

p = soup.p
print(p.parent)
print(p.parent.name)

content = soup.head.title.string
print(content.parent)
print(content.parent.name)

```

输出结果如下：

```html
<body>
<p class="title">Hello</p>
<p class="con">Python 技术</p>
<a class="xiaodu" href="https://www.baidu.com" id="l1">ddd</a>
</body>
body
<title>BeautifulSoup 技术详解</title>
title
```

- **兄弟节点**

兄弟节点是指和本节点位于同一级的节点，其中 `next_sibling` 属性是获取该节点的下一个兄弟节点，`previous_sibling` 则与之相反，取该节点的上一个兄弟节点，如果节点不存在，则返回 None。

```python
print(soup.p.next_sibling)
print(soup.p.prev_sibling)
```

- **前后节点**

调用属性 `next_element` 可以获取下一个节点，调用属性 `previous_element` 可以获取上一个节点，代码举例如下：

```python
print(soup.p.next_element)
print(soup.p.previous_element)
```

#### 3.搜索文档树

BeautifulSoup 定义了很多搜索方法，例如  `find()` 和 `find_all()`;
但`find_all()`是最常用的一种方法，而更多的方法与遍历文档树类似，包括父节点、子节点、兄弟节点等，使用find_all()方法的代码如下：

```python
# coding=utf-8
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html','rb'), "html.parser")
tag = soup.title

urls = soup.find_all('p')
for u in urls:
    print(u)
```

输出结果如下：

```html
<p class="title">Hello</p>
<p class="con">Python 技术</p>
```

使用 `find_all()` 可以查找到想要查找的文档内容。

### 总结

至此，阿酱理解范围内的 BeautifulSoup 基础知识及用法基本上已经概述完毕，有差池的地方希望大家海涵，我们一起努力前行。

### 参考

[BeautifulSoup 官网](https://www.crummy.com/software/BeautifulSoup/)
[https://blog.csdn.net/Eastmount](https://blog.csdn.net/Eastmount/article/details/109497225)
