#TorrentKittyKit

TorrentKittyKit是一个用来从 www.torrentkitty.com 查找 -哔- 资料的工具，提供了从关键字获取磁力链接的方法，亦可和迅雷离线脚本结合直接添加离线下载任务。

## tklib.py 使用例子

    import tklib
    results = tklib.tk_search("MIDD-962")

    for name,link in results:
        print name, link

## tk_lx 
    
脚本内容为

    #!/bin/bash

    KEYWORD=$1
    LX_CMD=lx

    python tklib.py $KEYWORD | xargs $LX_CMD add 

可将`LX_CMD`改为正确的迅雷离线脚本命令。使用例子

    ./tk_lx MIDD-962

## tk-server.py

一个简单的B/S查询服务器

    python tk-server.py

服务监听在8080端口

## 安装迅雷离线脚本

详见 [https://github.com/iambus/xunlei-lixian](https://github.com/iambus/xunlei-lixian)

查询服务器支持和离线下载工具的集成。缺省使用`lx`作为`lixian_cli.py`脚本的名字，可使用配置文件`~/.tk.conf`来设置它。配置文件如下：

    [lx]
    path=~/bin/lx



