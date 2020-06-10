---
layout: post
title: 如何指数级提高阅读能力
category: python
tagline: by 闲欢
tags: 
  - python
---

![封面](http://www.justdopython.com/assets/images/2020/06/readwc/fm.jpeg)

在这个信息大爆炸的时代，各种纷繁复杂的信息都在吸引我们的注意力，我们也需要通过这些信息来掌握各种知识，提高我们的认知。但是我们每个人一天只有24小时，面对这些信息，我们没办法多线程操作，只能提高单线程的效率。因此，提高阅读理解能力，迅速掌握信息的核心思想显得尤为重要。
<!--more-->


## 现代人阅读的困惑

我记得一直以来，有本书叫做《如何阅读一本书》比较风靡，时常会出现在我的视野当中。

![如何阅读一本书](http://www.justdopython.com/assets/images/2020/06/readwc/howtoread.jpg)

这本书提出了阅读的三个层次：基础阅读、检视阅读和分析阅读，同时也告诉大家针对不同种类的书籍该怎样去阅读。

看到这里，你是不是以为我在打广告，会提供一个链接，指引你去买书？

不，我并没有为这本书打广告的意思（无辜脸）。我只是引用来说明，阅读是有方法论的。但是，无论这本书讲的是什么方法理论，其核心思想不过是教人们有效阅读一本书，提高阅读理解能力，并且从书中提炼出对自己有用的知识或者思想。

阅读书籍属于集中深度阅读，它需要你花成片的时间，去系统化阅读，从而获取到完整的系统性的知识。

在这个年代，对于一般人来说，我们平时集中深度阅读一本书是件奢侈的事情，更多的是碎片化阅读。我们或许会在公交上看时事新闻，或许会在地铁上看感兴趣的公众号文章，或许会在午休时看看豆瓣、知乎等等论坛文章。我们可能关注了几十上百个公众号，可能会有几个常逛的论坛，这些自媒体或者平台每天都会根据我们的兴趣或者习惯给我们推送各种信息。

这些信息加起来基本上会超出我们阅读的极限，所以我们一方面必须要对信息进行筛选，另外一方面需要提高阅读理解能力，快速有效的阅读。

由于信息太泛滥了，每篇文章提供者都会想尽办法在标题上下功夫，争取让读者看到标题就有点进去阅读的冲动。针对这样的标题，我怎么知道它的内容是名副其实的干货还是“李鬼”呢？

在这个自媒体时代，人人都是平台，人人都可以推送文章给自己的受众。但是每个人的写作能力是不一样的，水平高的作者可以很好地组织内容，让读者很容易了解文章的主题。水平不好的作者可能下笔千言，不能自已，洋洋洒洒写了一篇长文，主题却不能很好地体现出来。针对这种文章，我们可得费点劲去理解了。

说起来容易，做起来难。上面的情况会导致我们不能很快地对文章进行筛选，也有可能无法快速有效阅读。


## 秘密武器

我们分析了大家碎片化阅读的痛点，明确了大家的需求——筛选文章和快速有效阅读。

作为一名 Python 爱好者，我立志用 Python 来解决碰到的难题。我冥思苦想，杀死了不少脑细胞，头顶好像又光亮了一下。终于，在某个夜深人静的时候，想到了一个好的解决方案——词云。对，你没看错，就是我们经常使用的词云。它可以迅速地提取文章中词语的使用频次，并且直观地展示出来。

对于一篇文章来说，为了突出主题，代表主题的词语必定会使用更多的频次，因此，我只需要将一篇文章的词云做出来，就能很快地知道这篇文章的主题了。

有了这个想法之后，我奋笔疾书，很快就写出了简洁的代码：

```python
"""
@author: 闲欢
"""
from os import path
import numpy as np
import jieba.analyse
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt


class WordsCloudUtils:

    default_path = path.dirname(__file__)
    default_pic_name = 'wc.png' # 默认输出图片名称
    default_stop_words_file = 'stopwordsbd.txt' # 停用词库
    default_font_path = '/System/Library/Fonts/PingFang.ttc' # 字体库路径，下载字体后，替换成自己电脑的存放路径，这里是Mac的存放路径

    # 分词
    @staticmethod
    def split_text(text):
        all_seg = jieba.cut(text, cut_all=False)
        all_word = ' '
        for seg in all_seg:
            all_word = all_word + seg + ' '

        return all_word

    @staticmethod
    def gen_wc_split_text(text='There is no txt', max_words=None, background_color=None,
                          font_path=default_font_path,
                          output_path=default_path, output_name=default_pic_name,
                          mask_path=None, mask_name=None,
                          width=400, height=200, max_font_size=100, axis='off'):
        split_text = WordsCloudUtils.split_text(text)

        # 设置一个底图
        mask = None
        if mask_path is not None:
            mask = np.array(Image.open(path.join(mask_path, mask_name)))

        wordcloud = WordCloud(background_color=background_color,
                              mask=mask,
                              max_words=max_words,
                              max_font_size=max_font_size,
                              width=width,
                              height=height,
                              # 如果不设置中文字体，可能会出现乱码
                              font_path=font_path)
        myword = wordcloud.generate(str(split_text))
        # 展示词云图
        plt.imshow(myword)
        plt.axis(axis)
        plt.show()

        # 保存词云图
        wordcloud.to_file(path.join(output_path, output_name))

    @staticmethod
    def gen_wc_file(file_path, max_words=None, background_color=None,
                    font_path=default_font_path,
                    output_path=default_path, output_name=default_pic_name,
                    mask_path=None, mask_name=None,
                    width=400, height=200, max_font_size=100, axis='off'):
        if not len(file_path):
            print('没有文件路径！')
            raise Exception('没有文件路径！')

        with open(file_path) as file:
            jieba.analyse.set_stop_words(path.join(WordsCloudUtils.default_path, WordsCloudUtils.default_stop_words_file))  # 设置止词列表
            tags = jieba.analyse.extract_tags(file.read(), 1000, withWeight=True)
            data = {item[0]: item[1] for item in tags}
            # 设置一个底图
            mask = None
            if mask_path is not None:
                mask = np.array(Image.open(path.join(mask_path, mask_name)))
            wordcloud = WordCloud(background_color=background_color,
                                  mask=mask,
                                  max_words=max_words,
                                  max_font_size=max_font_size,
                                  width=width,
                                  height=height,
                                  # 如果不设置中文字体，可能会出现乱码
                                  font_path=font_path).generate_from_frequencies(data)

            # 展示词云图
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis(axis)
            plt.show()

            # 保存词云图
            wordcloud.to_file(path.join(output_path, output_name))

    @staticmethod
    def gen_wc_tags(tags, max_words=None, background_color=None,
                    font_path=default_font_path,
                    output_path=default_path, output_name=default_pic_name,
                    mask_path=None, mask_name=None,
                    width=400, height=200, max_font_size=100, axis='off'):
        # 设置一个底图
        mask = None
        if mask_path is not None:
            mask = np.array(Image.open(path.join(mask_path, mask_name)))
        wordcloud = WordCloud(background_color=background_color,
                              mask=mask,
                              max_words=max_words,
                              max_font_size=max_font_size,
                              width=width,
                              height=height,
                              # 如果不设置中文字体，可能会出现乱码
                              font_path=font_path).generate_from_frequencies(tags)

        # 展示词云图
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis(axis)
        plt.show()

        # 保存词云图
        wordcloud.to_file(path.join(output_path, output_name))

if __name__ == '__main__':
    # 传入3个参数：文章文件路径，底图路径，底图图片名称（不使用传None）
    WordsCloudUtils.gen_wc_file('./wxdt', mask_path='./', mask_name='blackheart.jpeg')
```

运行代码很简单，我们只需要将文章复制下来，放入文本文件中，然后在 main 方法中传入文件路径就行。我的代码还支持设置词云的形状哦。


## 验证效果

写完代码后，我迫不及待地想看看效果，于是我找到了2020年两会的政府工作报告，看看政府工作报告的主题是啥？

![2020工作报告](http://www.justdopython.com/assets/images/2020/06/readwc/gzbg2020.jpg)

看到这个词云，主题重点一目了然，不用完整地看报告，我也可以迅速解读一下政府工作报告：
- 防控疫情
- 稳发展，促就业
- 脱贫攻坚

是不是 so easy ？刚好看到我的大哥“纯洁的微笑”发了一篇公众号文章，忍不住想拿来试验一把，看看是不是文不对题（冒死尝试）。他的文章标题叫做《当年，我也靠摆地摊，小赚了一把！》，我把文章内容复制到文本中，运行程序，得到了下面的词云。

![当年，我也靠摆地摊，小赚了一把！](http://www.justdopython.com/assets/images/2020/06/readwc/bt.jpg)

除去“摆地摊”这个主旨之外，我还看到了“大四”、“学姐”、“城管”、“QQ”等大字。看来微笑哥这篇文章是给我们讲了他在大四摆地摊发生的故事，于是我展开了丰富的联想：一方面他可能因为摆地摊跟城管玩起了躲猫猫的游戏，另一方面他可能通过摆地摊索要了学姐的QQ，进而学姐变成了女朋友？

看了文章内容之后，我发现他这篇文章确实是在讲摆地摊相关的事情，至于我的联想好像是误入歧途了（失落ing）。不过这样也足够了，我能够迅速知道文章内容是不是与标题相关，从而可以确定我是不是感兴趣。至于针对关键词的丰富联想就是这个功能附带的福利了，特别是有故事情节的文章，可能通过这种关键词组合联想，然后再去阅读文章，验证自己的联想，也不失是一件趣事。

有了这个工具之后，我要做的第一件事情就是去清理我的微信收藏，以及印象笔记收藏了。以前看到感兴趣的标题都会先收藏起来，想着有时间了拿出来看看，结果却是很少去看。正好趁这个机会去清理一批标题党！


## 总结

本文主要是讲述用词云工具来解决我们碎片化阅读时筛选文章和快速掌握文章主旨的问题。一段简单的 Python 代码，能够为我们节省很多时间，也可以帮助我们快速理解一篇文章的主旨，这就是 Python 的魔力！


> 示例代码 (https://github.com/JustDoPython/python-examples/tree/master/xianhuan/readwc)












