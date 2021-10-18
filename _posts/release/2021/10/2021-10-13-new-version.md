---
layout: post
category: python
title: python 3.10 的新特性用不到，你来打我!!!
tagline: by 某某白米饭
tags: 
  - python100
---

python 3.10 已经在 10月 4 号发布了，这次更新了错误语法提示对 python 新手更加友好。好几个新的特性非常的有用，一起来看看吧。

<!--more-->

### 更细致的错误语法提示

在调试代码的时候可以精确定位到错误语法的那行，而不是提示 SyntaxError 的行。

```python
# 1
expected = {9: 1, 18: 2, 19: 2, 27: 3, 
some_other_code = foo()

# 2
foo(x, z for z in range(10), t, w)

# 3 
try:
    build_dyson_sphere()
except NotEnoughScienceError, NotEnoughResourcesError:

# 4
f"Black holes {*all_black_holes} and revelations"

# 5
schwarzschild_black_hole = None
schwarschild_black_hole
```
3.9 提示的是

```python
# 1 
    some_other_code = foo()
                    ^
SyntaxError: invalid syntax

# 2 
    foo(x, z for z in range(10), t, w)
           ^
SyntaxError: Generator expression must be parenthesized

# 3
    except NotEnoughScienceError, NotEnoughResourcesError:
                                ^
SyntaxError: invalid syntax

# 4
    (*all_black_holes)
     ^
SyntaxError: f-string: can't use starred expression here

# 5
    schwarschild_black_hole
NameError: name 'schwarschild_black_hole' is not defined
```

3.10 提示的是

```python
# 1
    expected = {9: 1, 18: 2, 19: 2, 27: 3, 
               ^
SyntaxError: '{' was never closed

# 2
    foo(x, z for z in range(10), t, w)
           ^^^^^^^^^^^^^^^^^^^^
SyntaxError: Generator expression must be parenthesized

# 3
    except NotEnoughScienceError, NotEnoughResourcesError:
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: multiple exception types must be parenthesized

# 4
    (*all_black_holes)
     ^^^^^^^^^^^^^^^^
SyntaxError: f-string: cannot use starred expression here

# 5
    schwarschild_black_hole
NameError: name 'schwarschild_black_hole' is not defined. Did you mean: 'schwarzschild_black_hole'?
```

### 结构化模式匹配：match...case

相当于其他语言的 switch...case

```python
match subject:
    case <pattern_1>:
        <action_1>
    case <pattern_2>:
        <action_2>
    case <pattern_3>:
        <action_3>
    case _:
        <action_wildcard>
```

关键字 match 后跟变量名。 如果匹配，则将执行 case 块内的语句, 没有匹配，则执行 case _ 块内的语句。

```python
# 1
for i in [1,2,3,4,5,6,7]:
    match i:
        case 1:
            print('周一')
        case 2:
            print('周二')
        case 3:
            print('周三')
        case 4:
            print('周四')
        case 5:
            print('周五')
        case _:
            print('放假了')
```

结果：

```python
# 1
周一
周二
周三
周四
周五
放假了
放假了
```

再来一个 tuple 类型的

```python
# 2
point = (1, 2, 3)
match point:
    case (0, 0, _):
        print("原点")
    case (0, y, 0):
        print(f"Y={y}")
    case (x, 0, 0):
        print(f"X={x}")
    case (x, y, z):
        print(f"X={x}, Y={y}, Z={z}")
    case _:
        raise ValueError("Not a point")
```

结果：

```python
# 2
X=1, Y=2, Z=3
```

可以使用 tuple 类型，当然也可以使用 list 类型，类似于：points = [(1, 3),(1, 2)]


### 新型联合运算符

以 X|Y 的形式引入了新的类型联合运算符。

```python
def square(number: int|float): 
    return number ** 2

print(square(4))
print(square(4.4))
```

结果：

```python
16
19.360000000000003
```

也可以用作 isinstance()：一个对象是否是一个已知的类型  和 issubclass()：判断参数 class 是否是类型参数 classinfo 的子类 的第二个参数。

```python
isinstance("5",int|str) 
isinstance("xxxx",int|str) 
```

结果：

```python
True
True
```

### zip 的严格模式

函数 zip() 增加 strict 参数，如果设置 strict = True，而传输的参数的长度不相等将会抛出异常。

```python
x = [1,2,3,4,5]
y = [1,2,3]
z = zip(x,y, strict=True)
print(list(z))
```

结果：

```python
ValueError: zip() argument 2 is shorter than argument 1
```

### 字典增加了 mapping 属性

dict.items()、dict.keys()、dict.values() 分别增加了 mapping 属性

```python
x = {'name': '张三', 'age': 14}
keys = x.keys()
values = x.values()
items = x.items()
print(keys.mapping)
print(values.mapping)
print(items.mapping)
```

### 总结

python 3.10 更新的最有用的就是错误提示了，再也不会看到提示一团迷糊，定位更加的精确，match...case 终于来了。
