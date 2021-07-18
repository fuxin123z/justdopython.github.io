---
layout: post
title: 几行代码，网盘链接提头来见！
category: python
tagline: by 闲欢
tags: 
  - python
  - 网盘

---

### 背景

晚上，女朋友下班回来，我邀请她下楼去散步，她一副愁眉苦脸的样子，说今晚要加班。

仔细询问之下得知：女朋友今天接到上司一个任务，领导丢给她一个文件，里面密密麻麻满是百度网盘链接和提取码，需要她今天结束之前把网盘里的文件提取出来。

听到她说要熬夜肝工作那种委屈的模样，我是真的有点心疼。于是本能地问她，现在工作中最影响效率的是哪个环节，我来帮她一起肝。她告诉我，看这个百度网盘的链接看得眼都花了，要复制链接，以及复制提取码是个技术活，因为有其他文字干扰，经常复制不准。

链接类似下面这样的：

> 链接: https://pan.baidu.com/s/1ctcXiZymWst2NC_JPDkr4Q 提取码: j1ub 复制这段内容后打开百度网盘手机App，操作更方便哦

想必大家看到这个链接，都不会陌生。不止百度网盘，还有好多网盘都是这样的。

既然这样，那我当然要帮她解决这个棘手的问题。

### 思路

其实她的需求很简单，把网盘链接和对应提取码从这个分享文字中提取出来。

大家还记得咱们前段时间给大家分享了`正则表达式`的文章吧？忘记了就回头看看这两篇文章：
[懵了！女友突然问我什么是正则表达式](https://mp.weixin.qq.com/s?__biz=MzU1NDk2MzQyNg==&mid=2247493358&idx=1&sn=4e86e8de8292c7e3530e8da99a357734&chksm=fbd93e63ccaeb775b5159d2612eb1ee6aaf25a20091891ea526dfcf2ed22da81d6e2093d4f69&token=2146376003&lang=zh_CN#rd)

[这下女友总算满意了！](https://mp.weixin.qq.com/s?__biz=MzU1NDk2MzQyNg==&mid=2247493657&idx=1&sn=24d33c451586fb03eb3440bdd9dc05a7&chksm=fbd93094ccaeb982d94ff83023fdb8640782a1286e0ef657d31a54a937a917b5d01a85a50045&token=2146376003&lang=zh_CN#rd)

解决这个需求只需要用正则表达水匹配分享文字中的 URL 和提取码就行了。

### 实现解析

代码很简单，直接上：

```python

url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
code_pattern = '(?<=提取码: )[0-9a-z]{4}'
url_regex = re.compile(url_pattern)
code_regex = re.compile(code_pattern)

```

接下来，测试一下：

```python
str = '链接: https://pan.baidu.com/s/1ctcXiZymWst2NC_JPDkr4Q 提取码: j1ub 复制这段内容后打开百度网盘手机App，操作更方便哦'
print(url_regex.findall(str)[0])
print(code_regex.findall(str)[0])
```

可以在控制台上看到打印输出两行，第一行是链接，第二行是提取码：

> https://pan.baidu.com/s/1ctcXiZymWst2NC_JPDkr4Q
j1ub

几行代码一敲，事情就这么搞定了！

等等，这太程序员思维了！

现在还只是个程序，难道要她把一段段文字复制到我的程序里面再运行？这不是更麻烦吗？？？

![就这？](http://www.justdopython.com/assets/images/2021/07/panextract/1.jpg)

当然不行，我还是有点产品素养的！

当然要给个界面给她。我搜索了下我的知识库，准备用 `tkinter` 来画一个简单的界面给她使用。

其实现如下：

```python
def draw_window(self):
        self.init_window = Tk()  # 实例化出一个父窗口
        self.init_window.title("百度网盘提取链接工具_v1.0")  # 窗口名
        self.init_window.geometry('800x300+10+10')
        # 源信息
        self.init_data_label = Label(self.init_window, text="复制的提取信息")
        self.init_data_label.grid(row=0, column=0)
        self.init_data_text = Text(self.init_window, width=100, height=5, borderwidth=1, relief="solid")  # 原始数据录入框
        self.init_data_text.grid(row=1, column=0, columnspan=10)

        # 按钮
        self.str_trans_button = Button(self.init_window, text="提取", width=10, height=2, bg="blue",
                                       command=self.extractData)  # 调用内部方法  加()为直接调用
        self.str_trans_button.grid(row=2, column=2)

        # 链接
        self.link_data_label = Label(self.init_window, width=10, text="链接")
        self.link_data_label.grid(row=3, column=0, columnspan=1)
        self.link_data_text = Text(self.init_window, width=60, height=2, borderwidth=1, relief="solid")
        self.link_data_text.grid(row=3, column=1, columnspan=6)

        # 提取码
        self.code_data_label = Label(self.init_window, width=10, text="提取码")
        self.code_data_label.grid(row=3, column=7, columnspan=1)
        self.code_data_text = Text(self.init_window, width=20, height=2, borderwidth=1, relief="solid")
        self.code_data_text.grid(row=3, column=8, columnspan=2)

```

上面就是画一个界面的代码，运行之后长这样：

![界面](http://www.justdopython.com/assets/images/2021/07/panextract/2.jpg)

丑是丑了点，但是时间紧，任务重，先用起来再说。

和解析代码合体之后，正常的运行情况应该是这样的：

![运行](http://www.justdopython.com/assets/images/2021/07/panextract/3.jpg)

当然，还可以进一步改造，比如获取到网盘链接和提取码之后，直接使用 `selenium` 来自动控制浏览器打开相应的百度网盘页面，女朋友直接在页面选择文件点击下载即可。

但是今晚时间不够了，先让她用着。


### 总结

处理一个简单的需求，咱们就用到了正则、画界面，还可以使用浏览器模拟操作的 selenium ，可见平时的知识积累多重要。小伙伴们平时还是要有意识积累一些实用的技术，当需求来时方可信手拈来，而不是“书到用时方恨少”！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/panextract)