# Python 之装饰器

## 1. 概念介绍

**装饰器**（decorator），又称“装饰函数”，即一种返回值也是函数的函数，可以称之为“函数的函数”。其目的是在不对现有函数进行修改的情况下，实现额外的功能。

在 Python 中，装饰器属于纯粹的“语法糖”，不使用也没关系，但是使用的话能够大大简化代码，使代码更加易读——当然，是对知道这是怎么回事儿的人而言。

想必经过一段时间的学习，大概率已经在 Python 代码中见过`@`这个符号。没错，这个符号正是使用装饰器的标识，也是正经的 Python 语法。

> [语法糖]([https://baike.baidu.com/item/%E8%AF%AD%E6%B3%95%E7%B3%96/5247005?fr=aladdin](https://baike.baidu.com/item/语法糖/5247005?fr=aladdin))：指计算机语言中添加的某种语法，这种语法对语言的功能并没有影响，但是更方便程序员使用。通常来说使用语法糖能够增加程序的可读性，从而减少程序代码出错的机会。

## 2. 运行机制

简单来说，下面两段代码在语义上是可以划等号的（当然具体过程还是有一点微小区别的）：

```python
def IAmDecorator(foo):
    '''我是一个装饰函数'''
    pass

@IAmDecorator
def tobeDecorated(...):
    '''我是被装饰函数'''
    pass
```

与：

```python
def IAmDecorator(foo):
    '''我是一个装饰函数'''
    pass

def tobeDecorated(...):
    '''我是被装饰函数'''
    pass
tobeDecorated = IAmDecorator(tobeDecorated)
```

可以看到，使用装饰器的`@`语法，就相当于是将具体定义的函数作为参数传入装饰器函数，而装饰器函数则经过一系列操作，返回一个新的函数，然后再将这个新的函数赋值给原先的函数名。

最终得到的是一个与我们在代码中显式定义的函数**同名**而**异质**的新函数。

而装饰函数就好像为原来的函数套了一层壳。如图所示，最后得到的组合函数即为应用装饰器产生的新函数：

![2019-09-23-装饰器_03.gif](https://ws1.sinaimg.cn/large/006cMbyIly1g79vi4kevog30ui0ltadr.gif)

这里要注意一点，上述两段代码在具体执行上还是存在些微的差异。在第二段代码中，函数名`tobeDecorated`实际上是先指向了原函数，在经过装饰器修饰之后，才指向了新的函数；但第一段代码的执行就没有这个中间过程，直接得到的就是名为`tobeDecorated`的新函数。

此外，装饰函数**有且只能有**一个参数，即要被修饰的原函数。

## 3. 用法

Python 中，装饰器分为两种，分别是“函数装饰器”和“类装饰器”，其中又以“函数装饰器”最为常见，“类装饰器”则用得很少。

### 3.1 函数装饰器

对装饰函数的定义大致可以总结为如图所示的模板，即：

![装饰函数模板示意图.png](https://ws1.sinaimg.cn/large/006cMbyIly1g79wrt6bv4j30cf09pq2z.jpg)

由于要求装饰函数返回一个函数的缘故，为了在原函数的基础上对功能进行扩充，并且使得扩充的功能能够以函数的形式返回，因此需要在装饰函数的定义内部再定义一个内部函数，在这个内部函数中进一步操作。最后`return`的对象就应该是这个内部函数对象，也只有这样才能够正确地返回一个附加了新功能的函数。

如图一的动图所示，装饰函数就像一个“包装”，将原函数装在了装饰函数的内部，从而通过在原函数的基础上附加功能实现了扩展。装饰函数再将这个新的整体返回。

### 3.2 类装饰器



### 多个装饰器的情况

多个装饰器可以嵌套，具体的情况有两种理解：一种是理解为从下往上结合的复合函数；一种可以理解为下一个装饰器的值是前一行装饰器的参数。

## 参考资料

[1] [Python3 术语表-装饰器](https://docs.python.org/3/glossary.html#term-decorator)

[2] [Python3 文档-复合语句-函数定义](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

[3] [Python3 文档-复合语句-类定义](https://docs.python.org/3/reference/compound_stmts.html#class-definitions)

[4] [语法糖]([https://baike.baidu.com/item/%E8%AF%AD%E6%B3%95%E7%B3%96/5247005?fr=aladdin](https://baike.baidu.com/item/语法糖/5247005?fr=aladdin))