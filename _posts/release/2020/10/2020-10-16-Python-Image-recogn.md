---
layout: post     
title: Python 教你如何给图像分类
category: Python 教你如何给图像分类
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---

在日常生活中总是有给图像分类的场景，比如垃圾分类、不同场景的图像分类等；今天的文章主要是基于图像识别场景进行模型构建。图像识别是通过 Python深度学习来进行模型训练，再使用模型对上传的电子表单进行自动审核与比对后反馈相应的结果。主要是利用 Python Torchvision 来构造模型，Torchvision 服务于Pytorch 深度学习框架，主要是用来生成图片、视频数据集以及训练模型。


### 模型构建
构建模型为了直观，需要使用 Jupyter notebook 进行模型的构建，Jupyter notebook 的安装及使用详见公众号历史文章 [一文吃透 Jupyter Notebook](https://mp.weixin.qq.com/s/w9TSFo9EZ_Jt-KOOzKfvcQ),进入 JupyterNotebook 页面后即可进行编辑。详细页面如下：
![](https://imgkr2.cn-bj.ufileos.com/b4f8c435-15ea-49d6-b41f-3ad545c6a7a6.png?UCloudPublicKey=TOKEN_8d8b72be-579a-4e83-bfd0-5f6ce1546f13&Signature=nZ2BkqYDglV0wVFf1xxD9z5leLA%253D&Expires=1602946283)

#### 导入所需包
图像识别需要用到深度学习相关模块，所以需要导入相应的包，具体导入的包如下：

```python
%reload_ext autoreload
%autoreload 2

import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms as tfs
from torchvision import models
from torch import nn

import matplotlib.pyplot as plt
%matplotlib inline

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

```

#### 是否使用 GPU

模型的训练主要方式是基于 GPU 或者 CPU 训练，在没有 GPU 的条件下就在 CPU 下进行训练，模型的训练需要花费一定的时间，训练时长根据训练集的数据和硬件性能而定，训练结果精确性根据数据的多少和准确性而且，深度学习需要大量的素材才能判断出精确的结果，所以需要申明使用 CPU 进行训练：

```python
# 是否使用GPU
use_gpu = False
```

#### 数据增强

将拿到的数据进行训练集的数据预处理并设置训练分层数，再将拿到的图片进行水平翻转后对图片进行剪裁，
剪裁后将图片进行随机翻转，增强随机对比度以及图片颜色变化

```python
# 数据增强
train_transform = tfs.Compose([
    # 训练集的数据预处理
    tfs.Resize([224, 224]),
    tfs.RandomHorizontalFlip(),
    tfs.RandomCrop(128),
    tfs.ToTensor(),
    tfs.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

test_transform = tfs.Compose([
    tfs.Resize([224,224]),
#     tfs.RandomCrop(128),
    tfs.ToTensor(),
    tfs.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

# 每一个batch的数据集数目
batch_size = 10

```

#### 数据集和验证集准备

模型训练需要准备数据集和验证集，只有足够的照片才能得到更精准的答案。训练集和验证集部分代码如下：

```python
# 构建训练集和验证集
# 
train_set = ImageFolder('./dataset1/train', train_transform)
train_data = DataLoader(train_set, batch_size, shuffle=True, num_workers=0)

valid_set = ImageFolder('./dataset1/valid', test_transform)
valid_data = DataLoader(valid_set, 2*batch_size, shuffle=False, num_workers=0)

train_set.class_to_idx

len(valid_data)

# 数据集准备
try:
    if iter(train_data).next()[0].shape[0] == batch_size and \
    iter(valid_data).next()[0].shape[0] == 2*batch_size:
        print('Dataset is ready!')
    else:
        print('Not success, maybe the batch size is wrong')
except:
    print('not success, image transform is wrong!')
```

#### 模型构建并准备模型

```python
# 构建模型
def get_model():
    model = models.resnet50(pretrained=True)
    model.fc = nn.Linear(2048, 3)
    return model

try:
    model = get_model()
    with torch.no_grad():
        scorce = model(iter(train_data).next()[0])
        print(scorce.shape[0], scorce.shape[1])
    if scorce.shape[0] == batch_size and scorce.shape[1] == 3:
        print('Model is ready!')
    else:
        print('Model is failed!')
except:
    print('model is wrong')

if use_gpu:
    model = model.cuda()
```

#### 构建模型优化器

```python
# 构建loss函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 1e-4)

# 训练的epoches数目
max_epoch = 20

```

#### 模型训练和训练结果可视化

数据集和训练集准备好后进行模型训练和训练结果可视化，部分代码如下：

```python
def train(model, train_data, valid_data, max_epoch, criterion, optimizer):
    freq_print = int(len(train_data) / 3)
    
    metric_log = dict()
    metric_log['train_loss'] = list()
    metric_log['train_acc'] = list()
    if valid_data is not None:
        metric_log['valid_loss'] = list()
        metric_log['valid_acc'] = list()
    
    for e in range(max_epoch):
        model.train()
        running_loss = 0
        running_acc = 0

        for i, data in enumerate(train_data, 1):
            img, label = data
            if use_gpu:
                img = img.cuda()
                label = label.cuda()

            # forward前向传播
            out = model(img)

            # 计算误差
            loss = criterion(out, label.long())

            # 反向传播，更新参数
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 计算准确率
            _, pred = out.max(1)
            num_correct = (pred == label.long()).sum().item()
            acc = num_correct/img.shape[0]

            running_loss += loss.item()
            running_acc +=acc

            if i % freq_print == 0:
                print('[{}]/[{}], train loss: {:.3f}, train acc: {:.3f}' \
                .format(i, len(train_data), running_loss / i, running_acc / i))
        
        metric_log['train_loss'].append(running_loss / len(train_data))
        metric_log['train_acc'].append(running_acc / len(train_data))

        if valid_data is not None:
            model.eval()
            running_loss = 0
            running_acc = 0
            for data in valid_data:
                img, label = data
                if use_gpu:
                    img = img.cuda()
                    label = label.cuda()
                
                # forward前向传播
                out = model(img)

                # 计算误差
                loss = criterion(out, label.long())

                # 计算准确度
                _, pred = out.max(1)
                num_correct = (pred==label.long()).sum().item()
                acc = num_correct/img.shape[0]


                running_loss += loss.item()
                running_acc += acc

            metric_log['valid_loss'].append(running_loss/len(valid_data))
            metric_log['valid_acc'].append(running_acc/len(valid_data))
            print_str = 'epoch: {}, train loss: {:.3f}, train acc: {:.3f}, \
            valid loss: {:.3f}, valid accuracy: {:.3f}'.format(
                        e+1, metric_log['train_loss'][-1], metric_log['train_acc'][-1],
                        metric_log['valid_loss'][-1], metric_log['valid_acc'][-1])
        else:
            print_str = 'epoch: {}, train loss: {:.3f}, train acc: {:.3f}'.format(
                e+1,
                metric_log['train_loss'][-1],
                metric_log['train_acc'][-1])
        print(print_str)

        
    # 可视化
    nrows = 1
    ncols = 2
    figsize= (10, 5)
    _, figs = plt.subplots(nrows, ncols, figsize=figsize)
    if valid_data is not None:
        figs[0].plot(metric_log['train_loss'], label='train loss')
        figs[0].plot(metric_log['valid_loss'], label='valid loss')
        figs[0].axes.set_xlabel('loss')
        figs[0].legend(loc='best')
        figs[1].plot(metric_log['train_acc'], label='train acc')
        figs[1].plot(metric_log['valid_acc'], label='valid acc')
        figs[1].axes.set_xlabel('acc')
        figs[1].legend(loc='best')
    else:
        figs[0].plot(metric_log['train_loss'], label='train loss')
        figs[0].axes.set_xlabel('loss')
        figs[0].legend(loc='best')
        figs[1].plot(metric_log['train_acc'], label='train acc')
        figs[1].axes.set_xlabel('acc')
        figs[1].legend(loc='best')
```

#### 调参进行模型训练

```python
# 用作调参
train(model, train_data, valid_data, max_epoch, criterion, optimizer)
```

#### 保存模型

```python
# 保存模型
torch.save(model.state_dict(), './model/save_model2.pth')
```

### 总结

今天的文章主要是讲图像识别模型如何构建。希望对大家有所帮助。

你安利到了吗？

> 示例代码 [Python 教你如何给图像分类](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/Image_Recogn)