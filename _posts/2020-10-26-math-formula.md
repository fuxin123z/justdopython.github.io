---
layout: post
category: python
title: 没想到 Markdown 还可以这样写(副标：学会它再也不怕编辑数学公式)
tagline: by 極光
tags:
  - python
---

最近在复习高等数学，发现有好多的定理公式需要记住，才能在后续做题中灵活运用，然后就想把这些公式总结到文档中，方便有时间看看加深记忆。首先想到的文档编辑肯定是 `Word` ，但发现 `Word` 编辑公式很不方便，然后发现用 `Markdown` 也可以编辑公式，它可以通过键盘上几个特殊符号和字母数字的组合，就能编辑出想要的公式，所以很方便，现在就带大家一起来学习下。

<!--more-->

## 使用方式

1. 行内公式：可使用 `$`，例如 $ x^2 $
2. 单独一行公式：可使用 `$$`，例如 $$ x + y = z $$
3. 多行公式：可使用 ```math

好，接下来我们分几类介绍下常用的符号。

## 占位符、括号和上下标

|符号|举例|效果|说明|
|---|---|---|---|
|\qquad|x + y \qquad 2n|$x + y \qquad 2n$|两个空格|
|\quad|x + y \quad 2n|$x + y \quad 2n$|单空格|
| \\ |x \ y \ z|$x \ y \ z$|间距（大）|
| \\: |x \\: y \\: z|$x \: y \: z$|间距（中）|
| \\, |x \\, y \\, z|$x \, y \, z$|间距（小）|
| ! |x \\! y \\! z|$x \! y \! z$|间距（无）|
| () |(x)|$(x)$|小括号(最小)|
| \big |\big(x\big)|$\big(x\big)$|小括号(小)|
| \Big |\Big(x\Big)|$\Big(x\Big)$|小括号(中)|
| \bigg |\bigg(x\bigg)|$\bigg(x\bigg)$|小括号(大)|
| \Bigg |\Bigg(x\Bigg)|$\Bigg(x\Bigg)$|小括号(最大)|
| [ ]|[m + n]|$[m + n]$|中括号|
| \{ \}|\{ m + n\}|$\{ m + n\}$|大括号|
| ^ | x^2|$x^2$|上标|
| _ | y_2|$y_2$|下标|

## 运算符号

运算除了可以使用键盘直接录入的加减乘除等简单的运算符外，还可以有以下组合的运算符号。

|符号|举例|效果|说明|
|---|---|---|---|
|\pm| 1 \pm 2|$1 \pm 2$|加减|
|\mp| 1 \mp 2|$1 \mp 2$|减加|
|\times| 1 \times 2|$1 \times 2$|乘号|
|\div| 1 \div 2|$1 \div 2$|除号|
|\cdot| 1 \cdot 2|$1 \cdot 2$|点乘|
|\frac{分子}{分母}|\frac{1+2}{x+3}|$\frac{1+2}{x+3}$|分式（一）|
|{分子} \over {分母}|{x+1} \over {y}|${x+1} \over {y}$|分式（二）|
| \| \| | \|x + 1\|| $\|x + 1\|$ |绝对值 |
|\overline|\overline{abc}|$\overline{abc}$|平均数|
|\sqrt|\sqrt {a + 1}|$\sqrt {a + 1}$|开二次方|
|\sqrt[开方数]{被开方数}|\sqrt[3]{x+1}|$\sqrt[3]{x+1}$|开N次方|
|\log|\log(x+1)|$\log(x+1)$|对数运算|
|\sum|\sum^{a}_{b}{\frac{a+1}{b+2}}|$\sum^{a}_{b}{\frac{a+1}{b+2}}$|求和运算|
|\lim|\displaystyle \lim_{y \to 0}{\frac{x+1}{y+2}}|$\displaystyle \lim_{y \to 0}{\frac{x+1}{y+2}}$|极限运算|
|\int|\displaystyle \int^{\infty}_{0}{xdx}|$\displaystyle \int^{\infty}_{0}{xdx}$|积分运算|
|\partial|\frac{\partial (x+y)}{\partial (y+1)}|$\frac{\partial (x+y)}{\partial (y+1)}$|微分运算|

## 集合运算

|符号|举例|效果|说明|
|---|---|---|---|
|\in|A \in B|$A \in B$|属于|
|\notin|A \notin B|$A \notin B$|不属于|
|\subset|A \subset C|$A \subset C$|子集|
|\supset|A \supset C|$A \supset C$|子集|
|\subseteq|A \subseteq C|$A \subseteq C$|真子集|
|\subsetneq|A \subsetneq C|$A \subsetneq C$|非真子集|
|\not\subset|A \not\subset C|$A \not\subset C$|非子集|
|\cup|A \cup B|$A \cup B$|并集|
|\cap|A \cap B|$A \cap B$|交集|
|\setminus|A \setminus B|$A \setminus B$|差集|
|\bigodot|A \bigodot N|$A \bigodot N$|同或|
|\bigotimes|A \bigotimes N|$A \bigotimes N$|同与|
|\mathbb|\mathbb{R}|$\mathbb{R}$|实数集|
|\emptyset|\emptyset|$\emptyset$|实数集|

## 数学符号

|符号|举例|效果|说明|
|---|---|---|---|
|\infty|\infty|$\infty$|无穷|
|\imath或\jmath|\imath 或 \jmath|$\imath \ 或 \ \jmath$|虚数|
|\hat|\hat{m}|$\hat{m}$||
|\check|\check{m}|$\check{m}$||
|\breve|\breve{m}|$\breve{m}$||
|\tilde|\tilde{m}|$\tilde{m}$||
|\vec|\vec{m}|$\vec{m}$|矢量|
|\grave|\grave{m}|$\grave{m}$||
|\uparrow|\uparrow{m}|$\uparrow{n}$|箭头|
|\rightarrow|\rightarrow{m}|$\rightarrow{n}$|箭头|
|\ldots|1 \ 2 \ \ldots n|$1 \ 2 \ \ldots n$|省略号|

## 常用希腊字母

|符号|举例|效果|说明|
|---|---|---|---|
|\alpha|\alpha|$\alpha$|阿尔法|
|\beta|\beta|$\beta$|贝塔|
|\gamma|\gamma|$\gamma$|伽马|
|\delta|\delta|$\delta$|德尔塔|
|\epsilon|\epsilon|$\epsilon$|伊普西隆|
|\zeta|\zeta|$\zeta$|泽塔|
|\eta|\eta|$\eta$|伊塔|
|\theta|\theta|$\theta$|西塔|
|\iota|\iota|$\iota$|约塔|
|\kappa|\kappa|$\kappa$|卡帕|
|\lambda|\lambda|$\lambda$|兰姆达|
|\mu|\mu|$\mu$|米欧|
|\nu|\nu|$\nu$|纽|
|\xi|\xi|$\xi$|克西|
|\omicron|\omicron|$\omicron$|欧米克隆|
|\pi|\pi|$\pi$|派|
|\rho|\rho|$\rho$|柔|
|\sigma|\sigma|$\sigma$|西格玛|
|\tau|\tau|$\tau$|陶|
|\upsilon|\upsilon|$\upsilon$|玉普西隆|
|\phi|\phi|$\phi$|弗爱|
|\chi|\chi|$\chi$|凯|
|\psi|\psi|$\psi$|普赛|
|\omega|\omega|$\omega$|奥米伽|

## 总结

是不是突然发现 `MD` 还是很强大的，学会了这些，以后写数学方程再也不用去特殊符号里找了，想怎么写就怎么写。好了，如果你喜欢记得点 `在看`。
