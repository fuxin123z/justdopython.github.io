---
layout: post
category: Leetcode面试题
title:  LeetCode面试系列之：No.771 - 宝石与石头
tagline: by 萌较瘦
tags: 
  - LeetCode面试题系列
---



去年，萌较瘦我为大家分析了十多道LeetCode 面试题，相信大家在其中也有所收获。今天我们接着来分析一道轻松的字符串问题吧，题目为: **石头中找宝石**。

<!--more-->

![Leetcode](http://www.justdopython.com/assets/images/2019/python/LeetCode.png)

今天要给大家分析的面试题是 LeetCode 上第 **771** 号问题，

LeetCode - 771. 宝石与石头

<https://leetcode-cn.com/classic/problems/largest-perimeter-triangle/>



### 题目描述

给定字符串`J` 代表石头中宝石的类型，和字符串 `S`代表你拥有的石头。 `S` 中每个字符代表了一种你拥有的石头的类型，你想知道你拥有的石头中有多少是宝石。

`J` 中的字母不重复，`J` 和 `S`中的所有字符都是字母。字母区分大小写，因此`"a"`和`"A"`是不同类型的石头。

**示例 1:**

```
输入: J = "aA", S = "aAAbbbb"
输出: 3
```

**示例 2:**

```
输入: J = "z", S = "ZZ"
输出: 0
```

**注意:**

- `S` 和 `J` 最多含有50个字母。
-  `J` 中的字符不重复。

- 题目难度：**简单**

- 通过次数：69.8K

- 提交次数：85.3K

- 贡献者：LeetCode

  

- 相关标签 

  - 哈希表

    <https://leetcode-cn.com/tag/hash-table>

    

- 难度: **简单**



**解题思路:**

首先，我们理解一下题意，就是需要统计字符串`S`中有多少次出现`J`中含有的字符。

于是，我们只需要遍历字符串 `S`，另外对`J`中的字符进行去除重复，转换为set就行，而题目中提到 `J`中字符不重复，于是也不需要转成 set 了。

接下来，就是区分出 J 中字符，然后统计每一种字符出现的次数(用`count`函数)，最后求和即可~



已 AC 代码:

```python
class Solution:
    def numJewelsInStones(self, J: str, S: str) -> int:
        sum0 = 0

        for j in J:
            sum0 = sum0 + S.count(j)
        return sum0
```



**运行结果:**

![运行结果1](C:\Users\Bruce\Desktop\运行结果1.png)

执行用时: `36 ms`, 在所有 Python3 提交中击败了`59.15%`的用户.



示例代码: <https://github.com/JustDoPython/leetcode-python/tree/master/leetcode-976> .