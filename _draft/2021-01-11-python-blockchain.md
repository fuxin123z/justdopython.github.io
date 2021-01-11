---
layout: post
category: python
title: 比特币涨疯了，区块链是什么鬼？
tagline: by 太阳雪
tags:
  - python
  - 比特币
  - 区块链技术
---
2020 年底，数字货币鼻祖，比特币，高歌猛进，突破了惊人的 3万美元，直逼4万美元，再一次引起世人的眼球，又是一场褒贬不一，血雨腥风……
<!--more--->
![](http://justdopython.com/assets/images/2021/01/blockchain/01.jpg)

我们作为有头脑、有理智、有技术的人，不能像大多数人那样趋之若鹜，看个热闹就完了。那么这么厉害的、建立在计算机和网络之上的比特币，它的底层技术是什么呢？又，是如何才能实现的呢？

今天，我们用不到 50 行的代码，了解和领略一下比特币底层技术 —— 区块链的魅力吧，另外还有在实际项目中的应用噢，让同事刮目相看的机会来了，开干

## 什么是区块链

简单来说，区块链就是一系列的记录的集合，可以理解成数据库，不同的是，这些记录直接都通过一种类型链的东西串联在一起

如果链上的一个环节出了问题，那么它后面的记录就有问题，因此必须保证链上的记录都是真实可靠的链在一起的

也就是，后面的记录加入之前，需要和前面的数据关联起来才能加入

可想而知，这样的方式可以有效地防止数据被篡改，比如前面的数据被修改后，后面的数据与前面的数据将不匹配，很快就可以发现

这就是区块链的基本概念，就在这个简单的概念上，区块链催生了新的、完全数字化的货币，这些货币并不是由中心控制系统控制的，而是分布在整个互联网上，如比特币和莱特币。

而且区块链技术还在不断地革新，例如以太坊，Mixin 等等

## 区块链的原理

区块链的概念看起来挺简单的，实现原理是什么呢？

这里就需要了解一个概念，那就是 **数子签名**，也可以叫做 **不对称加密**

因为信息是由一系列字符成的，对于一个区块的记录来说，也可以看出一系列的字符，比如一个表示姓名和年龄的字符串:

`name:Tom;age:18`

对这个字符串进行 `Md5` 加密(一种常用的数字签名算法)，会得到类似这样的字符串：

```python
from hashlib import md5

m = md5()
m.update(b"name:Tom;age:18")
m.hexdigest()
# 'ca8d85b134922fe48d17bf36ceb38046'  当前记录的特征码
```

可以理解为记录的一个特征码

如果再来一条记录：`name:Jim;age:19`

特征码很好计算，不过怎么和上一条记录链接起来呢？

方法就是将上一个记录的特征码，一起编织在这一条的特征码中，例如：

`lastHash:ca8d85b134922fe48d17bf36ceb38046;name:Jim;age:19`

然后得到特征码：

```python
from hashlib import md5

m = md5()
m.update(b"lastHash:ca8d85b134922fe48d17bf36ceb38046;name:Jim;age:19")
m.hexdigest()
# '82391695a3760b2de1c92d512b83cc14'  当前记录的特征码
```

这样就完成了记录直接的链接

经验一条记录是否被修改，或者连续，只需要对这条记录和其上一记录一起重算一次特征码就好了

![](http://justdopython.com/assets/images/2021/01/blockchain/02.jpg)

当然，比特币，或者由实际应用的区块链会更为复杂，比如字段、加密算法等

## 实现一个区块链

下面，我们来实现一个比较完整的区块链

首先定义一个区块类：

```python
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("utf-8"))
        return sha.hexdigest()
```

- 初始化方法中，初始化了当前区块的索引、时间戳、数据（业务相关的信息）、紧前区块（上一个区块）的特征值，和当前区块的特征值
- `hash_block` 根据初始化中的一些信息，得到一个特征值，就是用它来计算当前区块的特征值

接下来，区块链中的第一个区块的特征值如何计算，它的紧前特征值是什么？

我们来定义一个产生 `起始区块` 的方法：

```python
def create_genesis_block():
    # 手工创建第一个区块，其索引为 0，且随意取给紧前特征值 '0'
    return Block(0, date.datetime.now(), "Genesis Block", "0")
```

然后，我们定义一个生成新区块的方法：

```python
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)
```

- 参数是 `紧前` 区块对象
- 对索引做递增处理
- 得到当前时间戳
- 产生区块业务数据（为了简便只做了相对固定的内容）
- 记录上个区块的特征值
- 最后根据以上信息，得到一个新区块

现在所有的基础工作已经完成了，我们建立一个区块数据库，即区块链，并计入第一个区块

```python
blockchain = [create_genesis_block()]
```

最后我们模拟一个产生区块的过程：

```python
# 设置产生区块的个数
num_of_blocks_to_add = 20

# 产生区块并加入区块链
for i in range(0, num_of_blocks_to_add):
    previous_block = blockchain[-1]
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    # 发布当前区块的信息
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))
```

运行后，我们可以得到如下结果：

```txt
Block #1 has been added to the blockchain!
Hash: 788ec79310315740f7df959e03c8788f102c3e02d6b6ce6488ed7b7d04cc3e01

Block #2 has been added to the blockchain!
Hash: 5b6c6e0be9659ae359356015ffe9ba9e4645f181d848bfd5127dd24d29f1747c

Block #3 has been added to the blockchain!
Hash: c40e3accb5de25728770754f24d7504cc72b8138d465f5d8f1b84ad149c9b59c

Block #4 has been added to the blockchain!
Hash: 9a118b7c8b90aaab2fe6a59dd84224adb90ba4af8aaa03bf4c9b08799cc81d9b

Block #5 has been added to the blockchain!
Hash: f8fbd5b6684d926fb96dd36b89f61db3c868...<省略>...
```

显示的结果就是区块链上的信息

实际当中，是在分布式环境下运行的，需要考虑更多的因素，如调度，合并，以及选举等，加密算法也需要更为安全，例如常用的是 `椭圆曲线加密算法(ECC)`, 来加强区块链的安全性和可靠性，但最基本的实现逻辑是一样的。

## 应用

有句虐心的话：

> 明白了很多道理，却还是过不好这一生

虽然粗浅地了解了区块链的基本概念和实现，然而有什么用呢？

既不能取改比特币（再说也不需要改），也不能创建一个区块链应用（虽然不是不可能）

不过这种思想可以在很多地方得到应用

这里我列举一个我实际工作中的例子：

在一个项目上，需要实现一个审计日志功能，基本要求就是需要**连续**并**防篡改**

如果不了解区块链的算法的话，可能需要考虑半天，然后得到一个蹩脚的方式，比如用额外的记录来控制日志记录，或者记录关联关系（之前确实这么干过）

现在，只需要在记录中增加两个字段：`上一个记录的特征码` 和 `当前特征码`

再实现一个，根据指定字段，计算特征码的方法

为了便于识别，再加一个检验方法，就好了

除了这样的应用，你还能想到哪些应用呢？欢迎留言交流

## 总结

截至写稿(2021年1月9日)，比特币的价格已经接近 27 万了，如此受热捧（也不是一直这么热，理财有风险，投资需谨慎），而其内在原理竟然如此简单

基于加密算法就可以完成可以承载巨大信息量的数据货币世界，这就是所谓 **越简单的, 就越有效和稳定** 的恰当解释

无论什么事物，总有其内在的基本原理和理论做支撑，只有了解和掌握了其内部原理，才能更好地认识一个事物，我们只需要多一些好奇心，多一点耐心就会，比心

## 参考

- [区块链白皮书: https://bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf)
- <https://zhuanlan.zhihu.com/p/28595570>
- <https://zhuanlan.zhihu.com/p/101907402>

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/taiyangxue/blockchain>
