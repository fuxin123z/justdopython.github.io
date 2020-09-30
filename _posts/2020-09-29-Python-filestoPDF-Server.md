---
layout: post     
title: Office 文件转 PDF 之服务实战
category: Office 文件转 PDF 之服务实战
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

小编之前写了一篇关于 Office 文件转 PDF 的实战文章，详见[Python 小技之 Office 文件转 PDF](https://mp.weixin.qq.com/s/AN2pYEw3KRvpcAbSXnVqOg)
但是在平时的工作中，咱们需要通过接口的形式来调用具体的转换逻辑，同时开可以将文件转换写成服务的形式，将服务开启后传入参数或者地址即可直接调用逻辑转换，今天的文章主要讲解如何将文件转换写成服务；

一起拭目以待吧！！！

### 文件服务器

Office 文件转 PDF 涉及到文件的传输，所以考虑用文件服务器来进行文件的传递，客户端如果有文件服务器的话，
同样在服务端也需要写一个文件服务器来返回转换完成的文件，以供客户端使用，文件服务器实现思路如下：

#### 逻辑结构

文件结构结构逻辑图如下：

![代码结构](https://imgkr2.cn-bj.ufileos.com/52c0766f-c27a-406c-a867-2003b3a85409.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=NGpmcBo9OzGfr%252F1Zyw3t%252F88n074%253D&Expires=1601471376)


#### 前端文件上传下载页面

```
<body>
    <form action="download" method="GET",enctype="multipart/form-data">
        要下载的文件: <input type="text" value="请上传文件" name="filename" />
        <input type="submit" value="download">
    </form>

    <form action="/file_server/cgi-bin/upload.py" method="POST" enctype="multipart/form-data">
        要上传的文件: <input type="file" name="filename" />
        <input type="submit" value="upload">
    </form>
```

#### 上传文件

上传文件 upload.py 部分代码如下：

```python
import cgi, os

form = cgi.FieldStorage()

item = form["filename"]

if item.filename:
    fn = os.path.basename(item.filename)
    open("/home/sxhlinux/data/" + fn, "wb").write(item.file.read())
    msg = "File" + fn + ' upload successfully !'
else:
    msg = 'no file is uploaded '

print("""\
Content-type: text/html\n
<html>
<head>
<meta charset="utf-8">
<title>Hello world</title>
</head>
<body>
<h2>名称: %s</h2>
</body>
<html>
""" % (msg,))
```
#### 下载文件

下载文件 download.py 部分代码如下:

```
form = cgi.FieldStorage()

filename = form.getvalue('filename')

dir_path = "F:/WorkSpace/FilesToPDF/file_server/tmp"

target_path = dir_path + str(filename)

if os.path.exists(target_path) == True:
    print("Content-Type: application/octet-stream")
    print('Content-Disposition: attachment; filename = "%s"' % filename)

    print(target_path)

    sys.stdout.flush()
    fo = open(target_path, "rb")
    sys.stdout.buffer.write(fo.read())
    fo.close()
else:
    print("""\
            Content-type: text/html\n
            <html>
            <head>
            <meta charset="utf-8">
            <title>File server</title>
            </head>
            <body>
            <h1> %s doesn't exist in the server:
            files in the server list below: </h1>""" % filename)

    for line in os.popen(filename):
        name = line.strip().split(' ', 8)
        type(name)
        if len(name) == 9:
            print("""
            <form action="/cgi-bin/download.py" method="get">%s
            <input type="submit" name="filename" value="%s">
            </form>""" % (line, name[8]))
```
#### 文件服务

文件服务入口 server.py 部分代码如下：

```python

if __name__ == '__main__':
    try:
        handler = CGIHTTPRequestHandler
        handler.cgi_directories = ['/cgi-bin', '/htbin']
        #port = int(sys.argv[1])
        port = 8001
        print('port is %d' % port)
        server = HTTPServer(('', port), handler)
        print('Welcome to my website !')
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()	
```

以上服务启动后即可使用。


### 转换逻辑接口

转换接口使用了 Python Flask框架，在文件转换逻辑里面需要引入具体的转换逻辑，接口逻辑实现代码如下：

```python
from flask import Flask, render_template,request
import requests
import config
from requests import get
import files2pdf  # 引入转换逻辑
import os, shutil
from flask import Flask, render_template, url_for, send_from_directory,json,make_response,jsonify

app = Flask(__name__, static_folder='/static')
app.config.from_object(config)
app.config["SECRET_KEY"] = "123456"

@app.route('/')
def index():
    return "Welcome to You,Please visit the url:http://IP:5000/upload_file?filePath=xxx.pptx"

#pathname = ''
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST' or request.method == 'GET':
            file_url = request.args.get('filePath', '')
            req = get(file_url)
            if req.status_code == 404:
                print("no file")

                return
            # 取正确的转换文件名称
            filename = file_url.split('/')[-1]
            name = filename.split('?')[1]
            ppt_name = name.split('=')[-1]
            print(ppt_name)

            with open(ppt_name, "wb") as file:
                # get request
                # response = get(url)
                # write to file
                file.write(req.content)

            # 判断要转换的文件是否存在
            if os.path.exists(ppt_name) and not os.path.exists(file_path + '/' + ppt_name):
                shutil.move(ppt_name, file_path)
            elif os.path.exists(ppt_name) and os.path.exists(file_path + '/' + ppt_name):
                print('file alreadly exists')
                os.remove(ppt_name)
                print("already deleted exists file")

            pdfConverter = files2pdf.PDFConverter(file_path + '/' + ppt_name)  # 调用文件转换逻辑
            # print("transform complete:"+pdfConverter)
            pdfConverter.run_conver()

            # file transform finshed --> Get file's name
            re_name = ppt_name.replace('.pptx', '.pdf')
            print('New name is:' + re_name)
            # /static/%E6%B0%B4%E9%92%A2%E9%9B%86%E5%9B%A2%E6%99%BA%E6%85%A7%E5%85%9A%E5%BB%BA%E5%9F%B9%E8%AE%AD%E8%B5%84%E6%96%990420%282%29.pdf
            re_url = 'IP:8001'  # 文件服务地址
            # urlfor = url_for('static', filename=re_name)
            return re_url + url_for('static', filename=re_name)
            #return  render_template('result_link.html')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
    
```
### 调用

先启动 server.py 后再启动 flaskdemo.py 传入参数即可调用逻辑。也可以用 postman 调用，调用实例如下：

![调用实例](https://imgkr2.cn-bj.ufileos.com/dceaf421-ac75-47a0-b5fb-2de73081b5e8.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=dkmDhEYj7FNueLMH%252FhE5Ac2u%252Bpc%253D&Expires=1601471874)


### 总结

今天的文章主要是继上一篇 Python 实战之小工具的运用的延申，希望对大家有所帮助，如有问题咱们讨论区见！

So 今天的小 Tip 你安利到了吗？

> 示例代码 [Office 文件转 PDF 之服务实战](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/FilesToPDF_Server)