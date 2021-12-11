---
layout: post
category: python
title: 几行代码，撸了个 元宇宙？！
tagline: by 李晓飞
tags:
  - 技术
  - 元宇宙
---
![封面](http://www.justdopython.com/assets/images/2021/12/superwomen/00.png)

Facebook 改名为 meta，一下子点燃了 元宇宙 这个概念。

今天我就用 Python 实现一个简单的迷你元宇宙。

代码简洁易懂，不仅可以学习 Python 知识，还能用实践理解元宇宙的概念。

还等什么，现在就开始吧！

## 迷你元宇宙

什么是元宇宙？

不同的人有不同的理解和认识，最能达成共识的是：

> 元宇宙是个接入点，每个人都可以成为其中的一个元素，彼此互动。

那么我们的元宇宙有哪些功能呢？

首先必须有可以接入的功能。

然后彼此之间可以交流信息。比如 a 发消息给 b，b 可以发消息给 a，同时可以将消息广播出去，也就是成员之间，可以私信 和 群聊。

另外，在元宇宙的成员可以收到元宇宙的动态，比如新人加入，或者有人离开等，如果玩腻了，可以离开元宇宙。

最终的效果像这样：

![效果](http://www.justdopython.com/assets/images/2021/12/meta/01.png)

## 设计

### 如何构建接入点

直接思考可能比较困难，换个角度想，接入点其实就是 —— 服务器。

只要是上网，每时每刻，我们都是同服务器打交的。

那就选择最简单的 TCP 服务器，TCP 服务器的核心是维护套接字（socket）的状态，向其中发送或者获取信息。

python 的 socket 库，提供了很多有关便捷方法，可以帮助我们构建。

核心代码如下：

```python
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((ip, port))
socket.listen()

data = socket.recv(1024)
...
```

创建一个 socket，让其监听机器所拥有的一个 ip 和 端口，然后从 socket 中读取发送过来的数据。

### 如何构建客户端

客户端是为了方便用户链接到元宇宙的工具，这里，就是能链接到服务器的工具，服务器是 TCP 服务器，客户端自然需要用可以链接 TCP 服务器的方式。

python 也已为我们备好，几行代码就可以搞定，核心代码如下：

```python
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip, port))

data = client.recv(1024)
...
```

代码于服务器很像，不过去链接一个服务器的 ip 和 `端口`。

### 如何构建业务逻辑

首先需要让服务器将接入的用户管理起来。

然后当接收到用户消息时做出判断，是转发给其他用户，广播还是做出回应。

这样就需要构造一直消息格式，用来表示用户消息的类型或者目的。

我们就用 `@username` 的格式来区分，消息发给特殊用户还是群发。

另外，为了完成注册功能，需要再定义一种命令格式，用于设置 `username`，我们可以用 `name:username` 的格式作为设置用户名的命令。

## 构建

有了初步设计，就可以进一步构建我们的代码了。

### 服务端

服务器需要同时响应多个链接，其中包括新链接创建，消息 和 链接断开 等。

为了不让服务器阻塞，我们采用非阻塞的链接，当链接接入时，将链接存储起来，然后用 select 工具，等待有了消息的链接。

这个功能，已经有人实现好了 [simpletcp](https://github.com/fschr/simpletcp 'simpletcp')，只要稍作改动就好。

将其中的收到消息，建立链接，关闭链接做成回调方法，以便再外部编写业务逻辑。

#### 核心业务

这里说明一下核心代码：

```python
# 创建一个服务器链接
self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self._socket.setblocking(0)
self._socket.bind((self.ip, self.port))
self._socket.listen(self._max_connections)

# 存放已建立的链接
readers = [self._socket]
# 存放客户端 ip和端口
IPs = dict()

# 退出标记 用于关闭服务器
self._stop = False

# 服务器主循环
while readers and not self._stop:
    # 利用 select 从 建立的链接中选取一些有新消息的
    read, _, err = select.select(readers, [], readers)
    
    for sock in read:
        if sock is self._socket:
            # 建立了新链接

            # 获取新链接的 socket 以及 ip和端口
            client_socket, client_ip = self._socket.accept()
            
            # 将链接设置为非阻塞的
            client_socket.setblocking(0)
            # 添加到监听队列
            readers.append(client_socket)
            # 存储ip信息
            IPs[client_socket] = client_ip

            # 调用建立链接回调函数
            self.onCreateConn(self, client_socket, client_ip)
        else:
            # 收到了新消息
            try:
                # 获取消息
                data = sock.recv(self.recv_bytes)
            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    # 表明链接已退出
                    data = None
                else:
                    raise e
            if data:
                # 调用收到消息回调函数
                self.onReceiveMsg(self, sock, IPs[sock], data)
            else:
                # 链接退出时，移除监听队列
                readers.remove(sock)
                sock.close()

                # 调用链接关闭回调函数
                self.onCloseConn(self, sock, IPs[sock])         
    # 处理存在错误的链接
    for sock in err:
        # 移除监听队列
        readers.remove(sock)
        sock.close()

        # 调用链接关闭回调函数
        self.onCloseConn(self, sock, IPs[sock])
```

- 首先利用 socket 建立一个服务器链接，这个和最初的 socket 核心代码一样
- 不同的是设置链接为非阻塞的，这样就可以通过 `select` 同时监控多个链接，也不至于阻塞服务器了。关于 select 可以看[这里](https://docs.python.org/zh-cn/3/library/select.html 'select')
- 在主循环中，筛选出有了消息的链接，判断是建立链接还是消息发送，调用不同的回调函数
- 最后处理一下异常

#### 事件处理

现在通过回调函数，就可以编写业务了，之间看代码。

这段是建立链接时的处理：

```python

def onCreateConn(server, sock, ip):
    cid = f'{ip[0]}_{ip[1]}'
    clients[cid] = {'cid': cid, 'sock': sock, 'name': None}
    sock.send("你已经接入元宇宙，告诉我你的代号,输入格式为 name:lily.".encode('utf-8'))
```

- 首先计算出客户端 id，即 cid，通过 ip 和 端口 组成
- clients 是个词典，用 cid 为 key，存储了 cid、链接、和名称
- 一旦建立起来链接，向链接发送一段问候语，并要求其设置自己的名称

然后时接收消息的回调函数，这个相对复杂一些，主要是处理的情况更多：

```python
def onReceiveMsg(server, sock, ip, data):
    cid = f'{ip[0]}_{ip[1]}'
    data = data.decode('utf-8')
    print(f"收到数据: {data}")
    _from = clients[cid]
    if data.startswith('name:'):
        # 设置名称
        name = data[5:].strip()
        if not name:
            sock.send(f"不能设置空名称，否则其他人找不见你".encode('utf-8'))
        elif not checkname(name, cid):
            sock.send(f"这个名字{name}已经被使用，请换一个试试".encode('utf-8'))
        else:
            if not _from['name']:
                sock.send(f"{name} 很高兴见到你，现在可以畅游元宇宙了".encode('utf-8'))
                msg = f"新成员{name} 加入了元宇宙，和TA聊聊吧".encode('utf-8')
                sendMsg(msg, _from)
            else:
                sock.send(f"更换名称完成".encode('utf-8'))
                msg = f"{_from['name']} 更换名称为 {name}，和TA聊聊吧".encode('utf-8')
                sendMsg(msg, _from)
            _from['name'] = name
        
    elif '@' in data:
        # 私信
        targets = re.findall(r'@(.+?) ', data)
        print(targets)
        msg = f"{_from['name']}: {data}".encode('utf-8')
        sendMsg(msg, _from, targets)
    else:
        # 群信
        msg = f"{_from['name']}：{data}".encode('utf-8')
        sendMsg(msg, _from)
```

- 代码分为两大部分，if 前面是处理收到的消息，将 bytes 转化为 字符串；if 开始处理具体的消息
- 如果收到 `name:` 开头的消息，表示需要设置用户名，其中包括判重，以及给其他成员发送消息
- 如果收到的消息里有 `@`，表示在发私信，先提取出需要发出的用户们，然后将消息发送给对应的用户
- 如果没有特殊标记，就表示群发
- 其中 sendMsg 用于发送消息，接收三个参数，第一个是消息，第二是发送者，第三个是接收者名称数组

当链接关闭时，需要处理一下关闭的回调函数：

```python
def onCloseConn(server, sock, ip):
    cid = f'{ip[0]}_{ip[1]}'
    name = clients[cid]['name']
    if name:
        msg = f"{name} 从元宇宙中消失了".encode('utf-8')
        sendMsg(msg, clients[cid])
    del clients[cid]
```

- 当收到链接断开的消息时，合成消息，发送给其他用户
- 然后从客户端缓存中删除

### 客户端

客户端需要解决两个问题，第一个是处理接收到的消息，第二个是允许用户的输入。

我们将接收消息作为一个线程，将用户输入作为主循环。

#### 接收消息

先看接收消息的代码：

```python
def receive(client):
    while True:
        try:
            s_info = client.recv(1024)  # 接受服务端的消息并解码
            if not s_info:
                print(f"{bcolors.WARNING}服务器链接断开{bcolors.ENDC}")
                break
            print(f"{bcolors.OKCYAN}新的消息：{bcolors.ENDC}\n", bcolors.OKGREEN + s_info.decode('utf-8')+ bcolors.ENDC)
        except Exception:
            print(f"{bcolors.WARNING}服务器链接断开{bcolors.ENDC}")
            break
        if close:
            break
```

- 这是线程中用的代码，接收一个客户端链接作为参数
- 在循环中不断地从链接中获取信息，如果没有消息时 `recv` 方法回阻塞，直到有新的消息过来
- 收到消息后，将消息显出到控制台上
- `bcolors` 提供了一些颜色标记，将消息显示为不同的颜色
- `close` 是一个全局标记，如果客户端需要退出时，会设置为 True，可以让线程结束

#### 输入处理

下面再看一下输入控制程序：

```python
while True:
    pass
    value = input("")
    value = value.strip()
    
    if value == ':start':
        if thread:
            print(f"{bcolors.OKBLUE}您已经在元宇宙中了{bcolors.ENDC}")
        else:
            client = createClient(ip, 5000)
            thread = Thread(target=receive, args=(client,))
            thread.start()
            print(f"{bcolors.OKBLUE}您进入元宇宙了{bcolors.ENDC}")
    elif value == ':quit' or value == ':stop':
        if thread:
            client.close()
            close = True
            print(f"{bcolors.OKBLUE}正在退出中…{bcolors.ENDC}")
            thread.join()
            print(f"{bcolors.OKBLUE}元宇宙已退出{bcolors.ENDC}")
            thread = None
        if value == ':quit':
            print(f"{bcolors.OKBLUE}退出程序{bcolors.ENDC}")
            break
        pass
    elif value == ':help':
        help()
    else:
        if client:
            # 聊天模式
            client.send(value.encode('utf-8'))
        else:
            print(f'{bcolors.WARNING}还没接入元宇宙，请先输入 :start 接入{bcolors.ENDC}')
    client.close()
```

- 主要是对不同的命令做出的相应，比如 `:start` 表示需要建立链接，`:quit` 表示退出等
- 命令前加 `:` 是为了和一般的消息做区分，如果不带 `:` 就认为是在发送消息

## 启动

完成了整体编码之后，就可以启动了，最终的代码由三部分组成。

第一部分是服务器端核心代码，存放在 simpletcp.py 中。

第二部分是服务器端业务代码，存放在 metaServer.py 中。

第三部分是客户端代码，存放在 metaClient.py 中。

另外需要一些辅助的处理，比如发送消息的 sendMsg 方法，颜色处理方法等，具体可以下载本文源码了解。

进入代码目录，启动命令行，执行 `python metaServer.py`，输入指令 `start`:

![server](http://www.justdopython.com/assets/images/2021/12/meta/02.png)

然后再打开一个命令行，执行 `python metaClient.py`，输入指令 `:start`，就可以接入到元宇宙：

![client](http://www.justdopython.com/assets/images/2021/12/meta/03.png)

设置自己的名字：
![name](http://www.justdopython.com/assets/images/2021/12/meta/04.png)

如果有新的成员加入时，就会得到消息提醒， 还可以玩点互动：
![new client](http://www.justdopython.com/assets/images/2021/12/meta/05.png)

怎么样好玩吧，一个元宇宙就这样形成了，赶紧让其他伙伴加入试试吧。

## 总结

元宇宙现在是个很热的概念，但还是基于现有的技术打造的，元宇宙给人们提供了一个生活在虚拟的神奇世界里的想象空间，其实自从有了互联网，我们就已经逐步生活在元宇宙之中了。

今天我们用基础的 TCP 技术，构建了一个自己的元宇宙聊天室，虽然功能上和想象中的元宇宙相去甚远，不过其中的主要功能已经成形了。

如果有兴趣还可以在这个基础上加入更好玩的功能，比如好友，群组，消息记录等等，在深入了解的同时，让这个元宇宙更好玩。

期望今天的你们元宇宙对你有所启发，欢迎在留言区写下你的想法与观点，比心！

## 参考代码

> https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/meta
