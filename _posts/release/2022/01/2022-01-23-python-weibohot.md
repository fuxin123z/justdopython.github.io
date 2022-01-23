---
layout: post
title: 太轻松！爬取12万数据盘点2021年热门大事件！
category: python
tagline: by 闲欢
tags: 
  - python
  - 词云
  - 微博
  - 2021
---



![封面](http://www.justdopython.com/assets/images/2022/01/weibohot/0.png)

2021年已经过去了，但是这一年发生了很多令人难忘的事情，相信每个人心目中都有很多感慨。

为了回顾2021年都发生了哪些大事，我打算从热搜下手，看看2021年都有哪些热搜事件。

大家都知道，微博热搜是实时更新的，并且没有历史记录，所以从微博的网站上找不到历史的热搜数据。我们只能另想它法了。经过我不懈的摸索，终于找到了一个网站，它记录了每日的微博实时热搜，并且是一分钟一次。也可以在网站上通过日期查询当天的数据。

![](http://www.justdopython.com/assets/images/2022/01/weibohot/1.png)

<!--more-->

### 下载数据

有了目标网站就好说，我们想办法从目标网站下载数据就好。这个网站提供了付费下载数据的方式。我这里为了给大家演示使用 Python 爬虫爬取数据，就不付费下载了。

网站的请求也比较简单，大家打开网页的开发工具，可以很快定位到获取请求的 URL 。这里就不赘述了，直接上代码：

```python
headers = {
        "Host": "google-api.zhaoyizhe.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

def scrapy(date):
    print('开始爬取%s' % date)
    url = 'https://google-api.zhaoyizhe.com/google-api/index/mon/sec?date=%s' % date
    try:
        time.sleep(random.randint(1, 3))
        res = requests.get(url, headers=headers).json()
        result = res['data']
        return result
    except Exception as err:
        print(err)
        return None

```

我们定义一个爬取的函数，通过传入日期来爬取一天的热搜数据。整个2021年的数据我们只需要循环请求每一天即可。

整个数据下载下来一共12万多条：

![](http://www.justdopython.com/assets/images/2022/01/weibohot/2.png)

### 制作词云

分析热点事件，最好的方法就是把这些事件描述制作成词云，突出显示的就是最热门的，一目了然。

```python
def gen_wc_split_text(data_list=[], max_words=None, background_color=None,
                      # font_path='/System/Library/Fonts/PingFang.ttc',
                      font_path=r'C:\Windows\Fonts\simhei.ttf',
                      output_path='', output_name='',
                      mask_path=None, mask_name=None,
                      width=400, height=200, max_font_size=100, axis='off'):
    stopwords = open(r'c:\pworkspace\mypy\pythontech\weibohot\stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
    words_dict = {}
    for data in data_list:
        text = data['topic']
        hotNumber = data['hotNumber']
        if hotNumber is None:
            hotNumber = 1
        all_seg = jieba.cut(text, cut_all=False)
        for seg in all_seg:
            if seg in stopwords or seg == 'unknow':
                continue
            if seg in words_dict.keys():
                words_dict[seg] += hotNumber
            else:
                words_dict[seg] = hotNumber

    # 设置一个底图
    mask = None
    if mask_path is not None:
        mask = np.array(Image.open(path.join(mask_path, mask_name)))

    wordcloud = WordCloud(background_color=background_color,
                          mask=mask,
                          max_words=max_words,
                          min_font_size=15,
                          max_font_size=80,
                          width=300,
                          height=400,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path=font_path)
    myword = wordcloud.generate_from_frequencies(words_dict)
    # 展示词云图
    # plt.imshow(myword)
    # plt.axis(axis)
    # plt.show()

    # 保存词云图
    wordcloud.to_file(path.join(output_path, output_name))

```

制作词云我们选择试用 `jieba` 分词，使用我们熟悉的 `wordcloud` 来制作词云。

我们先来看看2021年全年的词云图片：

![](http://www.justdopython.com/assets/images/2022/01/weibohot/3.png)

看着这张词云图片，是不是有好多熟悉的词汇？

接下来，我们按月份来统计热门事件，具体需要做的就是将每个月的热搜事件归集起来，然后根据热度以及出现频率叠加，来输出词云。

代码还是跟上面类似，只不过是将事件按月分类而已。

我们直接来看每个月的图片吧。


#### 1月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/4.png)


2021年在疫情中开启，在大家喊着“告别2020，开启2021”时，石家庄疫情爆发，进入战时状态。

薇娅也在这个月开始直播年货。

最后以陈翔出轨关晓彤导致工作室互怼结束。

#### 2月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/5.png)

这个月最热门的事件肯定是我们的传统春节了。

贾玲的导演处女作《你好，李焕英》，一上映就口碑炸裂。

这个月我们失去了两位明星，分别是赵英俊和吴孟达，一个时代的记忆就此落幕。

#### 3月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/6.png)

这个月明星白敬亭出尽风头。

HM、耐克等众多我们熟知的国外品牌抵制新疆棉花，遭到央视点评，全民愤怒。

这个月中美高层对话，71岁的杨洁篪老爷子怒怼东道主美国。

#### 4月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/7.png)

4月，各地大规模全员动员打疫苗。

也是这个月，日本宣布把福岛核废水排进太平洋。

这个月赵丽颖和冯绍峰宣布离婚，明星事件真是层出不穷。

#### 5月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/8.png)

最令人痛心的事件是杂交水稻之父袁老爷子走了，举国哀悼。

而就在同一天，“中国肝胆外科之父”吴孟超院士也去世了。

5月20日，全网盼离的佟丫丫，终于宣布和陈思诚离婚。


#### 6月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/9.png)

6月的大事件当属高考。

这个月，汪小菲和大S频上热搜。

这个月，神舟十二号飞船成功发射，3名航天员飞到了“天宫”。

#### 7月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/10.png)

这个月，河南郑州暴雨成灾，举国瞩目。

这个月，东京奥运会开幕，林丹和李宗伟一起看奥运。

这个月，吴亦凡翻车，都美竹爆料，网友又多了一个“吴签”的梗。


#### 8月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/11.png)

这个月，奥运会捷报频传，全红婵、苏炳添进入大众视野。

吴亦凡事件继续发酵，都美竹对吴亦凡的指控成真让他成为内娱被刑拘爱豆第一人。

演员张哲瀚被爆出进入靖国神社内部，拍摄多张开心比“耶”的照片，刚翻红就掉下去了。


#### 9月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/12.png)

孟晚舟在被困加拿大近三年后，终于回国。

体育盛事全运会刷屏。

全国人民中秋节一起吃月饼赏月。

#### 10月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/13.png)

国庆档大片《长津湖》打破8项影史记录。

知名钢琴家李云迪嫖娼被抓。朝阳群众又立一功。

上海一个独居女孩，被装进行李箱抛尸。


#### 11月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/14.png)

电竞战队EDG再夺冠，轰动全球。

上海迪士尼几万人封园做核酸。

双十一，董明珠隆重推出22岁的女助理孟羽童，“明珠羽童精选”直播间开播。


#### 12月

![](http://www.justdopython.com/assets/images/2022/01/weibohot/15.png)

娱乐圈优质偶像王力宏被曝渣男，彻底崩塌。

直播女王薇娅因偷漏税被罚了13.4亿。吃瓜群众惊呼，原来直播这么暴力。

西安出现“多源头不明的点状社区传播”，紧急“封城”。


### 总结

2021年是不平凡的一年，这一年，我们见证了太多。新冠疫情始终是笼罩我们上空的一团乌云。在这个特别的年份里，娱乐圈也是精彩不断，各种离婚事件层出不穷，几大优质形象瞬间成渣。

2022年也将是不平凡的一年，愿疫情早点过去，世界和我们都能更好！




> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/weibohot)
> 