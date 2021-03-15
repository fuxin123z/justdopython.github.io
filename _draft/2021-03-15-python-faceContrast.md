---
layout: post
category: python
title: 上班摸鱼程序，再也不怕领导偷偷出现在身后了
tagline: by 某某白米饭
tags: 
  - python
---

当你在上班摸鱼的时候，领导总会偷偷摸摸的出现在你的背后，例如小编曾经偷偷摸摸看《轻音》被抓包了。今天我们就用 Python 来破解这个摸鱼被抓的套路，主要的思路是用 opencv 调用电脑摄像头检测和比对人脸，当领导出现在后面的时候打开指定的应用程序浑水摸鱼。

<!--more-->

![](http://www.justdopython.com/assets/images/2021/03/faceContrast/1.png)

### 安装模块

在写程序之前得把 opencv 调用摄像头模块和 face_locations 人脸识别模块安装好。

```
# opencv 模块
pip3 insatll opencv-python
```

```
# face_locations 模块
pip3 install cmake
pip3 install face_recognition
```

### 人脸识别

先把领导的人脸进行编码，放入内存中以便随时和摄像头捕捉到的人脸识别进行编码比对。

例如对下图进行面部编码

![](http://www.justdopython.com/assets/images/2021/03/faceContrast/0.png)

```
import face_recognition

# 加载图片
pic_boss = face_recognition.load_image_file("/Users/xx/Desktop/face/0.png")
# 得到面部编码
boss_face_encoding = face_recognition.face_encodings(pic_boss)[0]
```

示例结果

```
[-0.02630499  0.12300251  0.01698755  0.01275834 -0.07418888 -0.00981654
 -0.03014973 -0.16349442  0.11407443 -0.03254088  0.26810074 -0.10167226
 -0.15427223 -0.11180711  0.01873804  0.18030289 -0.14980686 -0.12194286
 -0.02620432 -0.03438358  0.04720668  0.05182001  0.009987    0.09340413
 -0.11347414 -0.26094455 -0.07678577 -0.09128669  0.08928929 -0.07264765
 -0.11346096  0.1254302  -0.20916753 -0.10639326  0.09938065  0.05473833
 -0.04935627 -0.06184902  0.17554277 -0.02231439 -0.19398358  0.01744412
  0.10445927  0.26399308  0.21656345  0.05588599  0.00760998 -0.13855973
  0.12407181 -0.09017442  0.09778374  0.11776066  0.08498169  0.07626694
 -0.01237833 -0.20856641  0.02468708  0.06579788 -0.12179989  0.02987257
  0.1338616  -0.07621925  0.01559527 -0.03452411  0.18915619  0.01698355
 -0.04450341 -0.2167782   0.09793964 -0.11409818 -0.10012487  0.13745219
 -0.17124982 -0.15017164 -0.34856451 -0.01826046  0.41654593  0.09037441
 -0.21255262  0.04289294  0.01760755 -0.01859214  0.20364219  0.14642054
  0.00619181 -0.02451363 -0.15138477  0.00500458  0.25368348 -0.02767867
 -0.09737059  0.17870165 -0.02200082  0.03460512  0.03690759  0.06052291
 -0.0686012   0.04330266 -0.15649761 -0.09057935  0.00870521  0.04586265
 -0.04279764  0.18815981 -0.15697879  0.17292421  0.03271531  0.08370531
 -0.04779428 -0.05095051 -0.08721299  0.01937558  0.10537415 -0.21216688
  0.16163379  0.07646587  0.09025833  0.08259746  0.08811771  0.06535679
 -0.01029789 -0.06432205 -0.25512969 -0.03111095  0.12503427 -0.02948561
  0.15236887  0.03259711]
```

### 调用摄像头

用 cv2.VideoCapture(0) 方法调起摄像头，并把摄像头的每一个帧的图像进行面部编码，最后使用 face_recognition.compare_faces() 方法进行人脸比对。

```
import face_recognition
import cv2
import os
import time

# 调用摄像头，外部摄像头为：1
cap = cv2.VideoCapture(0)

while True:

    # 按帧读取视频
    # 其中ret是布尔值，如果读取帧是正确的则返回 True，
    # frame就是每一帧的图像
    ret, frame = cap.read()
    
    # 进行面部编码
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # 人脸对比
        results = face_recognition.compare_faces([boss_face_encoding], face_encoding)

        if results[0]:
            print("boss来了，快打开其他应用")

            os.system('open /Applications/PyCharm.app')
            time.sleep(300)
```


需要注意的是 cv2.VideoCapture(0) 方法在 VSCode 中用终端调用会报：Abort trap: 6 的错误。

![](http://www.justdopython.com/assets/images/2021/03/faceContrast/2.png)

在系统自带的终端中运行则没这个问题。

### 总结

在上班可以摸鱼的时候好好摸鱼，该拼命奋斗的时候千万千万别摸鱼了。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/faceContrast>
