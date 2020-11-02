---
layout: post
category: python
title: 奇技淫巧不可取，切记切记
tagline: by 轩辕御龙
tags:
  - python
---

# 奇技淫巧不可取，切记切记

之前我们介绍过Python有一个模块可以用来检查代码风格，并且u1s1，检查得还挺严的，搞得阿酱还挺怕怕的

就像读书时候有一个严厉的老大哥、啊不对，老师，一直始终盯着你，一旦犯错就会对你提出严厉的批评，羞得你无地自容。

<!--more-->

![01](http://www.justdopython.com/assets/images/2020/10/2020-10-20-abuse-of-list-comprehension/01.jpg)

上次就是这个老师，又把阿酱给训了一顿。不过讲心里话，老师训得还是有道理的，阿酱虽然口头上不爽嘟囔两句，但物理上也还是从善如流的——这肯定不是怕了老师手上的戒尺。

下面我就给大家好好儿讲讲我是怎么被训的——

## 问题呈现

作为Python的语法糖之一，想必大家对于**列表生成式**都已经熟悉得不能再熟悉了，甚至现在立马走出门去，不懂列表生成式都不敢理直气壮地说自己是个Pythonista——到了这种程度。

> 另外附赠一篇《[Pythoneer和Pythonista的区别](https://www.quora.com/Whats-the-exact-difference-between-a-Pythoneer-and-a-Pythonista)》以飨大家，不另行收费。
>
> ——啊！好像我们本来也不收费？

但是上次坑了阿酱的恰好就是这个列表生成式，这里也跟大家share一下阿酱的辛酸故事。（类似的话我前两句是不是才说过来着

话说那是一个月黑风高的夜晚（程序猿加班很正常对伐？所以这个描述很合理且应景），阿酱当时辛辛苦苦耕耘，码出了好长一段代码，然后喜滋滋地例行pylint扫了一下……

![02](http://www.justdopython.com/assets/images/2020/10/2020-10-20-abuse-of-list-comprehension/02.jpg)

啊咧？什么鬼？

```shell
R1721: Unnecessary use of a comprehension
```

不需要用列表生成式？

写的啥？

```python
l = [n for n in range(10)]
```

有毛病吗？这有毛病吗？这***有啥毛病啊？你倒是说啊？我这代码有什么问题？咋就不该用列表生成式了？那你让我用啥？用爱吗？

![03](http://www.justdopython.com/assets/images/2020/10/2020-10-20-abuse-of-list-comprehension/03.jpg)

## 冤有头债有主

好了到这里卡住了，接下来有请我们永远滴神——Google老大爷蹒跚登场

输入，搜索，到手！

![04](http://www.justdopython.com/assets/images/2020/10/2020-10-20-abuse-of-list-comprehension/04.png)

让我们点开看起来更正规的第二个链接——至于我为什么说第二个更正规呢？阿酱当然不会告诉你我已经都点开看过了

翻译一下，第二个链接标题“Enhancement: Add a [unnecessary-comprehension]-checker”，大概是“改进点：添加[unnecessary-comprehension]检查器”这么个意思——

什么什么？你给我等下。

感情刚刚困扰我的那个规范问题还是打你这儿出来的啊，冤有头债有主，别怪我不客……咳，读书人的事，终归还是讲点道理的，咱们还是先把这链接的内容看完，再不客气也不迟。

这位老哥说了啥来着？

> ...
>
> we could implement a checker that detects list/dict/set-comprehensions that can be replaced by the corresponding list/dict/set-constructors, which is faster and more readable.
> For example:
>
> - `list(iterable)` instead of `[x for x in iterable]`
> - `dict(some_dict)` instead of `{k: v for k, v in some_dict}`
> - `set(iterable)` instead of `{e for e in iterable}`
>
> Although these cases seem trivial/obvious, I think having such a checker would help in cases where longer/more complex variable-names are used.
>
> ...

老哥说，他要实现这么一个检查器，检查出那些可以被list/set/dict构造器替换的list/set/dict生成式，使代码性能更佳、可读性更好。具体来说有这么些blabla的示例。

再仔细一看，嗨，真有道理

你看看这个列表生成式，`[x for x in iterable]`，这不是脱了屁股放……啊错了，脱了裤子放屁吗？一个个迭代出来可迭代对象中的元素，然后原封不动地组装成一个列表；这种弱智活，直接交给内置的`list`不香吗？还会有傻*蠢到用列表生成式？哈哈哈哈哈哈，𥫗——

淦！我TM就是那个傻*？

## 奇技淫巧要慎用

u1s1，在此之前，我从来没有想过，一个简单的列表生成式还有这么多的讲究，压根儿就没有考虑过怎么样才能**有效**地使用Python的语法糖。

然而实际上，事实证明语法糖毕竟是语法糖，有其适用的场景，当然也有其不适用的场景。

没有什么东西是~~万金油~~银弹（这个修改是阿酱为了显得与国际接轨），只有用在了对的地方，它才能被称之为“语法糖”；否则更像是“语法毒药”，污染好大一片数字江山。

包括阿酱在内的不少同学，可能学了一阵儿Python，就沉浸于其中的各种奇技淫巧，每次遇到任何场景，都是不管三七二十一，直接套上一个trick。

**你以为你是四两拨千斤，其实不过是大力出奇迹。**

pylint增加的这个检查器能够检查的项不止于列表生成式这么一小块门类，继续阅读之前那个链接我们可以发现一套很有意义的范例，其中注释为`[unnecessary-comprehension]`的代码行，都是相关生成式的“坏的实践”，值得我们引以为鉴。

相关内容作为附录附在本文之后。

## 总结

本文我们再次（阿酱要哭了）从阿酱遇到的实际问题说开去，警醒了一些有点飘的同学：我们一定要脚踏实地，仰望星空；艰苦奋斗，持续搬砖。

奇技淫巧可以用，但是一定要分清场景。

## 参考资料

[Enhancement: Add a [unnecessary-comprehension]-checker #2905](https://github.com/PyCQA/pylint/issues/2905)

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-10-20-abuse-of-list-comprehension

## 附录

```python
# For name-reference see https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries

# List comprehensions
[x for x in iterable]  # [unnecessary-comprehension]
[y for x in iterable]  # expression != target_list
[x for x,y,z in iterable]  # expression != target_list
[(x,y,z) for x,y,z in iterable]  # [unnecessary-comprehension]
[(x,y,z) for (x,y,z) in iterable]  # [unnecessary-comprehension]
[x for x, *y in iterable]  # expression != target_list
[x for x in iterable if condition]  # exclude comp_if
[y for x in iterable for y in x]  # exclude nested comprehensions

# Set comprehensions
{x for x in iterable}  # [unnecessary-comprehension]
{y for x in iterable}  # expression != target_list
{x for x,y,z in iterable}  # expression != target_list
{(x,y,z) for x,y,z in iterable}  # [unnecessary-comprehension]
{(x,y,z) for (x, y, z) in iterable}  # [unnecessary-comprehension]
{x for x, *y in iterable}  # expression != target_list
{x for x in iterable if condition}  # exclude comp_if
{y for x in iterable for y in x}  # exclude nested comprehensions

# Dictionary comprehensions
{k: v for k, v in iterable}  # [unnecessary-comprehension]
{v: k for k, v in iterable}  # key value wrong order
{k: v for (k, v) in iterable}  # [unnecessary-comprehension]
{x: y for x,y,z in iterable}  # expression != target_list
{x[0]: x[1] for *x in iterable}  # [unnecessary-comprehension]
{x: y for x, y in iterable if condition}  # exclude comp_if
{y: z for x in iterable for y, z in x}  # exclude nested comprehensions
```

