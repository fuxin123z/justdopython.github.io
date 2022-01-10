---
layout: post
title: 丢弃Tkinter！几行代码快速生成漂亮GUI！
category: python
tagline: by 闲欢
tags: 
  - python
  - GUI
  - 工具
---


![封面](http://www.justdopython.com/assets/images/2022/01/pysimplegui/0.png)

Python 的 GUI 框架并不少，其中 Tkinter，wxPython，Qt 和 Kivy 是几种比较主流的框架。此外，还有不少在上述框架基础上封装的简化框架，例如 EasyGUI，PyGUI 和 Pyforms 等。

但问题在于，对于初学者而言，即使是最简单的主流框架，他们也无从下手；就算选择封装过的（简化）框架，但仍难以甚至无法创建自定义 GUI 布局。即便学会了某种（简化）框架，也需要编写连篇累牍的代码。

PySimpleGUI 尝试解决上述 GUI 难题，它提供了一种简单明了、易于理解、方便自定义的 GUI 接口。它诞生于2018年，设计宗旨是 “Simplicity is the ultimate sophistication” （简单即美）。

PySimpleGUI 包含了绝大多数原本需要用户界面构建编写的函数，不仅如此，它还具有 Auto-packer 技术，可以自动创建界面，使用者不需要像 tkinter 那样使用布局管理器。

<!--more-->

### 安装

和其他的模块一样，直接使用 pip 安装即可：

> pip install PySimpleGUI


### 使用步骤

一般使用 PySimpleGUI 都有固定套路，只要我们记住这个套路，其实就是使用 PySimpleGUI 的步骤，就能很容易地使用 PySimpleGUI 创建 GUI。

1.import 库
2.创建 layout UI 布局
3.window 窗口显示
4.Event loop 事件循环，用户持续交互
5.close 关闭窗口

下面详细讲解一下这些步骤。

#### import 库

```python
 import PySimpleGUI as sg
```

这个是 PySimpleGUI 官方推荐的写法。

#### 创建 layout 布局

这里的 layout 布局，其实就是画一些小部件，这些小部件就是你最终界面的一些元素组成，例如按钮、复选框、文本框等。

```python
layout = [
    [sg.Text('一句话概括Python')],
    [sg.Input(key='-INPUT-')],
    [sg.Button('确认'), sg.Button('取消')] 
]

```

我们上面代码中就包含标签、文本输入框、确认和取消按钮。

需要注意的是，PySimpleGUI 自动按行布局，所以我们需要把对应行中的所有部件放到一个列表中，如上“确认”与“取消”按钮放在一个列表中，两个文本部件放到一个列表中，最后形成一个嵌套列表layout。

#### window 窗口显示

定义好 layout 之后，我们只需要将其放在 window 窗口中就行了：

```python
window = sg.Window('PySimpleGUI Demo', layout)

```

#### 循环监听事件

我们定义了一个窗体，需要监听用户在我们的窗体界面上的输入操作来给与不同的事件处理。PySimpleGUI 给出的方案是通过构建一个循环来监听用户的输入：

```python
while True:
   event, values = window.read()
   if event in (None, '取消'):
       break

```
这里监听到 None（右上角的关闭）和“取消”按钮事件，就退出循环。


#### 关闭窗口

关闭窗口就一行代码：

```python
window.close()
```

#### 完整代码

```python
import PySimpleGUI as sg

layout = [
    [sg.Text('一句话概括Python')],
    [sg.Input(key='-INPUT-')],
    [sg.Button('确认'), sg.Button('取消')]
]
window = sg.Window('PySimpleGUI Demo', layout)
while True:
    event, values = window.read()
    print(event)
    print(values)
    if event in (None, '取消'):
        break
window.close()

```
这里我将监听到的事件和获取到的值打印到控制台。

运行效果截图：

![](http://www.justdopython.com/assets/images/2022/01/pysimplegui/1.png)

当我输入文本，然后点击“确定”按钮是，控制台会打印如下内容：

```python
确认
{'-INPUT-': '人生苦短，我爱Python'}
```

### 传递值

PySimpleGUI 传递值的方式不同于其他的 GUI，它是通过相同关键词进行绑定的。

```python
import PySimpleGUI as sg

layout = [
    [sg.Text('一句话概括Python')],
    [sg.Input(key='-INPUT111-')],
    [sg.Input(key='-INPUT222-')],
    [sg.Button('确认'), sg.Button('取消')],
    [sg.Text('输出：'), sg.Text(key='-OUTPUT-')]
]
window = sg.Window('PySimpleGUI Demo', layout)
while True:
    event, values = window.read()
    print(event)
    print(values)
    if event in (None, '取消'):
        break
    else:
        window['-OUTPUT-'].update(values['-INPUT222-'])
window.close()

```

我们再扩展一下上面的例子，我界面上有两个输入框，然后底下有一个输出行来显示输入框输入的内容。

运行之后的界面如下：

![](http://www.justdopython.com/assets/images/2022/01/pysimplegui/2.png)

当我在两个输入框分别输入内容时，只有第二个输入框的内容会显示在底下，这是因为我将第二个输入框的 key（'-INPUT222-'） 绑定在了底下的输出行中。

### 切换主题

PySimpleGUI 提供了很多其他主题供我们选择：

![](http://www.justdopython.com/assets/images/2022/01/pysimplegui/3.png)

你可以通过如下代码来查看主题：

```python
sg.preview_all_look_and_feel_themes()
```

切换主题的方式为：

```python
sg.change_look_and_feel("GreenMono")

```


### 总结

本文给大家介绍了一款非常简单实用的 GUI 神器，无需堆积如山的代码就可以打造一款简洁的 GUI，对初学者非常友好，也是快速生成 GUI 界面的不二选择。


> 示例代码：(https://github.com/JustDoPython/python-examples/tree/master/xianhuan/pysimplegui)
> 