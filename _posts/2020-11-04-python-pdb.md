---
layout: post
category: python
title: C有gdb，Python也有pdb
tagline: by 轩辕御龙
tags:
  - python
---



# C有gdb，Python也有pdb

写过C语言的同学们想必都很怀念（读者：¿）gdb调试器，使用gdb可以随意在程序运行过程中暂停流程、查看变量。

很多时候，我们单纯分析代码流程和日志信息无法定位的问题，都得靠调试器来帮忙；可以说有了调试器，程序员才是代码世界完整的上帝。

Python当然也不示弱，同样存在这样的巴别塔可以让人*升天*

<!--more-->

![01](http://www.justdopython.com/assets/images/2020/11/2020-11-04-python-pdb/01.jpg)

——不过阿酱必须承认的是，现代IDE集成的图形化调试功能已经很好使了，一般情况下使用命令行工具的场景并不多。

但是也确实存在无法使用图形化IDE的情况，因此对pdb工具略作了解还是很有必要的。毕竟谁也不知道可能被扔给一个什么样的环境啊哈哈

## pdb的使用

作为解释型语言，Python调试工具的使用跟gdb毕竟还是有区别的。

比如Python的调试就不需要什么符号表之类的东西，说到底，最终Python虚拟机执行的逻辑也是自带符号的。

也正是由于Python的这种特殊性，所有pdb其实有两种不太一样的使用方式，即侵入式和非侵入式。

其实按字面意思就很容易理解在两种方式的使用。类比一下脑机接口，也分为侵入式和非侵入式。侵入式就表示要将电极、芯片植入大脑皮层，“侵入”人体；而非侵入式则是在头骨外收集脑电波进行分析。

同样地，侵入式pdb调用就是将调用pdb的代码直接写入Python脚本当中；而非侵入式则是从命令行调用pdb，执行相应被调试脚本。

1. **侵入式pdb**

   使用方式如下代码所示，在代码中途插入一行调用：

   ```python
   import pdb; # pdb.set_trace()
   
   
   a = "just"
   b = "do"
   
   pdb.set_trace()
   
   c = ['p', 'y', 't', 'h', 'o', 'n']
   print(a)
   ```

   运行脚本，会进入这样一个交互式界面：

   ```shell
   D:\000-GitHub\python-examples\xuanyuanyulong\2020-11-04-python-pdb>python test_pdb_intrusive.py
   > d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py(21)<module>()
   -> c = ['p', 'y', 't', 'h', 'o', 'n']
   (Pdb)
   ```

   到这里已经启动了pdb，并且打印内容中`-> c = ['p', 'y', 't', 'h', 'o', 'n']`行首的箭头，表示当前程序执行流到了这一行代码，如果继续执行，将首先执行该行。

2. **非侵入式pdb**

   非侵入式要xue微简单一些，最大的好处是不需要改动代码。

   我们在控制台执行以下命令：

   ```shell
   D:\000-GitHub\python-examples\xuanyuanyulong\2020-11-04-python-pdb>python -m pdb test_pdb_intrusive.py
   > d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py(1)<module>()
   -> import pdb; # pdb.set_trace()
   (Pdb)
   ```

   可以看到，通过这种方式进入调试，程序执行流停在了程序开头。

   通过分析进入调试时代码执行流的位置，我们可以发现，实际上侵入式的插入`pdb.set_trace()`调用，等价于我们从命令行启动pdb，然后在这个调用的下一行打了一个断点，然后直接运行程序。

## 简单命令

gdb中有一些常用的简单命令，本节阿酱带大家熟悉一下，后续会做更深入的讨论。

1. **h(elp)**

   在pdb界面下输入`h`或`help`命令，即可列出pdb中支持的各种命令：

   ```shell
   (Pdb) h
   
   Documented commands (type help <topic>):
   ========================================
   EOF    c          d        h         list      q        rv       undisplay
   a      cl         debug    help      ll        quit     s        unt
   alias  clear      disable  ignore    longlist  r        source   until
   args   commands   display  interact  n         restart  step     up
   b      condition  down     j         next      return   tbreak   w
   break  cont       enable   jump      p         retval   u        whatis
   bt     continue   exit     l         pp        run      unalias  where
   
   Miscellaneous help topics:
   ==========================
   exec  pdb
   ```

   在pdb后带一个命令作为参数，还可进一步看到相应的使用说明：

   ```shell
   (Pdb) h h
   h(elp)
           Without argument, print the list of available commands.
           With a command name as argument, print help about that command.
           "help pdb" shows the full pdb documentation.
           "help exec" gives help on the ! command.
   ```

   相信我，`help`其实才是pdb里面最重要的命令。别的什么都可以记不住，但是`help`一定要记住。在以结果为导向的职场生活中也是一样，遇到问题要及时求助哟~

2. **l(ist)**

   打印当前文件的源代码。不带参数的话，默认打印当前行前后共计11行代码。继续执行该命令的话，则会继续往后打印最多11行代码，直到遇上文件结束符EOF。

   用`.`作为参数则限定要强一点，只会打印当前行前后11行代码。

   ```shell
   (Pdb) l
     1  -> import pdb; # pdb.set_trace()
     2
     3
     4     def addStr(a, b):
     5         return a + b
     6
     8         return ''.join(l)
     9
    10     def getSlogan(a, b, c):
    11         result = addStr(a, b) + mergeChar(c)
   ```

   当指定两个参数时，则打印这个区间内的代码：

   ```shell
   (Pdb) l 3, 7
     3
     4     def addStr(a, b):
     5         return a + b
     6
     7  -> def mergeChar(l: list):
   ```

   而当第二个参数b比第一个参数a小的时候，则表示“从第a行开始，*继续*往后打印b行”，也就是总共打印(1+b)行：

   ```shell
   (Pdb) l 7, 3
     7  -> def mergeChar(l: list):
     8         return ''.join(l)
     9
    10     def getSlogan(a, b, c):
   ```

3. **p/pp**

   打印某个对象的值。区别在于`pp`调用的是`pprint`函数，打印更加美观。

   ```shell
   (Pdb) p a
   'just'
   (Pdb) p addStr
   <function addStr at 0x000002087B0F9C80>
   ```

4. **!**

   使用`!`可以在pdb环境下，执行一般的Python语句。通常我们可以用来改变变量的值——要不怎么说调试器可以让你成为上帝呢？还有比这更为所欲为的吗？

   一般的话这个`!`其实可以省略，但是当要执行语句开头的单词与pdb的已有命令冲突，就得不到预期结果了，所以建议还是加上。

   > 这个用`!`领起命令的做法跟vim编辑器的逻辑很像，可以类比记忆。不熟悉的读者可以忽略。

   ```shell
   (Pdb) !a = "python"
   (Pdb) p a
   'python'
   ```

5. **r(eturn)**

   pdb中，`r`和`return`表示同一个意思，即“运行当前函数直到返回”。

   > 这一点上，`r`在pdb和gdb中的含义是不同的。读者不必在意

6. **run/restart**

   表示重新运行当前被调试程序。使用这个命令，可以为需要传入参数的脚本传入所需参数。

   格式与命令行执行该脚本一样，只是把相应的python命令和脚本路径替换为了`run`或`restart`。

   ```shell
   (Pdb) run a b c d kkk
   Restarting test_pdb_intrusive.py with arguments:
           test_pdb_intrusive.py
   > d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py(1)<module>()
   -> import pdb; # pdb.set_trace()
   (Pdb) !import sys
   (Pdb) p sys.argv
   ['test_pdb_intrusive.py', 'a', 'b', 'c', 'd', 'kkk']
   ```

7. **b(reak)**

   查看/添加断点。

   不带任何参数时，即列出当前已有断点。

   ```shell
   (Pdb) b 21
   Breakpoint 1 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   (Pdb) b 17
   Breakpoint 2 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   (Pdb) b
   Num Type         Disp Enb   Where
   1   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   2   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   ```

   同时，通过`run`和`restart`重新运行被调试程序，不会清除已有断点：

   ```shell
   (Pdb) run
   Restarting test_pdb_intrusive.py with arguments:
           test_pdb_intrusive.py
   > d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py(1)<module>()
   -> import pdb; # pdb.set_trace()
   (Pdb) b
   Num Type         Disp Enb   Where
   1   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   2   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   ```

8. **cl(ear)**

   有三种使用方式：1）类似设置断点时，清除特定文件特定行的断点；2）将要清除的断点号列出来，以空格分隔；3）不带参数，清除所有断点。

   下面一一演示：

   1）类似设置断点时，清除特定文件特定行的断点

   ```shell
   (Pdb) b
   Num Type         Disp Enb   Where
   1   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   2   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   (Pdb) clear test_pdb_intrusive.py:21
   (Pdb) b
   Num Type         Disp Enb   Where
   2   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   ```

   2）将要清除的断点号列出来，以空格分隔

   ```shell
   (Pdb) b 21
   Breakpoint 3 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   (Pdb) b 15
   Breakpoint 4 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) b
   Num Type         Disp Enb   Where
   2   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   3   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   4   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) clear 2 4
   Deleted breakpoint 2 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   Deleted breakpoint 4 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) b
   Num Type         Disp Enb   Where
   3   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   ```

   3）不带参数，清除所有断点

   ```shell
   (Pdb) b 17
   Breakpoint 5 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   (Pdb) b 15
   Breakpoint 6 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) b
   Num Type         Disp Enb   Where
   3   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   5   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   6   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) b
   Num Type         Disp Enb   Where
   3   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   5   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   6   breakpoint   keep yes   at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) clear
   Clear all breaks? yes
   Deleted breakpoint 3 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:21
   Deleted breakpoint 5 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:17
   Deleted breakpoint 6 at d:\000-github\python-examples\xuanyuanyulong\2020-11-04-python-pdb\test_pdb_intrusive.py:15
   (Pdb) b
   ```

好了打住打住，写之前感觉pdb没多少东西，没想到写起来才发现，这么一点内容就已经这么多了，今天又熬夜了……

![02](http://www.justdopython.com/assets/images/2020/11/2020-11-04-python-pdb/02.jpg)

~~狗命要紧~~各位读者老爷后会有期、后会有期

## 总结

pdb的内容出乎意料地丰富，还有很多内容在这篇文章中都没能涉及。之后会再写一篇以作补充。

软件调试其实也是一门很有趣的学问，当然，也是一门很有用的学问。

> 示例代码：<https://github.com/JustDoPython/python-examples/tree/master/xuanyuanyulong/2020-11-04-python-pdb