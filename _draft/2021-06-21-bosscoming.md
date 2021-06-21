---
layout: post
title: 为了上班摸鱼，我用Python开发“BOSS来了”！
category: python
tagline: by 闲欢
tags: 
  - python
  - 摸鱼
---

作为打工人来说，特别是996,、007的工作，除了干饭之外，最紧张刺激的莫过于上班的时候偶尔偷偷闲，去池塘里面摸摸鱼。

![996摸鱼](http://www.justdopython.com/assets/images/2021/06/bosscoming/1.jpg)

一般人摸得哪些鱼呢？聊天、微博、微信朋友圈、小游戏、小说、股票基金等等。

摸鱼的最大阻碍是什么？当然是包工头（老板）了，他们恨不得打工人24小时不间断地干活。

![老板抓摸鱼](http://www.justdopython.com/assets/images/2021/06/bosscoming/2.jpg)

但是人的精力是有限的，一天只能集中精力干那么几个小时，其他时间需要通过摸鱼来调剂有限，所以我们只要摸鱼不被包工头发现，那是相当愉快的一件事情。

为此，我用 Python 写了一个小工具——BOSS 来了，来监控老板，减少摸鱼被发现的概率。

<!--more-->

### 思路

我们知道，每台电脑或者手机等终端都有一个固定的 Mac 地址，而我们公司办公区域有几个 AP ，大家手机连接的都是距离自己最近的 AP ，所以理论上如果我知道老板手机的 Mac 地址，然后扫描局域网的所有 Mac 地址，如果出现老板手机的 Mac 地址，那么老板大概率是在我附近的，此时摸鱼比较危险；如果没有出现老板额 Mac 地址，那么老板可能离我比较远，此时摸鱼比较安全。

基于上面思路，我要做的就是搞到老板手机的 Mac 地址，然后不断轮询局域网的所有 Mac 地址，一旦发现出现老板手机的 Mac 地址，我就老老实实干活，一旦老板的 Mac 地址消失了，就可以摸鱼了。


### 实现

#### 获取老板手机Mac地址

怎么搞到老板的手机 Mac 地址？

好多人听到这个可能就感觉没戏了！总不能把老板的手机偷过来，然后去设置里面找吧。

天无绝人之路，只要肯动脑，办法可不少！

我的方法是这样的。当其他同事没有走动的时候，老板来的时候，保存一次局域网的 Mac 地址信息，当老板走的时候再保存一次，然后比对，找出老板手机的 Mac 地址。为了确保准确性，可以多试几次。

![机智如我](http://www.justdopython.com/assets/images/2021/06/bosscoming/3.jpg)

#### 获取所有Mac地址

第一步，使用 `ipconfig/all` 命令，可以找到当前所处的网段：

![网段](http://www.justdopython.com/assets/images/2021/06/bosscoming/4.jpg)

第二步，使用轮询命令逐个 `ping` 网段内的 IP ，这一步是为了建立 ARP 表。命令如下：

> for /L %i IN (1,1,254) DO ping -w 1 -n 1 192.168.1.%i 

其中，192.168.1.%i 是要查询的网段。

第三步，使用 `arp` 命令可以查询所有的Mac地址，命令为：

> arp -a

运行之后，你会看到类似下面的结果：

![mac地址列表](http://www.justdopython.com/assets/images/2021/06/bosscoming/5.jpg)


#### 代码实现

思路已经得到验证，准备工作也做好了，接下来就是代码实现了。

首先，我们根据上面的思路，先写一个获取局域网所有的 Mac 地址的方法。

```python

def get_macs():
    # 运行cmd控制窗口，输入“arp -a”，并将内容传递到res中
    res = os.popen("arp -a")
    # 读取res数据，转换为可读数据
    arps = res.read()
    print(arps)

    # 将获得的counts中的数据根据“换行符”来进行分割切片
    result = arps.split('\n')

    # 设一个空列表装ip
    ips = []
    # 设一个空列表装mac
    macs = []

    # 遍历
    for i in range(1, len(result)):
        # 获得列表中第idx个数据
        line = result[i]
        if ('Internet' in line) | ('' == line) | ('接口' in line):
            continue
        # 根据“ ”进行切片
        line_split = line.split(" ")
        index = 0
        for l in line_split:
            if l != '':
                index += 1
                if index == 1:
                    ips.append(l)
                elif index == 2:
                    macs.append(l)

    return ips, macs

```

然后，写一个定时轮询。

```python

# 老板的Mac地址
bossMac = "01-00-5e-0b-14-01"
sleep_time = 5
while 1 == 1:
    time.sleep(sleep_time)
    ips, macs = get_macs()
    is_come = 0
    for mac in macs:
        if mac == bossMac:
            is_come = 2
            # 如果boss来了，就隔5分钟扫描一次
            sleep_time = 300
            # 提示报警
            choice = g.msgbox(msg="有内鬼，终止交易！", title="OMG")
            break
    if is_come == 0:
        # 如果boss走了，就隔5秒钟扫描一次
        sleep_time = 5
        g.msgbox(msg="一切正常！", title="OMG")

```

我这里设定的是：如果老板出现了，就每隔 5 分钟轮询一次，因为老板在的话，要集中精力干活，不能太过频繁地想着摸鱼。如果老板走了，就每隔5秒钟轮询一次，摸鱼的时候还是要频繁预警比较好！

运行程序，当老板来时，预警弹窗是这样子的：

![有内鬼](http://www.justdopython.com/assets/images/2021/06/bosscoming/6.jpg)

当老板消失后，弹窗内容是这样的：

![老板走了](http://www.justdopython.com/assets/images/2021/06/bosscoming/7.jpg)


### 总结

当然，如果老板没有开 WiFi ，那么这个方法就失效了。或者老板过来了，但是 手机反应慢了，没有切换到这边的 AP ，那也会存在危险。所以不要完全依赖这个小工具，摸鱼的时候还是要偶尔观察一下周围环境。

最后，还是得提醒一下大家：少摸怡情，大摸伤身！


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/bosscoming)