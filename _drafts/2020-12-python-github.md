---
layout: post     
title:  github高级搜索技巧
category: github高级搜索技巧
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

在程序员眼中全球最大同性交友网站 github 上的优秀开源框架和教程数量是世上当之无愧的第一，如何高效的在 github 上搜索就成为了每一位程序员必会的技能之一
<!--more-->
### 搜索资源

#### 通过 in 关键字搜索

关键字 in 可以搜索出 github 上的资源名称 name、说明 description 和 readme 文件中的内容

```python
# 语法

关键字 in:

# 示例
python in:name,description,readme # 逗号分割表示或的意思
```

![](http://www.justdopython.com/assets/images/2020/12/github/1.png)

#### 通过 stars、fork 数量搜索

搜索 github 时用 star 数量和 fork 数量判断这个项目是否优秀的标准之一

##### 按照大于小于查询

```python
# 语法

关键字 stars:>=数量 forks:>=数量

#示例
python in:name stars:>94000 forks:>2400
```

![](http://www.justdopython.com/assets/images/2020/12/github/2.png)

##### 按照范围查询

star 数量和 fork 数量也可以按照一个范围取值搜索

```python
#语法

关键字 stars:范围1..范围2

# 示例
python in:name stars:90000..95000
```

![](http://www.justdopython.com/assets/images/2020/12/github/3.png)

#### 按创建、更新时间搜索

按创建、更新时间搜索可以把版本老旧的资源筛选出去

```python
# 语法

# 创建时间
关键字 created:>=YYYY-MM-DD

# 更新时间
关键字 pushed:>=YYYY-MM-DD

# 示例
python in:name created:>=2020-01-01 pushed:>=2020-01-01

```

![](http://www.justdopython.com/assets/images/2020/12/github/4.png)

### 搜索代码

在 github上搜索文件中的代码有一些限制

1. 在需要搜索 fork 资源 时，只能搜索到 star 数量比父级资源多的 fork 资源，并需要加上 fork:true 查询
2. 只有小于 384 KB 的文件可搜索
3. 只有少于 500,000 个文件的仓库可搜索
4. 除了 filename 搜索以外，搜索源代码时必须始终包括至少一个关键字
5. 搜索结果最多可显示同一文件的两个分段，但文件内可能有更多结果
6. 不能使用通配符

#### 按文件内容、路径搜索

```python
# 语法

# 文件内容
关键字 in:file

# 文件路径
关键字 in:path

# 示例
python in:file,path
```

![](http://www.justdopython.com/assets/images/2020/12/github/5.png)

#### 在某个资源下搜索

```python
# 语法

关键字 repo:资源

# 示例
python repo:JustDoPython/python-100-day
```

![](http://www.justdopython.com/assets/images/2020/12/github/6.png)

#### 按语言搜索

```python
# 语法

关键字 language:LANGUAGE

# 示例

python language:javascript # 搜索 javascript 中的 python
```

![](http://www.justdopython.com/assets/images/2020/12/github/7.png)

#### 按文件名、大小、扩展名搜索

```python
# 语法

# 文件名
关键字 filename:FILENAME

# 文件大小
关键字 size:>=大小

# 扩展名
关键字 extension:EXTENSION

# 示例
python filename:aaa size:>10 extension:py  

```

![](http://www.justdopython.com/assets/images/2020/12/github/8.png)

### 总结

在 github 上高效搜索资源，您学废了吗？JustDoPython 项目也是一个优秀的开源代码，希望大家多多 star

### 参考

- <https://docs.github.com/cn/free-pro-team@latest/github>
