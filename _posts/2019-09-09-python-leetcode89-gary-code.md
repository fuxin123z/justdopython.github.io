---
layout: post
title:  Python玩转Leetcode面试题系列 - 格雷码
tagline: by 萌较瘦
category: Leetcode面试题
copyright: python
excerpt: Leetcode面试题系列
---

最近，打算花点时间写个Python解决Leetcode题的系列文章~

大家是否还记得黑客帝国中的数字雨林的场景？事实上，计算机底层数据的存储和运算都是二进制的，因而面试题环节中面试官也经常会问到二进制相关问题。

![matrix](https://dev.tencent.com/u/legege007/p/leetcode-pySol/git/raw/master/images/matrix-01.gif)


比较典型的一个问题是 Leetcode 上第 89 号问题，

Leetcode 89. Gray Code

在线提交地址: <https://leetcode-cn.com/problems/gray-code/>
<!--more-->


### 题目描述

------

   格雷编码是一个二进制数字系统，在该系统中，两个连续的数值仅有一个位数的差异。

   给定一个代表编码总位数的非负整数 n，打印格雷码序列。格雷码序列必须以 0 开头。

   例如，给定 *n* = 2，返回 **[0,1,3,2]**。其格雷编码是：
```
　00 - 0
　01 - 1
　11 - 3
　10 - 2
```

 

  **说明:**

   对于给定的 *n*，其格雷编码的顺序并不唯一(因此返回结果的顺序不重要，可使用Vector或List)。

   例如 [0,2,3,1]也是一个有效的格雷编码顺序。

------
&nbsp; ● &nbsp;题目难度:  **Medium**

   - 相关话题 [回溯算法](https://leetcode-cn.com/tag/backtracking)

     相似题目 [1比特与2比特字符](https://leetcode-cn.com/problems/1-bit-and-2-bit-characters)

------



**解题思路:**

格雷码有个相应的数学公式，整数 *i*  的格雷码是i^(i/2)。而此题并没要求返回结果中的值的严格顺序。

![grayCode](https://dev.tencent.com/u/legege007/p/leetcode-pySol/git/raw/master/images/grayCode.png)

于是只需遍历从 0 到 2^n - 1的所有整数 *i*，使用公式将其转换为格雷码，添加到List中即可。



已AC代码(Python 3):

```python
class Solution:
    def grayCode(self, n: int) -> List[int]:
        res = [] 
        for i in range(1 << n): 
            res.append((i >> 1) ^ i) 
        return res
```



![code](https://dev.tencent.com/u/legege007/p/leetcode-pySol/git/raw/master/images/leetcode89-code.JPG)



如果需要在本地测试，需要先在代码开头引入`from typing import List`，然后实例化 `Solution`，最后调用相应的method即可。完整代码如下:

```python
from typing import List

class Solution:
    def grayCode(self, n: int) -> List[int]:
        res = [] 
        for i in range(1 << n): 
            res.append((i >> 1) ^ i) 
        return res
        
# 以下是测试代码
obj = Solution()
print(obj.grayCode(2))
```



**运行结果:**

执行用时: `48 ms`, 在所有 Python3 提交中击败了`87.40%`的用户。


**参考:**

[LeetCode] Gray Code - 穆穆兔兔 - 博客园

https://www.cnblogs.com/diegodu/p/4371807.html
