---
layout: post
title:  网易云音乐导出歌单-速食版
category: 工具
copyright: python
tagline: by 轩辕御龙
tags: 
---

# 网易云音乐导出歌单-速食版

## 动机是啥

随着之前版权大战的落幕，网易云音乐坐拥最忠实的一批用户，但是却在版权上缺失了一大块，带给用户很不好的使用体验。于是很多人纷纷转战QQ音乐等其他竞品。

本来我也就是偶尔听个响，对于听歌没有太大的需求，再一方面也是情怀，所以没有积极拥抱QQ音乐。但是实在架不住每次在网易云音乐要听啥歌没有啥，潜移默化地也就转移到了QQ音乐上。

到了QQ音乐一看，诶嘿，这不行啊，我辛辛苦苦积攒的家底儿都没了嘛这不是？就光秃秃的“我喜欢”，还大小没几首歌。这让习惯了网易云日推的我怎么能习惯啊……

<!--more-->

好了，以上都是前情提要。

实际上这篇文章的写作动机就是要把网易云音乐的歌单导入到QQ音乐中去。

本身QQ音乐提供了一个导入网易云音乐歌单的小公举，啊不，咳咳，是小工具。但是奈何出于不可名状的原因，这个工具常年出于抽风状态。其具体症状见下图：

![01](http://www.justdopython.com/assets/images/2020/06/29/01.png)

于是乎，官方是靠不住的了。

大力水手曾经曰过：“靠山山倒，靠人人跑。只有靠自己，最好。”自己动手，丰衣足食，现在这个社会谁还没点儿技术了吗？

## 选择的方法

好吧我承认，我没有技术……

![02](http://www.justdopython.com/assets/images/2020/06/29/02.jpg)

那好家伙，直接用我们社会主义劳动人民的老朋友`requests`来获取页面信息，返回来的倒也说不上是乱码，但就是没有咱们真正需要的内容——歌曲名称。

行吧，那我配置一下`User-Agent`。我去还是不行？

咋还出来了一个SSLError？这啥？

上网一查，还得手动关闭SSL证书验证。行叭，走你~

啊不对，不登录好像看不到完整的歌单？那就先登录吧。登录完好像还得在请求头里面加上用cookie来保持认证身份？……

好了，爷不伺候了。不就是这么一个页面，要啥技术啊，看我暴力破拆。

## 开工

首先在页面上点击鼠标右键，选中“检查”这一项；或者不点击鼠标，直接按下快捷键`Ctrl+Shift+I`。会弹出Chrome浏览器的控制台。此时找到其中的元素`<table class="m-table ">`，这个元素里边包含的就是我们想要的歌单了。

在这个标签内部又分为两大部分：`<thead>`和`<tbody>`。通过移动鼠标观察页面变化，可以发现`<tbody>`中的内容是主体。

再然后，轻易可以发现`<tbody>`中的每个子条目都对应于歌单中的一首歌：

![04](http://www.justdopython.com/assets/images/2020/06/29/04.png)

抓住这个点就是一顿分析（疯狂查找），一直找到最小的对应于歌曲名字的标签：

![05](http://www.justdopython.com/assets/images/2020/06/29/05.png)

行了，现在差不多可以开始编程了。

咱也不用假模假样再去用`requests`一顿爬了，直接copy-paste搞腚，呸，搞定。

鼠标选中，右键点击，依次选择：

![03](http://www.justdopython.com/assets/images/2020/06/29/03.png)

然后新建一个HTML文件，粘贴，保存，哈哈，数据爬下来啦~

请叫我人工全智能手动爬虫工程师。

接下来再利用vscode的HTML格式化插件，把一行的HTML格式化一下，大概就长这样了：

![06](http://www.justdopython.com/assets/images/2020/06/29/06.png)

文件有了，那接下来就好办了。

Python先把文件打开，把文件内容给读取进来：

```python
with open("test.html", "r", encoding="utf-8") as f:
    content = f.read()
```

此处`f.read()`返回一个由文本内容组成的字符串，我们使用`BeautifulSoup`来进行解析：

```python
from bs4 import BeautifulSoup

response = BeautifulSoup(content,'lxml')
```

仔细考察节点内容，会发现每首歌的名字都在一个特殊的标签`<b>`中，并且只在歌名处使用了这个标签，因此我们可以直接调用`find_all()`方法来获取相应节点：

```python
results = response.find_all("b")
```

由于歌曲名字是以标签`<b>`的属性`title`形式存在的，因此我们可以通过节点直接获取相应的属性值：

```python
for result in results:
    print(result['title'])
# 笑红尘 - (电影《东方不败之风云再起》主题曲)
# 爱你在心口难开
# 得意的笑
# 寂寞在唱歌
# ...
```

最后，我们将得到的歌曲名字统一保存为一个名为“SongList.txt”的文本文件，导出歌单的工作就大功告成了。

```python
with open("SongList.txt", "w+", encoding="utf-8") as f:
    f.writelines([result["title"] for result in results])
```

文件内容如下：

![07](http://www.justdopython.com/assets/images/2020/06/29/07.png)

此时结果都挤成一堆，所以我们还需要为每一个歌名末尾手动添加一个换行符，最终程序如下：

```python
from bs4 import BeautifulSoup


with open("test.html", "r", encoding="utf-8") as f:
    content = f.read()

response = BeautifulSoup(content,'lxml')

results = response.find_all("b")

with open("SongList.txt", "w+", encoding="utf-8") as f:
    f.writelines([result["title"] + "\n" for result in results])
```

别看文章写了这么多，其实代码非常之简短（毕竟真正有难度的部分已经由资深人工全智能爬虫工程师代劳了），说是速食，其实你排队打饭还没排到，歌单导出已经搞腚了。