---
layout: post
category: python
title: python 抓取阿里云盘资源
tagline: by 某某白米饭
tags: 
  - Python技巧
  - 编程
---

前阵子阿里云盘大火，送了好多的容量空间。而且阿里云盘下载是不限速，这点比百度网盘好太多了。这两天看到一个第三方网站可以搜索阿里云盘上的资源，但是它的资源顺序不是按时间排序的。这种情况会造成排在前面时间久远的资源是一个已经失效的资源。小编这里用 python 抓取后重新排序。
<!--more-->

![](https://files.mdnice.com/user/15960/424e2091-ca6c-4aab-b1cb-d4b39542059f.png)

### 网页分析

这个网站有两个搜索路线：搜索线路一和搜索线路二，本文章使用的是搜索线路二。

![](https://files.mdnice.com/user/15960/49f3031e-e1f5-4512-a94e-5b9dfc0f745e.png)

打开控制面板下的网络，一眼就看到一个 seach.html 的 get 请求。

![](https://files.mdnice.com/user/15960/299eb199-573a-4113-b9cf-3b449b5ad3b7.png)


上面带了好几个参数，四个关键参数：

* page：页数，
* keyword：搜索的关键字
* category：文件分类，all(全部)，video(视频)，image(图片)，doc(文档)，audio(音频)，zip(压缩文件)，others(其他)，脚本中默认写 all
* search_model：搜索的线路

也是在控制面板中，看出这个网页跳转到阿里云盘获取真实的的链接是在标题上面的。用 bs4 解析页面上的 div(class=resource-item border-dashed-eee) 标签下的 a 标签就能得到跳转网盘的地址，解析 div 下的 p 标签获取资源日期。

![](https://files.mdnice.com/user/15960/30678297-6178-44eb-af88-c581ab0f8bad.png)


### 抓取与解析

首先安装需要的 bs4 第三方库用于解析页面。

```python
pip3 install bs4
```

下面是抓取解析网页的脚本代码，最后按日期降序排序。

```python
import requests
from bs4 import BeautifulSoup
import string


word = input('请输入要搜索的资源名称：')
    
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

result_list = []
for i in range(1, 11):
    print('正在搜索第 {} 页'.format(i))
    params = {
        'page': i,
        'keyword': word,
        'search_folder_or_file': 0,
        'is_search_folder_content': 0,
        'is_search_path_title': 0,
        'category': 'all',
        'file_extension': 'all',
        'search_model': 0
    }
    response_html = requests.get('https://www.alipanso.com/search.html', headers = headers,params=params)
    response_data = response_html.content.decode()
   
    soup = BeautifulSoup(response_data, "html.parser");
    divs = soup.find_all('div', class_='resource-item border-dashed-eee')
    
    if len(divs) <= 0:
        break

    for div in divs[1:]:
        p = div.find('p',class_='em')
        if p == None:
            break

        download_url = 'https://www.alipanso.com/' + div.a['href']
        date = p.text.strip();
        name = div.a.text.strip();
        result_list.append({'date':date, 'name':name, 'url':download_url})
    
    if len(result_list) == 0:
        break
    
result_list.sort(key=lambda k: k.get('date'),reverse=True)
```

示例结果：

![](https://files.mdnice.com/user/15960/b50e8463-d736-47d5-b0df-219832a10be8.png)

### 模板

上面抓取完内容后，还需要将内容一个个复制到 google 浏览器中访问，有点太麻烦了。要是直接点击一下能访问就好了。小编在这里就用 Python 的模板方式写一个 html 文件。

模板文件小编是用 elements-ui 做的，下面是关键的代码：

```html
<body>
    <div id="app">
        <el-table :data="table" style="width: 100%" :row-class-name="tableRowClassName">
            <el-table-column prop="date" label="日期" width="180"> </el-table-column>
            <el-table-column prop="name" label="名称" width="600"> </el-table-column>
            <el-table-column label="链接">
              <template slot-scope="scope">
              <a :href="'http://'+scope.row.url"
                target="_blank"
                class="buttonText">{{scope.row.url}}</a>
            </template>
        </el-table>
    </div>

    <script>
      const App = {
        data() {
          return {
              table: ${elements}
            
          };
        },
        methods: {
            onSubmit() {
                
            }
        }
      };
      const app = Vue.createApp(App);
      app.use(ElementPlus);
      app.mount("#app");
    </script>
  </body>
```

在 python 中读取这个模板文件，并将 ${elements} 关键词替换为上面的解析结果。最后生成一个 report.html 文件。

```python
with open("aliso.html", encoding='utf-8') as t:
    template = string.Template(t.read())

final_output = template.substitute(elements=result_list)
with open("report.html", "w", encoding='utf-8') as output:
    output.write(final_output)
```

示例结果：

![](https://files.mdnice.com/user/15960/d74f6500-339e-4976-a447-a37a70dae226.png)

跳转到阿里云盘界面

![](https://files.mdnice.com/user/15960/bdb190e7-48fa-4730-aa41-2471921294a7.png)


### 总结

用 python 做一些小爬虫，不仅去掉网站上烦人的广告，也更加的便利了。
