---
layout: post
title: 用Python对摩斯密码加解密
category: python
tagline: by 闲欢
tags: 
  - python
  - 密码
  - 加密
  - 摩斯密码
---



![封面](http://www.justdopython.com/assets/images/2022/02/morse/0.jpg)


![](http://www.justdopython.com/assets/images/2022/02/morse/1.mp4)

在电影《无间道》中，刘建明（刘德华饰）作为黑帮的卧底在一次行动中发现了警察的卧底陈永仁（梁朝伟饰）与黄警督（黄秋生饰）通过摩斯电码进行通讯，经过紧急的群发区域短信 "有内鬼，终止交易" 避免了黑帮头目被抓。

通过动图能看到黄警督和陈永仁仅通过手指的敲击就能完成通讯，是不是很神奇？

<!--more-->

### 摩尔斯电码

摩斯密码的定义如下：

> 摩尔斯电码（ 又译为摩斯密码，英语：Morse code）是一种时通时断的信号代码，通过不同的排列顺序来表达不同的英文字母、数字和标点符号。是由美国人艾尔菲德·维尔与萨缪尔·摩尔斯在1836年发明。

摩尔斯电码是一种早期的数码化通信形式，它依靠一系列的**点和划**来传递编码信息，它的代码包括五种：

- 点（ · ）：1 （读 “滴” dit ，时间占据1t ）
- 划（—）：111 （读 “嗒” dah ，时间占据3t ）
- 字符内部的停顿（在点和划之间）：0 （时间占据1t ）
- 字符间停顿：000 （ 时间占据3t ）
- 单词间的停顿：0000000 （ 时间占据7t ）

点的长度（也就是上面的时间长度t）决定了发报的速度。

我们的英文字母、数字和标点符号与摩斯密码的对照图如下：

![](http://www.justdopython.com/assets/images/2022/02/morse/1.jpg)

我们现在要发送 “M O R S E(空格) C O D E” （morse code）这单词，通过查表可知，它应该是这样
> —— ——— ·—· ··· · / —·—· ——— —·· ·

对应的报文应该如下（滴 表示敲击，▢ 表示停顿）

> 滴滴滴▢滴滴滴▢▢▢滴滴滴▢滴滴滴▢滴滴滴▢▢▢滴▢滴滴滴▢滴▢▢▢滴▢滴▢滴▢▢▢滴▢▢▢▢▢▢▢滴滴滴▢滴▢滴滴滴▢滴▢▢▢滴滴滴▢滴滴滴▢滴滴滴

是不是很有意思？


### Python实现

用 Python 实现摩斯密码的加解密，其实很简单，只需要把对照表放在一个字典中，加密的时候将明文拆分，然后从字典中取出对应的密码组合在一起，解密的时候就是通过密文去对照表找对应的明文，然后拼在一起就行。

#### 摩斯密码对照表

我们把摩斯密码对照表用字典存储之后，是这样的：

```python
MORSE_CODE_DICT = {
                   'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..', 
                   '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', 
                   '7': '--...', '8': '---..', '9': '----.', '0': '-----', 
                   ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', 
                   '(': '-.--.', ')': '-.--.-'
                   }

```


#### 加密

加密的过程就是将明文通过对照表翻译成密文的过程。

我们逐个读取明文，如果是字母、数字或者标点符号就到字典里面找对应的密码，字符之间用空格隔开，如果是单词之间的空格，就添加两个连续空格，以隔开单词。

加密过程的代码如下：

```python
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            # 查字典并添加对应的摩斯密码
            # 用空格分隔不同字符的摩斯密码
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1个空格表示不同的字符
            # 2表示不同的词
            cipher += ' '
    return cipher
```


#### 解密

在解密的情况下，我们首先在要解码的字符串末尾添加一个空格，我们从字符串中提取字符。

一旦我们得到一个空格，我们就会在提取的字符序列（或我们的莫尔斯电码）中查找相应的英语字符，并将其添加到将存储结果的变量中。

一旦我们得到 2 个连续的空格，我们就会向包含解码字符串的变量添加另一个空格。

字符串末尾的最后一个空格将帮助我们识别莫尔斯电码字符的最后一个序列。

解密过程的代码如下：

```python
# 将字符串从摩斯解密为英文的函数
def decrypt(message):
    # 在末尾添加额外空间以访问最后一个摩斯密码
    message += ' '
    decipher = ''
    citext = ''
    global i
    for letter in message:
        # 检查空间
        if letter != ' ':
            i = 0
            # 在空格的情况下
            citext += letter
        # 在空间的情况下
        else:
            # 如果 i = 1 表示一个新字符
            i += 1
            # 如果 i = 2 表示一个新单词
            if i == 2:
                # 添加空格来分隔单词
                decipher += ' '
            else:
                # 使用它们的值访问密钥（加密的反向）
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return decipher

```

#### 测试

我们先来测试一下加密算法：

```python
message = "I LOVE YOU"
result = encrypt(message.upper())
print(result)

```

运行结果是：

> ..  .-.. --- ...- .  -.-- --- ..- 

大家可以自己对照着映射表来看看是否正确。

再测试一下解密算法：

```python
message = "..  .-.. --- ...- .  -.-- --- ..-"
result = decrypt(message)
print(result)

```

运行结果是：

> I LOVE YOU


### 总结

整个摩斯密码加密和解密的过程就是对字符串的操作，还比较简单。但是想想那些特务啥的通过敲击声或者其他方式去人工解密，还是有点技术难度的。这个加解密的程序装一下 13 还是蛮有用的，你觉得呢？



