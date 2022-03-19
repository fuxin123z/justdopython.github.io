---
layout: post
category: python
title: 为了下载抖音上的小姐姐，我斥巨资做了个钉钉机器人，简直不要太爽
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/douyin/logo.png)

上一篇文章介绍了如何绕过抖音的的防爬虫机制来轻松下再抖音短视频，尤其特别适合批量下载。

但还有个问题就是，需要用到电脑，有时候坐公交时刷到喜欢的视频就难顶了，于是，我就想，能不能搞个服务，输入参数为抖音口令，输出为无水印视频链接。

技术人都懂得，这搞个 HTTP 接口不就可以了么，问题是，接口好搞，在手机上怎么调用呢？总不能直接通过浏览器以 GET 方式调用吧，这太不专业了。

于是，我就想能不能像微信聊天那样，把口令发给机器人，然后机器人调用接口，拿到结果之后再转发给我，我是不是很天才。

说干就干，说到机器人基本就是企业微信机器人和钉钉机器人了，倒是有一些第三方的服务商基于微信的协议开发了一些第三方机器人，但由于不是官方出版，感觉不太稳定，同时也有可能会对账号造成不可逆的伤害，于是就放弃了。

了解一番之后选定了钉钉机器人，无他，因为开发成本低易接入而已。

钉钉机器人也分很多种，基于当下的需求用企业内部机器人是最合适的，其实机器人就相当于一个消息中专站。

开发一款钉钉机器人分为三步，分别是新建、开发和上线。

### 注册机器人

登录钉钉开发者后台，依次选择应用开发 > 企业内部开发 > 机器人，点击创建应用。

![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5582337161/p260188.png)填写下应用名称、应用描述和应用图标三个信息即可创建成功。

创建完成之后应该是这个样子的。

![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5582337161/p260212.jpg)


至此，机器人创建完毕。

### 开发机器人

由于我们的口令是机器人帮我们转发的，所以就需要一个接受抖音口令的接口，虽说接口是我们开发，但接口的入参形式可不能随便定义，需要根据钉钉机器人的发送格式来确定。

```json
{
    "conversationId": "xxx",
    "atUsers": [
        {
            "dingtalkId": "xxx",
            "staffId":"xxx"
        }
    ],
    "chatbotCorpId": "dinge8a565xxxx",
    "chatbotUserId": "$:LWCP_v1:$Cxxxxx",
    "msgId": "msg0xxxxx",
    "senderNick": "杨xx",
    "isAdmin": true,
    "senderStaffId": "user123",
    "sessionWebhookExpiredTime": 1613635652738,
    "createAt": 1613630252678,
    "senderCorpId": "dinge8a565xxxx",
    "conversationType": "2",
    "senderId": "$:LWCP_v1:$Ff09GIxxxxx",
    "conversationTitle": "机器人测试-TEST",
    "isInAtList": true,
    "sessionWebhook": "https://oapi.dingtalk.com/robot/sendBySession?session=xxxxx",
    "text": {
        "content": " 你好"
    },
    "msgtype": "text"
}
```

以上就是钉钉机器人的数据推送格式，我们只需要关注 `text` 下的 `content` 即可，这个就是消息体了，也即是你发给机器人的内容，其余均不需关心。

那么，我们如何将消息发回给机器人呢，官方文档做了如下说明。

```
{
    "at": {
        "atMobiles": [
            "180xxxxxx"
        ],
        "atUserIds": [
            "user123"
        ],
        "isAtAll": false
    },
    "text": {
        "content": "我就是我, @180xxxxxx 是不一样的烟火"
    },
    "msgtype": "text"
}
```

其中 `text` 和 `msgtype` 是必穿参数，其余均非必传。

于是，我们的接口应该是这个样子的。

```python
from flask import Flask, request, jsonify

@app.route("/douyin", methods=["POST", 'GET'])
def compute():
    timestamp = request.headers.get("timestamp")
    sign = request.headers.get("sign")
    logger.info(F'timestamp = {timestamp}, sign = {sign}')
    data = request.get_data()
    data = json.loads(data.decode('utf-8'))
    content = data['text']['content']
    url = get_douyin_video(content)
    return jsonify({"msgtype": "text", 'text': {'content': F'提取完成 {url}'}})
    
app.run(host="0.0.0.0", port=80, debug=False)
```

至此，接口已开发完毕，直接部署到一个公网可以访问的服务器上就可以啦。

### 发布机器人

发布之前，需要把我们的接口配置到机器人上。

我们可以在机器人详情页，单击开发管理，配置开发信息。

提供服务器出口 IP 和消息接收地址就大功告成啦。
![](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5582337161/p260213.png)


正式发布之前，理应做下功呢调试，确保是功能正常。

在开发者后台对应的机器人应用详情页面，单击版本管理与发布，然后单击调试，可以进入测试群，该群里预置了开发者配置的机器人，可以在群里 @机器人 进行应答功能的测试。

测试通过之后，单机上线即可发布，发布完成之后，即可再群聊中添加该机器人。

> 添加路径：进入要使用机器人的群 >【群设置】>【智能群助手】>【添加机器人】，在企业机器人列表中即可找到


### 总结

来看下最终效果吧。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/03/dingding/001.png)

以后直接看到喜欢的视频直接把口令发给机器人就行啦，是不是很省事呀～

当然这个程序目前还有一些漏洞，比如官方文档说的需要对钉钉的推送做签名校验。简言之就是钉钉会在请求头里面附带时间戳和签名信息，接收方根据接收到的时间戳重新生成签名，之后对比签名是否匹配即可。

代码这里就不提供啦，官方文档有完整的验签代码，大家自行查看官方文档即可。

>机器人文档： https://open.dingtalk.com/document/group/enterprise-created-chatbot
>数据相应格式说明：https://open.dingtalk.com/document/group/message-types-and-data-format