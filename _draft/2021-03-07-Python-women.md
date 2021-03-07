---
layout: post     
title:  惊艳！用 Python 送女神们别样的礼物！
category: 惊艳！用 Python 送女神们别样的礼物！
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---
![](https://imgkr2.cn-bj.ufileos.com/93940758-3c22-4941-8499-a8dc31751bf1.jpg?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=eJJ3U290qFSLkwpSnqyf9NiS3Js%253D&Expires=1615213935)

今天是 3 月 8 日，统称三八妇女节！

但是！请注意，三八妇女节不是妇女的节日，而且一个很有特殊意义的节日，阿酱在这里先祝各位女神们节日快乐！

### 关于三八妇女节

三八妇女节不是妇女的节日，而且关于女权的事！

**三八妇女节由来：**

19世纪，资本主义迅速发展，资本家开始雇佣女工，但女工与男工同工不同酬，女工每天工作十六七个小时，没有休息日，境况十分悲惨。
1908年3月8日，1500名妇女在纽约市游行，要求缩短工作时间，提高劳动报酬，享有选举权，禁止使用童工。

5月，美国社会党决定以2月的最后一个星期日作为国bai的妇女节。1910年8月，第二届国际社会主义妇女代表大会在丹麦哥本哈根召开，大会通过将美国妇女举行游行示威的3月8日这一天定为国际妇女节。

而中国妇女第一次纪念三八节，是在1924年。在中国共产党的领导下，广州的劳动妇女联合了各界被压迫妇女举行纪念会。

在联合国介绍国际妇女节的网页上，把“三八”国际妇女节的起源归因于20世纪初期系列的妇女运动大事，这些事件包括：

1909年，美国社会党人将2月28日定为全国妇女日；

1910年，第二国际哥本哈根会议上以克拉拉·蔡特金为首的来自17个国家的100余名妇女代表筹划设立国际妇女节，但未规定确切的日期；

1911年3月19日，奥地利、丹麦、德国和瑞士等国有超过100万妇女集会庆祝国际妇女节；

1913年2月的最后一个周日，俄罗斯妇女以示威游行的方式庆祝了她们的国际妇女节；

1914年3月8日，欧洲多国妇女举行反战示威游行；

1917年3月8日（俄历2月23日），为纪念在一战中丧生的近200万俄罗斯妇女，俄罗斯妇女举行罢工，拉开了“二月革命”的序幕，4天后，沙皇被迫退位，临时政府宣布赋予妇女选举权。 

20世纪初这一系列发生在欧洲和美洲的女权运动共同促成了“三八”国际妇女节的诞生。

在当今社会，无论在家庭还是工作中，女性的地位显得越来越重要，一个女人结婚后需要平衡家庭和事业，在家中要照顾小孩，在外要努力工作！

所以我觉得 **女人：很伟大！**


### 给女神们特别的礼物

今天我用 Python 给女神们制作了别样的礼物，愿大家永远健康美丽！礼物详情如下：

![](https://imgkr2.cn-bj.ufileos.com/71a5c0ab-249a-4a92-be70-c31f71d6dadc.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=dTi07y%252FKsGze5FmvC6eguxpE8U4%253D&Expires=1615213969)

上图是今天送给女神们别样的礼物，上图由两部分组成，一部分是桃心，一部分是玫瑰花，python 分两部分完成巨作，详解如下：

**画桃心代码：**

```python

# 画大号爱心（位置随机）
for x, y in list(zip(list1, list2)):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor("#FF6A6A")
    t.begin_fill()
    t.pencolor("#FF6A6A")
    t.forward(40)
    t.circle(20, 180)
    t.right(90)
    t.circle(20, 180)
    t.forward(40)
    t.end_fill()
    t.penup()
    t.goto(x, y)
# 画中号爱心（位置随机）
for x, y in list(zip(list5, list6)):
    t.pendown()
    t.fillcolor("#FFA07A")
    t.begin_fill()
    t.pencolor("#FFA07A")
    t.forward(30)
    t.circle(15, 180)
    t.right(90)
    t.circle(15, 180)
    t.forward(30)
    t.end_fill()
    t.penup()
    t.goto(x, y)
# 画小号爱心（位置随机）
for x, y in list(zip(list3, list4)):
    t.pendown()
    t.fillcolor("#FFD39B")
    t.begin_fill()
    t.pencolor("#FFD39B")
    t.forward(20)
    t.circle(10, 180)
    t.right(90)
    t.circle(10, 180)
    t.forward(20)
    t.end_fill()
    t.penup()
    t.goto(x, y)
# 画点点（位置随机）
for x, y in list(zip(list7, list8)):
    t.pendown()
    t.fillcolor("#FF6A6A")
    t.begin_fill()
    t.pencolor("#FF6A6A")
    t.circle(3, 360)
    t.end_fill()
    t.penup()
    t.goto(x, y)
```

**画玫瑰花代码如下：**
```python
# 初始位置设定
s = 0.2
# t.setup(450*5*s, 750*5*s)
t.pencolor("black")
t.fillcolor("#FF4040")
t.speed(100)
t.penup()
t.goto(0, 900 * s)
t.pendown()
# 绘制花朵形状
t.begin_fill()
t.circle(200 * s, 30)
DegreeCurve(60, 50 * s)
t.circle(200 * s, 30)
DegreeCurve(4, 100 * s)
t.circle(200 * s, 50)
DegreeCurve(50, 50 * s)
t.circle(350 * s, 65)
DegreeCurve(40, 70 * s)
t.circle(150 * s, 50)
DegreeCurve(20, 50 * s, -1)
t.circle(400 * s, 60)
DegreeCurve(18, 50 * s)
t.fd(250 * s)
t.right(150)
t.circle(-500 * s, 12)
t.left(140)
t.circle(550 * s, 110)
t.left(27)
t.circle(650 * s, 100)
t.left(130)
t.circle(-300 * s, 20)
t.right(123)
t.circle(220 * s, 57)
t.end_fill()
# 绘制花枝形状
t.left(120)
t.fd(280 * s)
t.left(115)
t.circle(300 * s, 33)
t.left(180)
t.circle(-300 * s, 33)
DegreeCurve(70, 225 * s, -1)
t.circle(350 * s, 104)
t.left(90)
t.circle(200 * s, 105)
t.circle(-500 * s, 63)
t.penup()
t.goto(170 * s, -30 * s)
t.pendown()
t.left(160)
DegreeCurve(20, 2500 * s)
DegreeCurve(220, 250 * s, -1)

# 绘制一个绿色叶子
t.fillcolor('#00CD00')
t.penup()
t.goto(670 * s, -180 * s)
t.pendown()
t.right(140)
t.begin_fill()
t.circle(300 * s, 120)
t.left(60)
t.circle(300 * s, 120)
t.end_fill()
t.penup()
t.goto(180 * s, -550 * s)
t.pendown()
t.right(85)
t.circle(600 * s, 40)
# 绘制另一个绿色叶子
t.penup()
t.goto(-150 * s, -1000 * s)
t.pendown()
t.begin_fill()
t.rt(120)
t.circle(300 * s, 115)
t.left(75)
t.circle(300 * s, 100)
t.end_fill()
t.penup()
t.goto(430 * s, -1070 * s)
t.pendown()
t.right(30)
t.circle(-600 * s, 35)

t.done()
```

### 写在最后

以上就是今天给女神们特别的礼物，在这个专属的日子里希望每个美丽的小姐姐都貌美如花！活得潇洒！


### 参考

https://blog.csdn.net/su_2018/article/details/88351847

### 总结

祝女神们节日快乐，希望家里有女神的男同胞们好好爱惜身边的伴侣！


