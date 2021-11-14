---
layout: post
title: 肝了三天三夜，一文道尽Python的xpath解析！
category: python
tagline: by 闲欢
tags: 
  - python
  - xpath
---


大家在写爬虫时，往往获取到网页之后，需要从网页中提取我们需要的信息。这时候就需要用到 xpath 或者 css 选择器来定位页面元素信息。但是，由于这两者都是非人性化的语法，导致好多人望而生畏，经常为这个发愁。

今天我就尝试用一篇文章来道尽 xpath 解析 HTML 的方方面面，希望大家看完这篇文章后，从此不再害怕 xpath 解析。


#### 路径表达式

- nodename：选取此节点的所有子节点
- `/`：从当前节点选取直接子节点
- `//`：从当前接点选取子孙节点
- `.`：选取当前节点
- `..`：选取当前接点的父节点
- `@`：选取属性
    
    
我们先放上一段 HTML 代码：

```html
<html>
  <head>
    <title>
      Xpath test page
    </title>
  </head>
  <body>
    <div class="navli">
      <span class="nav_tit">
        <a href="https://www.baidu.com/">
          百度
        </a>
        <i class="group" />
      </span>
    </div>
    <div class="navli">
      <span class="nav_tit">
        <a href="https://news.cctv.com/">
          新闻频道
        </a>
      </span>
    </div>
    <div class="navli">
      <span class="nav_tit">
        <a href="https://sports.cctv.com/">
          体育频道
        </a>
      </span>
    </div>
  </body>
</html>

```

接下来，我们针对这段 HTML 代码来进行 xpath 解析。

要进行 xpath 解析，我们先要将 HTML 文本转化成对象：

```python
from lxml import etree

text = '''
<div>
            <ul id='ultest'>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html"><span>fourth item</span></a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
             </ul>
         </div>
'''
# 调用HTML类进行初始化，这样就成功构造了一个XPath解析对象。
page = etree.HTML(text)    
print(type(page))

```

我们可以看到打印的结果：

```python
<class 'lxml.etree._Element'>

```

##### nodename

nodename 表示根据标签名字选取标签，注意只会选择子标签！比如：如果是儿子的儿子则选取不到。

```python
print(page.xpath("body"))

//[<Element body at 0x1966d1c48c0>]

print(page.xpath("ul"))

// []

```

这个 nodename 我有点不是太清楚，当我使用 body 时，可以找到出 body 节点元素，但是使用 ul 时，找不到 ul 节点元素，打印的是空。这个网上搜索也没有什么准确的答案，如果你知道这里面的原理，还请告诉我。

##### `/`

`/` 表示从根节点选取一级一级筛选（不能跳）。

```python
print(page.xpath("/html"))

// [<Element html at 0x27107f41100>]

print(page.xpath("/body"))

// []

```

可以看到，我选取根节点 html ，可以打印出根节点元素，而我选取 body 打印时，是找不到的，这个符号只能从根节点开始找。

##### `//`

`//` 表示从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 注意：是所有符合条件的。

```python
print(page.xpath("//li"))

// [<Element li at 0x1cd2a325780>, <Element li at 0x1cd2a325840>, <Element li at 0x1cd2a3259c0>, <Element li at 0x1cd2a325b00>, <Element li at 0x1cd2a325ac0>]

```

##### `.`

`.` 表示选取当前标签。

```python
ul = page.xpath("//ul")
print(ul)
print(ul[0].xpath("."))
print(ul[0].xpath("./li"))

// [<Element ul at 0x1cd2a325840>]
// [<Element ul at 0x1cd2a325840>]
// [<Element li at 0x1cd2a325700>, <Element li at 0x1cd2a325b00>, <Element li at 0x1cd2a325640>, <Element li at 0x1cd2a325ac0>, <Element li at 0x1cd2a325c00>]


```

我们先定位到 ul 元素节点，这里的结果是一个列表，然后再打印当前节点列表的第一个 ul，接着我们打印这个 ul 节点的子节点 li。

##### `..`

`..` 表示选取当前标签的父节点。

```python
print(ul[0].xpath(".."))

// [<Element div at 0x1cd2a325b00>]

```

这里打印第一个 ul 节点的父元素，也就是 div 。


##### `@`

`@` 表示获取标签的属性值。

```python
print(ul[0].xpath("@id"))

// ['ultest']

```

我们打印第一个 ul 节点的 id 属性，可以看到结果是 ‘ultest’。


#### 谓语

谓语用来查找某个或某些特定的节点或者包含某个指定值的节点。谓语被嵌在方括号中。

```python
//a[n] n为大于零的整数，代表子元素排在第n个位置的<a>元素
//a[last()]   last()  代表子元素排在最后个位置的<a>元素
//a[last()-]  和上面同理，代表倒数第二个
//a[position()<3] 位置序号小于3，也就是前两个，这里我们可以看出xpath中的序列是从1开始
//a[@href]    拥有href的<a>元素
//a[@href='www.baidu.com']    href属性值为'www.baidu.com'的<a>元素
//book[@price>2]  price值大于2的<book>元素
```

同样的，我们来举一些例子：

```python
# 第三个li标签
print(page.xpath('//ul/li[3]'))
# 最后一个li标签
print(page.xpath('//ul/li[last()]'))
# 倒数第二个li标签
print(page.xpath('//ul/li[last()-1]'))
# 序号小于3的li标签
print(page.xpath('//ul/li[position()<3]'))
# 有class属性的li标签
print(page.xpath('//li[@class]'))
# class属性为item-inactive的li标签
print(page.xpath("//li[@class='item-inactive']"))

```

#### 获取文本

##### text()

我们用text()获取某个节点下的文本：

```python
print(page.xpath('//ul/li/a/text()'))

// ['first item', 'second item', 'third item', 'fourth item', 'fifth item']

```

##### string()

我们用string()获取某个节点下所有的文本：

```python
print(page.xpath('string(//ul)'))

```

输出内容为：

```python
                 first item
                 second item
                 third item
                 fourth item
                 fifth item # 注意，此处缺少一个  闭合标签
```


#### 通配符

- `*` 任意元素
- `@*`  任意属性


`*` 表示匹配任何元素节点：

```python
print(page.xpath('//li/*'))

// [<Element a at 0x208931f0f00>, <Element a at 0x208931f0f40>, <Element a at 0x208931f0c40>, <Element a at 0x208931f0d80>, <Element a at 0x208931ff080>]

```

`@*` 表示匹配任何属性节点：

```python
print(page.xpath('//li/@*'))

// ['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']
```

#### 或运算

通过在路径表达式中使用"|"运算符，可以实现选取若干个路径。

```python
# 选取所有的li和a节点
print(page.xpath("//li|//a"))

// [<Element li at 0x29bb7190ac0>, <Element a at 0x29bb7190b00>, <Element li at 0x29bb7190f00>, <Element a at 0x29bb7190dc0>, <Element li at 0x29bb7190fc0>, <Element a at 0x29bb7190e00>, <Element li at 0x29bb7190f80>, <Element a at 0x29bb71b1080>, <Element li at 0x29bb71b1040>, <Element a at 0x29bb7190cc0>]

```

#### 函数

xpath内置很多函数。更多函数查看https://www.w3school.com.cn/xpath/xpath_functions.asp。

- contains(string1,string2)
- starts-with(string1,string2)
- text()
- last()
- position()
- node()


##### contains
有的时候，class作为选择条件的时候不合适@class='....' 这个是完全匹配，当网页样式发生变化时，class或许会增加或减少像active的class。用contains就能很方便。

```python
print(page.xpath("//*[contains(@class, 'item-inactive')]"))

// [<Element li at 0x21dd3504a00>]

```

##### starts-with

```python
print(page.xpath("//*[starts-with(@class, 'item-inactive')]"))
// [<Element li at 0x1a297641d00>]
```

其他几个函数，我们在上面使用过。
注意，并不是所有的 xpath 函数python都会支持，比如 ends-with(string1,string2) 和 upper-case(string)  就不支持。

#### 节点轴选择

##### ancestor轴

调用 ancestor 轴，获取所有祖先节点。其后需要跟两个冒号，然后是节点的选择器。返回结果：第一个li节点的所有祖先节点。

```python
print(page.xpath('//li[1]/ancestor::*'))

// [<Element html at 0x26ead5d2d40>, <Element body at 0x26eae63fdc0>, <Element div at 0x26eae628c00>, <Element ul at 0x26eae63fd40>]

```

##### attribute轴

调用 attribute 轴，获取所有属性值。返回结果：li节点的所有属性值。

```python
print(page.xpath('//li[1]/attribute::*'))

// ['item-0']
```

##### child轴

调用 child 轴，获取所有直接子节点。返回结果：选取 href 属性为 link1.html 的 a 子节点。

```python
print(page.xpath('//li[1]/child::a[@href="link1.html"]'))

// [<Element a at 0x13972af5b40>]

```

##### descendant轴

调用 descendant 轴，获取所有子孙节点。同时加了限定条件。返回结果：选取 li 节点下的子孙节点里的 span 节点。

```python
print(page.xpath('//li[4]/descendant::span'))

// [<Element span at 0x1a4d5700d00>]

```

##### following轴

调用 following 轴，获取当前节点之后的所有节点。

```python
print(page.xpath('//li[4]/following::*[2]'))

// [<Element a at 0x1583f8c0d00>]

```

##### following-sibling轴

调用 following-sibling 轴，获取当前节点之后的所有同级节点。

```python
print(page.xpath('//li[4]/following-sibling::*'))

// [<Element li at 0x1ff55435c00>]

```

#### 总结

到这里，我们的 xpath 学习之路就结束了，文章中基本涵盖了大家需要用的的 xpath 解析方法。大家看一遍没记住不要紧，以后遇到此类解析直接搬出这篇文章对照着写就行。
