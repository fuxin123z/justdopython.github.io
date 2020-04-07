---
layout: post     
title:  今天，我用 Python 给武汉人民发一封邮件                                             
category: 今天，我用 Python 给武汉人民发一封邮件 
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

2020 年，庚子病痛，从寒冬发酵，一种突然爆发的不知名病毒在无形中慢慢侵蚀一座城----湖北武汉，后经专家检测这是一种带冠状的新型病毒，和 SARS 很相似，感染力很强，潜伏期在 14 天左右。

<!--more-->

随着病毒的蔓延、感染人数不断增加，同时遇上春节将至，2020 年 1 月 23 日湖北省疫情防控指挥部发布封城通告：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407152503292.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

按下暂停键的湖北武汉以及其他地区在无声的和病魔斗争，在习主席的亲自指导下，在无数个前线医务人员的奋战下，在全国人民的积极配合下，中国打赢了这场胜仗，今天（2020年4月8日） 0 点武汉正式解除离鄂通道管制，也就是从今天开始，武汉就解除封城了，他们自由了。从新冠肺炎病毒爆发到 1 月 23 日武汉封城，再到今天武汉解封，等这一天的到来，武汉人民等了整整 77 天，他们也许是在等，古琴台上觅知音，黄鹤楼中故人归；但是不管经历了多少挫折和磨难，不管磨难过后是多么伤痕累累，只要山高水阔，他们便能重振旗鼓，一往无前，不管经历了什么，英雄还是那个英雄，终有归期！

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407152647473.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

今天我用 Python 给武汉人民发一封邮件，给这座英雄城市致敬，给前线的战士们致敬，让我们共同等待这座城市的伤口痊愈，我相信，当我们见面的时候，春会再来，花会再开，而看花人里，有一个是你。

### SMTP发送邮件原理

SMTP（Simple Mail Transfer Protocol）-简单邮件传输协议, 它是一组用于由源地址到目的地址传送邮件的规则，由它来控制信件的中转方式。python 的 smtplib 提供了一种很方便的途径发送电子邮件。它对 smtp 协议进行了简单的封装。下面是电子邮件主要构件和 SMTP 发送邮件的过程示意图：

![电子邮件主要构件](https://img-blog.csdnimg.cn/20200407163424334.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

![发送邮件示意图](https://img-blog.csdnimg.cn/20200407162950674.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

#### SMTP协议工作原理：

SMTP 工作在两种情况下：一是电子邮件从用户端传输到服务器：二是从某一个MTA(Message Transfer Agent)传输到另一个MTA。SMTP也是请求/响应协议，命令和响应都是基于NVT ASCII文本，并以CR和LF符结束。响应包括一个表示返回状态的三位数字代码。SMTP在TCP协议25号端口监听连续请求。

#### SMTP连接和发送过程

 1. 建立TCP 连接。
 2. 客户端发送 HELO 命令以标识发件人自己的身份，然后客户通过发送 MIAL 命令标识出电子邮件的发起人；服务器端正希望以 OK 作为响应，表明准备接收。
 3. 客户端发送 RCPT 命令，以标识该电子邮件的计划接收人，可以有多个RCPT行；服务器端则表示是否愿意为收件人接收邮件。
  
 4. 协商结束，发送邮件，用命令DATA发送。
  
 5. 以“.”号表示结束输入内容一起发送出去，结束此次发送，用QUIT命令退出


### Python 使用 SMTP 发送邮件
在 python 中，发送邮件主要包括 email 和smtplib，其中 email 实现邮件构造，smtplib 实现邮件发送。在smtplib库中，主要主要用smtplib.SMTP()类，用于连接SMTP服务器，并发送邮件。

**python 中通过 SMTP 发送邮件主要步骤如下：**
　
1. 开通邮箱SMTP服务，获取邮箱授权码，邮箱 SMTP 开通路径（以 QQ 邮箱为例）：邮箱设置/账户/POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
![邮箱账户设置](https://img-blog.csdnimg.cn/20200407165900988.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407165957649.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407170036666.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)
按照如上步骤开启。开启后点击链接生成授权码，按照步骤操作拿到相应的授权码即可。

2. 编辑邮件内容，主要包括三部分内容：信封，首部和正文；其中信封包括发送邮箱，接收邮箱等；

3. 初始化配置信息，调用SMTP发送邮件
4. QQ 邮箱 SMTP 服务器地址：smtp.qq.com，ssl 端口：465。


**Python 创建 SMTP 对象语法如下：**

```python
 import smtplib

smtpObj = smtplib.SMTP( [host [, port [, local_hostname]]] )

```
**参数详解：**
- host: SMTP 服务器主机。
- port: 如果你提供了 host 参数, 你需要指定 SMTP 服务使用的端口号，一般情况下 SMTP 端口号为25。
- local_hostname: 如果 SMTP 在你的本机上，你只需要指定服务器地址为 localhost 即可。


**发送邮件语法：**

```python

SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options])

```

**参数说明：**
- from_addr: 邮件发送者地址。
- to_addrs: 字符串列表，邮件发送地址。
- msg: 发送消息

###  Python 发送 QQ 邮件示例

 Python 发送邮件实例部分代码如下：
 
```python
def send_email():
    ret = True
    try:
        msg = MIMEText('待花开时，邀您一起赏花吃热干面，我们重新拥抱这座城市的热情', 'plain', 'utf-8')

        msg['From'] = formataddr(["知心。。。。", my_sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["知心。。。。", my_user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "静待归期！"  # 邮件主题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25

        server.login(my_sender, my_psw)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、授权码、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

ret = send_email()
```
**以上结果显示为：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407185924591.png)

### python 发送带附件邮件
Python 发送的邮件如果是附件，则需要用 add_header 加入附件的声明。

MIME有很多种类型，这个略麻烦，如果附件是图片格式，我要用MIMEImage，如果是音频，要用MIMEAudio...
对象类型如下：

- MIMEBase   
   - - MIMEMultipart  
   - -  MIMENonMultipart
     	- - - MIMEMessagel：其他信息
     	 - - -  MIMEText ：  文本
     	 - - -  MIMEImage：图片

最懒的方法就是，不管什么类型的附件，都用MIMEApplication，MIMEApplication默认子类型是application/octet-stream，使用部分示例如下：

```python
# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("潮汐同学", 'utf-8')
message['To'] =  Header("武汉人民", 'utf-8')
subject = '荆楚疫情去'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('南山镇守江南之都，且九州一心！月余，疫尽去，举国庆之！', 'plain', 'utf-8'))
message.attach(MIMEImage(''))
# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('./test.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test.txt"'
message.attach(att1)

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25

    server.login(my_sender, my_psw)  # 发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, my_user, message.as_string())
    server.quit()  # 关闭连接
```

**以上结果为：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407190042424.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

**附件可下载、可预览，显示结果为：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407190058425.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)


### Python 发送图片文件

最后小编同学精心制作了一副纪念日宣传图来纪念这特殊的日子，并且将这幅图片以邮件的形式发送出去，示例代码如下：

```python
def send():
    subject = "解封纪念日"  # 主题
    msg = MIMEMultipart('related')
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
    # msg = MIMEText(content)
    msg.attach(content)
    msg['From'] = Header("潮汐同学", 'utf-8')
    msg['To'] = Header("武汉人民", 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    file = open("./picture.png", "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    msg.attach(img)
    
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(my_sender, my_psw)
        s.sendmail(my_sender, my_user, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
```
输出结果为：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407191608407.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzEyOTc1MA==,size_16,color_FFFFFF,t_70)

### 总结

谨以此片纪念今天这个特殊的日子！
最后请大家还是要多注意，武汉解封不等于解防,江城市民仍要加强自我约束,不扎堆不聚集,非必要不出门，平时多喝水、勤洗手！祝大家安好！

> 申明：今天文章中的所有实例都是使用小编自己的 QQ 邮箱做实验，大家在后续自己实践的时候可以做相应的修改