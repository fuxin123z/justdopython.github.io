---
layout: post     
title:  Python 小技能之抓取天气信息发送给小姐姐      
category: Python 小技能之抓取天气信息发送给小姐姐  
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

每天一个 Python 小技巧，你学废了吗？
今天文章主要讲解如何将天气预报信息爬取下来并发送给小姐姐，感兴趣的朋友不妨试试，说不定会有意外收获呢！

### 抓取数据

爬虫的基本思路简易了解就三步：下载数据（根据需要爬取的 url 设定用户代理）、解析数据（编写爬取规则并获得数据）、保存数据。

知道上述步骤后咱们的需求是首先找到中国天气网链接 https://tianqi.so.com/weather/ ，抓取中国天气网的数据，获取天气信息部分代码如下：

```python
    data_list = []
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')  # 自动补全html代码，并按html代码格式返回
    
	wendu = soup.find('div', class_='temperature').get_text()
	
    tianqi = soup.find('div', class_='weather-icon-wrap').get_text()
	
    data_list.append("现在的温度：%s\n现在天气情况：%s" % (wendu, tianqi))
	
    list = soup.find_all('ul', class_='weather-columns')
	
    for item in list:
        data_list.append(item.get_text())
		
    print("列表数据：",data_list)
    a = 1
	#创建PrettyTable对象，用于将天气数据用表格的方式输出
    tb = pt.PrettyTable() 
    tb.field_names = ["日期","天气","详情"]
	
    for item in data_list:
        # print(a)
        if a != 1:
            tb.add_row([item.strip().split()[0]+item.strip().split()[1],item.strip().split()[2],item.strip().split()[3]])
        else: print(item.strip())
        a+=1
		
    print(tb)
    return tb
	
```
输出结果为：

```
现在的温度：23
现在天气情况：多云

+-------------+--------------+----------------+
|     日期    |     天气     |      详情      |
+-------------+--------------+----------------+
| 今天(07-28) |    雷阵雨    | 22/31℃优西南风 |
| 明天(07-29) |     多云     | 24/32℃良西南风 |
| 周四(07-30) |      阴      | 25/33℃良西南风 |
| 周五(07-31) |    雷阵雨    | 24/33℃良西南风 |
| 周六(08-01) |     多云     | 25/34℃良西南风 |
| 周日(08-02) | 中雨转雷阵雨 |  24/33℃优南风  |
| 周一(08-03) |     多云     |  25/32℃优东风  |
| 周二(08-04) |     小雨     | 22/32℃良东南风 |
| 周三(08-05) |   小雨转阴   |  22/32℃良南风  |
| 周四(08-06) |     小雨     | 22/32℃良东北风 |
| 周五(08-07) |  多云转小雨  |  21/33℃良南风  |
| 周六(08-08) |     小雨     | 21/34℃良西南风 |
| 周日(08-09) |  多云转小雨  |  21/34℃良南风  |
| 周一(08-10) |     小雨     |  21/34℃良南风  |
| 周二(08-11) |  多云转小雨  |  21/33℃良南风  |
+-------------+--------------+----------------+
```

### 发送邮件

将抓取的数据发送到相应的邮箱中，这里我将内容发送到自己的 QQ 邮箱，发送邮箱详细思路请详见 今天，我用 Python 给武汉人民发一封邮件，发送邮件代码如下：

**实现代码：**

```python
# 收件人
    receiver = receiver
    mail_title = '小姐姐，请查收今天以及往后15天的天气预报，愿你三冬暖，春不寒'
    mail_body = str(msg)
    # 创建一个实例
    message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文 
	# (plain表示mail_body的内容直接显示，也可以用text，则mail_body的内容在正文中以文本的形式显示，需要下载）
	
    
    # 邮件的发件人
	message['From'] = sender 
    # 邮件的收件人
	message['To'] = receiver  
	# 邮件主题
    message['Subject'] = Header(mail_title, 'utf-8')  
	
	# 创建发送邮件连接
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)  
	
	# 连接发送邮件的服务器
    smtp.connect(smtpserver)  
	
	# 登录到邮件服务器
    smtp.login(username, password)  
	
	# 填入邮件的相关信息并发送
    smtp.sendmail(sender, receiver, message.as_string())  

    smtp.quit()
```


### 调用发送邮件方法


```python
if __name__ == '__main__':
    sender = 'XXX@qq.com'
    # 发件人邮箱的SMTP服务器（即sender的SMTP服务器）
    smtpserver = 'smtp.qq.com'
    # 发件人邮箱的用户名和授权码（不是登陆邮箱的密码）
    username = 'XXX'
    # 邮箱授权码
    password = 'XXXXXXXXX'
    url1 = 'https://tianqi.so.com/weather/'
    receiver_list ='XXX@qq.com'
    tb = get_Data(url1) #获得每一个用户的数据
    send_mail(tb,receiver_list) #发送邮件
```

**发送结果如下：**

![](https://imgkr.cn-bj.ufileos.com/37ff25e3-e983-4e3f-99c7-c02ce330ea4a.png)

 
### 总结

今天的文章主要是使用 Python 爬虫和邮件发送功能两者结合使用的场景，如果学废的小伙伴请 扣 1，咱们明天见！


> 示例代码 [Python 小技能之抓取天气信息发送给小姐姐 ](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/send_weather)