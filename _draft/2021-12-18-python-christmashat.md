---
layout: post
title: 不用P图！用Python给头像加圣诞帽并制作成可执行软件！
category: python
tagline: by 闲欢
tags: 
  - python
  - 圣诞节
  - 圣诞帽
  - 头像
---


![封面](http://www.justdopython.com/assets/images/2021/12/christmashat/0.jpg)

随着圣诞节的到来，节日气氛也越来越浓厚。大街上随处可见挂满饰品的圣诞树，好多小伙伴的头上也多了一顶红色牛角的圣诞帽。

往年在这个时候，好多 P图软件 会推出给头像加一顶圣诞帽的功能，甚至有一年大伙 @微信官方 就可以在自己的微信头像上加一顶圣诞帽。

作为一个学习 Python 的技术人，自己可以写程序实现这个功能，做成一个软件当然是一件很酷的事情了。

今天就给大家分享一下如何用 Python 制作一款自动给头像添加圣诞帽的软件。

**如果不想看实现，可以直接跳到文末获取软件。**

<!--more-->

### 思路

我们的 `头像添加圣诞帽软件` 制作的大致思路如下：

- 要实现一个软件，我们需要制作一个 GUI 界面，供用户操作。
- 要实现头像戴圣诞帽功能，我们需要用户上传一张头像，我们还需要准备一顶圣诞帽子图片。
- 要把圣诞帽戴在头像上，我们需要识别头像中的人脸和头部特征，然后将帽子放在头顶合成一张图片。

基于以上思路，我们制作这款软件的关键词有：

- GUI 界面
- 圣诞帽图片
- 头像图片
- 人脸识别
- 打包软件

### 实现

看了以上思路，相信大家脑海中已经对这个软件制作的过程有了一个大致的框架了。我们的实现主要分为：图像制作、GUI界面、打包三大块内容。

#### 准备工作

首先列举一下本次软件制作过程中需要用的的一些包模块：

- cv2 
> pip install opencv-python
- os
> python 系统模块
- dlib 
> pip install dlib
- numpy
> pip install pandas
- PySimpleGUI
> pip install PySimpleGui

温馨提示：这其中安装 dlib 会遇到很多坑以及很多困难，一般需要一边安装一边上网搜索报错，从而找到解决办法。保证安装过一次之后不想尝试第二次。

#### 图像制作

##### 准备圣诞帽

我们需要准备一个圣诞帽的图片，格式最好为 png ，因为 png 图片我们可以直接用 `Alpha通道` 作为掩膜使用。如果是 jpg 图片，需要先转换成 png 格式图片。注意这里的转换不是只改个后缀名，那样是行不通的。

我们用到的圣诞帽如下图：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/1.png)

为了能够与 RGB 通道的头像图片进行运算，我们需要把圣诞帽图像分离成 RGB 通道图像和 alpha通道图像：

```python
r,g,b,a = cv2.split(hat_img)
rgb_hat = cv2.merge((r,g,b))
cv2.imwrite("hat_alpha.jpg",a)

```
分离之后，得到的 alpha通道图像如下所示：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/2.jpg)

##### 人脸识别

我从我的百宝箱中选择了一张傻萌傻萌的图片作为程序的测试图片。

![](http://www.justdopython.com/assets/images/2021/12/christmashat/3.jpg)

大家注意，因为我们要做人脸识别，然后自动添加帽子，所以选择的图片一定要是真人的正面照片，不然识别不了人脸，也就不知道在哪添加圣诞帽。

下面我们用 dlib 的正脸检测器进行人脸检测，用 dlib 提供的模型提取人脸的五个关键点。代码如下：

```python
# dlib人脸关键点检测器
      predictor_path = "shape_predictor_5_face_landmarks.dat"
      predictor = dlib.shape_predictor(predictor_path)  
  
      # dlib正脸检测器
      detector = dlib.get_frontal_face_detector()
  
      # 正脸检测
      dets = detector(img, 1)
  
      # 如果检测到人脸
      if len(dets)>0:  
          for d in dets:
              x,y,w,h = d.left(),d.top(), d.right()-d.left(), d.bottom()-d.top()
              # x,y,w,h = faceRect  
              cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2,8,0)
  
              # 关键点检测，5个关键点
              shape = predictor(img, d)
              for point in shape.parts():
                  cv2.circle(img,(point.x,point.y),3,color=(0,255,0))
  
              cv2.imshow("image",img)
              cv2.waitKey()  
```

我们把图片打印出来的效果是这样的：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/4.jpg)

看到这个图片是不是有点熟悉，网上好多人脸识别的图片都是这样的。

##### 调整帽子大小

我们选取两个眼角的点，求中心作为放置帽子的x方向的参考坐标，y 方向的坐标用人脸框上线的 y 坐标表示。

然后我们根据人脸检测得到的人脸的大小调整帽子的大小，使得帽子大小合适。

看到这里，你应该明白，我们头像的图片中人的脸越正面那么我们制作出来的效果越好。

```python
            # 选取左右眼眼角的点
            point1 = shape.part(0)
            point2 = shape.part(2)

            # 求两点中心
            eyes_center = ((point1.x+point2.x)//2,(point1.y+point2.y)//2)

            #  根据人脸大小调整帽子大小
            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w/rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w/rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1

            # 根据人脸大小调整帽子大小
            resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))

```

##### 帽子区域处理

我们先将帽子的 alpha通道 作为 mask掩膜：

```python
mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
mask_inv =  cv2.bitwise_not(mask)
```
接着，从人像图中去除需要添加帽子的区域：

```python
            # 帽子相对与人脸框上线的偏移量
              dh = 0
              dw = 0
              # 原图ROI
              # bg_roi = img[y+dh-resized_hat_h:y+dh, x+dw:x+dw+resized_hat_w]
              bg_roi = img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]
  
              # 原图ROI中提取放帽子的区域
              bg_roi = bg_roi.astype(float)
              mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
              alpha = mask_inv.astype(float)/255
  
              # 相乘之前保证两者大小一致（可能会由于四舍五入原因不一致）
              alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
              # print("alpha size: ",alpha.shape)
              # print("bg_roi size: ",bg_roi.shape)
              bg = cv2.multiply(alpha, bg_roi)
              bg = bg.astype('uint8')
```
提取后的效果图如下：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/5.jpg)

接下来，我们提取圣诞帽的区域：

```python
hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)

```

提取后的效果图如下：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/6.jpg)

##### 盖帽

图像处理的最后一步是盖帽了，就是把提取的圣诞帽区域和图片中提取的区域相加，然后再放到原图中去。这里需要注意的就是，相加之前resize一下保证两者大小一致

```python
              # 相加之前保证两者大小一致（可能会由于四舍五入原因不一致）
              hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))
              # 两个ROI区域相加
              add_hat = cv2.add(bg,hat)
              # cv2.imshow("add_hat",add_hat) 
  
              # 把添加好帽子的区域放回原图
              img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat
```
最后，我们得到的效果图如下：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/7.png)


#### GUI界面

我们先来看效果图：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/8.png)

然后再来看这部分的实现代码：

```python
import PySimpleGUI as sg
import os.path
import cv2

file_list_column = [
    [sg.Submit('生成', key='Go', size=(15, 1)), sg.Cancel('退出', key='Cancel', size=(15, 1))],
    [
        sg.Text("图片位置（选择文件夹）"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('浏览'),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ]
]
image_viewer_column = [
    [sg.Text("从左边图片列表中选择一张图片:")],
    [sg.Image(key="-IMAGE-")]
]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]
window = sg.Window("人像添加圣诞帽软件", layout)
filename = ''
while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".jpg", ".png"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            if filename.endswith('.jpg'):
                im = cv2.imread(filename)
                cv2.imwrite(filename.replace('jpg', 'png'), im)
            window["-IMAGE-"].update(filename=filename.replace('jpg', 'png'))
        except Exception as e:
            print(e)
    elif event == "Go":
        try:
            # output = add_hat(filename)
            # 展示效果
            # cv2.imshow("output",output)
            # cv2.waitKey(0)
            # cv2.imwrite("output.png",output)
            # print(output)
            window["-IMAGE-"].update(filename='output.png')
        except:
            print('OMG！添加失败了！')

        cv2.destroyAllWindows()
```
这里我选用的是 PySimpleGUI 框架来做的，比较简单。界面分为左右两部分，左边是两个按钮（确定和取消）加一个文件夹选择器，再加一个图片文件列表；右边是一个图片展示框。

左边选择文件夹后，会在下方列出文件夹里包含 `.png` 和 `.jpg` 的图片列表。点击图片列表中的图片，会在右边显示你所选择的图片。这个选中的图片也就是我们后面需要添加圣诞帽的图片。

这里需要注意的是，PySimpleGUI 的图片展示默认只支持 png 格式的，所以我在展示的时候做了判断，如果是 jpg 格式的图片，我就用 cv2 将其转换成 png 格式，然后再进行展示。

到这里，我们的关键步骤就完成了。接下来就是将我们两部分代码进行整合。其实也很简单，只需要在 GUI 界面上用户点击 “生成” 按钮时，后台接收到图片的路径，传递给我们的图片处理函数，在处理完后将图片保存在文件夹下，并更新 GUI 界面右边的展示的图片即可。

最终的运行效果：

![](http://www.justdopython.com/assets/images/2021/12/christmashat/9.gif)



#### 打包软件

打包软件我们还是用熟悉的 pyinstaller 模块，将代码打包成可执行的 exe 格式。

首先下载我们所需的模块包：

> pip install pyinstaller

接着在命令行敲下打包命令：

> pyinstaller christmashat.py

这个 `christmashat.py` 就是我们所写的程序了。

打包比较耗时，耐心等着就行。打包完成后，在我们代码的目录下会生成三个文件夹：

- `__pycache__`
- `build`
- `dist`

我们只需要关注 `dist` 就行。 `dist` 文件夹下面是 `christmashat` 子文件夹，再进去就可以找到我们的 `christmashat.exe` 文件了。由于我们的程序运行有两个依赖文件，分别是我们的圣诞帽图片和我们的人脸识别训练集，所以我们需要将这两个文件放入这个 EXE 文件所在的文件夹下。

现在双击 `christmashat.exe` 文件就可以正常运行了。

### 总结

本文从一个实际需求出发，向大家讲解了一个头像添加圣诞帽软件的诞生过程。相对于之前的一些小应用来说，涉及的知识点较多，可能还是有点复杂的。其中有一些知识点限于篇幅原因没有详细讲解，大家可以自己私下补充。

如果你觉得一时半会儿搞不定这个程序，可以先点个 **`在看`** 和 **`赞`**，然后直接获取可执行软件，过完这个圣诞节再去仔细研究。

软件获取方法：

点 **`在看`** 和 **`赞`** 之后，在公众号对话框输入暗号 “**圣诞帽**” 即可获取下载链接。


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/christmashat)



