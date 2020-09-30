---
layout: post     
title:  用 Python 制作音乐聚合下载器    
category: 用 Python 制作音乐聚合下载器
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

现在的音乐APP有很多，为了不下载很多的APP，所以咱用python做了一个聚合的音乐下载器，现在聚合了咪咕音乐、QQ音乐，下面是效果图
<!--more-->
![](http://www.justdopython.com/assets/images/2020/09/music/m_0.gif)

### 安装

需要安装一个辅助模块 prettytable，用于美化控制台的表格输出

```python
pip install prettytable
```

### 提取音乐链接

#### 搜索音乐

以下载 QQ 音乐为例，在首页（https://y.qq.com/） 上的搜索框中搜索 <<厚颜无耻>>， 打开 F12 的控制台面板，可以找到如下图的搜索链接，这个链接返回的是一个音乐列表的 json 串

![](http://www.justdopython.com/assets/images/2020/09/music/m_1.png)

```python
def get_request(self, url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response
    except Exception as e:
        print("请求出错：", e)
        
    return None

def search_music(self, key):
    # 20: 查询 20 条数据，key：关键字
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=%d&w=%s' % (20, key)
    resp = self.get_request(url)
    resp_json = json.loads(resp.text[9:][:-1])
    data_song_list = resp_json['data']['song']['list']
    song_list = []
    for song in data_song_list:
        singers = [s.get("name", "") for s in song.get("singer", "")]
        song_list.append({'name': song['songname'], 'songmid': song['songmid'], 'singer': '|'.join(singers)})

    return song_list
```

示例结果：

```json
[{'name': '富士山下', 'songmid': '003dtkNk26WhJD', 'singer': '陈奕迅'}, {'name': '不要说话', 'songmid': '002B2EAA3brD5b', 'singer': '陈奕迅'}, ...., {'name': '最佳损友', 'songmid': '003hFxQh276Cv5', 'singer': '陈奕迅'}]
```

#### 获取下载链接

把音乐列表页中的歌曲点击到播放音乐的页面，在控制面板找到多个以 m4a 结尾的音乐实际链接

![](http://www.justdopython.com/assets/images/2020/09/music/m_2.png)

它的参数部分有一个 vkey 的参数，把 vkey 当作关键字在 Network 面板中搜索，找到一个 musics.fcg 结尾的链接，vkey 的数据就在它返回的 json 串中，另外的 purl 的值就是上面的 m4a 链接，最后将 https://ws.stream.qqmusic.qq.com 和 purl 拼凑成音乐链接，musics.fcg 链接中 guid 参数是一个随机数，songmid 参数是上面单个音乐的 songmid，uin 参数是 QQ 号

![](http://www.justdopython.com/assets/images/2020/09/music/m_3.png)

```python
def download_url(self, song):
    guid = str(random.randrange(1000000000, 10000000000))

    purl_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?' \
                '&data={"req":{"param":{"guid":" %s"}},' \
                        '"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' \
                % (guid, guid, song['songmid'], 0, 0)

    resp = self.get_request(purl_url)

    if resp is None:
        return 'N', 'None', '.m4a'

    resp_json = json.loads(resp.text)

    purl = resp_json['req_0']['data']['midurlinfo'][0]['purl']

    # 有些音乐在网站上不能听
    if len(purl) < 1:
        msg = 'N'

    download_url = 'http://ws.stream.qqmusic.qq.com/' + purl
    song_data = self.get_request(download_url)
    if song_data:
        msg = 'Y'
    return msg, download_url, '.m4a'
```

示例结果：

![](http://www.justdopython.com/assets/images/2020/09/music/m_4.png)

只有一个域名的地址的下载链接表示这个音乐只能在客户端听，网页版听不了

到这里已经完了 QQ 音乐的搜索、抓取脚本，用同样的方式抓取咪咕音乐（http://m.music.migu.cn）做成咪咕音乐脚本，咪咕音乐更容易爬取

### 命令行主界面

主界面的主要功能就是以表格的方式显示搜索到的音乐和以序号的方式下载音乐

```python
import os

from qqMusic import QQMusic
from miguMusic import MiGuMusic
from prettytable import PrettyTable


class MusicBox(object):

    def __init__(self):
        pass

    def download(self, data, songName, type):

        save_path = 'music/' + songName + '.' + type
        file = 'music'
        if os.path.exists(file):
            pass
        else:
            os.mkdir('music')

        try:
            print("{}下载中.....".format(songName), end='')
            with open(save_path, 'wb') as f:
                f.write(data)
            print("已下载完成")
        except Exception as err:
            print("文件写入出错:", err)
            return None

    def main(self):
        print('请输入需要下载的歌曲或者歌手：')
        key = input()
        print('正在查询..\033[32mQQ音乐\033[0m', end='')
        qqMusic = QQMusic()
        qq_song_list = qqMusic.main(key)
        print('...\033[31m咪咕音乐\033[0m')
        miguMusic = MiGuMusic()
        migu_song_list = miguMusic.main(key)

        qq_song_list.extend(migu_song_list)
        song_dict = {}
        for song in qq_song_list:
            key = song['name'] + '\\' + song['singer']
            s = song_dict.get(key)
            if s:
                if s['msg'] != 'Y':
                    song_dict[key] = song
            else:
                song_dict[key] = song

        i = 0

        table = PrettyTable(['序号', '歌手', '下载', '歌名'])
        table.border = 0
        table.align = 'l'
        for song in list(song_dict.values()):
            i = i + 1
            table.add_row([str(i), song['singer'], song['msg'], song['name']])
        print(table)

        while 1:
            print('\n请输入需要下载，按 q 退出：')
            index = input()
            if index == 'q':
                return

            song = list(song_dict.values())[int(index) - 1]
            data = qqMusic.get_request(song['downloadUrl'])
            if song['msg'] == 'Y':
                self.download(data.content, song['name'], song['type'])
            else:
                print('该歌曲不允许下载')

if __name__ == '__main__':
    musicBox = MusicBox()
    musicBox.main()
```

### 总结

音乐聚合下载器最重要的部分还是爬虫抓取各个音乐网站的数据，命令行的方式则省去了画 GUI 的工作

> 示例代码：[用 Python 制作音乐聚合下载器](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/music)