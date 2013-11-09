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

可将LX_CMD改为正确的迅雷离线脚本命令。使用例子

    ./tk_lx MIDD-962

## 安装迅雷离线脚本

详见 [https://github.com/iambus/xunlei-lixian](https://github.com/iambus/xunlei-lixian)


