---
layout: post     
title:  Python 小技之 Office 文件转 PDF
category: Python 小技之 Office 文件转 PDF
copyright: python                           
tagline: by 潮汐       
tags: 
  - 
---
  在平时的工作中，难免需要一些 小Tip 来解决工作中遇到的问题，今天的文章给大家安利一个方便快捷的小技巧，将 Office（doc/docx/ppt/pptx/xls/xlsx）文件批量或者单一文件转换为 PDF 文件。
不过在做具体操作之前需要在 PC 安装好 Office，再利用 Python 的 win32com 包来实现 Office 文件的转换操作。
### 安装 win32com
在实战之前，需要安装 Python 的 win32com,详细安装步骤如下：

#### 使用 pip 命令安装  
```python

pip install pywin32

```

如果我们遇到安装错误，可以通过python -m pip install --upgrade pip更新云端的方式再进行安装即可：

```python

python -m pip install --upgrade pip	

```

#### 下载离线安装包安装

如果 pip 命令未安装成功的话还可以下载离线包安装，方法步骤如下：
首先在官网选择对应的 Python 版本下载离线包：https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/
下载好后傻瓜式安装好即可。

### 文件转换逻辑

详细代码如下：

```python
class PDFConverter:
    def __init__(self, pathname, export='.'):
        self._handle_postfix = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'] # 支持转换的文件类型
        self._filename_list = list()  #列出文件
        self._export_folder = os.path.join(os.path.abspath('.'), 'file_server/pdfconver')
        if not os.path.exists(self._export_folder):
            os.mkdir(self._export_folder)
        self._enumerate_filename(pathname)

    def _enumerate_filename(self, pathname):
        '''
        读取所有文件名
        '''
        full_pathname = os.path.abspath(pathname)
        if os.path.isfile(full_pathname):
            if self._is_legal_postfix(full_pathname):
                self._filename_list.append(full_pathname)
            else:
                raise TypeError('文件 {} 后缀名不合法！仅支持如下文件类型：{}。'.format(pathname, '、'.join(self._handle_postfix)))
        elif os.path.isdir(full_pathname):
            for relpath, _, files in os.walk(full_pathname):
                for name in files:
                    filename = os.path.join(full_pathname, relpath, name)
                    if self._is_legal_postfix(filename):
                        self._filename_list.append(os.path.join(filename))
        else:
            raise TypeError('文件/文件夹 {} 不存在或不合法！'.format(pathname))

    def _is_legal_postfix(self, filename):
        return filename.split('.')[-1].lower() in self._handle_postfix and not os.path.basename(filename).startswith(
            '~')

    def run_conver(self):
        print('需要转换的文件数是：', len(self._filename_list))
        for filename in self._filename_list:
            postfix = filename.split('.')[-1].lower()
            funcCall = getattr(self, postfix)
            print('原文件：', filename)
            funcCall(filename)
        print('转换完成！')
```
	
### doc/docx 转换为 PDF

doc/docx 转换为 PDF 部分代码如下所示：
```python

    def doc(self, filename):
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        print('保存 PDF 文件：', exportfile)
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
        pythoncom.CoInitialize()
        w = Dispatch("Word.Application")
        pythoncom.CoInitialize()  # 加上防止 CoInitialize 未加载
        doc = w.Documents.Open(filename)
        doc.ExportAsFixedFormat(exportfile, constants.wdExportFormatPDF,
                                Item=constants.wdExportDocumentWithMarkup,
                                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        w.Quit(constants.wdDoNotSaveChanges)
	def docx(self, filename):
        self.doc(filename)

```

### ppt/pptx 转换为 PDF

ppt/pptx 转换为 PDF 部分代码如下：

```python

	def ppt(self, filename):
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
        pythoncom.CoInitialize()
        p = Dispatch("PowerPoint.Application")
        pythoncom.CoInitialize()
        ppt = p.Presentations.Open(filename, False, False, False)
        ppt.ExportAsFixedFormat(exportfile, 2, PrintRange=None)
        print('保存 PDF 文件：', exportfile)
        p.Quit()

    def pptx(self, filename):
        self.ppt(filename)

```

### xls/xlsx 转换为 PDF

```python
    def xls(self, filename):
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        pythoncom.CoInitialize()
        xlApp = DispatchEx("Excel.Application")
        pythoncom.CoInitialize()
        xlApp.Visible = False
        xlApp.DisplayAlerts = 0
        books = xlApp.Workbooks.Open(filename, False)
        books.ExportAsFixedFormat(0, exportfile)
        books.Close(False)
        print('保存 PDF 文件：', exportfile)
        xlApp.Quit()

    def xlsx(self, filename):
        self.xls(filename)	

```

### 执行逻辑转换

```python
if __name__ == "__main__":
    # 支持文件夹批量导入
    #folder = 'tmp'
    #pathname = os.path.join(os.path.abspath('.'), folder)
    # 也支持单个文件的转换
    pathname = "G:/python_study/test.doc"
    pdfConverter = PDFConverter(pathname)
    pdfConverter.run_conver()
```

### 总结

今天的文章主要是 Python 实战之小工具的运用，希望对大家有所帮助，下一期将讲解如何通过接口的方式通过文件服务器来下载文件并转换，敬请期待。。。
So 今天的小 Tip 你安利到了吗？

> 示例代码 [Python 小技之 Office 文件转 PDF](https://github.com/JustDoPython/python-examples/tree/master/chaoxi/FilesToPDF)