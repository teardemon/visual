#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-8-31 下午7:53
# @Author  : youzeshun
# 导入模块的版本：
# 参考资料  :
# 说明     :获得终端，同时封装了一些常用的终端命令
import os

g_DictCmd = {
    'ip': "ip a|grep eth0$|grep brd|awk '{print $2}'|awk -F '/' '{print $1}'"
}


def RunCmd(sCmd):
    if sCmd in g_DictCmd:
        sCmd = g_DictCmd[sCmd]
    sRet = os.popen(sCmd).read()
    return sRet.rstrip()


if __name__ == '__main__':
    print RunCmd('ip')
    print RunCmd('pwd')
    print RunCmd('ls s')
    print RunCmd('ls s')
