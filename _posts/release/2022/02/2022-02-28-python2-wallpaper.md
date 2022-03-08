---
layout: post
category: python
title: Python 在手，高清壁纸不愁
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/wallpaper/logo.png)

话说小伙伴们平时都去哪里找壁纸呢。

有位将军曾将说过，好看也是战斗力，的确，好看的壁纸能让我们心情更舒畅，工作效率更高。今天指南妹就教大家如何获取海量高清壁纸。

今天爬取的目标网站如下，这是一个高清无版权图片库，里面有上万张不同领域高质量图片。

> https://unsplash.com/images

好看的小姐姐谁都喜欢，今天我们就以 「jk girls」为关键字来爬取高质量 jk 妹子图。

首先打开目标网站，输入「jk girls」观察下浏览器的请求。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/wallpaper/001.png)

打开请求中返回的链接，发现和网站中的图片是对应的，不出所料，果然是通过异步请求的方式来加载图片的，这就好办了。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/wallpaper/002.png)

往下滑动屏幕，看下分页请求。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/wallpaper/003.png)

一切梳理清楚之后，就可以写程序来爬取妹子图片了。

先搞一个下载图片的工具函数，直接使用 urllib 库来操作就行。

```python
def download_img(img_url, file_name):
    print(F'downloading {file_name}, img_url = {img_url}')
    try:
        img = req.get(img_url)
        with open(file_name, "wb") as f:
            f.write(img.content)  # 将内容写入图片
        return 'ok'
    except:
        return 'fail'
```

其次还需要一个发送请求获取 json 数据的函数，为了缓解服务器压力，每次请求前暂停 2 秒。

```python
def send_get(url, params):
    time.sleep(2)
    response = req.get(url, headers=None, params=params, verify=False)
    return response.text
```

再来一个处理服务器返回的 json 数据的函数，解析出每个图片的地址，循环调用下载函数即可。

```python
def deal_result(result, page):
    index = page * 20
    for i in range(len(result)):
        img_url = result[i]['urls']['regular']
        index += 1    
        download_img(img_url, str(index) + '.png')
```

最后写一个循环发送请求的函数就大功告成啦，我这里只请求了 5 页的数据，可以根据实际情况酌情调整大小。

```python
def loop():
    for i in range(2):
        url = 'https://unsplash.com/napi/search/photos?query=jk%20girls&per_page=20&page=' + str(i + 1) + '&xp='
        print(F'page = {i}, url = {url}')
        response = json.loads(send_get(url, None))
        deal_result(response['photos']['results'], i)
        
if __name__ == '__main__':
    loop()
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/wallpaper/004.png)