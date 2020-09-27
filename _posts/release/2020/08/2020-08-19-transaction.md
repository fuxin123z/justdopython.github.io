---
layout: post
category: python
title: 一文讲懂数据库隔离级别
tagline: by 豆豆
tags: 
  - python100
---

相信做后端开发的童鞋肯定没少和数据库打交道，提起数据库，又不能不说数据库事务隔离级别，毕竟这是保证数据可靠一致的重要基石。网上介绍数据库隔离级别的文章大都很生硬，理论居多，今天派森酱就用一个简单的故事来给大家说说隔离级别。

<!--more-->

奋斗多年，派森酱攒了些积蓄，想着总给别人打工也不是长久之计，于是萌生辞职创业的念头，和自己的同窗好友蟒蛇君合计之后觉得可行，于是就炒了老板鱿鱼自己当老板去啦。

别看派森酱这几年在公司闷头写代码，业余之际也没忘记给自己充电。产品，运营，市场，公关，财务等他都略知一二，本着勤俭节约的原则，派森酱每周都会拉着蟒蛇君一起对账，以便控制不必要的开支，这天他们突然发现公司账面上的钱和实际的好像对不上，公司账上少了一万大洋。这可把俩人吓坏了。

## 数据丢失

从傍晚核对到凌晨，二人终于发现了其中的猫腻，原来是因为他们同时操作了公司账户。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/001.png)

派森酱添加的一万大洋给丢失了。

这可难不倒派森酱，毕竟程序员出身，很快就找到了解决之道。加锁呀，遇事不决先加锁[狗头]。他们把这个锁叫做 X 锁，该锁有一个特点，就是在同一时刻只可以有一人持有，在未释放之前，另外一个人无法获得该锁。于是，通过加锁的方式巧妙地将二人的并行操作变成了串行，完美地解决了同时修改同一行数据造成数据丢失的问题。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/002.png)

这就是数据库最低的隔离级别 「Read uncommitted 读未提交」。可以解决数据丢失问题。

## 脏读

自此以后，派森酱和蟒蛇君在写数据的时候都要加上 X 锁才行，程序运行了很久都没发现什么问题，直到有一天，公司账上又多了一万大洋。

蟒蛇君说：老弟，是不是我们的锁有问题呀。

“不可能，加锁我可是专业的”。派森酱说。

说完，派森酱立马在脑海中构思着各种可能，终于，想到了些什么。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/003.png)

我读取到了你回滚的数据，所以，钱就多了。

”老弟，我读取数据的时候，你不能回滚啊，这样我读取的数据就是不靠谱的了，他们已经是「脏数据」了“。派森酱怨声载道。

蟒蛇君：“那怎么行，难道我操作错了也不可以回滚吗，这也太霸道了。要不我们读取数据的时候也加一个 X 锁吧。”

不不不，这样子太严格了，但是我们可以弄一个新的锁出来，简称 S 锁，用于读取数据。

这个锁和 X 锁有所区别，如果一行数据加了 X 锁，就不可以再加 S 锁了，同样加了 S 锁也不可以再加 X 锁，但是加了 S 锁的记录可以再加 S 锁。简言之就是 X 锁和 X 锁是互斥的，X 锁和 S 锁是互斥的，S 锁和 S 锁是不互斥的。

同时为了避免影响数据的写入，读取完数据之后我们要立马释放 S 锁。

于是，脏数据的问题也被派森酱给解决了。

这就是二级隔离级别 「Read committed 读提交」。可以解决数据丢失、脏读问题。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/004.png)

## 不可重复读

又到了周末对账时刻，刚好是月底，派森酱要核对下上月余额与当前月余额的差额，是否和明细都能对得上。由于本月流水较多，对到一半俩人有点累了，于是俩人就先把差额给记录了下来，假设为 10000 - 500 = 9500，就去吃饭去了，然后回去接着对，这一停不要紧，回来后发现钱变少了。俩人心态崩了。

怎么回事，二人疯狂分析日志，看看能否找到蛛丝马迹。

原来在他们吃饭的过程中，银行自动扣了本月税收。这可尴尬了，我读数据时，咋还有人改呢。刚开始是 11000 ，现在变成了 7100。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/005.png)

问题就出在 S 锁的释放时刻，读取完立马释放，就容易被人见缝插针，我们要一直持有 S 锁才行，直到把事务提交上去。

于是，不可重复读的问题也被解决。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2020/08/transaction/006.png)

这就是三级隔离级别「Repeatable read 可重复读」。可以解决数据丢失、脏读、不可重复读问题。这也是 MySQL 的默认隔离级别。

## 幻读

后来公司越做越大，公司员工也越来越多，这天派森酱心情大好，就想着给公司的员工多发点福利，本月每人增加 1000 绩效奖，于是执行了下面的语句。

```sql
SELECT name, salary FROM xxx;
UPDATE xxx SET salary = salary + 1000;
```

更新完之后派森酱想确认下是否全部都修改了，就又查询了一遍，这一查发现果然有一个人没有改。

原来，在派森查询和更新的中间，蟒蛇君又新增了一条数据，这又引发了新的问题。

咋处理个数据就这么麻烦呢。

没办法，要想避免这个问题，我们只能一个一个串行执行，要保证同一时刻只能有一个人操作数据库。

这就是隔离界别的最高级别了 「Serializable 串行化」。可以解决数据丢失、脏读、不可重复读、幻读问题

## 总结

至此我们说完了数据库的隔离级别，他们是层层递进的关系，事实上，通过加锁的方式完全可以实现，只不过会严重影响生产效率。下一篇文章我们来看看数据库大叔们到底是是如何实现这么复杂的隔离级别的。

## 参考

https://mp.weixin.qq.com/s/tSF_w9xUOj3Q2hmOxJkwLg