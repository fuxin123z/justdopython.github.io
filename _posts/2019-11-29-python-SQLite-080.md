---
layout: post
category: python
title: 第80天：Python 操作 SQLite
tagline: by 程序员野客
tags: 
  - python100
---

## 1 简介

SQLite 是一种轻型嵌入式关系型数据库，它包含在一个相对小的 C 库中。SQLite 占用资源低，处理速度快，它支持 Windows、Linux、Unix 等多种主流操作系统，支持 Python、Java、C# 等多种语言，目前的版本已经发展到了 SQLite3。

<!--more-->

SQLite 是一个进程内的库，它实现了自给自足、无服务器、无需配置、支持事务。Python 可以通过 sqlite3 模块与 SQLite3 集成，Python 2.5.x 以上版本内置了 sqlite3 模块，因此，我们在 Python 中可以直接使用 SQLite。 

## 2 基本使用

### 2.1 连接数据库

```
# 导入模块
import sqlite3
# 连接数据库
conn = sqlite3.connect('test.db')
```

如果数据库不存在，则会自动被创建。

### 2.2 游标

连接数据库后，我们需要使用游标进行相应 SQL 操作，游标创建如下所示：

```
# 创建游标
cs = conn.cursor()
```

### 2.3 创建表

我们在 test.db 库中新建一张表 student，如下所示：

```
# 创建表
cs.execute('''CREATE TABLE student
       (id varchar(20) PRIMARY KEY,
        name varchar(20));''')
# 关闭 Cursor
cs.close()
# 提交
conn.commit()
# 关闭连接
conn.close()
```

表创建好后，我们可以使用图形化工具 SQLiteStudio 直观的查看一下，官方下载地址： [https://sqlitestudio.pl/index.rvt?act=download]( https://sqlitestudio.pl/index.rvt?act=download )，打开如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio1.PNG)

以 Windows 系统为例，选择免安装版 portable 进行下载，下载好后解压文件，直接运行文件夹中的 SQLiteStudio.exe 即可，打开后如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio2.PNG) 

我们先点击上方工具栏上的 Database 按钮，然后选 Add a database，如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio3.PNG) 

接着点击文件下方右侧的绿色加号按钮或文件夹按钮，选择数据库文件，比如我们选择 test.db 文件，选好了后点击测试连接，如果能够正常连接，我们就点击 OK 按钮添加数据库。

添加完数据库后，再点击 SQLiteStudio 主界面上方工具栏中 View 按钮，接着选数据库，结果如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio4.PNG) 

接着双击 test 库，结果如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio5.PNG) 

此时已经看到 student 表了，双击 student 表，我们还可以查看表的更多信息，如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio6.PNG) 

### 2.4 新增

我们向 student 表中插入两条数据，如下所示：

```
cs.execute("INSERT INTO student (id, name) VALUES ('1', 'Jhon')")
cs.execute("INSERT INTO student (id, name) VALUES ('2', 'Alan')")
cs.close()
conn.commit()
conn.close()
```

执行完后，到 SQLiteStudio 中看一下，如图所示：

![](http://www.justdopython.com/assets/images/2019/sqlite/sqlitestudio7.PNG) 

我们看到数据已经进来了。

### 2.5 查询

前面我们是通过 SQLiteStudio 查看数据的，现在我们通过 SQL 查看一下，如下所示：

```
# 导入模块
import sqlite3
# 连接数据库
conn = sqlite3.connect('test.db')
# 创建游标
cs = conn.cursor()
# 查询数据
cs.execute("SELECT id, name FROM student")
data = cs.fetchall()
print(data)
cs.close()
conn.close()
```

输出结果：

```
[('1', 'Jhon'), ('2', 'Alan')]
```

### 2.6 更新

我们修改 id 为 1 这条数据的 name 值，如下所示：

```
# 导入模块
import sqlite3
# 连接数据库
conn = sqlite3.connect('test.db')
# 创建游标
cs = conn.cursor()
# 修改数据
cs.execute("SELECT id, name FROM student WHERE id = '1'")
print('修改前-->', cs.fetchall())
cs.execute("UPDATE student set name = 'Nicolas' WHERE id = '1'")
cs.execute("SELECT id, name FROM student WHERE id = '1'")
print('修改后-->', cs.fetchall())
conn.commit()
cs.close()
conn.close()
```

输出结果：

```
修改前--> [('1', 'Jhon')]
修改后--> [('1', 'Nicolas')]
```

### 2.7 删除

我们删除 id 为 1 这条数据，如下所示：

```
# 导入模块
import sqlite3
# 连接数据库
conn = sqlite3.connect('test.db')
# 创建游标
cs = conn.cursor()
# 删除
cs.execute("SELECT id, name FROM student")
print('删除前-->', cs.fetchall())
cs.execute("DELETE FROM student WHERE id = '1'")
cs.execute("SELECT id, name FROM student")
print('删除后-->', cs.fetchall())
conn.commit()
cs.close()
conn.close()
```

输出结果：

```
删除前--> [('2', 'Alan'), ('1', 'Jhon')]
删除后--> [('2', 'Alan')]
```

## 总结

本文为大家介绍了 SQLite 以及使用 Python 操作 SQLite，对 Python 工程师使用 SQLite 提供了支撑。

> 示例代码：[Python-100-days-day080](https://github.com/JustDoPython/python-100-day/tree/master/day-080)

参考：

[https://baike.baidu.com/item/SQLite/375020?fr=aladdin]( https://baike.baidu.com/item/SQLite/375020?fr=aladdin )

[https://www.liaoxuefeng.com/wiki/1016959663602400/1017801751919456](https://www.liaoxuefeng.com/wiki/1016959663602400/1017801751919456)

