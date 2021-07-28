---
layout: post
title: 自动抢票之 12306 抢票篇
category: python
tagline: by 某某白米饭
tags: 
  - python
  - 爬虫

---

大家好，这一篇是 12306 的自动预订车票篇，前篇已经撸完了 12306 的自动登录。小编希望小伙伴们能多给几个赞，以示鼓励。
<!--more-->

![](http://www.justdopython.com/assets/images/2021/07/12306_2/0.png)

### 查询车票

首先 selenium 打开到 `https://kyfw.12306.cn/otn/leftTicket/init` 购票查询车票页面。这个页面只有 2 个需要要模拟人工的操作：

1. 填写 出发地、目的地、出发日，点击查询按钮

![](http://www.justdopython.com/assets/images/2021/07/12306_2/1.png)

12306 的出发地、目的地、出发日的文本框用下面的代码自动写入似乎是没什么作用的。

```python
ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
self.driver.get(ticket_url)
self.wait.until(self.findElement(By.ID, 'fromStationText')).send_keys('上海')
self.wait.until(self.findElement(By.ID, 'toStationText')).send_keys('常州')
self.wait.until(self.findElement(By.ID, 'train_date')).send_keys('2021-07-23')
self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, '查询'))).click()
```

只能另辟蹊径了。在页面将目的地、出发地、出发日 填入，点击查询查询，惊喜的发现在 F12　控制面板下 cookie 中存放了日期值。

![](http://www.justdopython.com/assets/images/2021/07/12306_2/2.png)

可是没有看到出发地和目的地的汉字，猜测可能这些汉字被编码过了，在编码网站解析一番。

![](http://www.justdopython.com/assets/images/2021/07/12306_2/3.png)

于是就可以照猫画虎将编码过的目的地、出发地、出发日设置到　cookie　中，并刷新页面。

```python
self.driver.add_cookie({'name': '_jc_save_fromStation', 'value': '%u5E38%u5DDE%2CCZH'}) #常州
self.driver.add_cookie({'name': '_jc_save_toStation', 'value': '%u4E0A%u6D77%2CSHH'}) #上海
self.driver.add_cookie({'name': '_jc_save_fromDate', 'value': '2021-08-02'})
self.driver.refresh()
# 一个温馨提示弹窗
self.wait.until(self.findElement(By.LINK_TEXT, '确认')).click()

self.wait.until(self.findElement(By.LINK_TEXT, '查询')).click()
```
这时就将车票刷新出来了。

2. 找到车次所在的行，点击预定

这里用 XPath 语法找到车次所在的预订单元格，用判断浏览器地址是否改变的方式判断是否进入到预订页面。

![](http://www.justdopython.com/assets/images/2021/07/12306_2/4.png)

```python
# 是否进入预订页面
while self.driver.current_url == ticket_url:
    self.wait.until(self.findElement(By.LINK_TEXT, '查询')).click()
    time.sleep(2)
    try:
        a = self.driver.find_element_by_xpath("//tr[@datatran='K1511']/preceding-sibling::tr[1]/child::node()[last()]/a")
        if a.text == '预订':
            break
    except Exception as e:
        print("没有车次")
    
    a.click()
```

### 预订

在预订页面就简单了，只需要选择乘车人和票种、席别。将这些信息定义在数组中，有几个乘车人就定义几个数组元素。

![](http://www.justdopython.com/assets/images/2021/07/12306_2/5.png)

```python
passengers = ['xxx']
ticketType = ['成人票']
seatType = ['硬座（￥28.5）']
for index, p in enumerate(passengers, 1):
    self.driver.find_element_by_xpath("//label[text()='"+p+"']/preceding-sibling::input[1]").click()
    
    
    selectTicketType = Select(self.driver.find_element_by_id('ticketType_' + str(index)))
    selectTicketType.select_by_visible_text(ticketType[index - 1])
    
    selectSeatType = Select(self.driver.find_element_by_id('seatType_' + str(index)))
    selectSeatType.select_by_visible_text(seatType[index - 1])
    
    self.driver.find_element_by_id('submitOrder_id').click()
    
    self.driver.find_element_by_id('qr_submit_id').click()
```

到这里就可以使用手机支付火车票了。

### 总结

两篇文章写完了 12306 的抢票软件，大伙们只需要按照自己的需稍微的修改一下脚本，就可以在逢年过节抢抢抢了。

> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/12306)

