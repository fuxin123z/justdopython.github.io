---
layout: post     
title:  Psutil + Flask + Pyecharts + Bootstrap 开发动态可视化系统监控                        
category: Psutil + Flask + Pyecharts + Bootstrap 开发动态可视化系统监控       
copyright: python                           
tagline: by 某某白米饭           
tags: 
  - 
---

## psutil + Flask + pyecharts + Bootstrap 开发动态可视化系统监控

### psutil 是什么

psutil 是一个跨平台库（http://pythonhosted.org/psutil）能够获取到系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。主要用来做系统监控，性能分析，进程管理。支持 Linux、Mac OS、Windows 系统。

本文以 psutil 模块获取系统信息开发一个监控 Mac OS 系统的平台。
<!--more-->
![](http://www.justdopython.com/assets/images/2020/psutil-flask/total.gif)

### 准备工作

#### 技术选择

* 监控的系统是 Mac OS 系统
* 监控系统模块选择 psutil 模块
* Web 框架选择的是 Flask 框架
* 前端 UI 选择的是 Bootstrap UI
* 动态可视化图表选择 Pyecharts 模块

#### 安装 psutil

```
pip3 install psutil
```

#### 安装 Flask、pyecharts、Bootstrap 

* Flask 的教程是在公众号文章：Web 开发 Flask 介绍
* Pyecharts 的教程在公众号文章：Python 图表利器 pyecharts，按照官网 (http://pyecharts.org/#/zh-cn/web_flask) 文档整合 Flask 框架，并使用定时全量更新图表。
* Bootstrap 是一个 前端的 Web UI，官网地址是 (https://v4.bootcss.com)

![](http://www.justdopython.com/assets/images/2020/psutil-flask/flask.png)

### 获取系统信息

#### CPU信息

通过 psutil 获取 CPU 信息

```python
>>> import psutil

# 获取当前 CPU 的利用率
>>> psutil.cpu_percent()
53.8

# 获取当前 CPU 的用户/系统/空闲时间
>>> psutil.cpu_times()
scputimes(user=197483.49, nice=0.0, system=114213.01, idle=1942295.68)

# 1/5/15 分钟之内的 CPU 负载
>>> psutil.getloadavg()
(7.865234375, 5.1826171875, 4.37353515625)

# CPU 逻辑个数
>>> psutil.cpu_count()
4

# CPU 物理个数
>>> psutil.cpu_count(logical=False)
2
```

在监控平台上每 2 秒请求 url 获取 CPU 负载，并动态显示图表

```python
cpu_percent_dict = {}
def cpu():
    # 当前时间
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    #  CPU 负载
    cpu_percent = psutil.cpu_percent()
    cpu_percent_dict[now] = cpu_percent

    # 保持在图表中 10 个数据
    if len(cpu_percent_dict.keys()) == 11:
        cpu_percent_dict.pop(list(cpu_percent_dict.keys())[0])

def cpu_line() -> Line:
    cpu()
    # 全量更新 pyecharts 图表
    c = (
        Line()
            .add_xaxis(list(cpu_percent_dict.keys()))
            .add_yaxis('', list(cpu_percent_dict.values()), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
            .set_global_opts(title_opts=opts.TitleOpts(title = now + "CPU负载",pos_left = "center"),
                             yaxis_opts=opts.AxisOpts(min_=0,max_=100,split_number=10,type_="value", name='%'))
    )
    return c

@app.route("/cpu")
def get_cpu_chart():
    c = cpu_line()
    return c.dump_options_with_quotes()
```

示例结果

![](http://www.justdopython.com/assets/images/2020/psutil-flask/cpu.gif)

#### 内存

通过 psutil 获取内存和交换区信息

```python
# 系统内存信息 总内存/立刻可用给进程使用的内存/内存负载/已使用内存/空闲内存/当前正在使用或者最近使用的内存/未使用的内存/永久在内存
>>> psutil.virtual_memory()
svmem(total=8589934592, available=2610610176, percent=69.6, used=4251074560, free=387874816, active=2219110400, inactive=2069094400, wired=2031964160)

# 交换区内存 总内存/使用的内存/空闲的内存/负载/系统从磁盘交换进来的字节数(累计)/系统从磁盘中交换的字节数（累积）
>>> psutil.swap_memory()
sswap(total=2147483648, used=834404352, free=1313079296, percent=38.9, sin=328911147008, sout=3249750016)

```

在监控平台上每 2 秒请求 url 获取内存负载，并动态显示图表

```python
def memory():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    # 在 Mac OS 上 未使用内存 = 总内存 - (空闲内存 + 未使用内存)
    return memory.total, memory.total - (memory.free + memory.inactive), memory.free + memory.inactive, swap.total, swap.used, swap.free, memory.percent


def memory_liquid() -> Gauge:
    mtotal, mused, mfree, stotal, sused, sfree, mpercent = memory()
    c = (
        Gauge()
            .add("", [("", mpercent)])
            .set_global_opts(title_opts=opts.TitleOpts(title="内存负载", pos_left = "center"))
    )
    return mtotal, mused, mfree, stotal, sused, sfree, c

@app.route("/memory")
def get_memory_chart():
    mtotal, mused, mfree, stotal, sused, sfree, c = memory_liquid()
    return jsonify({'mtotal': mtotal, 'mused': mused, 'mfree': mfree, 'stotal': stotal, 'sused': sused, 'sfree': sfree, 'liquid': c.dump_options_with_quotes()})
```

示例结果

![](http://www.justdopython.com/assets/images/2020/psutil-flask/mem.gif)

#### 磁盘

通过 psutil 获取磁盘大小、分区、使用率和磁盘IO

```python
# 磁盘分区情况
>>> psutil.disk_partitions()
[sdiskpart(device='/dev/disk1s5', mountpoint='/', fstype='apfs', opts='ro,local,rootfs,dovolfs,journaled,multilabel'), sdiskpart(device='/dev/disk1s1', mountpoint='/System/Volumes/Data', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel'), sdiskpart(device='/dev/disk1s4', mountpoint='/private/var/vm', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel'), sdiskpart(device='/dev/disk1s3', mountpoint='/Volumes/Recovery', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel')]

# 磁盘的使用情况 磁盘总大小/已使用大小/空闲大小/负载
>>> psutil.disk_usage('/')
sdiskusage(total=250790436864, used=10872418304, free=39636717568, percent=21.5)

# 磁盘IO 读取次数/写入次数/读取数据/写入数据/磁盘读取所花费的时间/写入磁盘所花费的时间
>>> psutil.disk_io_counters()
sdiskio(read_count=26404943, write_count=11097500, read_bytes=609467826688, write_bytes=464322912256, read_time=7030486, write_time=2681553)
```

在监控平台上每 2 秒请求 url 获取磁盘信息，并动态显示图表

```python
disk_dict = {'disk_time':[], 'write_bytes': [], 'read_bytes': [], 'pre_write_bytes': 0, 'pre_read_bytes': 0, 'len': -1}
def disk():
    disk_usage = psutil.disk_usage('/')
    disk_used = 0
    # 磁盘已使用大小 = 每个分区的总和
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_disk_usage = psutil.disk_usage(partition[1])
        disk_used = partition_disk_usage.used + disk_used

    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    count = psutil.disk_io_counters()
    read_bytes = count.read_bytes
    write_bytes = count.write_bytes
    
    # 第一次请求
    if disk_dict['len'] == -1:
        disk_dict['pre_write_bytes'] = write_bytes
        disk_dict['pre_read_bytes'] = read_bytes
        disk_dict['len'] = 0
        return disk_usage.total, disk_used, disk_usage.free
    
    # 当前速率=现在写入/读取的总字节-前一次请求写入/读取的总字节
    disk_dict['write_bytes'].append((write_bytes - disk_dict['pre_write_bytes'])/1024)
    disk_dict['read_bytes'].append((read_bytes - disk_dict['pre_read_bytes'])/ 1024)
    disk_dict['disk_time'].append(now)
    disk_dict['len'] = disk_dict['len'] + 1
    
    # 把现在写入/读取的总字节放入前一个请求的变量中
    disk_dict['pre_write_bytes'] = write_bytes
    disk_dict['pre_read_bytes'] = read_bytes
    
    # 保持在图表中 50 个数据
    if disk_dict['len'] == 51:
        disk_dict['write_bytes'].pop(0)
        disk_dict['read_bytes'].pop(0)
        disk_dict['disk_time'].pop(0)
        disk_dict['len'] = disk_dict['len'] - 1

    return disk_usage.total, disk_used, disk_usage.free


def disk_line() -> Line:
    total, used, free = disk()
    c = (
        Line(init_opts=opts.InitOpts(width="1680px", height="800px"))
        .add_xaxis(xaxis_data=disk_dict['disk_time'])
        .add_yaxis(
            series_name="写入数据",
            y_axis=disk_dict['write_bytes'],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="读取数据",
            y_axis=disk_dict['read_bytes'],
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name_location="start",
                type_="value",
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name='KB/2S'
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="磁盘IO",
                pos_left="center",
                pos_top="top",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts( type_="value", name='KB/2S'),
        )
        .set_series_opts(
            axisline_opts=opts.AxisLineOpts(),
        )
    )

    return total, used, free, c

@app.route("/disk")
def get_disk_chart():
    total, used, free, c = disk_line()
    return jsonify({'total': total, 'used': used, 'free': free, 'line': c.dump_options_with_quotes()})
```

示例结果

![](http://www.justdopython.com/assets/images/2020/psutil-flask/disk.gif)

#### 网卡

通过 psutil 获取网络接口和网络连接的信息

```python
# 获取网络字节数和包的个数 发送的字节数/收到的字节数/发送的包数/收到的包数
>>> psutil.net_io_counters()
snetio(bytes_sent=9257984, bytes_recv=231398400, packets_sent=93319, packets_recv=189501, errin=0, errout=0, dropin=0, dropout=0)

# 获取当前的网络连接 注意：net_connections() 需要用管理员权限运行 Python 文件
>>> psutil.net_connections()
[sconn(fd=6, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='192.168.5.31', port=50541), raddr=addr(ip='17.248.159.145', port=443), status='ESTABLISHED', pid=1897), 
sconn(fd=12, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='192.168.5.31', port=50543), raddr=addr(ip='17.250.120.9', port=443), status='ESTABLISHED', pid=1897), 
sconn(fd=6, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='0.0.0.0', port=0), raddr=(), status='NONE', pid=1790),
sconn(fd=10, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='0.0.0.0', port=0), raddr=(), status='NONE', pid=1790),
sconn(fd=11, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='0.0.0.0', port=0), raddr=(), status='NONE', pid=1790),
...
sconn(fd=30, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='0.0.0.0', port=137), raddr=(), status='NONE', pid=1),
sconn(fd=31, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='0.0.0.0', port=138), raddr=(), status='NONE', pid=1)]

# 获取网络接口信息
>>> psutil.net_if_addrs()
{'lo0': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None), 
snicaddr(family=<AddressFamily.AF_INET6: 30>, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None), snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::1%lo0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)], 
..., 
'utun1': [snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::b519:e5df:2bd4:857e%utun1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)]}

# 获取网络接口的状态
>>> psutil.net_if_stats()
{'lo0': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=16384), 
...
'utun1': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=2000)}
```

在监控平台上每 2 秒请求 url 获取网卡IO，并动态显示图表

```python
net_io_dict = {'net_io_time':[], 'net_io_sent': [], 'net_io_recv': [], 'pre_sent': 0, 'pre_recv': 0, 'len': -1}
def net_io():
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    # 获取网络信息
    count = psutil.net_io_counters()
    g_sent = count.bytes_sent
    g_recv = count.bytes_recv

    # 第一次请求
    if net_io_dict['len'] == -1:
        net_io_dict['pre_sent'] = g_sent
        net_io_dict['pre_recv'] = g_recv
        net_io_dict['len'] = 0
        return

    # 当前网络发送/接收的字节速率 = 现在网络发送/接收的总字节 - 前一次请求网络发送/接收的总字节
    net_io_dict['net_io_sent'].append(g_sent - net_io_dict['pre_sent'])
    net_io_dict['net_io_recv'].append(g_recv - net_io_dict['pre_recv'])
    net_io_dict['net_io_time'].append(now)
    net_io_dict['len'] = net_io_dict['len'] + 1

    net_io_dict['pre_sent'] = g_sent
    net_io_dict['pre_recv'] = g_recv

    # 保持在图表中 10 个数据
    if net_io_dict['len'] == 11:
        net_io_dict['net_io_sent'].pop(0)
        net_io_dict['net_io_recv'].pop(0)
        net_io_dict['net_io_time'].pop(0)
        net_io_dict['len'] = net_io_dict['len'] - 1


def net_io_line() -> Line:
    net_io()

    c = (
    Line()
    .add_xaxis(net_io_dict['net_io_time'])
    .add_yaxis("发送字节数", net_io_dict['net_io_sent'], is_smooth=True)
    .add_yaxis("接收字节数", net_io_dict['net_io_recv'], is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="网卡IO/2秒"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
    ))
    return c

@app.route("/netio")
def get_net_io_chart():
    c = net_io_line()
    return c.dump_options_with_quotes()
```
示例结果

![](http://www.justdopython.com/assets/images/2020/psutil-flask/netio.gif)

#### 进程

通过 psutil 可以获取所有进程的信息

```python
# 所有进程的 pid
>>> psutil.pids()
[0, 1, 134, 135, 138, 139, 140, 141, 144, 145, 147, 152, ..., 30400, 97792]

# 单个进程
>>> p = psutil.Process(30400)

# 名称
>>> p.name()
'pycharm'

# 使用内存负载
>>> p.memory_percent()
12.838459014892578

# 启动时间
>>> p.create_time()
1587029962.493182

# 路径
>>> p.exe()
'/Applications/PyCharm.app/Contents/MacOS/pycharm'

# 状态
>>> p.status()
'running'

# 用户名
>>> p.username()
'imeng'

# 内存信息
>>> p.memory_info()
pmem(rss=1093005312, vms=9914318848, pfaults=7813313, pageins=8448)
```

列出所有不需要权限的进程

```python
def process():
    result = []
    process_list = []
    pid = psutil.pids()
    for k, i in enumerate(pid):
        try:
            proc = psutil.Process(i)
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time()))
            process_list.append((str(i), proc.name(), proc.cpu_percent(), proc.memory_percent(), ctime))
        except psutil.AccessDenied:
            # 需要管理员权限
            pass
        except psutil.NoSuchProcess:
            pass
        except SystemError:
            pass
        
        # 按负载排序
        process_list.sort(key=process_sort, reverse=True)

    for i in process_list:
        result.append({'PID': i[0], 'name': i[1], 'cpu': i[2], 'mem': "%.2f%%"%i[3], 'ctime': i[4]})

    return jsonify({'list', result})

def process_sort(elem):
    return elem[3]

@app.route("/process")
def get_process_tab():
    c = process()
    return c

@app.route("/delprocess")
def del_process():
    pid = request.args.get("pid")
    os.kill(int(pid), signal.SIGKILL)
    return jsonify({'status': 'OK'})
```

示例结果

![process.gif](http://www.justdopython.com/assets/images/2020/psutil-flask/process.gif)

### 总结

本文以 Psutil + Flask + Pyecharts + Bootstrap 开发一个简单的系统监控平台，可以算做是本公众号内容的一个学以致用。在 Psutil 还有许多方法文章没有列举感兴趣的小伙伴可以去尝试并使用。

> 示例代码：[Psutil + Flask + Pyecharts + Bootstrap 开发动态可视化系统监控](https://github.com/JustDoPython/python-examples/tree/master/moumoubaimifan/psutil-flask)
