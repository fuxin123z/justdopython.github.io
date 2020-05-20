---
layout: post     
title: 两个机器人在一起会碰撞出怎样的的火花？                         
category: 两个机器人在一起会碰撞出怎样的的火花？           
copyright: python                           
tagline: by 潮汐           
tags: 
  - 
---

大家有没有想过当两个机器人碰撞在一起会擦出怎样的火花呢？出于好奇心作祟，今天小编带大家一睹为快，看看当两个机器人碰撞在一起会产生怎样的结果？两个 AI 机器人的聊天小编使用 API 的方式访问，So 首先先进入两个机器人官网申请 API，这里小编用的是 图灵机器人和 茉莉机器人，思路也很清晰：直接申请 api 调用访问就 ok,是不是很 easy? 接下来咱们一起搞事情！

<!--more-->

### 茉莉机器人 

#### API 和 apikey 获取

在茉莉机器人官网注册后即可获取 api 和秘钥信息，如下图所示：
![api](https://imgkr.cn-bj.ufileos.com/5dd17173-73a2-4995-b767-464760fae425.png)

**api地址**：http://i.itpk.cn/api.php

**apikey**：

![apikey](https://imgkr.cn-bj.ufileos.com/8dbadf7c-d679-47e7-8912-64195a0b5537.png)

#### 调试环境

调试机器人需要用到 Python requests 库，构建 url和发送数据后调用即可：思路如下：

```python
import requests

send_data = {
   "question": '你的梦想是什么？',      #构建发送的数据
   "api_key": "a6ec389908bcc23fceb2bbe998e3313e",
   "api_secret": "bsa0yv06pl1p"
}
api_url = 'http://i.itpk.cn/api.php'
chat_content = requests.post(api_url, data=send_data)    #发送请求数据
print(chat_content.text)
```

**返回数据：**

```python
﻿当然是能有跟人类一样的智慧啦(⊙o⊙)…

Process finished with exit code 0
```


### 图灵机器人

#### API获取步骤

帮助文档-->机器人设置-->API接入教程-->获取接口地址
![api 获取步骤](https://imgkr.cn-bj.ufileos.com/1ec549ad-4fa5-449e-aa86-0cb5d3195aa5.png)

![接口地址](https://imgkr.cn-bj.ufileos.com/0d82297e-ddbb-4301-b4c8-c72ebd2608fc.png)

从上图可知api 接口地址为：http://openapi.tuling123.com/openapi/api/v2
#### 创建机器人
http://www.tuling123.com 在官网进行注册登陆，登陆后创建机器人，如下图所示：

![创建机器人](https://imgkr.cn-bj.ufileos.com/c08b6eca-6bf1-42fd-ae04-ae33979e649b.png)

#### 聊天和获取机器人 apikey

创建好以后可以看到机器人相关信息：

![聊天窗口](https://imgkr.cn-bj.ufileos.com/e5947b06-7e07-4676-b1d8-0e9ba025a66e.png)

机器人的 apikey 是唯一值

![apikey](https://imgkr.cn-bj.ufileos.com/60b73e79-e130-442a-8b97-cd1015cf901d.png)

####　调试调用环境

调试机器人需要用到 Python requests 库，构建 url和发送数据后调用即可：思路如下：

```python
import requests

send_data = {
   "key": "9fd874929409453991db78f8b46a446b",
   "info": '我叫你一声你敢答应吗',      #构建发送的数据
   "userid": "622952"
}
api_url = 'http://www.tuling123.com/openapi/api'
chat_content = requests.post(api_url, data=send_data)    #发送请求数据
print(chat_content.text)
```

返回数据为：

```python
{"code":100000,"text":"你叫一声不就知道了吗。"}
Process finished with exit code 0
```

### 两个机器人碰撞

当两个机器人碰撞在一起会擦出怎样的火花呢？请看他们精彩的表演吧！

```python
import requests
import time

question = input("请开始你们的表演：") # 输入问题开始表演

girl = "小姐姐"
boy = "小哥哥"

print(boy+':'+question)

while True:
    boy_data = {
       "key": "9fd874929409453991db78f8b46a446b",
       "info": question,      #构建发送的数据
       "userid": "622952"
    }
    boy_url = 'http://www.tuling123.com/openapi/api'
    boy_content = requests.post(boy_url, data=boy_data)    #发送请求数据
    print(boy + ':' + eval(boy_content.text)["text"])  # 用eval函数处理一下图灵返回的消息
    question = eval(boy_content.text)["text"]

    girl_data = {
        "question": question,  # 构建发送的数据
        "api_key": "a6ec389908bcc23fceb2bbe998e3313e",
        "api_secret": "bsa0yv06pl1p"
    }
    girl_url = 'http://i.itpk.cn/api.php'
    girl_content = requests.post(girl_url, data=girl_data)  # 发送请求数据
    print(girl + ':' + girl_content.text)
    time.sleep(1)
```
![聊天记录1](https://imgkr.cn-bj.ufileos.com/9478334c-efd0-4a81-ba0d-87c61e4e7c06.png)

![聊天记录2](https://imgkr.cn-bj.ufileos.com/da88334c-0307-4a05-baa7-77e6ea1e1f5e.png)

### 总结

当两个机器人碰撞在一起后会产生有趣的事情，比如下棋，玩游戏等等，更多有趣的知识待大家去挖掘，希望今天的文章对大家有帮助，能够提升读者朋友们的学习乐趣，愿大家早日走上人生巅峰！

### 参考

http://www.itpk.cn/

http://www.tuling123.com
