---
layout: post
category: python
title: 第101天： Python XGBoost算法项目实战
tagline: by 戴景波
tags: 
  - python100
---

## Python实现机器学习

如果你的机器学习预测模型表现得不尽如人意，那就用XGBoost。XGBoost算法现在已经成为很多数据工程师的重要武器。

<!--more-->

说到XGBoost，不得不提GBDT(Gradient Boosting Decision Tree)。

因为XGBoost本质上还是一个GBDT，但是力争把速度和效率发挥到极致，所以叫X (Extreme) GBoosted。

包括前面说过，两者都是boosting方法。XGBoost高效地实现了GBDT算法并进行了算法和工程上的许多改进，被广泛应用在Kaggle竞赛及其他许多机器学习竞赛中并取得了不错的成绩。

这一篇最适合刚刚接触XGBoost的人阅读，通过一个实战项目拆解整个XGBoost算法。

对于第71天爬取到的数据如下：（作为训练集FBP_train.csv）
ID列为每一场比赛，从0或1开始递增，ysb、li等代表易胜博、立博等公司的初始主队获胜赔率，最后一列y代表比赛结果，1代表主队获胜，2代表主队不胜。

以下代码构造训练集，爬取新的预测集放到FBP_predict.csv

```python
    trainFilePath = 'E:/PythonLearn/pc_ex/AdaBoost_PeiLv/FBP_train.csv'
    testFilePath = 'E:/PythonLearn/pc_ex/AdaBoost_PeiLv/FBP_predict.csv'
    data = pd.read_csv(trainFilePath)
    X_test= pd.read_csv(testFilePath)
###############第二处调参：选择全部特征还是部分特征###########################
    X_train=data[[f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10]]#全特征
    y_train=data['y']
    trainandTest(X_train, y_train,X_test)
```

将数据加载到对应变量后通过参数传递给trainandTest函数：
其中train_test_split函数是sklearn.cross_validation模块中用来按比例划分训练集和测试集，第一个参数X是被划分的样本特征集;

第二个参数y是被划分的样本标签;

第三个参数test_size是样本占比;

第四个参数是随机数的种子，其实就是该组随机数的编号，在需要重复试验的时候，保证得到一组一样的随机数。
比如你每次都填1，其他参数一样的情况下你得到的随机数组是一样的。

但填0或不填，每次都会不一样。随机数的产生取决于种子，随机数和种子之间的关系遵从以下两个规则：种子不同，产生不同的随机数；
种子相同，即使实例不同也产生相同的随机数。

model=XGBClassifier()为 XGBoost训练过程。此处用无参数的函数。当然也可以自己手动调整里边的参数，但需多次回测才能调整最优参数，建议用无参数的XGBClassifier方法让系统自己选择最优参数。

```python
def trainandTest(X, y,X_t):
    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.33, random_state=7)   
    #####特征向量化############
    vec=DictVectorizer(sparse=False)
    ###########归一化和标准化#################
    X_train=vec.fit_transform(X_train.to_dict(orient='record'))
    X_test=vec.transform(X_t.to_dict(orient='record'))
    model=XGBClassifier()#无参数
    model.fit(X_train,y_train)
    # 对测试集进行预测
    ans = model.predict(X_test)
    ans_len = len(ans)    id_list = np.arange(5953, 5956)
    data_arr = []
    for row in range(0, ans_len):
        data_arr.append([int(id_list[row]), ans[row]])
        print(ans[row])
    np_data = np.array(data_arr)
    # 写入文件
    pd_data = pd.DataFrame(np_data, columns=['id', 'y'])
    pd_data.to_csv('FBP_submit.csv', index=None)
```

首先通过train_test_split函数按照33%的比例分割训练集X和对应的结果标签y，得到新的训练集X_train和对应的结果标签y_train;

再经过DictVectorizer将赔率特征转化为向量形式，再经过fit_transform可以理解为先fit拟合后transform标准化，同理对预测集X_t也进行拟合-标准化。

这时就可以新建模型model了，按照拟合标准化后的X_train训练集进行进一步拟合模型，用此模型对标准化的预测集进行预测了。

将返回的预测结果存到列表data_arr，再通过DataFrame存到CSV文件中。

注：(github.com.cn/acredjb/FBP有完整机器学习源码)

## 总结

以上我们以一个实战项目为依托，从零开始，深入浅出，让读者能够实践Python机器学习的整个过程。

## 代码地址


> 示例代码：[Python-100-days-day101](https://github.com/JustDoPython/python-100-day/tree/master/day-101)

