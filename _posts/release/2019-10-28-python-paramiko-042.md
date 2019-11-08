---
layout: post
category: python
title: 第42天： paramiko模块
tagline: by 某某白米饭
tags:
  - python100
---

## paramiko 模块

paramiko 是一个用 Python 语言编写的、遵循 SSH2 协议、支持以加密和认证方式进行连接远程服务器的模块。改模块可以对远程服务器进行一些命令或文件操作。
<!--more-->

### 安装

使用 pip3 安装 paramiko 模块

```python
pip3 install paramiko
```

### 常用函数

#### SSHclient 类

SSH 客户端

1.connect：远程连接服务器

```python
# hostname：主机IP地址
# port：ssh服务的端口号，默认为22
# username和password：用户名和密码
# timeout 连接的超时时间

connect(hostname, port=22, username=None, password=None, timeout=None,...)
```

2.exec_command：远程执行命令

```python
# command：需要执行的命令
# timeout：连接超时设置
exec_command(command, timeout=None,...)
```

3.invoke_shell：生成交互的Shell

```python
# term：终端的类型
# width，height：生成终端的宽度和高度
# width_pixels，height_pixels：像素为单位的终端宽度和高度
# environment：命令的环境
invoke_shell(term='vt100', width=80, height=24, width_pixels=0, height_pixels=0, environment=None)
```

4.open_sftp：打开 sftp

```python
open_sftp()
```

#### Channel类

SSH2 的抽象通道

1.get_pty：打开一个终端

```python
# 从服务器请求一个终端，在创建连接通道之后立刻使用这个命令，要求服务器为 invoke_shell() 提供调用 shell 的终端语义
get_pty(*args, **kwds)
```
2.send(s)/sendall(s)：发送命令

```python
# s：发送的命令，
send(s)

sendall(s)
```

3.settimeout(timeout)：设置超时时间

```python
settimeout(timeout)
```

4.shutdown(how)：关闭连接

```python
# how：0（停止接收），1（停止发送）或2（停止接收和发送）
shutdown(how)
```

#### SFTP Client类

用 SFTP 的方式打开 SSH 连接，并远程执行文件操作，可用于上传和下载文件。

1.chmod：为文件赋予执行权限

```python
# path：文件路径
# mode：执行权限
chmod(path, mode)
```
2.close：关闭连接通道

```python
close()
```

3.file/open：打开文件

```python
# filename：文件名
# mode：文件的读写模式
# bufsize：所需要的缓存大小
file(filename, mode='r', bufsize=-1)

open(filename, mode='r', bufsize=-1)
```

4.get：下载文件

```python
# remotepath：远程文件路径
# localpath：本地文件路径
# callback：文件下载完成后执行的函数
get(remotepath, localpath, callback=None)
```

5.getcwd：当前远程文件路径

```python
getcwd()
```

6.listdir：文件列表

```python
# path：文件夹路径
listdir(path='.')
```

7.mkdir：创建文件夹

```python
# path：文件夹路径
# mode：文件夹权限
mkdir(path, mode=511)
```

8.posix_rename/rename：重命名文件

```python
# oldpath：需要重命名的文件
# newpath：新的文件路径
posix_rename(oldpath, newpath)

rename(oldpath, newpath)
```

9.put：上传文件

```python
# localpath：本地文件路径
# remotepath：远程文件路径
# callback：上传完成后调用的函数
# confirm：是否对文件确认大小
put(localpath, remotepath, callback=None, confirm=True)
```

10.remove/rmdir：删除文件

```python
# path：文件路径
remove(path)

rmdir(path)
```

### 实例

#### 连接远程服务器

paramiko 模块连接远程服务器可以使用远程服务器的用户名、密码登录

```python
import paramiko

# 创建一个SSHClient对象
ssh = paramiko.SSHClient()
# 将信任的主机加到 host_allow 列表
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect("服务器IP地址", "服务器端口号", "用户名", "密码")
```

#### 使用命令

在登录远程服务器后，利用 paramiko 模块可以使用 shell 命令操作远程服务器，比如：df 命令、pwd 命令、cat 命令等等...

```python
# 打印磁盘情况
# 执行df命令，结果放到 dfout 中，如果有错误将放到 dferr 中
dfout, dferr = ssh.exec_command('df')
print(dfout.read().decode('utf-8'))

# 使用cd、cat命令查看文件内容
# paramiko.txt文件为/root/data/paramiko.txt
catin, catout,caterr = ssh.exec_command('cd data;cat paramiko.txt')
print(catin.read().decode('utf-8'))
```

在 exec_command 函数中，exec_command 执行的是单个会话，执行完成后会回到登录的缺省目录，多个命令需要 命令1;命令2;命令3 的写法

#### sftp 上传和下载文件

```python
import paramiko

transport = paramiko.Transport(("服务器IP地址",服务器端口号))
transport.connect(username = "用户名", password = "密码")
sftp = paramiko.SFTPClient.from_transport(transport)
# 从远程服务器下载文件
# 远程服务器文件路径为/data/paramiko.txt
sftp.get('/data/paramiko.txt', 'paramiko.txt', print("下载完成！"))
# 从本地上传文件到远程服务器
sftp.put('upload_paramiko.txt', '/data/upload_paramiko.txt', print("上传完成！"))
```

#### 服务器文件修改内容

sftp 对象可以在线修改远程服务器上文件的内容

```python
import paramiko

# 登录远程服务器
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("服务器IP地址",,"服务器端口号","用户名", "密码", timeout=5)
sftp = client.open_sftp()
# 远程服务器文件地址为/data/paramiko.txt
remoteFile = sftp.open("/data/paramiko.txt", 'a')
remoteFile.write("\n");
remoteFile.write("这里是追加的内容！");
remoteFile.close()
sftp.close()
```

#### 查询文件

使用 sftp 对象获取远程服务器上的文件列表

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("服务器IP地址",,"服务器端口号","用户名", "密码", timeout=5)
sftp = client.open_sftp()
for fileName in sftp.listdir("/root/data"):
    if fileName.endswith(".txt"):
        print(fileName)
sftp.close()
```

#### 在 Linux 模拟终端

```python
import paramiko
import select
import sys
import tty
import termios


# 创建一个安全的通道
trans = paramiko.Transport(('IP地址', 22))
# 启动一个客户端
trans.start_client()

# 如果使用用户名和密码登录
trans.auth_password(username='用户名', password='密码')
# 打开一个通道
channel = trans.open_session()
# 获取一个终端
channel.get_pty()
# 激活终端
channel.invoke_shell()

# 获取Linux操作终端的属性
oldtty = termios.tcgetattr(sys.stdin)
try:
    # 将Linux操作终端的属性设置为 SSH 服务器的终端属性，并使用 TAB 键
    tty.setraw(sys.stdin)
    channel.settimeout(0)

    while True:
        read_list, write_list, err_list = select.select([channel, sys.stdin,], [], [])
        # 输入命令，sys.stdin会发生变化
        if sys.stdin in read_list:
            # 获取输入的内容
            input_cmd = sys.stdin.read(1)
            # 将命令发送给服务器
            channel.sendall(input_cmd)

        # SSH服务器返回结果
        if channel in read_list:
            result = channel.recv(1024)
            # 断开连接后退出
            if len(result) == 0:
                print("连接断开了！")
                break
            sys.stdout.write(result.decode())
            sys.stdout.flush()
finally:
    # 还原Linux终端属性
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

channel.close()
trans.close()
```

### 结语

以上是 paramiko 模块的基本操作，学会以上内容后在多个远程服务器的情况下，可以快速、便捷的操作服务器内容

> 示例代码：[Python-100-days-day042](https://github.com/JustDoPython/python-100-day/tree/master/day-042)
