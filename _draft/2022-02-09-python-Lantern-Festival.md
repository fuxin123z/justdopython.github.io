---
layout: post
category: python
title: 网友：强烈要求实现一户一墩！安排！
tagline: by 豆豆
tags: 
  - python100
---

![封面](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/logo.png)

随着冬奥会的开幕，冬奥吉祥物冰墩墩着实火了一把，无论是线上还是线下，都「一墩难求」。

作为一名派森工程师，虽然实体冰墩墩咱买不到，但用派森画一个冰墩墩过把瘾这不过分吧，也算是为国家的冬奥事业贡献了自己的力量。

先来看下成果图。

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/001.mp4)

下面再来看下分解动作。

### 画轮廓

```python
def draw_body():
    # 头
    turtle.penup()
    turtle.goto(-73, 230)
    turtle.pencolor("lightgray")
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/002.png)

### 画左手

```python
def draw_left_hand():
    turtle.penup()
    turtle.goto(177, 112)
    turtle.pencolor("lightgray")
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/003.png)

### 画双腿

```python
def draw_legs():
    turtle.pencolor("black")
    turtle.fillcolor("black")
    turtle.penup()
    turtle.goto(108, -168)
    turtle.begin_fill()
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/004.png)

### 画耳朵

```python
def draw_ears():
    turtle.pencolor("black")
    turtle.fillcolor("black")
    turtle.penup()
    turtle.goto(90, 230)
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/005.png)

### 画面部

```python
def draw_eyes():
    turtle.penup()
    turtle.goto(-64, 120)
    ...

def draw_nose():
    turtle.penup()
    turtle.goto(37, 80)
    turtle.fillcolor("black")
    ...

def draw_mouth():
    turtle.fillcolor("black")
    turtle.penup()
    turtle.goto(-15, 48)
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/006.png)

### 画五环

```python
def draw_rings():
    turtle.penup()
    turtle.goto(-135, 120)
    turtle.pensize(5)
    turtle.pencolor("cyan")
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/007.png)

### 画标语

```python
def draw_text():
    turtle.pensize(1)
    turtle.penup()
    turtle.goto(-5, -170)
    ...
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/008.png)

### 大功告成

最后把上面的分解动作合到一个入口函数中，就大功告成啦。

```python
if __name__ == '__main__':
    draw_body()
    draw_left_hand()
    draw_legs()
    draw_ears()

    draw_eyes()
    draw_nose()
    draw_mouth()

    draw_rings()
    draw_text()
    turtle.done()
```

![](https://raw.githubusercontent.com/JustDoPython/justdopython.github.io/master/assets/images/2022/02/BingDwenDwen/001.mp4)

### 总结

其实用到的技术不难，就是 `turtle` 库，比较抠细节，要仔细调整画笔的位置和颜色。

参看资料：https://mp.weixin.qq.com/s/jZfrS-js1f2yAa-KXDSuLw