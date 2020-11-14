---
layout: post
category: python
title: 怎么自学python，大概要多久
tagline: by 太阳雪
tags:
  - python
  - 学习
---
2020年10月 TIOBE 排行榜超过了 Java，[历史上首次 Python 超越了 Java](https://mp.weixin.qq.com/s/djrPr34u0iYJmM31rcpy9A)，再次让许多朋友对 Python 产生了兴趣，今天我们来梳理下学习 Python 几个阶段或者级别，期望对持续进化的你有所帮助
<!--more-->

本文缘起于知乎上的一个提问：`怎么自学python，大概要多久？`，当时做了一个回答，这次重新整理了一遍，全文如下：

看了回答区的很多回答，感觉很专业也很详尽，觉得要回答多久的问题，需要先回答 **学习的目标是什么** 这个问题，这里将目标分为 入门、进阶、深入和终极四个部分来说明

## 入门：只是了解

Python 已然是最流行的语言，特别是在数据分析和机器学习风靡的情况下，Python 也受到了少儿编程的青睐，所以许多同学处于各种原因，只是需要了解一下

那么需要先了解 Python 环境搭建，了解一下操作系统的基本只是，比如环境变量、命令行工具等
然后安装 Python，并且可以在命令行中执行进入 Python，执行简单操作

![python 命令行](http://justdopython.com/assets/images/2020/11/how/01.jpg)

接着，在文件文件中，写入 `print(Hello World)`，保存，执行

![python 命令行](http://justdopython.com/assets/images/2020/11/how/02.jpg)

这就可以算入门了，整个过程不到一个小时

> 对应入门来说，推荐用命令行的方式，很多教成会推荐 Anaconda，PyCharm 等集成开发工具，虽然功能强大，界面美观，不太信息量太大，比如容易分散注意力，且不利用 Python 环境的理解

![入门](http://justdopython.com/assets/images/2020/11/how/03.jpg)

## 进阶：完成简单任务

要完成一些简单任务或者是写写脚本，比如处理下 Excel、Word、文本中的数据，做些文件处理操作，写个自娱自乐的小程序（非微信\支付宝\头条等小程序）等

只需要了解基本 Python 语法，比如变量定义，基础数据结构，判断语句，循环语句，方法定义等

另外学习一下相关软件包，比如 OpenPyXl （可参考[《Excel 神器 —— OpenPyXl》](https://mp.weixin.qq.com/s/Q9EmcBB-r-2b2AW0Qx1Hcw)）用于处理 Excel

Python-docx（可参考[《Word 神器 python-docx》](https://mp.weixin.qq.com/s/os7Y2HouQet873oey_6zUw)），用于处理 Word

Python 内置模块 os，用于处理文件系统，Pygame 简单游戏包（可参考[《做硬核老爸，我用 Python》](https://mp.weixin.qq.com/s/czcGKk6RTrZVi6-KRUAR0w)），用来做些好玩的游戏，等等

这一阶段，只要持续练习，一个月左右，就能熟练上手，做出自己想要的东西，提高工作效率

我公司有个通信设备工程师，为了方便调试主机，开始学 Python，不到一年时间，不仅解决了工作中的问题，得到了嘉奖，还成了部门 Python 专家，经常指导其他人学习 Python

![进阶](http://justdopython.com/assets/images/2020/11/how/04.jpg)

## 高级：构建应用系统

如果想让更多的人用自己写的程序，而不仅仅用于自己，就需要构建一个系统或者应用。

### Web 系统

需要学习 Flask（可以参考[《Web 开发 Flask 介绍》](https://mp.weixin.qq.com/s/czcGKk6RTrZVi6-KRUAR0w)） 或者 Django 等 Web 框架

更重要的是，需要了解网络基础知识，如 Http，域名，云服务器等

数据库处理等相关知识，如 Sql 语句，Mysql 数据库，或者 Sqlite 数据库等

安全相关知识，如 Session，token，OAuth 认证机制（可以参考[《OAuth2.0 简介》](https://mp.weixin.qq.com/s/9CYQzx68FV_AD2ITCigsQQ)）等

服务部署相关知识或技能，将自己的程序通过网络方式提供更多的人使用（可参考[《部署 Flask 应用》](https://mp.weixin.qq.com/s/b9Mmp0bSCmNVDzaExJlJ0w)）

### 桌面应用

比如在 Windows，或者 Linux 下的应用，需要了解操作系统相关知识

并学习 wxpython、PythonWin、PyGTK、PyQt 等软件包，像 wxpython 有强大丰富的功，并且支持跨平台的桌面应用，让你做的程序有更好的适应环境

Windows 下的应用，可参考[《公交闹钟 —— 再也不用白等车了》](https://mp.weixin.qq.com/s/3mz-FbB_ReD6M2b6RVSZTw)]，其中描述了如何构建一个Windows 定时任务，以及将 Python 程序打包成 `可执行文件` 的方式

如果要达到构建系统的目标，除了 Python 语言本身以及相关软件包的学习之外，更多的是需要学习网络、操作系统、编程思想、设计模式等方面的知识

如果是从头学习，至少需要半年使时间，如果要到达精通，且在商业项目中应用，则可能需要一到两年时间

![高级](http://justdopython.com/assets/images/2020/11/how/05.jpg)

## 深入：数据分析与机器学习

python 几乎是个万能的语言，特别实在数据分析和机器学习方面，因为其写更少的代码，做更多的事的理念，深受数据科学家们的追捧。

如果目标是做数据分析，首先需要对数据分析思想和过程有所了解（可以参考[《这个数据分析报告，居然没写一行代码》](https://mp.weixin.qq.com/s/TTHq1xpICu9fPGKdzfSs9g)）

然后需要学习，数据采集、数据整理、数据可视化等方面的知识或者技能：

- **数据采集**
基本上就是常说的爬虫，从网络上获取需要分析的数据，相关框架或者软件包有 Scrapy，Selenium，Requests 等

- **数据整理**
就是对要分析的数据进行清洗、分解、归类、转换等操作，常用的包有 Numpy、Pandas 等，可以以极为高效的方式处理完成任务，例如我写的一篇 [《干掉公式——Numpy就该这么学》](https://mp.weixin.qq.com/s/jhrdTBNXp4UEJWnvIisKuA)，从另一个侧面介绍了 Numpy 的强大

- **数据可视化**
只有能被人直观感受到，才能更多的发挥数据的价值，通过条形图、圆饼图、雷达图、散点图等直观有效的图像，将数据直观的呈现出来，是数据分析必不可少的环节，相关框架和软件包有 matplotlib、pyecharts、Dexplot 等，我写过一篇关于 Flask 和 pyecharts 结合的文件可以参考[《Python Flask 数据可视化》](https://mp.weixin.qq.com/s/UeXvan5hcTVRCAQurWJeOA)

如果你的目标是做数据分析，从头学起，坚持练习，三个月，就可以做基本工作了，这是找个相关数据分析的工作，不成问题，如果想要深入研究，数据分析、甚至机器学习相关的原理算法，并能应用自如，没个三五年估计很难做到

![深入](http://justdopython.com/assets/images/2020/11/how/06.jpg)

## 终极：成为专家

其实任何领域成为专家，有一个共识定律：一万小时定律，想成为 Python 的专家也不例外

python 之所以成为众多领域中首选的编程语言，并非 Python 是众多领域的核心，而是 Python 可以作为一种处理问题的思想和实现工具

所以更多的学习者是想将 Python 作为一种学习和工作的工具，提高某个领域中解决问题的效率，因此，如果目标是成为专家，可以先选择一个 Python 可以得到应用的领域，比如系统构建、数据分析、机器学习、视频游戏等等

然后通过在该领域的不断深入，使 Python 技能在该领域上得到最大限度的发挥，可能是个成为专家的捷径

如果问需要多久，只能说看造化了。

![终极](http://justdopython.com/assets/images/2020/11/how/07.jpg)

## 总结

无论你的目标是什么，都离不开不断的学习与实践

学习分为三个阶段，第一阶段是学，即了解和学习相关习知识；第二阶段是教，即跟着老师或者教材学；第三个阶段是练，这个阶段是最为重要，需要自己多练

希望这篇短文对你的学习之旅有所启发，祝你早日实现自己的目标。

## 参考

- <https://mp.weixin.qq.com/s/djrPr34u0iYJmM31rcpy9A>
- <https://www.zhihu.com/question/300985609/answer/1341878811>
